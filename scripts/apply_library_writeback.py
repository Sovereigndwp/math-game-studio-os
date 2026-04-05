#!/usr/bin/env python3
"""
Apply a pending library write-back produced by the Misconception Architect.

Usage:
    # Dry-run — show what would change without modifying anything:
    python scripts/apply_library_writeback.py <pending_file>

    # Apply and stage for git review:
    python scripts/apply_library_writeback.py <pending_file> --apply

    # Apply without git staging:
    python scripts/apply_library_writeback.py <pending_file> --apply --no-git

Workflow:
    1. Run the Misconception Architect with --llm --write-back
    2. Review the pending file it produces
    3. Run this script in dry-run mode to see the exact diff
    4. Run with --apply to update the library, create a backup,
       and stage the changes for git review
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from agents.misconception_architect.agent import apply_library_writeback, revert_library_writeback  # noqa: E402

PENDING_DIR = REPO_ROOT / "artifacts" / "misconception_library" / "pending"


def list_pending() -> None:
    """List all pending write-back files with summary info."""
    if not PENDING_DIR.is_dir():
        print("No pending directory found.")
        return

    files = sorted(PENDING_DIR.glob("*.json"))
    if not files:
        print("No pending write-back files.")
        return

    print(f"{'File':<50s} {'Status':<20s} {'Game':<18s} {'Job ID':<30s} {'Pending'}")
    print("-" * 145)

    for path in files:
        try:
            with open(path) as f:
                wb = json.load(f)
        except (json.JSONDecodeError, OSError):
            print(f"{path.name:<50s} (unreadable)")
            continue

        status = wb.get("status", "?")
        game = wb.get("game_name", "?")
        job_id = wb.get("source_job_id", "?")
        entries = wb.get("entries_to_update", [])
        pending_count = sum(1 for e in entries if not e.get("applied"))
        total_count = len(entries)

        print(f"{path.name:<50s} {status:<20s} {game:<18s} {job_id:<30s} {pending_count}/{total_count}")

    print()
    print(f"Directory: {PENDING_DIR.relative_to(REPO_ROOT)}")


BACKUP_DIR = REPO_ROOT / "artifacts" / "misconception_library" / "backups"


def prune_backups(keep: int = 3, do_delete: bool = False) -> None:
    """List and optionally prune old backup files, keeping the N most recent per game."""
    if not BACKUP_DIR.is_dir():
        print("No backups directory found.")
        return

    # Group backups by base library filename (everything before the timestamp)
    from collections import defaultdict
    groups: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(BACKUP_DIR.glob("*.bak")):
        # Format: <library-name>.json.<timestamp>.bak
        # Extract base name: everything up to and including .json
        name = path.name  # e.g. fire-dispatch-misconceptions.json.20260405T124806.bak
        parts = name.split(".json.")
        if len(parts) == 2:
            base = parts[0] + ".json"
        else:
            base = name
        groups[base].append(path)

    if not groups:
        print("No backup files found.")
        return

    total_prunable = 0
    total_kept = 0

    for base, paths in sorted(groups.items()):
        # Sort by modification time (newest last)
        paths.sort(key=lambda p: p.stat().st_mtime)
        to_keep = paths[-keep:] if keep > 0 else []
        to_prune = [p for p in paths if p not in to_keep]

        print(f"{base}: {len(paths)} backups, keeping {len(to_keep)}, pruning {len(to_prune)}")
        for p in paths:
            marker = "  PRUNE" if p in to_prune else "  keep "
            size_kb = p.stat().st_size / 1024
            print(f"  {marker}  {p.name} ({size_kb:.1f} KB)")

        if do_delete:
            for p in to_prune:
                p.unlink()
                print(f"    deleted: {p.name}")

        total_prunable += len(to_prune)
        total_kept += len(to_keep)

    print()
    if do_delete:
        print(f"Pruned {total_prunable} backups, kept {total_kept}.")
    else:
        print(f"Dry run: {total_prunable} would be pruned, {total_kept} would be kept.")
        if total_prunable > 0:
            print(f"To prune: python scripts/apply_library_writeback.py --prune-backups --keep {keep} --apply")


def _print_field_diff(field: str, diff: dict, indent: str = "    ") -> None:
    old = diff["old"]
    new = diff["new"]
    # Truncate long values for display but show enough to be useful
    max_len = 120
    old_display = old.replace("\n", " ")
    new_display = new.replace("\n", " ")
    if len(old_display) > max_len:
        old_display = old_display[:max_len] + "..."
    if len(new_display) > max_len:
        new_display = new_display[:max_len] + "..."
    print(f"{indent}{field}:")
    print(f"{indent}  - {old_display}")
    print(f"{indent}  + {new_display}")


def dry_run(pending_path: Path, only_categories: list = None) -> dict:
    """Show what would change without modifying any files."""
    with open(pending_path) as f:
        wb = json.load(f)

    status = wb.get("status")
    if status not in ("pending_review", "partially_applied"):
        print(f"  Status is '{status}'.")
        if status == "applied":
            print(f"  This write-back was fully applied at {wb.get('last_applied_at', 'unknown')}.")
        return wb

    library_file = REPO_ROOT / "artifacts" / "misconception_library" / wb["library_file"]

    print(f"Pending write-back: {pending_path.name}")
    print(f"  Game       : {wb['game_name']}")
    print(f"  Family     : {wb['game_family']}")
    print(f"  Source job : {wb['source_job_id']}")
    print(f"  Timestamp  : {wb['timestamp']}")
    print(f"  Library    : {wb['library_file']}")
    print(f"  Status     : {status}")
    if only_categories:
        print(f"  Filter     : --only {','.join(only_categories)}")
    print()

    if not library_file.exists():
        print(f"  ERROR: Library file not found: {library_file}")
        return wb

    with open(library_file) as f:
        library = json.load(f)

    lib_by_cat = {}
    for m in library.get("misconceptions", []):
        cat = m.get("category")
        if cat:
            lib_by_cat[cat] = m

    entries = wb.get("entries_to_update", [])
    eligible = []
    skipped = []
    already_applied = []

    for entry in entries:
        cat = entry["category"]
        if entry.get("applied"):
            already_applied.append(entry)
        elif only_categories and cat not in only_categories:
            skipped.append(entry)
        else:
            eligible.append(entry)

    if already_applied:
        print(f"Already applied: {len(already_applied)} ({', '.join(e['category'] for e in already_applied)})")
    if skipped:
        print(f"Skipped (not in --only): {len(skipped)} ({', '.join(e['category'] for e in skipped)})")
    print(f"Entries to update: {len(eligible)}")
    print()

    for entry in eligible:
        cat = entry["category"]
        entry_id = entry["entry_id"]
        fields = entry["fields_changed"]
        rationale = entry.get("change_rationale", "")

        current = lib_by_cat.get(cat)
        if not current:
            print(f"  [{cat}] {entry_id} — SKIPPED (category not found in current library)")
            continue

        print(f"  [{cat}] {entry_id}")
        print(f"    Fields changed: {len(fields)}")
        print(f"    Rationale: {rationale[:150]}")
        print()

        for field, diff in entry["field_diff"].items():
            _print_field_diff(field, diff)
        print()

    print("---")
    if eligible:
        print(f"Dry run complete. {len(eligible)} entries would be updated in {wb['library_file']}.")
        only_flag = f" --only {','.join(e['category'] for e in eligible)}" if only_categories else ""
        print(f"To apply: python scripts/apply_library_writeback.py {pending_path} --apply{only_flag}")
    else:
        print("Nothing to apply.")

    return wb


def _stage_and_diff(library_path: str, pending_path: Path, source_job: str) -> None:
    """Stage files and show git diff."""
    print("Staging for git review...")

    files_to_stage = [
        Path(library_path),
        pending_path.resolve(),
    ]

    for f in files_to_stage:
        abs_f = f if f.is_absolute() else (REPO_ROOT / f)
        try:
            rel = abs_f.relative_to(REPO_ROOT)
        except ValueError:
            rel = abs_f
        subprocess.run(
            ["git", "add", str(rel)],
            cwd=str(REPO_ROOT),
            capture_output=True,
        )
        print(f"  staged: {rel}")

    print()
    print("=" * 60)
    print("GIT DIFF (staged changes)")
    print("=" * 60)
    diff_result = subprocess.run(
        ["git", "diff", "--cached", "--stat"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    print(diff_result.stdout)

    lib_rel = Path(library_path).relative_to(REPO_ROOT)
    content_diff = subprocess.run(
        ["git", "diff", "--cached", str(lib_rel)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    lines = content_diff.stdout.split("\n")
    if len(lines) > 100:
        for line in lines[:100]:
            print(line)
        print(f"  ... ({len(lines) - 100} more lines, use 'git diff --cached' to see all)")
    else:
        print(content_diff.stdout)

    print()
    print("Review the staged changes, then commit when ready:")
    print(f"  git commit -m \"library: apply write-back from {source_job}\"")


def apply(pending_path: Path, git_stage: bool = True, only_categories: list = None) -> None:
    """Apply the write-back, create backup, optionally stage for git."""

    print("=" * 60)
    print("DRY-RUN PREVIEW")
    print("=" * 60)
    wb = dry_run(pending_path, only_categories=only_categories)
    print()

    if wb.get("status") not in ("pending_review", "partially_applied"):
        return

    print("=" * 60)
    print("APPLYING WRITE-BACK")
    print("=" * 60)

    result = apply_library_writeback(
        pending_path, REPO_ROOT, dry_run=False,
        only_categories=only_categories,
    )

    if not result.get("applied"):
        print(f"  ERROR: {result.get('error', 'unknown error')}")
        return

    library_path = result["library_file"]
    backup_path = result.get("backup_path", "none")
    entries_updated = result["entries_updated"]
    entries_skipped = result.get("entries_skipped", [])

    # Re-read to get current status
    with open(pending_path) as f:
        wb_after = json.load(f)

    print(f"  Library updated : {Path(library_path).relative_to(REPO_ROOT)}")
    print(f"  Backup created  : {Path(backup_path).relative_to(REPO_ROOT)}")
    print(f"  Entries updated : {len(entries_updated)} ({', '.join(entries_updated)})")
    if entries_skipped:
        print(f"  Entries skipped : {len(entries_skipped)} ({', '.join(entries_skipped)})")
    print(f"  Pending status  : {wb_after.get('status')}")

    if git_stage:
        print()
        _stage_and_diff(library_path, pending_path, wb.get("source_job_id", "unknown"))


def revert(pending_path: Path, do_revert: bool = False, git_stage: bool = True) -> None:
    """Show revert dry-run or execute revert from backup."""
    with open(pending_path) as f:
        wb = json.load(f)

    status = wb.get("status")
    if status not in ("applied", "partially_applied"):
        print(f"  Status is '{status}' — nothing to revert.")
        return

    library_filename = wb["library_file"]
    library_file = REPO_ROOT / "artifacts" / "misconception_library" / library_filename
    backup_dir = REPO_ROOT / "artifacts" / "misconception_library" / "backups"

    # Find the most recent backup
    pattern = f"{library_filename}.*.bak"
    backups = sorted(backup_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True) if backup_dir.is_dir() else []

    if not backups:
        print(f"  ERROR: No backups found for {library_filename}")
        return

    backup_to_use = backups[0]

    entries_applied = [e["category"] for e in wb.get("entries_to_update", []) if e.get("applied")]

    print(f"Revert write-back: {pending_path.name}")
    print(f"  Game       : {wb['game_name']}")
    print(f"  Source job : {wb['source_job_id']}")
    print(f"  Status     : {status}")
    print(f"  Library    : {library_filename}")
    print(f"  Backup     : {backup_to_use.name}")
    print(f"  Entries to revert: {len(entries_applied)} ({', '.join(entries_applied)})")
    print()

    # Show diff: current library vs backup (what would change)
    if library_file.exists():
        current = library_file.read_text(encoding="utf-8")
        backup_text = backup_to_use.read_text(encoding="utf-8")

        if current == backup_text:
            print("  Library already matches backup — nothing to revert.")
            return

        # Use a simple line-count comparison for the dry-run summary
        current_lines = current.splitlines()
        backup_lines = backup_text.splitlines()
        changed = sum(1 for a, b in zip(current_lines, backup_lines) if a != b)
        extra = abs(len(current_lines) - len(backup_lines))
        print(f"  Diff: ~{changed + extra} lines differ between current library and backup")

    if not do_revert:
        print()
        print("Dry run complete. Library was NOT modified.")
        print(f"To revert: python scripts/apply_library_writeback.py {pending_path} --revert --apply")
        return

    # Execute revert
    print()
    print("=" * 60)
    print("REVERTING")
    print("=" * 60)

    result = revert_library_writeback(pending_path, REPO_ROOT, dry_run=False)

    if not result.get("reverted"):
        print(f"  ERROR: {result.get('error', 'unknown error')}")
        return

    print(f"  Library restored from: {Path(result['backup_used']).name}")
    print(f"  Entries reverted: {len(result['entries_reverted'])} ({', '.join(result['entries_reverted'])})")
    print(f"  Pending status  : reverted")

    if git_stage:
        print()
        _stage_and_diff(result["library_file"], pending_path, wb.get("source_job_id", "unknown"))


def main():
    parser = argparse.ArgumentParser(
        description="Apply a pending library write-back from the Misconception Architect.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  # Dry-run (show all entries):\n"
            "  python scripts/apply_library_writeback.py <pending_file>\n\n"
            "  # Dry-run (show only specific categories):\n"
            "  python scripts/apply_library_writeback.py <pending_file> --only representation_mismatch,strategic_overload\n\n"
            "  # Apply all entries:\n"
            "  python scripts/apply_library_writeback.py <pending_file> --apply\n\n"
            "  # Apply only selected categories:\n"
            "  python scripts/apply_library_writeback.py <pending_file> --apply --only representation_mismatch\n"
        ),
    )
    parser.add_argument(
        "pending_file",
        nargs="?",
        type=Path,
        default=None,
        help="Path to the pending write-back JSON file (not needed with --list)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        default=False,
        help="List all pending write-back files with summary info",
    )
    parser.add_argument(
        "--prune-backups",
        action="store_true",
        default=False,
        help="Show (dry-run) or delete (with --apply) old backups. Use --keep N to set retention.",
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=3,
        help="Number of most recent backups to keep per game file (default: 3). Used with --prune-backups.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="Apply the write-back (default is dry-run only)",
    )
    parser.add_argument(
        "--only",
        type=str,
        default=None,
        help="Comma-separated list of categories to apply (e.g., representation_mismatch,strategic_overload). Others are left pending.",
    )
    parser.add_argument(
        "--revert",
        action="store_true",
        default=False,
        help="Revert an applied write-back from its backup. Dry-run by default; use --apply to execute.",
    )
    parser.add_argument(
        "--no-git",
        action="store_true",
        default=False,
        help="Skip git staging after applying (default: stage for review)",
    )
    args = parser.parse_args()

    if args.list:
        list_pending()
        return 0

    if args.prune_backups:
        prune_backups(keep=args.keep, do_delete=args.apply)
        return 0

    if args.pending_file is None:
        parser.error("pending_file is required (use --list to see available files)")

    if not args.pending_file.exists():
        print(f"ERROR: File not found: {args.pending_file}")
        sys.exit(1)

    if args.revert:
        revert(args.pending_file, do_revert=args.apply, git_stage=not args.no_git)
        return 0

    only_categories = None
    if args.only:
        only_categories = [c.strip() for c in args.only.split(",")]

    if args.apply:
        apply(args.pending_file, git_stage=not args.no_git, only_categories=only_categories)
    else:
        dry_run(args.pending_file, only_categories=only_categories)

    return 0


if __name__ == "__main__":
    sys.exit(main())

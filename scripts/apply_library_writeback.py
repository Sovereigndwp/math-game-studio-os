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

from agents.misconception_architect.agent import apply_library_writeback  # noqa: E402


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


def dry_run(pending_path: Path) -> dict:
    """Show what would change without modifying any files."""
    with open(pending_path) as f:
        wb = json.load(f)

    if wb.get("status") != "pending_review":
        print(f"  Status is '{wb.get('status')}' — not pending_review.")
        if wb.get("status") == "applied":
            print(f"  This write-back was already applied at {wb.get('applied_at', 'unknown')}.")
        return wb

    library_file = REPO_ROOT / "artifacts" / "misconception_library" / wb["library_file"]

    print(f"Pending write-back: {pending_path.name}")
    print(f"  Game       : {wb['game_name']}")
    print(f"  Family     : {wb['game_family']}")
    print(f"  Source job : {wb['source_job_id']}")
    print(f"  Timestamp  : {wb['timestamp']}")
    print(f"  Library    : {wb['library_file']}")
    print(f"  Status     : {wb['status']}")
    print()

    if not library_file.exists():
        print(f"  ERROR: Library file not found: {library_file}")
        return wb

    # Load current library to show the actual diff
    with open(library_file) as f:
        library = json.load(f)

    lib_by_cat = {}
    for m in library.get("misconceptions", []):
        cat = m.get("category")
        if cat:
            lib_by_cat[cat] = m

    entries = wb.get("entries_to_update", [])
    print(f"Entries to update: {len(entries)}")
    print()

    for entry in entries:
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

    # Summary
    print("---")
    print(f"Dry run complete. {len(entries)} entries would be updated in {wb['library_file']}.")
    print(f"To apply: python scripts/apply_library_writeback.py {pending_path} --apply")

    return wb


def apply(pending_path: Path, git_stage: bool = True) -> None:
    """Apply the write-back, create backup, optionally stage for git."""

    # Show dry-run first
    print("=" * 60)
    print("DRY-RUN PREVIEW")
    print("=" * 60)
    wb = dry_run(pending_path)
    print()

    if wb.get("status") != "pending_review":
        return

    print("=" * 60)
    print("APPLYING WRITE-BACK")
    print("=" * 60)

    result = apply_library_writeback(pending_path, REPO_ROOT, dry_run=False)

    if not result.get("applied"):
        print(f"  ERROR: {result.get('error', 'unknown error')}")
        return

    library_path = result["library_file"]
    backup_path = result.get("backup_path", "none")
    entries_updated = result["entries_updated"]

    print(f"  Library updated : {Path(library_path).relative_to(REPO_ROOT)}")
    print(f"  Backup created  : {Path(backup_path).relative_to(REPO_ROOT)}")
    print(f"  Entries updated : {len(entries_updated)} ({', '.join(entries_updated)})")
    print(f"  Pending status  : applied")

    if git_stage:
        print()
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

        # Show the git diff for review
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

        # Show the actual content diff for the library file
        lib_rel = Path(library_path).relative_to(REPO_ROOT)
        content_diff = subprocess.run(
            ["git", "diff", "--cached", str(lib_rel)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        # Print a manageable portion of the diff
        lines = content_diff.stdout.split("\n")
        if len(lines) > 80:
            for line in lines[:80]:
                print(line)
            print(f"  ... ({len(lines) - 80} more lines, use 'git diff --cached' to see all)")
        else:
            print(content_diff.stdout)

        print()
        print("Review the staged changes, then commit when ready:")
        print(f"  git commit -m \"library: apply write-back from {wb.get('source_job_id', 'unknown')}\"")


def main():
    parser = argparse.ArgumentParser(
        description="Apply a pending library write-back from the Misconception Architect.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  # Dry-run:\n"
            "  python scripts/apply_library_writeback.py artifacts/misconception_library/pending/fire-dispatch-pass2-changed_*.json\n\n"
            "  # Apply and stage:\n"
            "  python scripts/apply_library_writeback.py artifacts/misconception_library/pending/fire-dispatch-pass2-changed_*.json --apply\n"
        ),
    )
    parser.add_argument(
        "pending_file",
        type=Path,
        help="Path to the pending write-back JSON file",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="Apply the write-back (default is dry-run only)",
    )
    parser.add_argument(
        "--no-git",
        action="store_true",
        default=False,
        help="Skip git staging after applying (default: stage for review)",
    )
    args = parser.parse_args()

    if not args.pending_file.exists():
        print(f"ERROR: File not found: {args.pending_file}")
        sys.exit(1)

    if args.apply:
        apply(args.pending_file, git_stage=not args.no_git)
    else:
        dry_run(args.pending_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())

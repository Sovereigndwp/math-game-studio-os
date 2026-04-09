# games/

## Status: empty by design

This directory is the **release archive layer** of the Math Game Studio OS.
At the time this README was committed, it contains **zero released games**.

**Empty is the correct state.** It does not indicate missing files, broken
tooling, or a migration gap. Nothing has shipped yet, so nothing lives here.

## Purpose

This is where immutable, tagged, SemVer-versioned game releases live. Each
release is a frozen snapshot of a review build that passed the Taskade
ship-ready gate. Once a release directory exists, its contents are never
modified — a new release always means a new version directory.

See [`docs/pipeline_policy.md`](../docs/pipeline_policy.md) for the full
pipeline policy. The three repo layers and their distinct lifecycles:

| Layer | Path | Mutability | Who writes to it |
|---|---|---|---|
| Concepts | `concepts/<slug>/` | Edited when specs change | Humans |
| Reviews | `reviews/<slug>/current/` | Mutable, rolling head of dev work | Humans / development process only |
| **Releases** | **`games/<slug>/releases/<version>/`** | **Immutable once created** | **`promote-build` workflow only** |

## What lives here (when a release exists)

Once releases start landing, the layout will be:

```
games/
  <slug>/
    releases/
      v0.1.0/
        index.html           ← frozen copy of reviews/<slug>/current/index.html
        [pass-N.html]        ← any pass files copied from reviews/<slug>/current/
        [pass-N-record.md]
        [other per-game files]
      v0.1.1/
        index.html           ← patch release (bug fix only)
        ...
      v0.2.0/
        index.html           ← minor release (new content / balance)
        ...
```

Every file under `games/<slug>/releases/<version>/` is a byte-for-byte copy
of the corresponding file in `reviews/<slug>/current/` at the moment the
Taskade gate went GREEN.

## How files get here

**Only one path is allowed:** the `promote-build` GitHub Actions workflow
([`.github/workflows/promote-build.yml`](../.github/workflows/promote-build.yml))
creates release directories in response to a `repository_dispatch` event
from Taskade carrying a GREEN gate verdict.

The end-to-end flow:

```
  Taskade (ship-ready gate → GREEN)
      │
      ▼
  repository_dispatch event_type=promote_build
  client_payload: { slug, version, gate_status: "GREEN", ... }
      │
      ▼
  promote-build workflow
      ├─ validates reviews/<slug>/current/index.html exists
      ├─ validates games/<slug>/releases/<version>/ does NOT exist
      ├─ copies reviews/<slug>/current/ → games/<slug>/releases/<version>/
      ├─ commits to main as github-actions[bot]
      ├─ tags as game/<slug>/v<version>
      └─ pushes commit + tag
      │
      ▼
  games/<slug>/releases/<version>/ now exists, immutable
```

## Anti-patterns — do not do these

These actions are policy violations. They will corrupt the release archive
and break the traceability guarantee between a GREEN gate and an immutable
shipped artifact.

- ❌ **Do not create release directories by hand.** No `mkdir games/bakery/releases/v0.1.0`. No `cp reviews/bakery/current/index.html games/bakery/releases/v0.1.0/index.html`. The workflow is the only path.
- ❌ **Do not modify files inside an existing release directory.** Once `games/<slug>/releases/v0.1.0/` exists, its contents are frozen forever. If you need to change something, cut a new version.
- ❌ **Do not delete a release directory to "re-release" the same version.** The tag `game/<slug>/v<version>` is also immutable. If a release needs to be retracted, cut a new version — do not rewrite history.
- ❌ **Do not commit directly to main with changes under `games/`.** Main is reserved for (1) policy and infrastructure (this README qualifies) and (2) releases created by the `promote-build` workflow. Any other direct-to-main commit touching `games/` is a policy violation.
- ❌ **Do not copy review builds into `games/` to "test" the workflow.** If you need to test plumbing, use a dry-run dispatch against a throwaway slug, or run the workflow in a feature branch first. Do not pollute the real release archive with test artifacts.

## What does NOT live here

- Review builds — those live in `reviews/<slug>/current/`
- Concept packets — those live in `concepts/<slug>/`
- Pass records — those stay alongside their review builds in `reviews/<slug>/current/`
- Historical snapshots for games that were never shipped under this policy — those stay in git history via the Phase 2 renames
- A `latest/` symlink or alias — not part of the current policy (tracked as an open follow-up in `docs/pipeline_policy.md`)
- Non-game releases (docs, infrastructure, tooling) — those belong elsewhere in the repo with their own versioning if needed

## First release

No game has shipped yet.

The first release will happen when you explicitly dispatch a `promote_build`
event from Taskade for a game you have formally passed through the
ship-ready gate. Until then, this directory stays empty.

See the migration state section of [`docs/pipeline_policy.md`](../docs/pipeline_policy.md)
for the full phase plan and current state.

## Questions to answer before the first release

Before the first real dispatch lands here, these things should be decided
and documented (they are not blockers for Phase 4, just for the first ship):

- Which game ships first? (Candidates: bakery, fire, unit-circle, power-grid.)
- What is the first version? (Policy says `v0.1.0` for all first releases.)
- Who has the Taskade dispatch credentials?
- Has the regex validation (Phase 5) been added to the workflow?
- Has a dry-run dispatch been run successfully?

None of these are answered in this Phase 4 commit — they get answered when
you are ready to ship.

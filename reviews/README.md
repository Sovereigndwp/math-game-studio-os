# reviews/

## What this is

The **mutable review-build layer** of the Math Game Studio OS. This is where the active, in-development version of every game prototype lives.

**Nothing here is a shipped artifact.** Review builds are explicitly *not* releases. They may change between any two commits. A file at `reviews/<slug>/current/index.html` does not mean the game has been approved, playtested successfully, or declared ship-ready.

Shipped, immutable, SemVer-tagged releases live in [`games/`](../games/). See [`docs/pipeline_policy.md`](../docs/pipeline_policy.md) for the full policy.

## Canonical layout

```
reviews/
  <slug>/
    current/
      index.html           ← active review build (rolling head of dev work)
      [pass-N.html]        ← optional historical pass snapshot
      [pass-N-record.md]   ← optional pass-N design record
      [other per-game files]
```

The canonical path referenced by the policy doc, the `promote-build` workflow, and the family registry is:

```
reviews/<slug>/current/index.html
```

### Pass files are optional

A `current/` directory may also contain one or more `pass-N.html` snapshots and `pass-N-record.md` design records. These are **not required**. They exist only when a historical playable checkpoint is worth preserving outside of git history.

The only file in `current/` that must always exist is `index.html`. It is always the head of the current development work. Pass files are a convenience for comparison and handoff, not a required structure.

### Mutability

`reviews/<slug>/current/` is **mutable**. Files there may be edited, replaced, or deleted as development proceeds. There is no SemVer tag, no immutability guarantee, no frozen state.

If you need an immutable snapshot of a build at a specific quality bar, that is what the release archive (`games/<slug>/releases/<version>/`) is for. See [`games/README.md`](../games/README.md).

## How writes happen

Humans write to `reviews/<slug>/current/` through normal development work: edits, commits, passes, playtest iterations, bug fixes.

**The `promote-build` workflow does not write to `reviews/`.** Promotion copies *from* `reviews/<slug>/current/` *to* `games/<slug>/releases/<version>/`. The flow is one-way: reviews → games, never the reverse.

## Current games

| Slug | State | Contents of `current/` |
|---|---|---|
| `bakery` | Active review build | `index.html`, `pass-3.html` |
| `counting` | Active review build | `index.html` |
| `echo-heist` | Active review build | `index.html`, `pass-1.html`, `pass-1-record.md` through `pass-5-record.md`, `playtest.js` |
| `fire` | Active review build | `index.html`, `pass-3.html` |
| `power-grid` | Active review build | `index.html` |
| `unitcircle` | Active review build | `index.html`, `pass-3.html` |
| `snack-line-shuffle` | **Placeholder only** | `README.md` at the slug level; no `current/` subdirectory, no prototype exists yet |

The `snack-line-shuffle` entry is deliberately asymmetric. See [`reviews/snack-line-shuffle/README.md`](snack-line-shuffle/README.md) and [`concepts/snack-line-shuffle/status.md`](../concepts/snack-line-shuffle/status.md) for why.

## Related layers

| Layer | Path | Purpose |
|---|---|---|
| Concepts | [`concepts/<slug>/`](../concepts/) | Approved specs, P1 Definition of Done, misconception notes |
| **Reviews** | `reviews/<slug>/current/` *(this directory)* | Mutable in-development builds |
| Releases | [`games/<slug>/releases/<version>/`](../games/) | Immutable shipped artifacts |

## Related documents

| Doc | Purpose |
|---|---|
| [`docs/pipeline_policy.md`](../docs/pipeline_policy.md) | Full pipeline policy |
| [`docs/concept_lanes.md`](../docs/concept_lanes.md) | Active concept lane tracker |
| [`games/README.md`](../games/README.md) | Release archive rules |
| [`.github/workflows/promote-build.yml`](../.github/workflows/promote-build.yml) | GREEN gate → release workflow |

## What this directory is NOT

- ❌ Not a release archive (that is `games/`)
- ❌ Not a concept spec layer (that is `concepts/`)
- ❌ Not the V1 Python pipeline output layer (that is `memory/job_workspaces/`, gitignored)
- ❌ Not a historical record of every pass — git history is the primary record
- ❌ Not a staging area for the release workflow — the workflow reads from here but does not write here

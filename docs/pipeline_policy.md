# Pipeline Policy

This document is the source of truth for how concepts become review builds
and how review builds become released games.

It is the **human-readable companion** to the automation in
`.github/workflows/promote-build.yml`. If the workflow and this document
ever disagree, the workflow is authoritative for enforcement and this
document is authoritative for intent. Resolve any drift by updating both.

---

## Two-system model

The Math Game Studio OS runs on a two-system split:

| System | Role | Scope |
|---|---|---|
| **Taskade** | Live pipeline | Concept lanes, playtests, reviews, gate decisions, approval flow |
| **GitHub** | Review + release archive | Policy docs, concept source of truth, review builds, shipped releases, CI enforcement |

Taskade is where humans decide "is this ready to ship?" GitHub is where
the answer gets recorded immutably.

The only automated bridge between the two systems is the GitHub Actions
workflow `.github/workflows/promote-build.yml`, which is triggered by a
`repository_dispatch` event from Taskade when a gate goes GREEN.

---

## Repo layers

Three filesystem layers, each with a distinct purpose and a distinct
lifecycle. Do not conflate them.

### 1. `concepts/<slug>/` — spec and planning

The approved concept packet, P1 Definition of Done, locked approvals,
misconception notes, and lane status for each concept. Concepts do not
ship. Concepts **become** review builds.

Files in `concepts/` are edited when the concept itself is revised (rare)
or when lane status changes. They are not tied to SemVer.

### 2. `reviews/<slug>/current/index.html` — active review build

The current in-development preview for each game. This is what
playtesters, critics, educators, and the Delight Gate evaluate.

Review builds are **mutable** — `current/` is the rolling head of dev
work. Earlier passes may be preserved alongside `index.html` as
`pass-N.html` + `pass-N-record.md` (matching the existing per-game
convention).

Review builds do not get SemVer tags. They are not shippable artifacts.
They may change between any two commits.

### 3. `games/<slug>/releases/<version>/index.html` — immutable release

A shipped, tagged, frozen release of a game. Created only by the
`promote-build` workflow on a GREEN Taskade gate dispatch.

Release builds are **immutable** — once `games/<slug>/releases/v0.1.0/`
exists, it is never modified. A new release always means a new version
directory. Replacing files inside an existing release is a policy
violation.

---

## Branch and commit policy

Main branch is for two kinds of content only:

1. **Policy and infrastructure changes** — this document, CI workflow
   files, registry schemas, taxonomy edits, concept folder updates,
   migration commits, tooling. These may be committed directly to main.

2. **Ship-ready game releases** — and only through the `promote-build`
   workflow, triggered by a Taskade GREEN gate dispatch. Humans do not
   run `git push` for a release; the workflow does.

Everything else — feature work, bug fixes, playtest iterations, pass
revisions on a review build — happens on a **feature branch**.

Game feature branches merge back into main only when a release is cut
for the affected game, and only via the promote-build workflow. Policy
and infrastructure branches may merge to main outside the release
workflow. A game feature branch with unshipped work can live
indefinitely; it does not block the release pipeline for other games.

### Forward-only history policy

History already on main at the time this policy was adopted is
**not rewritten**. All direct-to-main commits prior to this policy
are considered grandfathered infrastructure/planning work. This
includes recent concept normalization, game fixes, and the original
addition of the `promote-build` workflow.

Going forward, the forward-only rule means:

- No `git rebase -i` of shared main history.
- No `git push --force` to main under any circumstances.
- No backdated commits.

If main ever drifts from the policy, fix it with a new forward commit
(or a corrective PR), not by rewriting past history.

---

## SemVer rules

All release versions follow strict **MAJOR.MINOR.PATCH**.

- **Starting version for any game's first release: `v0.1.0`.**
- Versions below `v1.0.0` are pre-release in the policy sense: they
  have not yet been externally validated or shipped to paying users.
- `v1.0.0` is reserved for the first external-validation release —
  i.e., the first time a game is considered fit for paid distribution
  or published classroom use. Do not bump to `v1.0.0` just because
  a review build "feels finished."
- **No pre-release suffixes** (`v0.1.0-rc.1`, `v0.1.0-beta.2`) in the
  current policy. If that becomes necessary later, both this document
  and the version regex in the workflow must be updated in the same
  commit.

Version bump rules within the pre-1.0 regime:

| Change type | Example | Bump |
|---|---|---|
| Bug fix only, no new content | "fix vault timer display" | PATCH (`v0.1.0` → `v0.1.1`) |
| Playtest pass revision, new content, balance changes | "Pass 4: mastery layer added" | MINOR (`v0.1.0` → `v0.2.0`) |
| Breaking change in player-facing mechanics or save format | "reshape core loop" | MINOR pre-1.0, MAJOR post-1.0 |

---

## Ship-ready gate

A release is only created when the Taskade ship-ready gate goes GREEN.

The ship-ready gate is **not** automated. It is a structured human
decision in Taskade that evaluates, at minimum:

- Game Design Critic review of the most recent pass record
- Playtest evidence (at least one real learner session, documented)
- Delight Gate pass (conditional passes must have their conditions
  resolved before the gate can go GREEN)
- Educator review where the concept claims a CCSS standard
- Misconception library entries populated for the game
- Loop purity and difficulty ramp audits passed
- P1 Definition of Done fully checked for the game's current stage

Taskade owns the gate checklist. GitHub only sees the final verdict
via the dispatched `gate_status` field. If `gate_status != "GREEN"`,
the workflow refuses to promote.

---

## Promotion flow (end-to-end)

```
  Taskade (gate goes GREEN)
      │
      ▼
  POST https://api.github.com/repos/Sovereigndwp/math-game-studio-os/dispatches
      event_type: promote_build
      client_payload: { slug, version, gate_status: "GREEN", gate_url, summary }
      │
      ▼
  .github/workflows/promote-build.yml (on: repository_dispatch)
      │
      ├─ Checkout main (full history)
      ├─ Read payload into step outputs
      ├─ Block unless gate_status == "GREEN"
      ├─ Validate reviews/<slug>/current/index.html exists
      ├─ Validate games/<slug>/releases/<version>/ does not exist
      ├─ Copy reviews/<slug>/current/ → games/<slug>/releases/<version>/
      ├─ Commit to main as github-actions[bot]:
      │     "Release <slug> v<version>"
      ├─ Create annotated tag: game/<slug>/v<version>
      └─ Push commit + tag to origin
      │
      ▼
  main branch now contains the immutable release at
  games/<slug>/releases/v<version>/ and a matching tag.
```

At no point in this flow does a human run `git push` for the release.
Humans only dispatch; the workflow commits and pushes.

---

## Slug and version validation

The workflow enforces strict formats to prevent bad paths, tag
collisions, and silent corruption.

| Field | Regex | Examples ✅ | Examples ❌ |
|---|---|---|---|
| `slug` | `^[a-z0-9]+(-[a-z0-9]+)*$` | `bakery`, `snack-line-shuffle`, `power-grid` | `Bakery`, `snack_line_shuffle`, `fire/dispatch`, `-bakery`, `bakery-` |
| `version` | `^[0-9]+\.[0-9]+\.[0-9]+$` | `0.1.0`, `1.2.3`, `0.12.5` | `v0.1.0` (no leading `v`), `0.1.0-rc.1`, `1.2`, `1.2.3.4` |

Both regex checks run before any filesystem changes. Validation
failure exits non-zero with a clear error message and no side effects.

> **Note:** The regex validation is the one aspect of the workflow
> that is not yet implemented in the current committed version. It
> will be added as a small follow-up commit.

---

## Tag format

Release tags are annotated tags (`git tag -a`) with the format:

```
game/<slug>/v<version>
```

Examples:

- `game/bakery/v0.1.0` — first Bakery release
- `game/bakery/v0.1.1` — Bakery patch release
- `game/snack-line-shuffle/v0.1.0` — first Snack Line Shuffle release

The `game/` prefix prevents collisions with any future non-game tags
(e.g., `infra/v1.0.0`, `docs/v1.0.0`). Tag messages match the commit
subject: `Release <slug> v<version>`.

Tags are immutable once pushed. If a release needs to be retracted,
cut a new version — do not delete or rewrite the tag.

---

## Current migration state

This policy is being adopted in phases. At the time of its first
commit, the repo state is:

- ✅ `concepts/` exists, with one concept (`snack-line-shuffle/`)
- ✅ `.github/workflows/promote-build.yml` exists (commit `9717e98`)
- ❌ `reviews/` does **not** exist yet
- ❌ `games/` does **not** exist yet
- ⚠ 7 games currently live in `previews/<slug>/current.html`
  (legacy layer, to be migrated)

**The workflow is non-functional until the migration completes.**
Any `promote_build` dispatch issued before Phase 2 will fail at the
"Validate review build exists" step with
`Missing reviews/<slug>/current/index.html`.

### Migration phases

| Phase | Scope | State |
|---|---|---|
| **1** | Write this policy doc | **IN PROGRESS** |
| **2** | `git mv previews/<slug>/current.html reviews/<slug>/current/index.html` for every game; move per-pass files alongside; preserve history | Not started |
| **3** | Update 4 active cross-reference files: `memory/registries/family_registry.json`, `concepts/snack-line-shuffle/status.md`, `docs/concept_lanes.md`, `reviews/snack-line-shuffle/README.md` | Not started |
| **4** | Create `games/` directory with a `README.md` explaining the release archive intent; no releases created yet | Not started |
| **5** | Add regex validation to the workflow file (slug + version) | Not started |
| **6** | Dry-run dispatch test against one game (e.g., `unitcircle`) to confirm end-to-end plumbing | Not started |
| **7** | First real release — only when explicitly approved | Not started |

### What is not migrated

The following files contain references to `previews/` paths and are
**intentionally left unchanged**:

- `artifacts/learning_captures/2026-04-07-counting-concept-lane.md` — historical
- `artifacts/learning_captures/2026-04-07-counting-p0p1-implementation-plan.md` — historical
- `docs/repo_systems_audit.md` — audit document recording past repo state
- `agents/implementation_plan/agent.py` — prompt text; will be updated
  only if it causes a correctness problem

Historical artifacts document what the repo looked like at the time
they were written. Rewriting them loses information and creates a
false impression that the policy was always in force. Do not rewrite
them retroactively.

---

## Glossary

- **Concept** — an approved idea with a spec, P1 Definition of Done,
  and locked approvals. Lives in `concepts/<slug>/`. Does not ship.
- **Review build** — a playable preview of a concept that is under
  active development, review, or playtest. Lives in
  `reviews/<slug>/current/index.html`. Mutable. Does not ship on its own.
- **Release build** — an immutable, tagged, shipped snapshot of a
  review build that passed the Taskade GREEN gate. Lives in
  `games/<slug>/releases/<version>/index.html`. Never modified once
  created.
- **Gate (ship-ready gate)** — the structured Taskade checklist that
  determines whether a review build is ready to become a release build.
  Produces a GREEN/AMBER/RED verdict. Only GREEN promotes.
- **Promotion** — the act of copying a review build into a release
  directory, creating a tag, and committing to main. Performed by the
  `promote-build` workflow, never by hand.
- **Dispatch** — a `repository_dispatch` event sent from Taskade to
  GitHub via the REST API. Carries the slug, version, and gate status
  in its `client_payload`.
- **Slug** — the machine-safe, kebab-case identifier for a game.
  Matches `^[a-z0-9]+(-[a-z0-9]+)*$`. Used in both filesystem paths
  and tag names.
- **Ship-ready** — the quality bar for a release, owned by the
  Taskade gate. Not a self-assessed label; it only exists as a GREEN
  gate verdict.

---

## Open follow-ups (tracked here, not blocking policy adoption)

- Phase 2 through Phase 7 of the migration above
- Adding slug/version regex validation to `promote-build.yml`
- Writing a human-readable "how to dispatch from Taskade" runbook
  for the first real release
- Deciding whether `games/<slug>/releases/latest/` should be a
  convenience symlink/copy of the most recent version (not in scope
  for v0 of this policy)

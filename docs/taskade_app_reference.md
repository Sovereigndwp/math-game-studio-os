# Taskade App Reference

## Purpose and scope

This document is the single repo-native reference for the **durable structure** of the Taskade live operating layer.

It records the stable relationship between Taskade and the repo. It is meant to help future workflows, future cleanup work, and future contributors understand what Taskade owns, what the repo owns, and how the two systems connect.

This document captures **structure**, not live operational state.

Values in this document use Option A wording: real values where known, explicit unset values (`"none"` or `"not yet decided"`) where a governance decision has not been made, and no invented or placeholder values.

It does capture:
- the primary Taskade space reference
- the current live Taskade agent roster
- the currently known workflow state
- the Taskade ↔ GitHub release connection
- the shipping payload contract
- the repo utilization rule
- maintenance ownership and review expectations

It does not capture:
- daily task status
- transient discussion threads
- per-day concept lane changes
- per-day playtest notes
- any secret value such as the actual GitHub PAT

For current durable repo policy, see [`docs/pipeline_policy.md`](pipeline_policy.md).
For current repo-side lane state, see [`docs/concept_lanes.md`](concept_lanes.md).
For the current repo-side family registry, see [`memory/registries/family_registry.json`](../memory/registries/family_registry.json).

---

## Primary Taskade space

| Field | Value |
|---|---|
| **Taskade space URL** | `https://www.taskade.com/spaces/63ifx7l9wtgfvsop/app/default/preview` |
| **Taskade space name** | not yet decided |
| **Owner / account** | not yet decided |
| **Alternate or secondary spaces** | none |

### Current note

The space URL is known and stable. The space name and accountable owner are **not yet decided**. That is currently the highest-value missing governance decision because it affects credential ownership, rotation, and document maintenance.

---

## What Taskade is the source of truth for

Taskade is the source of truth for the **live operating layer**:

- active concept lane movement
- current assignments
- current next actions
- current gate-review status
- current human approval flow
- current review discussions
- pass closure activity
- day-to-day orchestration
- in-progress operational decisions

If the question is "what is happening right now?" the answer should come from Taskade first.

---

## What the repo is the source of truth for

The repo is the source of truth for the **durable artifact layer**:

- policy documents
- concept packets
- review-build structure
- release-archive structure
- machine-readable registries
- shipped releases
- workflow enforcement
- dated audits and historical reference material

If the question is "what is the durable documented structure?" the answer should come from the repo.

---

## Division of responsibilities

| Thing | Taskade | Repo |
|---|---|---|
| Live concept lane state | authoritative | snapshot only |
| Approval flow | authoritative | documented indirectly |
| Ship-ready gate decision | authoritative | enforced only after dispatch |
| Review build code | operationally referenced | authoritative artifact |
| Release archive | triggers it | stores it |
| Policy rules | informs operation | authoritative durable source |
| Family/game registry | may inform decisions | authoritative durable source |
| Historical audits | not primary | authoritative historical record |

---

## Current live Taskade agents

These are the currently known Taskade agents. This section refers to **Taskade agents**, not the Era 1 Python pipeline agents in the repo's `agents/` directory.

### Active agents

| Agent | Role | Trigger | Owner | Status |
|---|---|---|---|---|
| **Math Question QA** | QA agent for math-question content and correctness checks. | manual — run when a QA check is requested | not yet decided | active |
| **Pass Closure Agent** | Captures post-pass learnings and promotes validated rules back into the OS. | event-driven — after a completed prototype pass / pass closure request | not yet decided | active |
| **Game Build Standards Agent** | Runs Stage 8.5 Build Standards Gate (CO + MG compliance) and returns GREEN/AMBER/RED. | manual — invoked immediately after Prototype Engineer outputs (Stage 8) | not yet decided | active |
| **Player Clarity Auditor** | Audits first-time user clarity and instructional/UX comprehension risks. | manual — run when a clarity audit is requested | not yet decided | active |
| **Pipeline Orchestrator** | Coordinates the end-to-end concept pipeline from idea → spec → gate → build handoff. | manual — run when pipeline coordination is requested | not yet decided | active |
| **Subject Expansion Scout** | Scouts and proposes new subject/domain expansions and opportunities. | manual — run when expansion scouting is requested | not yet decided | active |
| **Prototype Engineer** | Produces prototype specs/build-ready handoffs (Stages 6–8). | manual — run when a prototype spec is requested | not yet decided | active |
| **Curriculum Architect** | Ensures standards alignment, learning objectives, and curriculum fit. | manual — run when curriculum alignment is requested | not yet decided | active |
| **Brainstorming Specialist** | Generates raw game ideas and variations for a given learning goal/theme. | manual — run when ideation is requested | not yet decided | active |
| **Software Developer** | Implements the game after Stage 8.5 GREEN gate approval. | manual — started only after GREEN gate | not yet decided | active |
| **Game Design Critic** | Provides rigorous gate reviews and critiques to enforce quality and viability. | manual — run when a design review is requested | not yet decided | active |

### Deprecated agents still present

These agents still exist in Taskade but are explicitly deprecated and should not be used for active system work.

| Agent | Role | Trigger | Owner | Status |
|---|---|---|---|---|
| **⛔ Project Manager [DEPRECATED]** | Deprecated project management agent (do not use). | manual — legacy only | not yet decided | active (deprecated) |
| **⛔ SEO Content Writer [DEPRECATED]** | Deprecated SEO writing agent (do not use). | manual — legacy only | not yet decided | active (deprecated) |
| **⛔ Researcher [DEPRECATED]** | Deprecated research agent (do not use). | manual — legacy only | not yet decided | active (deprecated) |

### Governance note

Many agents are operationally live, but ownership is still unset. This creates ambiguity in accountability. The next governance improvement should be assigning an explicit **owner / account** for the space and then a clear owner for each live agent.

---

## Current live Taskade workflows

### Current known state

No live workflows or automations have yet been confirmed from the current retrieval view of the Taskade space.

| Field | Value |
|---|---|
| **Workflow discovery state** | not yet discovered in this space via current retrieval (no automations returned) |
| **Purpose** | not yet decided |
| **Trigger** | not yet decided |
| **Outputs** | not yet decided |
| **Status** | not yet decided |

### Interpretation note

This does **not** prove there are no workflows in Taskade. It only means that, from the current retrieval path used during documentation, no automations were returned. Treat this section as an honest temporary record of current visibility, not a claim that the space has no workflows.

If workflows are later confirmed, this section should be revised.

---

## How Taskade connects to the GitHub release flow

The durable release handoff is one-way:

**Taskade gate → GitHub dispatch → repo release archive**

### Release flow

```text
Taskade ship-ready gate goes GREEN
        ↓
repository_dispatch to GitHub
        ↓
.github/workflows/promote-build.yml
        ↓
reviews/<slug>/current/ copied to games/<slug>/releases/<version>/
        ↓
commit to main + annotated release tag
```

### Dispatch target

- **Repo:** `Sovereigndwp/math-game-studio-os`
- **Workflow:** `.github/workflows/promote-build.yml`
- **Event type:** `promote_build`

### Required payload fields

| Field | Required | Rule |
|---|---|---|
| `slug` | yes | must match `^[a-z0-9]+(-[a-z0-9]+)*$` |
| `version` | yes | must match `^[0-9]+\.[0-9]+\.[0-9]+$` |
| `gate_status` | yes | must equal `GREEN` |
| `gate_url` | optional | audit trail link back to Taskade |
| `summary` | optional | short release summary |

### Important enforcement rule

A review build is **not** a shipped artifact.

A game is only treated as shipped when both are true:
1. the Taskade ship-ready gate is GREEN
2. a release exists under `games/<slug>/releases/<version>/`

---

## GitHub dispatch credential storage

| Field | Value |
|---|---|
| **Where the GitHub PAT is stored in Taskade** | not yet decided |
| **Secret/key name** | not yet decided |
| **Notes** | not yet decided |

### Security note

The token itself must never be stored in this document. Only the storage location, naming convention, and governance details belong here.

Because PAT storage is still undecided, the Taskade ↔ GitHub dispatch chain is documented structurally but not yet fully governed operationally.

---

## PAT rotation policy

| Field | Value |
|---|---|
| **Rotation schedule** | not yet decided |
| **Responsible party** | not yet decided |

### Governance note

This should be finalized only after the Taskade space owner/account is explicitly assigned. Until ownership is clear, token rotation responsibility is structurally ambiguous.

---

## Repo utilization rule

This section mirrors the Taskade-side rule and is meant to prevent regression or confusion when Taskade agents consult the repo.

### Priority order when using repo material

1. **Canonical repo policy**
   - `docs/pipeline_policy.md`
   - `games/README.md`
   - `reviews/README.md`
   - `.github/workflows/promote-build.yml`

2. **Structured repo references**
   - `docs/concept_lanes.md`
   - `memory/registries/family_registry.json`
   - `concepts/<slug>/...`

3. **Historical repo context only**
   - `docs/repo_systems_audit.md`
   - `docs/repo_systems_audit_2026-04-09.md`
   - learning captures
   - archived pending files
   - old pass records

### Rules

- Do not let older repo snapshots override better current Taskade live state.
- Use structured repo references conservatively.
- Historical repo documents are for context, not operational truth.
- Review builds are not shipped artifacts.
- If Taskade has a better live structure than an older repo document, preserve the better live structure.
- If a repo document is policy, follow it unless Taskade explicitly records that the policy has been superseded.
- If a repo document is a historical snapshot, extract useful context only and do not treat it as a current instruction set.

---

## What statuses and fields matter for shipping

The following are the most important fields when a Taskade workflow or agent prepares a release handoff:

| Field | Why it matters |
|---|---|
| `slug` | determines the review and release path |
| `version` | determines the immutable release folder and tag |
| `gate_status` | must be GREEN or the workflow rejects the dispatch |
| `gate_url` | supports auditability |
| review build existence | `reviews/<slug>/current/index.html` must exist |
| release nonexistence | `games/<slug>/releases/<version>/` must not already exist |

### Operational reminder

The GitHub workflow enforces syntax and archive rules.
Taskade is responsible for the **human judgment** that the build is actually ready.

---

## Maintenance policy

Update this document when, **and only when**, the durable structure changes. The triggers below are the complete list. Anything not on this list is operational noise and does not warrant a doc update.

### 1. Taskade space governance changes

- the Taskade space URL changes
- the Taskade space name is decided (currently `not yet decided`)
- the owner / account is assigned (currently `not yet decided`)
- a secondary space is added

### 2. Agent roster changes

- any agent is added, removed, or renamed
- any agent's status changes (active / paused / draft)
- any agent becomes deprecated, or a previously deprecated one is removed
- any agent's owner is assigned or changed

### 3. Workflow / automation reality becomes known or changes

- the first time live workflows or automations are confirmed in the space (this section currently records "not yet discovered" — confirming any workflow triggers an update)
- any workflow is added, removed, or renamed
- any workflow's trigger, outputs, or status changes

### 4. GitHub dispatch credential governance changes

- the PAT storage location is decided
- the secret / key name changes
- the PAT rotation schedule or responsible party changes

### 5. Release contract changes

- the target repo, workflow file path, event type, or required payload fields change
- the slug or version regex changes
- the release archive path layout changes
- any enforcement rule for what counts as "shipped" changes

### 6. Repo utilization rule changes

- any change to the priority order of repo material tiers
- any change to the file lists inside any priority tier
- any change to the rule bullets

### 7. Document governance changes

- the review cadence is set or changed
- the maintainer is set or changed
- the next scheduled review date is set or changed
- the doc is reviewed (so `Date last reviewed` changes)

### Rule of thumb

If a future contributor could make a wrong durable decision because this doc is stale, update it. If it is just weekly operational state, do not.

### What does NOT trigger an update

Do **not** update this document for:
- daily task movement
- single playtest events
- one-off discussions
- ephemeral lane changes
- temporary experiments that do not change durable structure

---

## Current governance gaps

The following are explicitly unresolved as of this snapshot:

1. **Taskade space name** — not yet decided
2. **Owner / account** — not yet decided
3. **Agent ownership** — not yet decided for every listed agent
4. **Workflow discovery** — no automations returned from current retrieval path
5. **PAT storage location** — not yet decided
6. **PAT rotation policy** — not yet decided
7. **Review cadence** — not yet decided
8. **Maintainer** — not yet decided
9. **Next scheduled review date** — not yet decided

### Recommended next decision

Decide and record a single accountable **Owner / account** for the space first. That decision should happen before finalizing PAT storage, PAT rotation responsibility, or long-term maintainer ownership.

---

## Review cadence for this doc

| Field | Value |
|---|---|
| **Review cadence** | not yet decided |

Until a formal cadence exists, this document should be reviewed whenever:
- a Taskade agent is added, removed, or deprecated
- a Taskade workflow is added or confirmed
- dispatch credential handling changes
- the repo utilization rule changes
- the Taskade ↔ GitHub bridge changes materially

---

## Maintainer

| Field | Value |
|---|---|
| **Maintained by** | not yet decided |

---

## Next scheduled review

| Field | Value |
|---|---|
| **Next scheduled review date** | not yet decided |

---

## Related repo documents

| File | Purpose |
|---|---|
| [`docs/pipeline_policy.md`](pipeline_policy.md) | canonical Era 3 policy |
| [`docs/concept_lanes.md`](concept_lanes.md) | repo-side lane snapshot |
| [`memory/registries/family_registry.json`](../memory/registries/family_registry.json) | machine-readable family/game registry |
| [`reviews/README.md`](../reviews/README.md) | review-build layer |
| [`games/README.md`](../games/README.md) | release-archive layer |
| [`.github/workflows/promote-build.yml`](../.github/workflows/promote-build.yml) | GitHub-side enforcement of release dispatch |
| [`docs/repo_systems_audit_2026-04-09.md`](repo_systems_audit_2026-04-09.md) | post-migration structural audit |

## Document metadata

| Field | Value |
|---|---|
| **Path** | `docs/taskade_app_reference.md` |
| **Mode** | Option A — real values where known; explicit unset values allowed (`"none"` / `"not yet decided"`); no invented values |
| **Status** | durable structure reference |
| **Date created** | 2026-04-09 |
| **Date last reviewed** | 2026-04-09 |

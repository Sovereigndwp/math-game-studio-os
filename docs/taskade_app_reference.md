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
| **Taskade space ID** | `63ifx7l9wtgfvsop` |
| **Taskade space name** | `Concept Journey Dashboard` |
| **Taskade space emoji** | 🔥 |
| **Taskade space visibility** | `collaborator` |
| **Owner / account** | not yet decided |
| **Alternate or secondary spaces** | none |
| **Space export repo** | [`github.com/Sovereigndwp/math-games`](https://github.com/Sovereigndwp/math-games) (description: `"Exported from Taskade"`) |
| **Last confirmed export** | `2026-04-10T14:51:53.528Z` (from `taskade_exports/manifest.json`) |

### Current note

The space URL, space ID, space name (`Concept Journey Dashboard`), emoji, and visibility (`collaborator`) are all confirmed from the 2026-04-10 export manifest and are now durable in the repo. The **accountable owner** is still not yet decided at the governance level and remains the highest-value missing decision because it affects credential ownership, rotation, and document maintenance. Do not assume the GitHub owner of the export repo is the accountable Taskade owner unless this is explicitly recorded.

A normalized snapshot of all Taskade projects, agents, and automations lives in [`taskade_exports/`](../taskade_exports/) — see [`taskade_exports/README.md`](../taskade_exports/README.md) for the full inventory.

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

### Active agents (14 total — confirmed from 2026-04-10 export)

The 2026-04-10 Taskade export contains **17 agent definition JSON files** in [`taskade_exports/agents/`](../taskade_exports/agents/). Of these, 14 are active and 3 are explicitly deprecated. The roster below is sourced from the export, not from informal recall.

| Agent | Taskade agent ID | Role | Trigger | Owner | Status |
|---|---|---|---|---|---|
| **Math Question QA** | `01KNMYTFPEHNWARKW3EBMPSXPQ` | QA agent for math-question content and correctness checks. | manual — run when a QA check is requested | not yet decided | active |
| **Pass Closure Agent** | `01KNQKQDTCWCX46233P9SC50RH` | Captures post-pass learnings and promotes validated rules back into the OS. | event-driven — after a completed prototype pass / pass closure request | not yet decided | active |
| **Game Build Standards Agent** | `01KNQF8R7MKP55BTX318H0HFYG` | Runs Stage 8.5 Build Standards Gate (CO + MG compliance) and returns GREEN/AMBER/RED. Evaluates specs against [`docs/build_standards_gate.md`](build_standards_gate.md). | manual — invoked immediately after Prototype Engineer outputs (Stage 8) | not yet decided | active |
| **Player Clarity Auditor** | `01KNN06QC17WFGVCFNGJ5FJRA4` | Audits first-time user clarity and instructional/UX comprehension risks. Author of the Echo Heist clarity audit. | manual — run when a clarity audit is requested | not yet decided | active |
| **Pipeline Orchestrator** | `01KNMNAPBV02J41TQPV2W5XV51` | Coordinates the end-to-end concept pipeline from idea → spec → gate → build handoff. | manual — run when pipeline coordination is requested | not yet decided | active |
| **Subject Expansion Scout** | `01KNMNA5N5S9TDB6XV9VV79YH0` | Scouts and proposes new subject/domain expansions and opportunities. | manual — run when expansion scouting is requested | not yet decided | active |
| **Prototype Engineer** | `01KNMN9NTZ9R9SVMEPPB2RPQ57` | Produces prototype specs/build-ready handoffs (Stages 6–8). | manual — run when a prototype spec is requested | not yet decided | active |
| **Curriculum Architect** | `01KNMN97E63DVSZFE50AW67BN6` | Ensures standards alignment, learning objectives, and curriculum fit. | manual — run when curriculum alignment is requested | not yet decided | active |
| **Brainstorming Specialist** | `01KNM59YXXTZ9XVS17KJ2JPV1M` | Generates raw game ideas and variations for a given learning goal/theme. | manual — run when ideation is requested | not yet decided | active |
| **Software Developer** | `01KNM0J5XFMSQTNF126ER8MS6R` | Implements the game after Stage 8.5 GREEN gate approval. | manual — started only after GREEN gate | not yet decided | active |
| **Game Design Critic** | `01KNM0ECMQFA8EYBP45WTV587M` | Provides rigorous gate reviews and critiques to enforce quality and viability. | manual — run when a design review is requested | not yet decided | active |
| **Content Expansion Agent** | `01KNT43VDGP9ZHWD4PP2D0FJTS` | P2b specialist: analyses content set, plans difficulty ramp, writes content expansion spec, validates misconception coverage, checks CCSS alignment. Author of the Trig Tower M1-rounds draft. | manual — P2b work | not yet decided | active |
| **Release Gate Agent** | `01KNT44QZCAS478T59ZCH4PVSB` | 5-domain release certification: Build Standards Compliance, Content Completeness, Player Clarity, QA Audit Status, Pass Record Completeness. Issues GREEN/AMBER/RED. Authority is final. | manual — run when release certification is requested | not yet decided | active |
| **Trig Tower Tutor** | `01KNT2RH182338E1EEG9755Q36` | Game-specific tutor agent for the Trig Tower prototype. | manual — embedded in Trig Tower UI as slide-in chat | not yet decided | active |

### Deprecated agents still present (3 total — confirmed from 2026-04-10 export)

These agents still exist in Taskade but are explicitly deprecated and should not be used for active system work.

| Agent | Taskade agent ID | Role | Trigger | Owner | Status |
|---|---|---|---|---|---|
| **⛔ Project Manager [DEPRECATED]** | `01KNM1GS0FMEFMD1Y93SA1CD8Y` | Deprecated project management agent (do not use). | manual — legacy only | not yet decided | active (deprecated) |
| **⛔ SEO Content Writer [DEPRECATED]** | `01KNM1PQG1KA37BNBT3BCJX0GH` | Deprecated SEO writing agent (do not use). | manual — legacy only | not yet decided | active (deprecated) |
| **⛔ Researcher [DEPRECATED]** | `01KNM0ENKR4NDJG812FK33969Y` | Deprecated research agent (do not use). | manual — legacy only | not yet decided | active (deprecated) |

### Governance note

Many agents are operationally live, but ownership is still unset. This creates ambiguity in accountability. The next governance improvement should be assigning an explicit **owner / account** for the space and then a clear owner for each live agent.

---

## Current live Taskade workflows

### Current known state

The 2026-04-10 Taskade export contains 15 automation JSON files under `taskade_exports/automations/`. This is the current durable export-based view of configured automations captured at export time. It is not a claim that these are the only automations that have ever existed in the space, and it does not by itself prove current enable-state or runtime usage.

| Automation | Taskade flow ID | Trigger (displayName in JSON) |
|---|---|---|
| **Game Design Pipeline Review** | `01KNM0B599YCAR5Y2JN47G8XZQ` | New Game Concept Submitted |
| **Agent Tool: Researcher** | `01KNM1NFCBFA5DPEB839QG78YC` | Agent Tool |
| **Agent Tool: Researcher** (duplicate entry) | `01KNM1P1RV4ZQJGBZ16ZP3WV7N` | Agent Tool |
| **Agent Tool: Brainstorming Specialist** | `01KNM5G0R2E5P9PRQC42TGAB41` | Agent Tool |
| **Brainstorm → Pipeline Review** | `01KNMNC88WD2TCGE2S8E5F7AF7` | New Game Concept Added (`task.added`) |
| **GO Decision → Curriculum Slot Assignment** | `01KNMND4MFXZQ73J0GFAMZX452` | GO Decision Logged on Pipeline Concept |
| **Misconception Architect — Post-Pipeline Analysis** | `01KNMPE00ZG4RQAW7V4J1MZ1GX` | Game Concept — GO Decision |
| **Pass Closure — Learning Capture & Promotion** | `01KNMPFZ021BFFKKN66GNKWD34` | Pass Completed — Capture Learnings |
| **Pull Request Issue Flow** | `01KNMRW4009NXSJJQ4H03D44BR` | New Pull Request (GitHub integration) |
| **Echo Heist — Question Audit Pipeline** | `01KNMYV115D5QC7T5MG7A0J80T` | Template Task Flow |
| **Scout Brief → Brainstorming Specialist Handoff** | `01KNQN2SYG36XVDY3ZX57V5Z06` | Scout Expansion Brief Received |
| **Scout Brief → Brainstorming Specialist Handoff v2** | `01KNQNCTBH5YSHP7AP4KACRG92` | Scout Expansion Brief Received |
| **Pass Closure Agent Automation** | `01KNQQECN35WHYYRMY8KZSRW1X` | (trigger metadata absent in export) |
| **Pipeline Stage Advancement — GO advances, NO-GO archives** | `01KNSQWQDBVEKXJC9HSY4C3JS9` | GO / NO-GO Decision Changed |
| **Pass Execution — Stage Work Dispatch (P2A→Release)** | `01KNT45P8NDC6AYZKGKCC961SQ` | Pipeline Stage Advanced (P2A → Release) |

### Interpretation notes

Observations based strictly on what the exported JSON files contain:

- **Two "Agent Tool: Researcher" entries exist** — `01KNM1NFCBFA5DPEB839QG78YC` and `01KNM1P1RV4ZQJGBZ16ZP3WV7N` — with different IDs. The Researcher agent itself is marked `[DEPRECATED]` in the agent roster above. The deprecated-agent status does not automatically disable its tool flows; if the Researcher agent is retired, these two flow entries should be audited and removed from the Taskade space.
- **Only the Pull Request Issue Flow** (`01KNMRW4009NXSJJQ4H03D44BR`) is triggered by a GitHub event in this export. It is the only automation with any observable connection to this repo's GitHub workflow surface. The other 14 automations operate entirely inside Taskade by their trigger displayNames.
- **No automation in this export explicitly targets** the `promote-build.yml` workflow via `repository_dispatch`. Whether the release-bridge automation exists outside this export, exists inside an automation not yet captured as a saved flow, or does not yet exist at all is an open governance question.
- **Owner and enable-state** are not recorded inside the exported JSON files. Both remain separate open questions that a future export or Taskade-side audit would need to answer.

If a future export changes any of the above, this section should be revised against that new export, not against recollection.

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

Updated against the 2026-04-10 Taskade export. Items that were closed by the export are marked **RESOLVED**; new items that the export surfaced are marked **NEW OPEN**; items that remain open are left as "not yet decided".

### Resolved by the 2026-04-10 export

1. ✅ **Taskade space name** — **RESOLVED** (`Concept Journey Dashboard`, confirmed from `taskade_exports/manifest.json`)
2. ✅ **Workflow discovery state** — **RESOLVED** for existence. The export-based view in the Workflows section above documents 15 automation JSON files by ID, title, and trigger displayName. Per-automation owner, enable-state, and runtime-usage documentation remain open and are tracked as a separate item below.

### Newly surfaced by the 2026-04-10 export

3. **NEW OPEN — Duplicate "Agent Tool: Researcher" automations.** Two flow entries exist (`01KNM1NFCBFA5DPEB839QG78YC` and `01KNM1P1RV4ZQJGBZ16ZP3WV7N`), and the Researcher agent itself is marked deprecated. Both flow entries should be audited and at least one removed on the Taskade side.
4. **NEW OPEN — No GitHub dispatch automation captured.** None of the 15 exported automations explicitly targets `promote-build.yml` via `repository_dispatch`. Either the release-bridge automation is not captured in this export or it does not yet exist as a saved flow. This affects the durable release handoff path documented below.

### Still open (unchanged from prior snapshot)

5. **Accountable Owner / account for the space** — not yet decided. The GitHub owner of the export repo is not automatically the accountable Taskade owner unless this is explicitly recorded.
6. **Per-agent ownership** — not yet decided for any of the 14 active agents or 3 deprecated agents. The 2026-04-10 export makes this list itemisable by Taskade agent ID, which is a prerequisite for assigning per-agent owners, but the owner field itself remains unset.
7. **PAT storage location** — not yet decided
8. **PAT rotation policy** — not yet decided
9. **Per-automation enable-state / runtime-usage documentation** — not recorded inside the exported JSON files; not yet decided
10. **Review cadence for this document** — not yet decided
11. **Maintainer of this document** — not yet decided
12. **Next scheduled review date** — not yet decided

### Recommended next decision

Now that space name, agent roster, and automation roster are resolved at the identification level, the highest-value next decision is still the single accountable **Owner / account** for the space. That decision should happen before finalizing PAT storage, PAT rotation responsibility, per-agent owner assignments, or long-term maintainer ownership.

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
| [`docs/build_standards_gate.md`](build_standards_gate.md) | Stage 8.5 Build Standards Gate policy (normalized from Taskade project `pBj7H2VZq1WPfZBs`) |
| [`docs/taskade_concept_inbox.md`](taskade_concept_inbox.md) | Taskade-tracked concepts with no formal repo packet |
| [`memory/registries/family_registry.json`](../memory/registries/family_registry.json) | machine-readable family/game registry |
| [`reviews/README.md`](../reviews/README.md) | review-build layer |
| [`games/README.md`](../games/README.md) | release-archive layer |
| [`.github/workflows/promote-build.yml`](../.github/workflows/promote-build.yml) | GitHub-side enforcement of release dispatch |
| [`docs/repo_systems_audit_2026-04-09.md`](repo_systems_audit_2026-04-09.md) | post-migration structural audit |
| [`taskade_exports/README.md`](../taskade_exports/README.md) | raw Taskade export snapshot provenance and layout |

## Document metadata

| Field | Value |
|---|---|
| **Path** | `docs/taskade_app_reference.md` |
| **Mode** | Option A — real values where known; explicit unset values allowed (`"none"` / `"not yet decided"`); no invented values |
| **Status** | durable structure reference |
| **Date created** | 2026-04-09 |
| **Date last reviewed** | 2026-04-10 (refreshed after first full Taskade export normalization) |
| **Authoritative snapshot** | [`taskade_exports/`](../taskade_exports/) — full 2026-04-10 export of the `Concept Journey Dashboard` space |

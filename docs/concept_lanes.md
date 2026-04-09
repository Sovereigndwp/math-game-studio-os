# Concept Lanes

This file tracks concepts that are in active pipeline stages. It is the
repo-native source of truth for which concepts are currently being worked
on, what stage each one is in, and which agent owns the next step.

It is deliberately lightweight. If a concept needs more detail, link out
to its concept source of truth under `concepts/<concept-slug>/`.

## What a lane entry is — and is not

A lane entry records the **approval and ownership state** of a concept as
it moves through the pipeline. It is **not**, by itself, evidence of any
of the following:

- build validation (a working preview prototype has been implemented)
- playtest validation (the concept has been tested with real learners)
- curricular coverage proof (a standard has been demonstrably taught)
- Delight Gate full pass (only conditional passes may be noted)
- Game Design Critic P1 pass record review

If a concept's build state is anything less than "prototype built and
playtested," the lane entry is a promise of future work, not a record of
completed work. Do not cite a lane entry as evidence that a family,
interaction type, or standard has been proven in the portfolio.

---

## Active concepts

### Snack Line Shuffle

> ⚠ **Validation status: approved concept only — not yet prototyped.**
> This entry documents that Snack Line Shuffle has been approved for
> concept normalization and repo placement. **No preview build exists.**
> No playtests have been run. No P1 Definition of Done has been checked.
> This lane entry must not be cited as evidence of build validation,
> curricular coverage proof, or family/interaction-type coverage. It
> records the approval state of the concept only.

- **Concept source of truth:** [`concepts/snack-line-shuffle/`](../concepts/snack-line-shuffle/)
- **Family:** Compare and Order
- **Interaction type:** `sequence_and_order`
- **Primary standard:** CCSS.MATH.CONTENT.1.OA.C.6 *(alignment claim, not fluency claim; see concept.md fluency caution)*
- **Grade band:** K–2 core (Grade 2+ ceiling layers gated)
- **Current stage:** Approved concept, entering normalization
- **Build state:** No review build — deferred. **No prototype exists.**
- **Playtest state:** None. No learners have played this concept.
- **P1 Definition of Done:** Drafted, not yet checked. See [`concepts/snack-line-shuffle/p1_definition_of_done.md`](../concepts/snack-line-shuffle/p1_definition_of_done.md).
- **Intended review path:** `reviews/snack-line-shuffle/current/index.html` (not created)
- **Slug-level placeholder:** [`reviews/snack-line-shuffle/README.md`](../reviews/snack-line-shuffle/README.md) — documents why no prototype exists yet
- **First member of family:** yes — structurally, not evidentially
- **First proof case for interaction type:** yes — pending a prototype that actually demonstrates the type
- **Next agent after normalization:** Game Design Critic (reviews P1 pass record — *after* P1 implementation, which requires separate approval)
- **Next owner after that:** Prototype Engineer (pre-build → build transition)
- **Current blocker:** None for normalization. P1 implementation requires separate explicit approval.
- **Misconception linkage:** [`artifacts/misconception_library/snack-line-shuffle-misconceptions.json`](../artifacts/misconception_library/snack-line-shuffle-misconceptions.json) — M4–M7 linked to canonical categories (core fields populated; enrichment pending after P1 playtest data)

---

## Retired / archived concepts

(none yet)

---

## Lane schema

Each active concept entry should include, at minimum:

- concept source of truth path
- family and interaction type
- primary CCSS standard and grade band
- current stage
- build state (no preview, P0, P1, P2A/B, P3, P4, P5)
- intended preview path
- next agent and next owner
- current blocker (if any)
- misconception library link

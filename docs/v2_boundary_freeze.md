# Math Game Studio OS — V2 Boundary Freeze

**Tag:** `v2.0-boundary` · **Commit:** `83a4b1b` · **Date:** 2026-04-04

---

## Status

V1 remains hardened and benchmark-stable (tag `v1.0` at `ce1c246`).
The V2 boundary is now defined. Prototype building has not begun.

This freeze marks the end of V2 boundary design, not the start of
implementation.

---

## What was added in this phase

This phase added the first V2 boundary layer across 9 commits (`8a98c64`
through `83a4b1b`):

**Core V2 artifact:**
- `prototype_spec` as the first V2 artifact and schema
- Prototype Spec Agent (prompt, config, stub with concept-specific overrides)
- `prototype_spec` gate logic (6 dimensions, reject/revise severity mapping)
- Bakery as the first V2 example (Fire Dispatch and Unit Circle Pizza Lab
  also covered by concept overrides)

**Pipeline integration:**
- Stage 6 wired into `pipeline.py` after Core Loop (Stage 5)
- Stage ledger updated to track `prototype_spec` versions, revision counts,
  and gate states
- Benchmarks 1–3 updated: `expected_stop` changed from `lowest_viable_loop_brief`
  to `prototype_spec`

**Gate hardening (post-initial implementation):**
- `fidelity_notes` non-empty check added to gate (revise on empty notes)
- Deferred/excluded overlap check added to gate (revise on intersection)
- Readiness score differentiated: concept overrides score 0.92, generic
  fallback scores 0.75

**Prompt refinements:**
- Timer/urgency rule clarified (structural only, not engagement padding)
- Dual-validation architecture documented (agent sets status, gate re-validates)

**Documentation:**
- `docs/v2_boundary.md` — scope, gate criteria, known limitations
- `docs/v1_handoff.md` — what V1 delivered and what's stable
- `README.md` — top-level orientation with pipeline stages, benchmarks,
  repo structure, gate engine summary

---

## What is now stable

The following are considered stable at this checkpoint:

- V1 benchmark stability: 5/5 passing in stub mode, 5/5 in LLM mode
- V2 boundary definition (`docs/v2_boundary.md`)
- `prototype_spec` artifact schema (`artifacts/schemas/prototype_spec.schema.json`)
- Prototype Spec Agent contract (`agents/prototype_spec/prompt.md`, `config.yaml`)
- Prototype Spec Agent stub logic (`agents/prototype_spec/agent.py`)
- `prototype_spec` gate logic (`engine/gate_engine.py :: gate_prototype_spec`)
- Pipeline integration: Stage 6 runs after Stage 5, gate enforces all 6 dimensions
- Stage ledger tracks `prototype_spec` alongside all V1 artifacts
- Bakery, Fire Dispatch, and Unit Circle Pizza Lab all produce approved
  `prototype_spec` artifacts in stub mode

---

## What remains intentionally out of scope

- Building the prototype (UI, playable implementation)
- Production game development
- Progression systems beyond prototype needs
- Monetization, analytics, or dashboard systems
- Teacher/parent-facing platforms
- Release packaging or post-launch infrastructure
- New interaction types or family types beyond the V1 taxonomy
- Broader V3 systems of any kind

---

## Known limitations documented but not fixed

The following are documented in `docs/v2_boundary.md § Known Limitations` and
in code comments, but intentionally not solved in this phase:

1. **Fidelity claims are self-reported.** The gate validates that
   `concept_fidelity_check` booleans are true and `fidelity_notes` is non-empty,
   but cannot cross-validate against upstream V1 artifacts. The gate interface
   only receives the output artifact. Fixing this requires a gate architecture
   change affecting all stages (V3+).

2. **Concept override matching is brittle.** Short keys (`"fire"`, `"pizza"`)
   match by substring against `world_theme`. False positives are possible if
   intake produces novel themes containing these words. Documented in a code
   comment at the matching block. Should be replaced with `(theme,
   interaction_type)` pair matching before LLM mode deployment.

3. **Readiness score is a support signal, not calibrated.** Concept overrides
   always score 0.92; generic fallback always scores 0.75. The score is
   informational — the gate does not use it for pass/revise decisions above 0.5.
   A per-field specificity model would be more accurate but is a scoring redesign
   outside current scope.

4. **Gate checks presence, not specificity.** Fields like
   `first_player_action` and `success_signals` are validated as non-empty strings,
   not as implementation-ready descriptions. A generic fallback output can pass the
   gate with vague wording. Stronger heuristics should be added before LLM mode
   deployment.

---

## Exact files defining the V2 boundary

| File | Role |
|---|---|
| `artifacts/schemas/prototype_spec.schema.json` | Artifact schema (24 required fields, constrained enums) |
| `agents/prototype_spec/prompt.md` | Agent contract (reasoning rules, fidelity rules, forbidden behaviors) |
| `agents/prototype_spec/config.yaml` | Agent config (allowed reads/writes, revision limit, model profile) |
| `agents/prototype_spec/agent.py` | Agent implementation (concept overrides, generic templates, stub/LLM) |
| `engine/gate_engine.py` | Gate logic (`gate_prototype_spec` — 6 dimensions) |
| `pipeline.py` | Pipeline integration (Stage 6 after Stage 5) |
| `orchestrator/stage_ledger.py` | Ledger constants updated for `prototype_spec` |
| `artifacts/schemas/stage_ledger.schema.json` | Ledger schema updated for `prototype_spec` |
| `scripts/run_benchmarks.py` | Benchmarks 1–3: `expected_stop` set to `prototype_spec` |
| `docs/v2_boundary.md` | V2 scope, gate criteria, known limitations |
| `docs/v1_handoff.md` | V1 freeze reference |
| `README.md` | Top-level orientation |

---

## Recommended next step

Define the first prototype implementation plan for Bakery, starting from the
approved `prototype_spec` artifact. Do not begin building in this document.

---

## Closing

This freeze marks the handoff point between V2 boundary design and future
prototype implementation planning. All V1 behavior is preserved. All V2
boundary work is documented, tested, and pushed.

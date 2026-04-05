# OS Document Usage Guide

## Purpose
Tell the workflow which OS document to consult for which kind of task.

## Use this when
- Starting any new pass
- Diagnosing a playtest result
- Deciding what to work on next
- Reviewing whether a pass is done

## Controls
- Every task should name which OS doc governs the work
- When multiple docs seem relevant, use the priority order below
- Do not consult docs that are not relevant to the current pass type

## Do not use this for
- Implementation details (use the game's prototype directly)
- Orchestrator or pipeline decisions (separate system)
- Broad architecture planning

---

## Document Router

### "What pass am I in?"
→ `docs/pass_system.md` — pass labels and quick diagnostic

### "What are the rules for this pass?"
→ `docs/pass_rules.md` — non-negotiable constraints, exit criteria, per-pass rules

### "Did this pass work?"
→ `docs/pass_fail_scorecard.md` — pass/fail/hold/split decision template

### "Is this level doing the right thing?"
→ `docs/level_role_map.md` — every level's one job, catches progression mistakes

### "Why does this game feel dead / boring / flat?"
→ `docs/engagement_failure_modes.md` — 20 numbered failure modes with pass-to-fix mapping

### "What should the player feel?"
→ `docs/player_feeling_targets.md` — target feelings per pass and per run phase

### "Has someone already solved this?"
→ `docs/reusable_patterns_library.md` — 12 proven patterns from existing games

### "What are the engagement rules?"
→ `docs/os_engagement_rules.md` — non-negotiable engagement patterns from game audits

### "Is this game ready to ship?"
→ `docs/release_blockers.md` — 12 hard-gate blockers with current status

### "What did the ATC / Grocery Dash audit teach?"
→ `docs/atc_math_tower_audit.md` or `docs/grocery_dash_audit.md`

### "What engagement patterns exist across all games?"
→ `docs/game_engagement_playbook.md`

---

## Priority Order

When multiple docs seem relevant, consult in this order:

1. **pass_rules.md** — am I following the rules for this pass type?
2. **pass_fail_scorecard.md** — how will I know if this pass worked?
3. **engagement_failure_modes.md** — what specific problem am I fixing?
4. **level_role_map.md** — is the progression well-shaped? (P2B only)
5. **player_feeling_targets.md** — what should the player feel after?
6. **reusable_patterns_library.md** — has this been solved before?
7. **release_blockers.md** — is there a shipping blocker? (P5 only)

---

## Rule for Future Tasks

Every task should begin with:

> **Governing doc:** `docs/<filename>.md`
> **Pass:** Game Name P#
> **Bottleneck:** one sentence

This makes the scope explicit and the stop condition clear.

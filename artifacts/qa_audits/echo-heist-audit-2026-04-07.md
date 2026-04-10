# Echo Heist — Question Audit (2026-04-07)

## Header

| Field | Value |
|---|---|
| **Game** | Echo Heist |
| **Audit date** | 2026-04-07 (Player Clarity Audit component) · 2026-04-09 (T1 / T2 fix completion) |
| **Auditor** | Player Clarity Auditor (Taskade agent `01KNN06QC17WFGVCFNGJ5FJRA4`) + Math Question QA |
| **Source file audited** | `previews/echo-heist/current.html` (external "Studio OS" codebase — NOT this repo) |
| **SHA** | `3b673e601fe372f1ee136a3bc3a17e9258fc3e70` |
| **Origin** | normalized from Taskade project `1A7jTuKq9Zqa1sMF` |
| **Raw source** | [`taskade_exports/projects/1A7jTuKq9Zqa1sMF.json`](../../taskade_exports/projects/1A7jTuKq9Zqa1sMF.json) |

### Important scope note — read before citing anything in this file

**This audit does NOT apply to `reviews/echo-heist/current/index.html`.**

This audit targets the Echo Heist build in a **separate, parallel codebase** — the Taskade-side "Studio OS" app at `app/previews/echo-heist/current.html` (SHA `3b673e601fe372f1ee136a3bc3a17e9258fc3e70`). That is a different implementation from this repo's Echo Heist review build at [`reviews/echo-heist/current/index.html`](../../reviews/echo-heist/current/index.html), which has its own pass records `pass-1-record.md` through `pass-5-record.md` in-place.

This file is preserved in the repo for **two** reasons, and **only** these two reasons:

1. **Durable cross-game engineering lessons.** The T10 float-precision root-cause analysis is the source of the canonical `roundTo()` helper now codified in [`docs/build_standards_gate.md`](../../docs/build_standards_gate.md#mg-1--float-precision-critical) (rule MG-1). The D1–D7 Player Clarity findings are the source of the six named anxiety points AP-1 through AP-6 in the same gate policy. These lessons are reusable across any game in the studio regardless of which codebase they originated in.

2. **Provenance for the above.** The gate policy cites this audit as its source of truth. Removing this file would sever that provenance chain.

**What this file is NOT:**

- It is **not** automatic evidence that `reviews/echo-heist/current/index.html` has the same bugs, the same fixes, or the same clarity gaps.
- It is **not** a pass record for this repo's Echo Heist build.
- It is **not** authorization to update `reviews/echo-heist/current/` based on anything documented below.

**How to use this file safely:**

- **Do** cite the T10 fix pattern when designing new procedural generators in any game.
- **Do** check the AP-1 through AP-6 taxonomy when auditing any game's first-interaction experience.
- **Do not** apply any diff, patch, or fix from this file to `reviews/echo-heist/current/index.html` without first independently verifying the bug exists in that build.
- **Do not** treat the "FIXES APPLIED" and "FIX DOCUMENTED" markers below as statements about this repo's build. Those markers refer to the parallel Studio OS build only.

If this repo's Echo Heist build needs its own audit, that should be a separate, freshly-run audit targeting the file at `reviews/echo-heist/current/index.html` and recorded in a separate file under `artifacts/qa_audits/`.

---

## Procedural template status (T1–T12)

| Template | Topic | Status |
|---|---|---|
| **T1** | One-step equations (`x + a = b`, `x / a = b`) | ✅ FIXES APPLIED 2026-04-09 — hint2 truncation (`makeT1` + `makeT12`) |
| **T2** | Two-step equations (`ax + b = c`, `ax - b = c`) | ✅ COMPLETE 2026-04-09 — procedural generator + 10 Echo Heist narrative wrappers + clean hints |
| **T3** | Percent change (increase / decrease from base) | ✅ FIX DOCUMENTED — `toFixed(4)` on float calculation |
| **T4** | Decimal ↔ percent conversion | open |
| **T5** | Fraction of quantity (`a/b` of `n`) | ✅ FIX DOCUMENTED — trivial-answer guard + `Math.round()` for both banks |
| **T6** | Fraction add / subtract (`a/b ± c/d`) | open |
| **T7** | Rate-time-distance (`d = r×t`, `t = d÷r`) | open |
| **T8** | Rate comparison (A vs B) | ✅ FIX DOCUMENTED — tie guard + hint2 rate-reveal fixed in patch |
| **T9** | Integer operations (signed arithmetic) | open |
| **T10** | Rounding (nearest 10, 0.1, 0.01, 100) | ✅ **CRITICAL FIX DOCUMENTED** — `roundTo()` helper + Training Gallery + Escape Lines generators patched |
| **T11** | Angle relationships (complementary / supplementary) | open |
| **T12** | Expected value (`EV = p×V₁ + (1−p)×V₂`) | open |

## Curated D3 questions (Missions 21–30)

| Mission | Title | Content |
|---|---|---|
| M21 | Platform Timing | 5 prompts + vault + escape |
| M22 | Rooftop Angles | 6 prompts + vault + escape |
| M23 | Cargo Weight | 5 prompts + vault + escape |
| M24 | Two-Step Sprint | 5 prompts + vault + escape |
| M25 | Fraction + Rate | 5 prompts + vault + escape |
| M26 | Market Choices | 5 prompts + vault + escape |
| M27 | Probability Payoff | 6 prompts + vault + escape |
| M28 | Alarm Cascade | 5 prompts + vault + escape |
| M29 | The Long Run | 5 prompts + vault + escape |
| M30 | Grand Terminal | 6 prompts + vault + escape |

## Cross-cutting issues

- [ ] **Equivalent form acceptance** — `1/2 = 0.5 = .5 = 50%` (all directions)
- [ ] **Negative answer display** — `checkAnswer('-1')` and HUD rendering
- [ ] **T8 answer bias audit** — "A" vs "B" distribution across all generated problems
- [ ] **Floating-point precision** — rounding and multiplication edge cases (root cause of the T10 critical)

---

## T10 Fix Brief — CRITICAL

### Bug summary

- **Template** — T10 Rounding
- **Severity** — CRITICAL — systematic wrong answers
- **File** — `previews/echo-heist/current.html`
- **Affected generators** — Training Gallery bank (`b = 0.1`) and Escape Lines bank (`b = 0.01`)

### Root cause

Both generators compute the rounded answer as:

```javascript
Math.round(a / b) * b
```

The division `a / b` is done in float before `Math.round()`, and JS float representation of decimal fractions is not exact. This causes the value passed to `Math.round()` to land just below the `.5` boundary, flipping it down instead of up.

**Concrete proof cases (paste in browser console to verify):**

| Input | Float intermediate | `Math.round` | Final | Expected |
|---|---|---|---|---|
| `6.65 / 0.1` | `66.49999999999999` | `66` | `6.6` ✗ | `6.7` |
| `2.45 / 0.1` | `24.499999999999996` | `24` | `2.4` ✗ | `2.5` |
| `3.845 / 0.01` | `384.49999999999994` | `384` | `3.84` ✗ | `3.85` |

### The fix — exponential notation rounding

Use exponential notation to shift the decimal point into integer space before rounding, then shift back. This avoids the float division entirely.

```javascript
function roundTo(val, decimals) {
  return Number(Math.round(+(val + 'e' + decimals)) + 'e-' + decimals);
}
```

**Proof it works (browser console):**

| Call | Result |
|---|---|
| `roundTo(6.65, 1)` | `6.7` ✓ |
| `roundTo(2.45, 1)` | `2.5` ✓ |
| `roundTo(3.845, 2)` | `3.85` ✓ |
| `roundTo(17.86, 1)` | `17.9` ✓ |
| `roundTo(9.45, 1)` | `9.5` ✓ |
| `roundTo(7.445, 2)` | `7.45` ✓ (D3 M29v2 authored case still passes) |

This canonical helper is the source of [`docs/build_standards_gate.md`](../../docs/build_standards_gate.md) MG-1.

### Diff 1 — Training Gallery bank, T10 `mk()` function

Location: inside `banks['Training Gallery']` array, 4th entry.

```
FIND:    b>=1?Math.round(a/b)*b:parseFloat((Math.round(a/b)*b).toFixed(1))
REPLACE: b>=1?Math.round(a/b)*b:roundTo(a,1)

FIND:    (Math.random()*10).toFixed(2)
REPLACE: (Math.random()*10).toFixed(1)
```

The `toFixed(2)` → `toFixed(1)` change restricts generated values to 1 decimal place (e.g. `6.6`, `3.4`) rather than 2 (e.g. `6.65`, `3.47`), eliminating the `.x5` boundary class as a secondary guard. Students still get genuine rounding practice; they just won't see ambiguous banker's-rounding edge cases.

### Diff 2 — Escape Lines bank, T10 `mk()` function

Location: inside `banks['Escape Lines']` array, 4th entry.

```
FIND:    b>=1?Math.round(a/b)*b:parseFloat((Math.round(a/b)*b).toFixed(2))
REPLACE: b>=1?Math.round(a/b)*b:roundTo(a,2)

FIND:    (Math.random()*5).toFixed(3)
REPLACE: (Math.random()*5).toFixed(2)
```

D3 authored questions (M27p6: `0.994 → 0.01`, M29v2: `7.445 → 0.01`) are authored data, not generated, so they are unaffected.

### Verification checklist (run in browser console after patch)

- [ ] `roundTo(6.65, 1) === 6.7`
- [ ] `roundTo(2.45, 1) === 2.5`
- [ ] `roundTo(3.845, 2) === 3.85`
- [ ] `roundTo(7.445, 2) === 7.45` (authored D3 M29v2 still correct)
- [ ] `roundTo(9.45, 1) === 9.5`
- [ ] `roundTo(17.86, 1) === 17.9` (authored D3 M21p4 still correct)
- [ ] `roundTo(246, 10)` — should still use the `b >= 1` integer path → `250` (no change to integer branch)
- [ ] Run 100 Training Gallery T10 prompts in game — confirm no prompt shows a float artifact
- [ ] Run 50 Escape Lines T10 prompts — confirm same
- [ ] Play D3 M29 mission in-game — solve vault lock M29v2 (`7.445 → 0.01`) and confirm answer `7.45` still accepted

### Scope — what this fix does NOT touch

- All authored D3 rounding questions (M21p4, M23p3, M25p5, M27p6, M29p3, M29v2, M23v3) — static data, unchanged
- The integer rounding branch (`b >= 1`, e.g. round to nearest 10 or 100) — `Math.round(a/b)*b` is exact for integers
- `checkAnswer` tolerance — no change needed; `roundTo()` produces exact decimal strings
- T3, T4, T5, T7, T9 generators — separate issues tracked in their own QA rows

---

## Player Clarity Audit (2026-04-07)

- **Auditor** — Player Clarity Auditor (Taskade agent `01KNN06QC17WFGVCFNGJ5FJRA4`)
- **Source audited** — `raw.githubusercontent.com/Sovereigndwp/math-game-studio-os/main/previews/echo-heist/current.html`
- **Onboarding Gap Score** — **0 / 7 dimensions clear**
- **Estimated Cold-Start Success Rate** — **~30%**
- **Top-priority fix** — Add a single Heist Briefing screen before the first puzzle with (1) objective statement, (2) controls + costs summary, (3) one worked example of answering a math lock.

### D1 — Cold Start Clarity · OPAQUE

Issues:
- No statement of the overall goal — the player does not know they are cracking a vault or what winning looks like
- No statement that prompts are math questions — the terminal just appears with no framing
- No tutorial or worked example before the first live prompt
- "Heat" used before it is defined — `Esc to cancel (costs heat)` has no explanation of what heat is or its maximum
- `H for hint (−50)` — −50 of what is never stated

**Fix:** Add a Heist Briefing screen. Text: *"You're cracking the Echo Vault. Each lock is a math puzzle. Type your answer and press Enter. Crack all N locks before heat reaches 100 to escape."* Include one worked example. Define heat, score, and hint cost explicitly.

### D2 — Goal Legibility · PARTIALLY LEGIBLE

Issues:
- No lock counter visible — player cannot tell how many locks remain
- No heat threshold labeled — player cannot see `Heat: 40/100` so they don't know how close to failure they are
- Win condition changes (vault → escape) with no announced objective change

**Fix:** HUD must show `Locks: X/N`, `Heat: Y/100`, `Score: Z` at all times. Add a pre-play objective panel.

### D3 — Stage Transition Clarity · PARTIAL / OPAQUE

Issues:
- Vault entry: no labeled overlay — player drops directly into the first terminal prompt with no stage marker
- Escape phase: silent transition — guards accelerate, escape gate appears, no announcement
- Class ability activation: no explanation of keys, cooldowns, or costs on first encounter
- Focus mode (Tab): slows time and drains points — neither effect is explained before first use

**Fix:** Interrupting overlay (require keypress) for each new phase: vault entry, escape phase, first class ability use, first focus mode use. Each overlay names the phase and states the new rule in one sentence.

### D4 — Instruction Completeness · PARTIAL

Issues:
- Answer format unstated: no instruction on whether to type integers, decimals, fractions, or percents
- Cost of a wrong submitted answer is never stated
- `Esc to cancel` — scope of cancel is ambiguous: current input, current lock, or whole mission
- Hint behavior unstated: how many hints per lock, what form the hint takes

**Fix:** Briefing screen must include: *"Type as a number (e.g. 12, 3.5, −2). Fractions: 1/2. Percents: type the number only (e.g. 25 for 25%). Wrong answer: +10 Heat. Esc: skip this lock (+20 Heat). H: one hint per lock (−50 score)."*

### D5 — Feedback Legibility · PARTIAL

Issues:
- Wrong answer: no visible message showing what the correct answer was
- Heat and score deltas are not shown as labeled numbers — bar moves but player cannot tell by how much
- Esc and H actions produce no visible confirmation message

**Fix:** Labeled feedback on every action:
- Correct → green `LOCK CRACKED! +100 score`
- Wrong → red `Wrong. Answer: [X]. +10 Heat`
- Hint → amber `Hint shown. −50 score`
- Esc → orange `Lock skipped. +20 Heat`

### D6 — Vocabulary & Language · PARTIAL

Issues:
- "Heat" used without definition — could mean temperature or fire to a Gr 6–8 student unfamiliar with stealth conventions
- "Cancel" is too broad — does not specify scope (input, lock, or mission)

**Fix:** Define in briefing: *"Heat = guard suspicion (0–100). If it hits 100 you're caught."* Replace `Esc to cancel` with `Esc = skip this lock (+20 Heat)`. Replace `H for hint (−50)` with `H = hint (costs 50 score)`.

### D7 — Anxiety Points (source of AP-1 through AP-6 in `build_standards_gate.md`)

| Severity | Issue |
|---|---|
| **HIGH** | Heat pressure from second one with no defined maximum or consequence — player fears submitting any answer |
| **HIGH** | All three action costs (wrong answer, Esc, H) are ambiguous — player cannot make informed decisions |
| **MEDIUM** | Sudden vault → escape transition with accelerating guards and no overlay explaining the new phase |
| **MEDIUM** | Focus mode Tab cost (2 pts/sec drain) is not explained before activation — player may hesitate to use a core scaffold tool |
| **LOW** | Esc is dual-purpose (skip lock + possible exit intent) — players afraid to accidentally skip a lock when trying to pause |

---

## Player Clarity Fix Tasks

| Code | Priority | Task | Status |
|---|---|---|---|
| **PC1** | 🔴 TOP | Heist Briefing Screen (4-section: objective · costs & controls · worked example · answer formats) | ✅ FIX DOCUMENTED (patch FIX 7) |
| **PC2** | 🔴 | Labeled feedback on every action (correct / wrong / hint / Esc) with color + duration spec | ✅ FIX DOCUMENTED (patch FIX 8) |
| **PC3** | 🟠 | HUD: labeled heat maximum `Heat: 40/100`, lock counter `Locks: 2/5`, score label `Score: 450` | ✅ FIX DOCUMENTED (patch FIX 9) |
| **PC4** | 🟠 | Focus-mode first-use tooltip (1500 ms non-blocking) + active banner `FOCUS ACTIVE — 2 pts/sec` | ✅ FIX DOCUMENTED (patch FIX 10) |
| **PC5** | 🟡 | Separate pause key (`P`) from `Esc` (skip-lock + heat cost) | ✅ FIX DOCUMENTED (patch FIX 11) |

---

## Patch status

- **Patch doc** — `app/docs/echo-heist-patch-2026-04-07.md` — 11 fixes, copy-paste ready
- **CRITICAL fixes** — T10 float (FIX 1–3), T8 tie+hint (FIX 4), T3 float (FIX 5), T5 trivial+float (FIX 6)
- **Clarity fixes** — PC1 briefing (FIX 7), PC2 feedback overlays (FIX 8), PC3 HUD labels (FIX 9), PC4 focus tooltip (FIX 10), PC5 P=pause (FIX 11)

### Follow-ups

- [ ] Engineer applies patch to `previews/echo-heist/current.html` and commits (external codebase)
- [ ] Run verification checklist (11 items at bottom of patch doc)
- [ ] Re-run audit pipeline on T8, T10 after patch to confirm PASS status
- [ ] **This repo:** check `reviews/echo-heist/current/index.html` for the same T10 float bug and apply the `roundTo()` helper if missing

## Related repo documents

- [`docs/build_standards_gate.md`](../../docs/build_standards_gate.md) — policy document derived from this audit (MG-1, AP-1 through AP-6)
- [`reviews/echo-heist/current/`](../../reviews/echo-heist/current/) — this repo's Echo Heist build (separate codebase from the audit source)
- [`artifacts/learning_captures/2026-04-09-fire-dispatch-audit-lessons.md`](../learning_captures/2026-04-09-fire-dispatch-audit-lessons.md) — sibling audit lessons

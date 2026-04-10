# Echo Heist — Question Audit Results

# Procedural Templates (D1 + D2)

- [ ] T1 — One-Step Equations (x+a=b, x/a=b) *✅ FIXES APPLIED 2026-04-09 — hint2 truncation (makeT1 + makeT12)*
- [ ] T2 — Two-Step Equations (ax+b=c, ax-b=c) *✅ COMPLETE 2026-04-09 — procedural generator + 10 Echo Heist narrative wrappers + clean hints*
- [ ] T3 — Percent Change (increase/decrease from base) *✅ FIX DOCUMENTED — toFixed(4) on float calculation*
- [ ] T4 — Decimal ↔ Percent Conversion
- [ ] T5 — Fraction of Quantity (a/b of n) *✅ FIX DOCUMENTED — trivial answer guard + Math.round() for both banks*
- [ ] T6 — Fraction Add/Subtract (a/b ± c/d)
- [ ] T7 — Rate-Time-Distance (d=r×t, t=d÷r)
- [ ] T8 — Rate Comparison (A vs B, which is better?) *✅ FIX DOCUMENTED — tie guard + hint2 rate reveal fixed in patch*
- [ ] T9 — Integer Operations (signed arithmetic)
- [ ] T10 — Rounding (nearest 10, 0.1, 0.01, 100) *✅ FIX DOCUMENTED — roundTo() helper + Training Gallery + Escape Lines generators patched*
- [ ] T11 — Angle Relationships (complementary/supplementary)
- [ ] T12 — Expected Value (EV = p×V₁ + (1−p)×V₂)

# Curated D3 Questions (Missions 21–30)

- [ ] M21 — Platform Timing (5 prompts + vault + escape)
- [ ] M22 — Rooftop Angles (6 prompts + vault + escape)
- [ ] M23 — Cargo Weight (5 prompts + vault + escape)
- [ ] M24 — Two-Step Sprint (5 prompts + vault + escape)
- [ ] M25 — Fraction + Rate (5 prompts + vault + escape)
- [ ] M26 — Market Choices (5 prompts + vault + escape)
- [ ] M27 — Probability Payoff (6 prompts + vault + escape)
- [ ] M28 — Alarm Cascade (5 prompts + vault + escape)
- [ ] M29 — The Long Run (5 prompts + vault + escape)
- [ ] M30 — Grand Terminal (6 prompts + vault + escape)

# Cross-Cutting Issues

- [ ] Equivalent form acceptance — 1/2 = 0.5 = .5 = 50% (all directions)
- [ ] Negative answer display — checkAnswer('-1') and HUD rendering
- [ ] T8 answer bias audit — 'A' vs 'B' distribution across all generated problems
- [ ] Floating-point precision — rounding and multiplication edge cases

# Player Clarity Audit — Fix Tasks (2026-04-07)

- [x] 🔴 P1 — Vault Entry Transition: no warning, no explanation, instant timed puzzle *\[Prototype Engineer → DONE ✅]*
- [x] 🔴 P2 — Escape Phase Activation: silent state change, guards accelerate, new locked gate appears with no introduction *\[Prototype Engineer → DONE ✅]*
- [x] 🟠 P3 — Heat & Noise undefined: both systems are live from the first second of play with no explanation *\[Prototype Engineer → DONE ✅]*

# T10 Fix Brief — Prototype Engineer

## Bug Summary

- **Template: T10 — Rounding**
- **Severity: CRITICAL — systematic wrong answers**
- File: **previews/echo-heist/current.html** (SHA 3b673e601fe372f1ee136a3bc3a17e9258fc3e70)
- Affected generators: Training Gallery bank (b=0.1) and Escape Lines bank (b=0.01)

## Root Cause

Both generators compute the rounded answer as:

**Math.round(a / b) \* b**

The division a/b is done in float before Math.round(), and JS float representation of decimal fractions is not exact. This causes the value passed to Math.round() to land just below the .5 boundary, flipping it down instead of up.

Concrete proof cases (paste in browser console to verify):

1. 6.65 / 0.1  →  66.49999999999999  →  Math.round = 66  →  66 \* 0.1 = 6.6  ✗  (correct: 6.7)
2. 2.45 / 0.1  →  24.499999999999996  →  Math.round = 24  →  24 \* 0.1 = 2.4  ✗  (correct: 2.5)
3. 3.845 / 0.01  →  384.49999999999994  →  Math.round = 384  →  384 \* 0.01 = 3.84  ✗  (correct: 3.85)

## The Fix — Exponential Notation Rounding

Use exponential notation to shift the decimal point into integer space before rounding, then shift back. This avoids the float division entirely.

Add this helper once, near the top of the \<script> block (after the CONSTANTS section, before DISTRICT CONFIG):

**function roundTo(val, decimals) { return Number(Math.round(+(val + 'e' + decimals)) + 'e-' + decimals); }**

Proof it works (browser console):

1. roundTo(6.65, 1)   →  6.7  ✓
2. roundTo(2.45, 1)   →  2.5  ✓
3. roundTo(3.845, 2)  →  3.85 ✓
4. roundTo(17.86, 1)  →  17.9 ✓
5. roundTo(9.45, 1)   →  9.5  ✓
6. roundTo(7.445, 2)  →  7.45 ✓  (D3 M29v2 authored case still passes)

## Diff 1 — Training Gallery bank, T10 mk() function

Location: inside banks\['Training Gallery'] array, 4th entry (the Round {a} to nearest {b} template). Search for the string: Math.round(a/b)\*b).toFixed(1)

**BEFORE:**

mk:(a,b)=>{const r=b>=1?Math.round(a/b)\*b:parseFloat((Math.round(a/b)\*b).toFixed(1));return{answer:''+r,hint1:'Rounding',hint2:\`Look at the digit after ${b}\`}},gen:()=>{const rules=\[\[10,()=>10+Math.floor(Math.random()\*90)],\[0.1,()=>parseFloat((Math.random()\*10).toFixed(2))]];const\[b,fn]=rules\[Math.floor(Math.random()\*rules.length)];return{a:fn(),b}}

**AFTER:**

mk:(a,b)=>{const r=b>=1?Math.round(a/b)\*b:roundTo(a,1);return{answer:''+r,hint1:'Rounding',hint2:\`Look at the digit after ${b}\`}},gen:()=>{const rules=\[\[10,()=>10+Math.floor(Math.random()\*90)],\[0.1,()=>parseFloat((Math.random()\*10).toFixed(1))]];const\[b,fn]=rules\[Math.floor(Math.random()\*rules.length)];return{a:fn(),b}}

Two changes in this diff:

1. mk(): replace parseFloat((Math.round(a/b)\*b).toFixed(1)) with roundTo(a,1)
2. gen(): change (Math.random()\*10).toFixed(2) to (Math.random()\*10).toFixed(1)  — this restricts generated values to 1dp (e.g. 6.6, 3.4) rather than 2dp (e.g. 6.65, 3.47), eliminating the .x5 boundary class as a secondary guard. Students still get genuine rounding practice; they just won't see ambiguous banker's-rounding edge cases.

## Diff 2 — Escape Lines bank, T10 mk() function

Location: inside banks\['Escape Lines'] array, 4th entry (Round {a} to nearest {b}). Search for the string: Math.round(a/b)\*b).toFixed(2)

**BEFORE:**

mk:(a,b)=>{const r=b>=1?Math.round(a/b)\*b:parseFloat((Math.round(a/b)\*b).toFixed(2));return{answer:''+r,hint1:'Rounding',hint2:'Look at the next digit'}},gen:()=>{const rules=\[\[100,()=>100+Math.floor(Math.random()\*900)],\[0.01,()=>parseFloat((Math.random()\*5).toFixed(3))]];const\[b,fn]=rules\[Math.floor(Math.random()\*rules.length)];return{a:fn(),b}}

**AFTER:**

mk:(a,b)=>{const r=b>=1?Math.round(a/b)\*b:roundTo(a,2);return{answer:''+r,hint1:'Rounding',hint2:'Look at the next digit'}},gen:()=>{const rules=\[\[100,()=>100+Math.floor(Math.random()\*900)],\[0.01,()=>parseFloat((Math.random()\*5).toFixed(2))]];const\[b,fn]=rules\[Math.floor(Math.random()\*rules.length)];return{a:fn(),b}}

Two changes in this diff:

1. mk(): replace parseFloat((Math.round(a/b)\*b).toFixed(2)) with roundTo(a,2)
2. gen(): change (Math.random()\*5).toFixed(3) to (Math.random()\*5).toFixed(2)  — restricts to 2dp values, removing the 3dp .xx5 boundary class. D3 authored questions (M27p6: 0.994→0.01, M29v2: 7.445→0.01) are authored data, not generated, so they are unaffected.

## Complete patch (copy-paste ready)

Step 1 — Add helper after the DEG constant line (search: const DEG = Math.PI / 180;):

**function roundTo(val,decimals){return Number(Math.round(+(val+'e'+decimals))+'e-'+decimals);}**

Step 2 — Training Gallery T10 generator. Find exact string:

FIND:    b>=1?Math.round(a/b)\*b:parseFloat((Math.round(a/b)\*b).toFixed(1))

**REPLACE: b>=1?Math.round(a/b)\*b:roundTo(a,1)**

FIND:    (Math.random()\*10).toFixed(2)

**REPLACE: (Math.random()\*10).toFixed(1)**

Step 3 — Escape Lines T10 generator. Find exact string:

FIND:    b>=1?Math.round(a/b)\*b:parseFloat((Math.round(a/b)\*b).toFixed(2))

**REPLACE: b>=1?Math.round(a/b)\*b:roundTo(a,2)**

FIND:    (Math.random()\*5).toFixed(3)

**REPLACE: (Math.random()\*5).toFixed(2)**

## Verification checklist (run in browser console after patch)

- [ ] roundTo(6.65,1) === 6.7
- [ ] roundTo(2.45,1) === 2.5
- [ ] roundTo(3.845,2) === 3.85
- [ ] roundTo(7.445,2) === 7.45  (authored D3 M29v2 still correct)
- [ ] roundTo(9.45,1) === 9.5
- [ ] roundTo(17.86,1) === 17.9  (authored D3 M21p4 still correct)
- [ ] roundTo(246,10) — should still use the b>=1 integer path → 250 (no change to integer rounding branch)
- [ ] Run 100 Training Gallery T10 prompts in game — confirm no prompt shows a float artifact in the answer or hint text
- [ ] Run 50 Escape Lines T10 prompts — confirm same

# 🔎 Player Clarity Audit — 2026-04-07

- Auditor: Player Clarity Auditor (Agent 01KNN06QC17WFGVCFNGJ5FJRA4)
- Source: https://raw.githubusercontent.com/Sovereigndwp/math-game-studio-os/main/previews/echo-heist/current.html
- **Onboarding Gap Score: 0/7 dimensions clear**
- **Estimated Cold-Start Success Rate: \~30%**
- **Top Priority Fix:** Add a single Heist Briefing screen before the first puzzle with (1) objective statement, (2) controls + costs summary, (3) one worked example of answering a math lock.

## D1 — Cold Start Clarity · OPAQUE

- No statement of the overall goal — the player does not know they are cracking a vault or what winning looks like
- No statement that prompts are math questions — the terminal just appears with no framing
- No tutorial or worked example before the first live prompt
- 'Heat' used before it is defined — 'Esc to cancel (costs heat)' has no explanation of what heat is or its maximum
- 'H for hint (−50)' — −50 of what is never stated

**Fix:** Add a Heist Briefing screen. Text: 'You're cracking the Echo Vault. Each lock is a math puzzle. Type your answer and press Enter. Crack all N locks before heat reaches 100 to escape.' Include one worked example. Define heat, score, and hint cost explicitly.

## D2 — Goal Legibility · PARTIALLY LEGIBLE

- No lock counter visible — player cannot tell how many locks remain or what completing them achieves
- No heat threshold labeled — player cannot see 'Heat: 40/100' so they don't know how close to failure they are
- Win condition changes (vault → escape) with no announced objective change

**Fix:** HUD must show 'Locks: X/N', 'Heat: Y/100', 'Score: Z' at all times. Add a pre-play objective panel: '• Crack all N locks. • Keep heat below 100. • Escape once all locks are cracked.'

## D3 — Stage Transition Clarity · PARTIAL / OPAQUE

- Vault entry: no labeled overlay — player drops directly into the first terminal prompt with no stage marker
- Escape phase: silent transition — guards accelerate, escape gate appears, no announcement
- Class ability activation: no explanation of keys, cooldowns, or costs on first encounter
- Focus mode (Tab): slows time and drains points — neither effect is explained before first use

**Fix:** Interrupting overlay (require keypress) for each new phase: vault entry, escape phase, first class ability use, first focus mode use. Each overlay names the phase and states the new rule in one sentence.

## D4 — Instruction Completeness · PARTIAL

- Answer format unstated: no instruction on whether to type integers, decimals, fractions, or percents
- Cost of a wrong submitted answer is never stated — player has no way to know whether pressing Enter on an uncertain answer is risky
- 'Esc to cancel' — scope of cancel is ambiguous: current input, current lock, or whole mission
- Hint behavior unstated: how many hints per lock, what form the hint takes

**Fix:** Briefing screen must include: 'Type as a number (e.g. 12, 3.5, −2). Fractions: 1/2. Percents: type the number only (e.g. 25 for 25%). Wrong answer: +10 Heat. Esc: skip this lock (+20 Heat). H: one hint per lock (−50 score).'

## D5 — Feedback Legibility · PARTIAL

- Wrong answer: no visible message showing what the correct answer was
- Heat and score deltas are not shown as labeled numbers — bar moves but player cannot tell by how much
- Esc and H actions produce no visible confirmation message

**Fix:** On correct: green 'LOCK CRACKED! +100 score'. On wrong: red 'Wrong. Answer: \[X]. +10 Heat'. On hint: amber 'Hint shown. −50 score'. On Esc: orange 'Lock skipped. +20 Heat'. All as brief floating text overlays with labeled delta.

## D6 — Vocabulary & Language · PARTIAL

- 'Heat' used without definition — could mean temperature or fire to a Gr 6–8 student unfamiliar with stealth game conventions
- 'Cancel' is too broad — does not specify scope (input, lock, or mission)

**Fix:** Define in briefing: 'Heat = guard suspicion (0–100). If it hits 100 you're caught.' Replace 'Esc to cancel' with 'Esc = skip this lock (+20 Heat)'. Replace 'H for hint (−50)' with 'H = hint (costs 50 score)'.

## D7 — Anxiety Points

- **HIGH —** Heat pressure from second one with no defined maximum or consequence — player fears submitting any answer
- **HIGH —** All three action costs (wrong answer, Esc, H) are ambiguous — player cannot make informed decisions
- **MEDIUM —** Sudden vault → escape transition with accelerating guards and no overlay explaining the new phase
- **MEDIUM —** Focus mode Tab cost (2pts/sec drain) is not explained before activation — player may hesitate to use a core scaffold tool
- **LOW —** Esc is dual-purpose (skip lock + possible exit intent) — players afraid to accidentally skip a lock when trying to pause

# 🛠 Player Clarity Fix Tasks — Prototype Engineer

- [x] **🔴 PC1 — Heist Briefing Screen (TOP PRIORITY)** *✅ FIX DOCUMENTED in patch (FIX 7)*
  - Show before Mission 1 and any mission with no prior play — requires keypress (Space or Enter) to dismiss
  - Section 1 — Objective: 'You're cracking the Echo Vault. Each lock is a math puzzle. Crack all locks before heat reaches 100 to escape.'
  - Section 2 — Costs & Controls: Wrong answer: +10 Heat | Esc = skip this lock (+20 Heat) | H = hint (−50 score, 1 per lock) | Tab = Focus (slows time, costs 2 pts/sec) | P = pause
  - Section 3 — Worked example: 'Lock: 3x + 5 = 14. You type: 3. Press Enter → LOCK CRACKED. +100 score.'
  - Section 4 — Answer formats: 'Type as a number (12, 3.5, −2). Fractions: 1/2. Percents: type digits only (25 for 25%).' If game accepts both 0.5 and 1/2, say so explicitly.
- [x] **🔴 PC2 — Labeled Feedback on Every Action** *✅ FIX DOCUMENTED in patch (FIX 8)*
  - Correct: green floating text 'LOCK CRACKED! +100 score' — 1200ms, top-center
  - Wrong: red floating text 'Wrong — answer was \[X]. +10 Heat.' — 2000ms, shows correct answer always
  - Hint: amber text 'Hint shown. −50 score.' — 1000ms
  - Esc: orange text 'Lock skipped. +20 Heat.' — 1000ms
- [x] **🟠 PC3 — HUD: Labeled Heat Maximum and Lock Counter** *✅ FIX DOCUMENTED in patch (FIX 9)*
  - Heat bar label must read 'Heat: 40/100' (not just a bar) — player must know the maximum
  - Add lock counter to HUD: 'Locks: 2/5' visible at all times during mission
  - HUD score label: 'Score: 450' — not a raw number, needs the label
- [x] **🟠 PC4 — Focus Mode First-Use Tooltip** *✅ FIX DOCUMENTED in patch (FIX 10)*
  - On Tab press for first time ever: show 1500ms non-blocking overlay 'FOCUS MODE — Time slows to 25% speed. Costs 2 points per second. Press Tab again to exit.' — use focusModeTipFired flag (localStorage)
  - While Focus is active: show purple banner 'FOCUS ACTIVE — 2 pts/sec' — same style as the existing softstep indicator
- [x] **🟡 PC5 — Separate Pause Key from Esc** *✅ FIX DOCUMENTED in patch (FIX 11)*
  - Assign P key to pause/settings (no heat cost). Esc remains 'skip this lock (+20 Heat)' only.
  - Update all control legend text to distinguish Esc (skip, costs heat) from P (pause, free)

<!---->

- [ ] Play D3 M29 mission in-game — solve vault lock M29v2 (7.445 → 0.01) and confirm answer '7.45' still accepted

## Scope — what this fix does NOT touch

- All authored D3 rounding questions (M21p4, M23p3, M25p5, M27p6, M29p3, M29v2, M23v3) — these are static data and unchanged
- The integer rounding branch (b >= 1, e.g. round to nearest 10 or 100) — Math.round(a/b)\*b is exact for integers and is not changed
- checkAnswer tolerance — no change needed. roundTo() produces exact decimal strings that match student input directly
- T3, T4, T5, T7, T9 generators — separate issues tracked in their own QA rows

# 📋 Patch Status — 2026-04-07

- Patch doc: **app/docs/****echo-heist-patch-2026-04-07.md** — 11 fixes, copy-paste ready
- CRITICAL fixes ready: T10 float (FIX 1-3), T8 tie+hint (FIX 4), T3 float (FIX 5), T5 trivial+float (FIX 6)
- Clarity fixes ready: PC1 briefing (FIX 7), PC2 feedback overlays (FIX 8), PC3 HUD labels (FIX 9), PC4 focus tooltip (FIX 10), PC5 P=pause (FIX 11)

<!---->

- [ ] Engineer applies patch to previews/echo-heist/current.html and commits
- [ ] Run verification checklist (11 items at bottom of patch doc)
- [ ] Re-run audit pipeline on T8, T10 after patch to confirm PASS status

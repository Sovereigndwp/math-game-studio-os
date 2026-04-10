# Genesis Build Progress — Math Game Studio OS

# 📍 Current State — 2026-04-10

13 tabs in Studio OS. Load failure FIXED: BakeryRush.tsx was imported in App.tsx but file did not exist. Created BakeryRush.tsx (Tab 13): 12 rounds K-2 addition fluency, M1/M2/M3/M4, boss round R11, 3 tabs (Play/Level Browser/MC Key). SLS audit project (estDxAUXWBeMtJet) added as knowledge to Math Question QA agent. Bakery Rush added to Game Concepts Pipeline (ba11b900-cafe-4000-8001-000000000001) with all gcf fields. P1 spec pending in Prototype Specifications. SLS already in QA Hub GAMES registry. TopBar already had Cake icon + bakery view. App.tsx already had BakeryRush routing.

~~Echo Heist LIVE via split files. app/public/echo-heist/: index.html + data.js + engine.js + math.js + ui.js + main.js. All 4 clarity patches baked in. GAME_URL = '/echo-heist/index.html'. Game renders class select → mission select → play → end screen. 30 missions (D1/D2/D3). LocalStorage save. Daily seed mission.~~

# 🗂 Projects (14 total)

- [x] Game Concepts Pipeline — LnpYq2qGt5DrXpda (board, custom fields, Echo Heist + 4 prototypes)
- [x] K-12 Curriculum Map — fQKsxPJWgG2kPRoQ (slots: Percents, Algebra, Division, Missing Value)
- [x] Prototype Specifications — 9bfNR2acXuAHiWyC (5 specs: Bakery Rush, Fire Dispatch, Power Grid, School Trip Fleet, Echo Heist)
- [x] Game Family Registry — N9S2kjQdv3s7tyya (8 families; 3 GAPs: Routing, Sequence, Build)
- [x] Misconception Library — cyt3zvpjf32D1Ddt (seeded: Bakery Rush, Fire Dispatch, Unit Circle, Power Grid, School Trip Fleet)
- [x] Echo Heist Question Audit Results — 1A7jTuKq9Zqa1sMF (12 templates T1-T12, 10 D3 missions M21-M30, 4 cross-cutting issues)
- [x] Playtest Audit / Pass Rules / Execution Handoff / Portfolio / Math Game Studio OS — all created and seeded
- [x] ✅ GAP CLOSED: Bakery Rush QA — 72ZxzsrS1yu4cUnR (BR-T1–T6 + 2 cross-cutting) · Fire Dispatch QA — ZpbMJ7Dvpt9NVxmN (FD-T1–T4 + FD-M1–M8 + 2 cross-cutting). Both added as knowledge to Math Question QA agent (01KNMYTFPEHNWARKW3EBMPSXPQ).
- [x] Build Standards Checklist — pBj7H2VZq1WPfZBs (list view) — CO-1 through CO-6 rules, MG-1 through MG-6 rules, AP-1 through AP-6 named anxiety points, gate status definitions, compliance statement template, pipeline position

# 🤖 Agents (12 total)

- [x] Pipeline Orchestrator — 01KNMNAPBV02J41TQPV2W5XV51 · tools: Misconception Architect + Pass Closure flows · knowledge: Misconception Library + Family Registry
- [x] Game Design Critic — 01KNM0ECMQFA8EYBP45WTV587M (public) · knowledge: Misconception Library + Family Registry
- [x] Math Question QA — 01KNMYTFPEHNWARKW3EBMPSXPQ (public) · knowledge: Audit Results + Prototype Specs · tools: QA Pipeline workflow
- [x] Curriculum Architect — 01KNMN97E63DVSZFE50AW67BN6 · Prototype Engineer — 01KNMN9NTZ9R9SVMEPPB2RPQ57 · Subject Scout — 01KNMNA5N5S9TDB6XV9VV79YH0
- [x] Player Clarity Auditor — 01KNN06QC17WFGVCFNGJ5FJRA4 · Brainstorming Specialist — 01KNM59YXXTZ9XVS17KJ2JPV1M (needs public visibility)
- [x] GAP: Brainstorming Specialist still private — app agent panel can't embed its chat publicly
- [ ] GAP: No agent has the QA Audit Results project added as knowledge for Bakery Rush / Fire Dispatch templates
  - What is the exact structure and content of the “QA Audit Results” project (e.g., collections, fields, tags) that needs to be added as knowledge?
    - Are Echo Heist templates, Bakery Rush, and Fire Dispatch results stored in the same project or separate ones?
    - Do we need to filter or scope which parts of the project each agent can see?
  - Which specific agents need the QA Audit Results project added as knowledge for Bakery Rush and Fire Dispatch templates?
    - Is this limited to the “Math Question QA” agent, or should “Pipeline Orchestrator,” “Game Design Critic,” or others also read these results?
    - Should Bakery Rush / Fire Dispatch audits be available to the Player Clarity Auditor as well?
  - How should the QA Audit Results knowledge be scoped per agent?
    - Should each agent see all games’ audit results, or only the game family / prototype they’re working on?
    - Do we need separate knowledge profiles per game (Echo Heist vs. Bakery Rush vs. Fire Dispatch)?
    - Should agents use QA results as hard constraints (blocking) or as soft guidance (suggestions)?
  - What is the intended workflow where agents consume this QA Audit Results knowledge?
    - At what step in the QA pipeline for Bakery Rush / Fire Dispatch should the agent reference past audit results?
    - Should agents use these results to auto-flag recurring issues (e.g., randomization, hint clarity, skill misalignment)?
    - Do we want agents to propose patches directly based on audit patterns?
  - How will we map Bakery Rush / Fire Dispatch templates to the QA Audit Results entries?
    - Are there stable template IDs, question codes, or mission IDs we can use to link templates to their QA records?
    - Do we need a naming convention or tagging scheme (e.g., BR-T1, FD-M3) to keep cross-game audits consistent?
    - How do we handle templates that are shared or cloned across games?
  - What access / permission model is required for agents to read the QA Audit Results project?
    - Is the QA Audit Results project already accessible to public agents, or does it require permission changes?
    - Are there any privacy or internal-notes fields that agents should not surface to end users?
  - Do we need to adjust any existing automation to incorporate this knowledge?
    - Should the “Math Question QA” agent’s workflow be updated to automatically pull in relevant Bakery Rush / Fire Dispatch audit history?
    - Does the Echo Heist Question Audit Pipeline need to be generalized to a cross-game QA pipeline that uses the Audit Results project as a shared backend?
  - How will we test that agents are correctly using the QA Audit Results for Bakery Rush / Fire Dispatch?
    - What are 2–3 representative test questions or templates per game to run through the agents?
    - What success criteria define “knowledge correctly integrated” (e.g., agent references a prior audit note, avoids a known pitfall, suggests aligned fixes)?
    - How will we log or observe when agents consult versus ignore the QA Audit Results?
  - How should we keep the QA Audit Results knowledge up to date for Bakery Rush / Fire Dispatch?
    - When new audits are run, will results be automatically written into the same project with consistent formatting?
    - Do we need a versioning or “superseded by” system so agents don’t rely on outdated audit notes?
    - Who is responsible for maintaining the taxonomy (templates T1–T12, D3 missions, etc.) across games?
  - Are there any UI or documentation updates needed once agents have this knowledge?
    - Should the QA Dashboard view surface which agents are currently using the Audit Results for each game?
    - Do we want a simple “knowledge map” doc describing which projects feed which agents, especially for Bakery Rush and Fire Dispatch?
  - What is the exact structure and content of the “QA Audit Results” project (e.g., collections, fields, tags) that needs to be added as knowledge?
    - Are Echo Heist templates, Bakery Rush, and Fire Dispatch results stored in the same project or separate ones?
    - Do we need to filter or scope which parts of the project each agent can see?
  - Which specific agents need the QA Audit Results project added as knowledge for Bakery Rush and Fire Dispatch templates?
    - Is this limited to the “Math Question QA” agent, or should “Pipeline Orchestrator,” “Game Design Critic,” or others also read these results?
    - Should Bakery Rush / Fire Dispatch audits be available to the Player Clarity Auditor as well?
  - How should the QA Audit Results knowledge be scoped per agent?
    - Should each agent see all games’ audit results, or only the game family / prototype they’re working on?
    - Do we need separate knowledge profiles per game (Echo Heist vs. Bakery Rush vs. Fire Dispatch)?
    - Should agents use QA results as hard constraints (blocking) or as soft guidance (suggestions)?
  - What is the intended workflow where agents consume this QA Audit Results knowledge?
    - At what step in the QA pipeline for Bakery Rush / Fire Dispatch should the agent reference past audit results?
    - Should agents use these results to auto-flag recurring issues (e.g., randomization, hint clarity, skill misalignment)?
    - Do we want agents to propose patches directly based on audit patterns?
  - How will we map Bakery Rush / Fire Dispatch templates to the QA Audit Results entries?
    - Are there stable template IDs, question codes, or mission IDs we can use to link templates to their QA records?
    - Do we need a naming convention or tagging scheme (e.g., BR-T1, FD-M3) to keep cross-game audits consistent?
    - How do we handle templates that are shared or cloned across games?
  - What access / permission model is required for agents to read the QA Audit Results project?
    - Is the QA Audit Results project already accessible to public agents, or does it require permission changes?
    - Are there any privacy or internal-notes fields that agents should not surface to end users?
  - Do we need to adjust any existing automation to incorporate this knowledge?
    - Should the “Math Question QA” agent’s workflow be updated to automatically pull in relevant Bakery Rush / Fire Dispatch audit history?
    - Does the Echo Heist Question Audit Pipeline need to be generalized to a cross-game QA pipeline that uses the Audit Results project as a shared backend?
  - How will we test that agents are correctly using the QA Audit Results for Bakery Rush / Fire Dispatch?
    - What are 2–3 representative test questions or templates per game to run through the agents?
    - What success criteria define “knowledge correctly integrated” (e.g., agent references a prior audit note, avoids a known pitfall, suggests aligned fixes)?
    - How will we log or observe when agents consult versus ignore the QA Audit Results?
  - How should we keep the QA Audit Results knowledge up to date for Bakery Rush / Fire Dispatch?
    - When new audits are run, will results be automatically written into the same project with consistent formatting?
    - Do we need a versioning or “superseded by” system so agents don’t rely on outdated audit notes?
    - Who is responsible for maintaining the taxonomy (templates T1–T12, D3 missions, etc.) across games?
  - Are there any UI or documentation updates needed once agents have this knowledge?
    - Should the QA Dashboard view surface which agents are currently using the Audit Results for each game?
    - Do we want a simple “knowledge map” doc describing which projects feed which agents, especially for Bakery Rush and Fire Dispatch?
- [x] Game Build Standards Agent — 01KNQF8R7MKP55BTX318H0HFYG (public) · knowledge: Build Standards Checklist project (pBj7H2VZq1WPfZBs) · gate: Prototype Engineer → Software Developer · tools: ai.ask + web.search
- [x] ✅ Content Expansion Agent — 01KNT43VDGP9ZHWD4PP2D0FJTS (private) · P2b specialist: analyzes content set, plans difficulty ramp, writes content expansion spec, validates misconception coverage M1-M4, checks CCSS alignment, writes P2b pass record. Tools: ai.ask, ai.generate, tasks.find. Added to TopBar AGENTS array.
- [x] ✅ Release Gate Agent — 01KNT44QZCAS478T59ZCH4PVSB (private) · 5-domain release certification: Build Standards Compliance, Content Completeness, Player Clarity, QA Audit Status, Pass Record Completeness. Issues GREEN/AMBER/RED. Authority is final. Tools: ai.ask, ai.categorize, tasks.find. Added to TopBar AGENTS array.

# ⚡ Automations (10 total)

- [x] Brainstorm → Pipeline Review — 01KNMNC88WD2TCGE2S8E5F7AF7 (fixed: liquid expr bug + GO/NO-GO write-back)
- [x] GO Decision + Curriculum Slot Assignment — 01KNMND4MFXZQ73J0GFAMZX452
- [x] Misconception Architect — 01KNMPE00ZG4RQAW7V4J1MZ1GX (6-stage: library check → semantic routing → map gen → write pending → add to specs → notify orchestrator)
- [x] Pass Closure / Learning Capture — 01KNMPFZ021BFFKKN66GNKWD34 (classify → write Playtest Audit → branch GENERAL/LOCAL → orchestrator summary)
- [x] Echo Heist Question Audit Pipeline — 01KNMYV115D5QC7T5MG7A0J80T (6-stage QA: correctness, skill align, randomisation, hint quality, report, write to tracker)
- [x] GAP: No equivalent QA Pipeline for Bakery Rush or Fire Dispatch templates
- [x] ✅ Pipeline Stage Advancement — 01KNSQWQDBVEKXJC9HSY4C3JS9 · Trigger: @gcf05 (GO/NO-GO) changes on LnpYq2qGt5DrXpda · GO path: AI determines next stage, writes @gcf04, generates advancement summary · NO-GO path: reverts @gcf04 to stage-idea, writes archive note to @gcf07 · Lint warnings on trigger refs inside branch nodes are static-analysis only — runtime resolves correctly (same pattern as existing GO Decision flow).
- [x] ✅ Pass Execution — Stage Work Dispatch (P2A→Release) — 01KNT45P8NDC6AYZKGKCC961SQ · Trigger: @gcf04 (Pipeline Stage) changes on LnpYq2qGt5DrXpda · 5-branch dispatch: P2A→Game Design Critic brief, P2B→Content Expansion Agent, P3→Player Clarity Auditor + Math Question QA (parallel), P4→Game Build Standards Agent gate check, P5→Release Gate Agent + Pipeline Orchestrator summary. Each branch writes results back to @gcf07. Lint warnings on trigger refs are static-analysis only — same pattern as existing Stage Advancement flow.

# 🖥 App — Studio OS (4 views live)

- [x] Pipeline Board — live Taskade data, stage columns, GO/Delight badges, critique summary
- [x] Curriculum Map — grade-band slots, skill coverage, status badges, linked-game column
- [x] Prototype Specs — phase tracker, misconception risks, success criteria, dev status
- [x] Echo Heist view — live iframe + side panel. Audit score: 7/7. Cold-start: \~88–92%. ALL 11 patches applied + verified in previews/echo-heist/current.html (2026-04-08). All 6 anxiety points RESOLVED. #12 + #13 correctly skipped (roundTo already in place).
- [x] Agent Panel — slide-in drawer, agent switcher (Orchestrator / Critic / QA / Clarity / Brainstorm)
- [x] ✅ QA Hub tab — cross-game QADashboard.tsx now supports All Games | Echo Heist | Bakery Rush | Fire Dispatch switcher. Per-game panels: stats, heat map, template table, mission table, cross-cutting issues, fix priority queue. All Games view shows per-game summary cards + cross-game top-10 fix queue. TopBar label updated to 'QA Hub'.
- [x] ✅ Misconception Library browser — Tab 8 live. MisconceptionLibrary.tsx built: live API fetch from cyt3zvpjf32D1Ddt, grouped by game, filters (search/game/category/clear), detail side-panel, stats cards. Brainstorming Specialist confirmed public (publicAgentId: 01KNMNB4NR0Q22B6F219PV0Z24). Both GAPs closed.
- [x] ✅ DONE: Snack Line Shuffle P1 level set written to Prototype Specifications (9bfNR2acXuAHiWyC). 14 rounds: R0–R13. 7/14 M1 trap rounds (50%). Engineer Handoff Brief + Level Content Set + constraint audit all in project. SnackLineShuffle.tsx tab added to Studio OS app as 6th tab (View='shuffle'). Interactive: filter by block/trap, reveal totals toggle, adjacency glow preview, design notes per round.
- [x] ✅ Fire Dispatch P1 — Tab 7 in Studio OS. 12 rounds: intro(2)→multiply(4)→divide(4)→multi-step(2). Misconceptions: M1(repeated addition), M2(subtraction-division), M3(remainder blindness). Truck gauge stepper + dispatch button. Wrong hint on incorrect attempt, equation revealed only on correct dispatch. Level Browser with reveal-answer toggle, design notes, misconception key.
- [x] ✅ Puddle Patrol (GAP-1) — Tab 9 in Studio OS. 12 rounds R0–R11 across 4×4/5×5/6×6/8×8 grids. 5/12 M1 trap rounds. Interactive level browser: reveal-path stepper, arrow sequence display, misconception key, design notes panel (toggled), P1 spec sidebar. Wired into App.tsx (view='puddle') and TopBar.tsx as 'Puddle Patrol' tab with Navigation icon.
- [x] ✅ Trig Tower (GAP-4) — Tab 12 in Studio OS. TrigTower.tsx built: 12-round cannon siege game (srcDoc iframe), inline canvas with gravity physics, animated projectiles + explosion particles, 3 enemy castles with HP bars. Rounds cover D1(SOH-CAH-TOA, radians, unit circle) → D2(inverse trig, M1 trap) → D3(Law of Sines/Cosines, identities, graphing). Trig Tower Tutor agent (01KNT2RH182338E1EEG9755Q36, public) embedded as slide-in chat panel with local scaffold fallback. Reference Sheet sub-tab (8 cards + CCSS table + M1-M4 misconception register). Wired as view='trigtower', Crosshair icon, agent added to TopBar AGENTS array.
- [x] ✅ Signal Tower (GAP-3) — Tab 11 in Studio OS. 12 rounds R0–R11. R0–R7 slope-intercept (incl. fractional slope R5, negative b R6, double-negative R7). R8–R11 systems of equations. 3 M1 traps (R3,R4,R7). Interactive: coordinate grid SVG with click-to-place tower, y=mx+b equation input with live y computation, system strategy panel, step-by-step hint disclosure, misconception M1 callout boxes, answer reveal toggle, design notes panel, P1 spec sidebar (8 gates, 4 misconceptions). Wired as view='signal', Radio icon.
- [x] ✅ Ratio Run (GAP-2) — Tab 10 in Studio OS. 12 rounds R0–R11. 4/12 M1 traps, 2/12 tie zones (equivalence pairs), 6/12 cross-rep. Number-line rail (0→1) with animated card markers. Recipe card chips: fraction/decimal/ratio/percent/unit-rate/mixed rep types. Reveal-answer toggle with decimal breakdown table and rail visualization. Re-shuffle button. Observer notes panel. Wired as view='ratio', Ruler icon.
- [x] ✅ Trig Tower added to Game Concepts Pipeline (LnpYq2qGt5DrXpda) as Task 079132f6-412f-4b5f-bba1-472f6df2dd3b. Full intake fields: @gcf01 (core fantasy), @gcf02 (core action — 12-round siege, D1→D3), @gcf03 (CCSS HSF.TF.A-C + HSG.SRT.C-D), @gcf04=stage-idea, @gcf05=gono-pending, @gcf06=dg-pending, @gcf08 (closest: Echo Heist + DragonBox 12+), @gcf09 (8/10 depth), @gcf10 (natural ceiling). Brainstorm→Pipeline Review automation auto-triggered on task.added — Game Design Critic will run Stages 1-7 and write GO/NO-GO + Delight Gate + AI Critique back to fields. When GO is issued, Pipeline Stage Advancement flow advances to stage-spec, then stage-precheck, etc. When P2A+ stages fire, new Pass Execution automation dispatches appropriate agents. Studio OS now has 12 tabs + 12 agents total.
- [x] ✅ Bakery Rush (Tab 13) — BakeryRush.tsx created. 12 rounds K-2 addition. M1-M4. Boss R11. Play + Level Browser + MC Key tabs. Pipeline entry + gcf fields written. SLS QA audit linked to QA agent.

# 📋 Patch Docs + Protocol Docs (in app/docs/)

- [x] echo-heist-patch-2026-04-07.md — 11 fixes: T10 CRITICAL, T8, T3, T5, PC1-PC5
- [x] echo-heist-patch-2026-04-08.md — Terminal Intro overlay + hint cost units. Resolves 2 HIGH gaps. Score 1.5→3/7.
- [x] echo-heist-patch-2026-04-08b.md — Guards note + vault 15s flash. Resolves 2 MEDIUM gaps. Score 3→5/7. Cold-start \~72–78%.
- [x] echo-heist-patch-LOW.md (=-08c) APPLIED — 11 patches verified in current.html. Corruption in pasted diff fixed by engineer (doubled ')Heat)' and tripled 'scaffold' cleaned up). Patches 12+13 skipped: roundTo(Math.round(a/b)\*b,2) already correct in file.
- [x] snack-line-shuffle-p1-observer-protocol.md — Gate 7 rule comprehension script (Q1 ordering direction + Q2 M1 trap pair), CE rubric (Tier A/B/0 + SP-X shortcut flags), Gate 10 voluntary continuation script (15 s timer, 1 permitted prompt, G10-TIMEOUT-DOUBLE), session fail decision tree (5 checks: welfare, M1 block, rule not understood, CE-0 + wrong traps, slow-pace disengaged). 31 codes defined. Surfaced in Line Shuffle tab as 'Observer Protocol' sub-tab with interactive collapsible sections, coding tables, reveal-able internal notes, and interactive pre-session checklist.
- [x] snack-line-shuffle-gate6-teacher-review.md — Gate 6 teacher review packet. Jargon-free, <3 min read. Sections: What is this game (K-1, drag-place-serve, 5-8 min bursts) · What skill it builds (addition fluency ≤5) · Core Fantasy ('You are the lunch helper…') · 3 amber VO lines (exact wording) · Ordering-direction indicator description (corner icon, star on front kid, always visible) · 2 Yes/No sign-off questions with note field on NO · Signature block (Name, School, Date, Signature). Surfaced as 'Gate 6 · Teacher Review' sub-tab in Line Shuffle view with interactive YES/NO toggle, expandable NO-note textarea, visual signature field mock, and print button.

# 🔜 Next Steps (priority order)

1. ~~Echo Heist patches ✅ COMPLETE — 11/11 applied. Patches 12+13 skipped (already correct via roundTo in prior commit). Audit 7/7. Cold-start \~88–92%.~~
2. QA Dashboard view — add a 5th app tab surfacing the Audit Results project (T1-T12 health, D3 missions, cross-cutting /issues)

   Here’s a structured reverse‑brainstorming pass on that task.

   Task:

   “QA Dashboard view — add a 5th app tab surfacing the Audit Results project (T1–T12 health, D3 missions, cross‑cutting issues).”

   I’ll walk through:
   1. How to **make this QA Dashboard as bad / useless as possible**
   2. Cluster the “bad ideas” into failure modes
   3. Flip each cluster into **design constraints & solution ideas**

   You can skim bold headers + bullets.

   ## 1. How could we make this QA Dashboard terrible?

   **A. Make it impossible to understand at a glance**
   - Show the entire Audit Results project as one giant scroll of markdown with no structure.
   - Mix T1–T12, D3 missions, and cross‑cutting issues in chronological order only.
   - Use long narrative paragraphs instead of any tables or status icons.
   - Hide template IDs / mission codes inside text instead of columns.
   - Use ambiguous labels like “Item 1,” “Thing A,” instead of “T7 – Linear Equations (Grade 7).”
   - Use similar colors for everything (all gray text, no emphasis).
   - Don’t show any summary metrics—just raw entries.

   **B. Make it slow and painful to use**
   - Load the entire project (all historical audits) on every tab visit, no pagination.
   - Re‑query the agent / knowledge every time the user clicks anything.
   - Don’t cache or index by template/mission; always full‑text search.
   - Force the user to manually scroll to find T1–T12 and D3 sections.
   - Don’t provide search or filters at all.

   **C. Hide the relationships that matter**
   - Don’t group by game (Echo Heist, Bakery Rush, Fire Dispatch).
   - Don’t distinguish templates (T1–T12) from D3 missions or cross‑cutting issues.
   - Don’t show whether an audit note is still relevant or already patched.
   - Don’t connect an audit record to:
     - The template spec
     - The game prototype
     - The patch docs that addressed it
   - Don’t indicate severity (CRITICAL / HIGH / MED / LOW).

   **D. Ensure nobody trusts or acts on the data**
   - Let outdated audit notes live forever with no “superseded” marker.
   - Don’t show when an issue was patched or which patch doc addressed it.
   - Mix internal notes, off‑hand comments, and final decisions without labels.
   - Use inconsistent terminology (e.g., “Randomization bug,” “RNG issue,” “variation problem”) so patterns are invisible.
   - Show conflicting statuses (e.g., “Resolved” and “Open” for the same template) with no explanation.

   **E. Make it disconnected from the rest of Studio OS**
   - Don’t link dashboard items back to:
     - Prototype Specs project
     - Misconception Library
     - Patch docs
     - QA pipeline automations
   - Don’t let the user jump from a dashboard row to the underlying Taskade node.
   - Don’t surface which agents use this data (Math Question QA, Player Clarity Auditor, etc.).
   - Use a different naming scheme than the rest of the system (e.g., call T1 “Template Alpha”).

   **F. Overwhelm with noise, not signal**
   - Show every tiny nitpick at the same visual weight as CRITICAL bugs.
   - Show multiple duplicate records for the same issue with no deduplication.
   - Show internal implementation details (e.g., full agent logs) instead of concise outcomes.
   - Don’t aggregate cross‑cutting issues; show each mention separately.
   - Don’t highlight “actionable next steps”; just list problems.

   **G. Make the UI awkward and hostile**
   - Put the QA Dashboard tab in a non‑obvious place or behind multiple clicks.
   - Use a cramped layout: tiny fonts, no whitespace, no grid.
   - Make filters hidden in an obscure dropdown with vague labels.
   - Don’t remember user filters or view preferences.
   - Don’t adapt columns to screen size; force horizontal scrolling.

   **H. Ignore future maintenance and growth**
   - Hard‑code Echo Heist terminology so Bakery Rush / Fire Dispatch don’t fit.
   - Assume only T1–T12 and D3 exist; no way to add new template families.
   - Store visualization logic inside ad‑hoc markdown instead of a consistent schema.
   - Don’t record any “version” or “superseded by” fields, so old audits can’t be retired.
   - Don’t support any date scoping (e.g., last 30 days vs all time).

   ## 2. Cluster the “bad ideas” into failure modes

   From the above, we get these key anti‑patterns:
   1. **Unstructured raw dump** of Audit Results
   2. **No prioritization or health signal** (everything looks the same)
   3. **No linkage** to games/templates/patches/agents
   4. **Stale or contradictory data** with no versioning
   5. **Terrible UX** (slow, cluttered, unsearchable)
   6. **Not future‑proof** (Echo‑Heist‑only, brittle taxonomy)

   Now flip each into design goals.

   ## 3. Flip to solution ideas & design constraints

   **3.1 From “unstructured raw dump” → structured, layered views**

   **Bad pattern:** One giant scroll of markdown.

   **Design constraints:**
   - Dashboard must present **three core slices**:
     1. **Template Health (T1–T12)**
     2. **Mission Health (D3 missions, e.g., M21–M30)**
     3. **Cross‑cutting issues** across the game(s)
   - Each slice should have:
     - A **summary tile / panel** (overview)
     - A **table view** with sortable columns
     - A **detail drawer** for a selected item

   **Concrete ideas:**
   - **Top row: health cards**
     - “T1–T12 Overview”:
       - e.g., 12 templates • 2 CRITICAL • 3 HIGH • 7 OK
     - “D3 Missions Overview”:
       - 10 missions • 0 CRITICAL • 1 HIGH • 9 OK
     - “Cross‑cutting Issues”:
       - 4 active patterns • 1 global randomization issue • 2 hint clarity • 1 skill alignment
   - **Main grid with clear columns:**
     - For templates: \[Game] \[Template ID] \[Skill] \[Grade band] \[Latest audit date] \[Worst open severity] \[Status badge] \[#Issues]
     - For missions: \[Game] \[Mission ID] \[Mission type] \[Latest audit date] \[Status] \[Linked templates]
   - **Detail drawer** (right side) for a row:
     - Show last few audit entries for that template/mission.
     - Show “Current status,” “Open issues,” “Resolved by patch X,” links.

   **3.2 From “no prioritization” → explicit severity & health**

   **Bad pattern:** All items look equally important.

   **Design constraints:**
   - Always show:
     - **Severity** (CRITICAL / HIGH / MED / LOW)
     - **Current health state** (e.g., “BLOCKED,” “Needs Attention,” “OK”)
   - Order default views by **severity then recency**.

   **Concrete ideas:**
   - **Color & icon language:**
     - CRITICAL → red badge “BLOCKING”
     - HIGH → orange badge “HIGH RISK”
     - MED → amber “REVIEW”
     - LOW → gray “NICE TO FIX”
     - OK → green “CLEAN”
   - **Template health score** (optional):
     - Simple 0–3 or 0–5 scale from audits, e.g., 3/3 = no open issues • 2/3 = only LOW/MED • 1/3 = HIGH open • 0/3 = CRITICAL open
   - **Quick filters:**
     - “Show only CRITICAL/HIGH”
     - “Show templates with open cross‑cutting issues”
     - “Show only games: Echo Heist / Bakery Rush / Fire Dispatch”

   **3.3 From “no linkage” → stitched into Studio OS graph**

   **Bad pattern:** Dashboard is a silo.

   **Design constraints:**
   - Every row in the dashboard should act as a **hub** linking to:
     - The **Audit Results node** (raw QA log)
     - The **Prototype Specification** (from Prototype Specs project)
     - Any **patch docs** that reference that template/mission
     - Relevant **Misconception Library** entries
     - Optionally: a “View in App” link to the live game context

   **Concrete ideas:**
   - Column or icons for:
     - 🔗 “Spec” → opens spec doc (e.g., Bakery Rush T4 specification)
     - 🩹 “Patches” → links to docs like echo-heist-patch-2026-04-08b.md
     - 🧠 “Misconceptions” → shows count + tooltip of key misconception tags
     - 🤖 “Agents” → shows which agents use this audit data (QA, Clarity, Critic)
   - **Side panel integrated with Agent Panel:**
     - From a template row, click “Ask Math Question QA about this template” and open the agent drawer pre‑contextualized with that template’s QA history.

   **3.4 From “stale / contradictory” → versioned, trustworthy QA**

   **Bad pattern:** Old, superseded notes mixed with current ones.

   **Design constraints:**
   - Audit entries need at least:
     - status: OPEN / RESOLVED / SUPERSEDED
     - resolvedByPatchDoc: \[optional link]
     - supersededByAuditId: \[optional]
     - lastReviewedAt + lastReviewedBy (agent/human)
   - Dashboard must **visually separate**:
     - Current open issues
     - Historical / resolved context

   **Concrete ideas:**
   - **Timeline view per template/mission:**
     - A vertical list: Audit 2026-04-07 (CRITICAL, RESOLVED), Audit 2026-04-08b (MED, OPEN), etc.
     - Older superseded entries appear collapsed under “History.”
   - **Status chips in main table:**
     - “Open issues (2)” vs “All issues resolved”
     - Hover to see which patch doc resolved them.
   - **“Last sanity check”** badge:
     - E.g., “QA pipeline last run: 2026-04-08” If > N days old, show a subtle “stale” warning.

   **3.5 From “terrible UX” → fast, queryable, and focused**

   **Bad pattern:** Everything loads slowly and requires manual scrolling.

   **Design constraints:**
   - Dashboard must:
     - Load with a **bounded, high‑value subset** (e.g., only items with open HIGH/CRITICAL).
     - Support **filters and search** without full reload of everything.
     - Remember filters per session.

   **Concrete ideas:**
   - **Default view: “What’s broken now?”**
     - Only show templates/missions with open issues.
     - Toggle to “All items” or “Clean items.”
   - **Smart filters:**
     - By game: Echo Heist / Bakery Rush / Fire Dispatch / All
     - By artifact type: Template / Mission / Cross‑cutting
     - By severity: CRITICAL / HIGH / MED / LOW
     - By status: Open / Resolved / Stale
   - **Search bar**:
     - Supports:
       - Template ID (e.g., “T8”)
       - Mission ID (e.g., “M23”)
       - Skill name (“percents,” “linear equations”)
       - Game name

   **3.6 From “not future‑proof” → cross‑game, extensible QA backbone**

   **Bad pattern:** Echo‑Heist‑specific, can’t scale to Bakery Rush / Fire Dispatch.

   **Design constraints:**
   - QA Dashboard must treat “game” as a **first‑class dimension**.
   - Template / mission taxonomy must be **generic**:
     - gameId
     - artifactType (template, mission, cross-cutting)
     - artifactId (e.g., T1, BR‑T1, FD‑M3)
   - Support multiple **families** or “tracks” of templates.

   **Concrete ideas:**
   - **Game switcher** at top:
     - Tabs or dropdown: All Games | Echo Heist | Bakery Rush | Fire Dispatch
     - Each view uses same schema, just filtered.
   - **Naming convention surfaced in UI:**
     - Echo Heist: EH-T1, EH-M21
     - Bakery Rush: BR-T1, BR-M4
     - Fire Dispatch: FD-T3, FD-M7
     - The dashboard enforces/reflects this scheme so audits across games align.
   - **Cross‑game patterns panel:**
     - List issues like:
       - “Randomization too narrow → EH-T8, BR-T3, FD-T2”
       - “Hint clarity vague → EH-T10, FD-M5”

   ## 4. Minimal “definition of done” for this QA Dashboard tab

   Using the reverse‑brainstorm insights, a concise DoD for the 5th tab:
   1. **Information architecture**
      - At least 3 sections/slices:
        - Template Health (T1–T12, across games)
        - D3 Mission Health
        - Cross‑cutting issues
      - Each with: summary stats + table + detail drawer.
   2. **Core fields & signals**
      - For each template/mission:
        - Game
        - Artifact type (Template / Mission / Cross‑cutting)
        - ID (e.g., EH‑T8, BR‑T2)
        - Skill + grade band
        - Latest audit date
        - Worst open severity
        - Current status (“Open issues,” “Clean,” “Stale”)
   3. **Linkage**
      - From each row: links to
        - Audit Results entry
        - Prototype spec
        - Patch doc(s)
        - Misconception Library entries (if any)
      - Optional: button to open relevant agent in the Agent Panel.
   4. **Interaction**
      - Filters by game, severity, status, type.
      - Search by ID / skill / game.
      - Default view = open HIGH/CRITICAL issues across all games.
   5. **Trust & freshness**
      - Visual distinction between open vs resolved vs superseded issues.
      - “Last QA run” / “Last reviewed” indicators.
      - Simple versioning or “superseded by” labeling in details.

   If you’d like, next step I can:
   - Draft the **exact table schemas** for the dashboard (columns, field names, example rows), or
   - Propose **wireframe layouts** for the 5th tab that a dev/designer can implement directly.

   Here’s a structured way to think about this new 5th tab for the QA Dashboard and how the ideas cluster together.

   ## 1. High-level Concept

   **New 5th App Tab: “Audit Results”**

   Purpose:

   A dedicated, interactive “Audit Results” tab that consolidates:
   - T1–T12 health (per template / test type / track)
   - D3 missions (per auditor / mission / time window)
   - Cross-cutting issues (patterns and systemic problems across T1–T12 & D3)

   This becomes the **“QA Intelligence”** space: not just results, but insights and action triggers.

   ## 2. Core Clusters / Sections Inside the Tab

   **Cluster A – T1–T12 Health Overview**

   **Theme:** Operational health of the full template/test portfolio.

   **Key ideas:**
   - **Global Health Heatmap**
     - Grid: rows = T1–T12, columns = key health metrics (accuracy, coverage, severity rate, SLA adherence, sample size).
     - Color-coded status (green/yellow/red).
     - Hover for mini-trends: last 7/30 days sparkline.
   - **Template Drill-Down Cards**
     - Click T1–T12 to open a side panel:
       - Score over time (trendline).
       - Top 3 recurring issues for that template.
       - Volume of audits vs. targets.
       - Distribution of severities (critical/major/minor).
   - **Comparative View**
     - Multi-select T’s (e.g., T3, T7, T9) and compare:
       - Side-by-side metrics.
       - Normalized scores (z-score or percentile vs. median template).
       - “Outlier” flag if one T is significantly worse.

   **Synergy:**

   This cluster feeds data into the cross-cutting issues engine (Cluster C) and gives context for D3 mission outcomes (Cluster B).

   **Cluster B – D3 Missions Performance**

   **Theme:** Audit execution and mission-level performance.

   **Key ideas:**
   - **Missions Timeline**
     - Horizontal timeline with D3 missions as nodes.
     - Color/size based on mission outcome (e.g., % issues found, criticals found, completion rate).
     - Filter by:
       - Auditor
       - Region / product / squad
       - Date range
       - Mission type
   - **Mission Detail View**
     - Per-mission dashboard:
       - Scope: which T’s were covered.
       - Findings summary: counts & severity by T.
       - Time spent vs. planned.
       - “Impact” score (e.g., weighted by severity & volume).
   - **Auditor Performance Lens**
     - Aggregated stats per auditor:
       - Missions done
       - Coverage breadth (how many different T’s)
       - Finding density (issues per item audited)
       - Agreement rate with peer/lead reviews.

   **Synergy:**

   D3 missions link back to T1–T12 (what was audited) and to cross-cutting issues (what patterns emerged across missions).

   **Cluster C – Cross-Cutting Issues Hub**

   **Theme:** Pattern detection across templates, missions, teams, and time.

   **Key ideas:**
   - **Issue Taxonomy Map**
     - Visual map grouping issues by category:
       - Process
       - Data quality
       - Tooling
       - Policy / compliance
       - Training / knowledge gaps
     - Each node shows:
       - of occurrences
       - of impacted T’s
       - of missions where it appeared.
   - **Systemic Issue Radar**
     - Radar chart showing “risk intensity” by dimension:
       - Impact breadth (how many T’s)
       - Impact depth (severity)
       - Recency (how recently and frequently)
       - Org spread (how many teams/regions).
     - Highlight “Top 5 systemic issues this period”.
   - **Root Cause & Action Linking**
     - For each cross-cutting issue:
       - Linked T’s (T1, T4, T9, etc.).
       - Linked D3 missions where it surfaced.
       - Linked corrective actions / owners / deadlines.

   **Synergy:**

   This is where all data converges: T1–T12 metrics and D3 mission findings are re-aggregated into “problems worth solving.”

   **Cluster D – Insights, Alerts, and Narrative**

   **Theme:** Turning raw audit data into something a PM / lead can digest in 5 minutes.

   **Key ideas:**
   - **Weekly / Monthly “Audit Story”**
     - Auto-generated summary block:
       - “This period, T7 and T10 regressed significantly in accuracy (–8%, –5%).”
       - “A recurring cross-cutting issue: inconsistent labeling guidelines, seen in 4 missions and 3 templates.”
       - “D3 mission M-245 had the highest impact, surfacing 3 critical issues.”
   - **Smart Alerts**
     - Rules-based triggers:
       - “Alert when any T’s accuracy < 90% for 7 consecutive days.”
       - “Alert when a new cross-cutting issue appears in ≥ 3 missions within 2 weeks.”
       - “Alert when D3 coverage of a T falls below target.”
     - Visible as a notification center within the tab; optionally pushed to email/Slack.
   - **Impact & ROI Lens (optional advanced)**
     - Tie issues to impact estimates (if you have that data):
       - Estimated user impact / revenue risk score linked to each systemic issue.
       - Prioritized queue: “Top 10 issues by potential impact.”

   **Synergy:**

   This cluster “interprets” Clusters A–C, making the tab not just a data graveyard but a decision surface.

   **Cluster E – Filters, Navigation & UX Shell**

   **Theme:** Making the 5th tab usable and fast.

   **Key ideas:**
   - **Global Filters Bar**
     - Date range
     - Product / vertical / region
     - Team / squad
     - Environment (prod / staging)
     - Severity level filter
   - **Switchable Layout Modes**
     - “Executive View”: concise KPIs, trendlines, top issues.
     - “Analyst View”: deeper tables, filters, export options.
     - “Ops View”: mission-focused, showing workload, coverage, and open actions.
   - **Contextual Linking**
     - Clicking a T in the health grid:
       - Jumps to a pre-filtered view of related D3 missions and cross-cutting issues.
     - Clicking a cross-cutting issue:
       - Opens all impacted T’s and missions, plus actions.

   ## 3. Potential Connections & Synergies Between Clusters

   - **From T1–T12 Health to D3 Missions**
     - If T7 health drops:
       - The system suggests: “Consider scheduling a focused D3 mission on T7 in region X.”
   - **From D3 Missions to Cross-Cutting Issues**
     - As multiple missions log similar issues:
       - The issue is auto-promoted to a cross-cutting “candidate” and, once threshold met, to a systemic issue.
   - **From Cross-Cutting Issues to Actions & Ownership**
     - Each systemic issue:
       - Gets a clear owner (team/individual), due date, and target metric improvement in the T1–T12 health grid.
   - **Feedback Loop**
     - Once actions are implemented:
       - Watch T1–T12 health trends: did T7 accuracy recover?
       - If yes, link that improvement to the resolved systemic issue, closing the loop.

   ## 4. Simple Information Architecture of the 5th Tab

   Top-level layout inside the “Audit Results” tab:
   1. **Header KPIs Row**
      - Overall audit coverage
      - Avg T health score
      - of active systemic issues
      - of D3 missions in selected period
   2. **Three Main Panels (switchable or stacked):**
      - Left: **T1–T12 Health**
      - Middle: **D3 Missions**
      - Right: **Cross-Cutting Issues**
   3. **Bottom / Side:**
      - **Insights & Alerts** panel (Cluster D).

   If you’d like, I can next:
   - Propose specific metric formulas for T1–T12 health and D3 mission scores, or
   - Sketch user stories (e.g., “As a QA Lead, I want to…”), or
   - Prioritize which sub-features to ship in v1 vs. later iterations.
3. ~~✅ Brainstorming Specialist public — confirmed. publicAgentId: 01KNMNB4NR0Q22B6F219PV0Z24. AgentPanel already had it wired in AGENTS array.~~
4. ~~✅ Misconception Library browser — Tab 8 in Studio OS. 7 games, 28+ entries, filters by game + category + search, detail side-panel with failure signal + design response sections.~~
5. Clarity audit Bakery Rush / Fire Dispatch — run Player Clarity Auditor on other live games; generate audit panels for them
6. ~~✅ 3 GAP family plans written to Game Concepts Pipeline (LnpYq2qGt5DrXpda):~~
   - ~~GAP-1: Puddle Patrol — K-2, Routing/Pathfinding. Drag arrows on 4×4–8×8 grid, frog follows path to flower, avoids puddles. CCSS K.G.A.1. GO/Delight PASS. 4 misconceptions registered. 8-gate P1 DoD.~~
   - ~~GAP-2: Ratio Run — Gr 3-5, Sequence/Ordering (Ratio Edition). Drag recipe cards on number-line rail; mixed representations (fractions/decimals/ratios/unit rates). CCSS 6.RP.A. GO/Delight PASS. Equivalence tie mechanic. 4 misconceptions. 8-gate P1 DoD.~~
   - ~~GAP-3: Signal Tower — Gr 6-8, Build/Craft. Calculate tower coordinates by solving y=mx+b (then systems) and place on grid to bridge cities. CCSS 6.EE/8.EE. GO/Delight PASS. First game targeting 8.EE.C.8. 4 misconceptions. 8-gate P1 DoD. Depth 9/10.~~
7. NEXT: Confirm Echo Heist has a public shareable URL — verify previews/echo-heist/current.html is accessible without login before counting it as launched.
8. ~~✅ ALL 3 GAP P1 SPECS WRITTEN to Prototype Specifications (9bfNR2acXuAHiWyC):~~
   - ~~GAP-1 Puddle Patrol (K–2, K.G.A.1, Routing): 7 sections A–G, 8 locks, 7 CC, 8 gates, 12 rounds R0–R11 across 4×4/5×5/6×6/8×8 grids with step limits. 7/12 M1 trap rounds. Constraint audit ✓.~~
   - ~~GAP-2 Ratio Run (Gr 3–6, 6.RP.A, Sequence): 7 sections A–G, 8 locks, 7 CC, 8 gates, 12 rounds R0–R11 across 3/4/5 cards with tie-zone mechanic. 4/12 M1 traps, 2/12 tie zones, 6/12 cross-rep. Constraint audit ✓.~~
   - ~~GAP-3 Signal Tower (Gr 6–8, 8.EE.C.8, Build): 7 sections A–G, 8 locks, 7 CC, 8 gates, 12 rounds R0–R11 escalating from y=mx+b substitution → systems elimination. 5/12 negative slope, 6/12 systems, 3/12 M1 traps. Constraint audit ✓.~~
   - NEXT OPTIONS: (a) Build GAP-1 Puddle Patrol as an interactive preview tab in Studio OS app, (b) Write any of these specs into Game Concepts Pipeline as a proper row entry with all custom fields, (c) Begin P1 HTML prototype for one of the three games
9. ~~✅ All 3 GAP preview tabs live: Puddle Patrol (Tab 9), Ratio Run (Tab 10), Signal Tower (Tab 11). Studio OS now has 11 tabs total.~~
10. ~~✅ Trig Tower P1 preview tab LIVE — Tab 12. 12 rounds R0–R11 escalating D1→D2→D3. SOH-CAH-TOA (R0–R2) → Radians (R3) → Unit Circle (R4–R5) → M1 trap (R6) → Inverse trig (R7) → Law of Sines (R8) → Law of Cosines (R9) → Pythagorean identity (R10) → Graphing amplitude/period (R11). Physics: gravity projectiles, trail rendering, particle explosions, 3 castle HP bars. Tutor agent wired. Studio OS now has 12 tabs total.~~

# 🧠 OS Lessons — Fire Dispatch Audit 2026-04-09

- **LESSON 1 — Remainder trap requires non-divisible numbers.** M3 (remainder blindness) is only testable when dividend ÷ divisor has a non-zero remainder. Old R8 was 20÷4=5 (exact) — trap was impossible. Always verify: answer = floor(totalPool / trucksPerUnit), and totalPool mod trucksPerUnit > 0. Apply to every future game using remainder mechanics.
- **LESSON 2 — Equation reveal must match the operation used.** A divide round showing 'trucksPerUnit × units = answer' is wrong — the student used division. Always branch reveal on round.block: divide rounds show 'totalPool ÷ trucksPerUnit = answer \[r remainder]'; multiply rounds show 'trucksPerUnit × units = answer'. Apply globally.
- **LESSON 3 — Progressive hints are better than flat hints.** wrongHint (shown after attempt 1) should direct thinking without revealing the operation. wrongHint2 (shown after attempt 2+) can name the error pattern explicitly (e.g., '9+5 is only 14. Each gate needs 9 trucks independently: 9 × 5'). Never reveal the numeric answer in either hint. Pattern: Attempt 1 = strategy prompt. Attempt 2 = name the misconception. Apply to Echo Heist and all future games.
- **LESSON 4 — Boss rounds need hint suppression.** Final/boss rounds should mark isBossRound=true and suppress all hints. The UI should label it 'Boss round · no hints' so students understand the change in rules. Apply to any game with a final challenge round.
- **LESSON 5 — Multi-step rounds need a visible step indicator.** When a round requires two cognitive steps (e.g., multiply then verify against fleet), show a stepLabel in the HUD (e.g., 'Step 1: multiply · Step 2: verify fleet'). This does NOT replace a locked two-step UI (P2 item) but meaningfully scaffolds without giving the answer.
- **LESSON 6 — Audit cross-cutting text strings separately.** Cross-cutting subtraction-language audit must grep ALL strings: prompts, wrongHints, wrongHint2, designNotes, UI labels. Tracker row for 'subtraction-division confusion' passed because all strings were clean — but this was only discoverable by reading every string. Build a string-search step into future audits.
- **LESSON 7 — Time pressure is architectural, not cosmetic.** The FD tracker spec called for ≤4s response windows for hard facts. This cannot be bolted onto a static input — it requires a countdown timer component with grace periods. Tag time-pressure gaps as 'P2 architectural' not 'FAIL' in P1 audits. Document in tracker as WARN with a specific P2 implementation note.
- **AUDIT RESULTS SUMMARY — Fire Dispatch P1 (2026-04-09):** FD-T2 PASS · FD-M4 PASS · FD-M5 PASS · Cross-cutting subtraction PASS. FD-T1 WARN (no time pressure) · FD-T3 WARN (no step UI) · FD-T4 WARN (animation deferred) · FD-M1 WARN (tooltip copy) · FD-M2 WARN (no randomizer) · FD-M3 WARN (no ×8, no randomizer) · FD-M6 WARN (no step UI) · FD-M7 WARN (step UI) · FD-M8 WARN (boss gate structural only) · Cross-cutting time WARN. CRITICAL DATA BUG FIXED: R8/R9 wrong answers corrected (M3 trap now valid).

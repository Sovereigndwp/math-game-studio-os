# Playable Prototype Checkpoints

Files in this folder are **playable prototype snapshots** — not final product files, not throwaway junk.

Open any `.html` file directly in a browser. No server required.

---

## What these files are

Each file is a frozen, self-contained checkpoint of a game prototype at a specific design stage.

They are:
- **Temporary** in the sense of not final product
- **Permanent** in the sense of useful design history

Their value is as:
- Testable states
- Audit trail
- Comparison points between passes
- Handoff artifacts
- Proof that a concept improved from one pass to the next

---

## Pass convention

Every game follows the same three-pass structure. A new pass file is created only when it marks a **meaningful design shift** — not for every small change.

| Pass | Purpose | Keep if it proves |
|------|---------|-------------------|
| **Pass 1** | Core loop proof | The basic loop works · the math is inside the action · the concept works at all |
| **Pass 2** | Pressure and progression proof | The loop survives pressure · progression helps · the game starts to feel alive |
| **Pass 3** | UI, feedback, and feel proof | Emotional presence · feedback quality · reward rhythm · the game starts to feel real |

**Good reasons to create a new pass file:**
- New mechanic
- New pacing model
- New difficulty structure
- New UI behavior
- Major feedback upgrade

**Do not keep every small change.** `pass-2-ui-v2.html` only exists if it changes feel meaningfully.

---

## Folder structure

```
previews/
  [game-name]/
    pass-1.html     ← core loop proof
    pass-2.html     ← pressure and progression proof
    pass-3.html     ← UI, feedback, and feel proof
```

---

## Games

### bakery/

| File | Pass | What it proves |
|------|------|----------------|
| `pass-1.html` | Core loop | Count-matching loop · customer character · flying pastry arc · full-screen feedback overlay |
| `pass-2.html` | Pressure + progression | Moving conveyor belt · 5 unlockable shifts · lives · patience timer · streak bonuses · score thresholds |
| `pass-3.html` | Feel + UI layer | Customer character reaction on success · scale-in full-screen overlay · arc animation from belt to box · stronger reward rhythm |

---

## Connection to the OS pipeline

These files are the output of **Phase D: Playable Pass Generation** in the pipeline:

```
Phase A  →  Idea intake          (Stages 0–5)
Phase B  →  Prototype shaping    (Stages 6–8)
Phase C  →  Implementation       (Stages 9–10)
Phase D  →  Playable passes      previews/[game]/pass-N.html
Phase E  →  Improvement loop     playtest_diagnostic → revision_brief → next patch
```

Each pass file corresponds to one completed `implementation_patch_plan` artifact from Stage 10.

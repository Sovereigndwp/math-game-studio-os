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
    current.html    ← live playable version (always the latest)
    pass-3.html     ← frozen P3 snapshot (historical checkpoint)
```

### Naming rule

- `current.html` is the **source of truth** — all new fixes and passes go here
- `pass-N.html` files are **frozen snapshots** created only when you need a historical checkpoint
- History lives in pass records, scorecards, and git — not in filename proliferation

---

## Games

### bakery/

| File | Role |
|------|------|
| `current.html` | Live playable version (P3: chef character, status strip, tiered celebration) |
| `pass-3.html` | Frozen P3 checkpoint |

### fire/

| File | Role |
|------|------|
| `current.html` | Live playable version (P3: incident personality, dispatch status strip, L5 victory) |
| `pass-3.html` | Frozen P3 checkpoint |

### unitcircle/

| File | Role |
|------|------|
| `current.html` | Live playable version (P3: Chef Cosina, lab status strip, tiered celebration) |
| `pass-3.html` | Frozen P3 checkpoint |

---

## Connection to the OS pipeline

These files are the output of **Phase D: Playable Pass Generation** in the pipeline:

```
Phase A  →  Idea intake          (Stages 0–5)
Phase B  →  Prototype shaping    (Stages 6–8)
Phase C  →  Implementation       (Stages 9–10)
Phase D  →  Playable passes      previews/[game]/current.html
Phase E  →  Improvement loop     playtest_diagnostic → revision_brief → next patch
```

Each game's `current.html` reflects the latest completed pass.

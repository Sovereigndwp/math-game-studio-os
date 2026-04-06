# Playtest Evidence

Field notes from real play sessions. This is the third layer of the pass system:

1. **Scorecard** (`docs/pass_fail_scorecard.md`) — did the pass work? Pass/fail/hold/split.
2. **Pass records** (`artifacts/pass_records/`) — what changed, what was proved, what's next.
3. **Playtest evidence** (this folder) — what happened in real testing.

## Structure

```
artifacts/playtests/
  bakery-rush/
  fire-dispatch/
  unit-circle/
```

## File naming

`YYYY-MM-DD-<description>.md`

Examples:
- `2026-04-05-p3-verification.md`
- `2026-04-06-live-playtest.md`
- `2026-04-07-l5-endpoint-test.md`

## Template

```markdown
# Playtest: [Game] — [Description]

| Field | Value |
|---|---|
| **Date** | |
| **Game** | |
| **Build** | current.html as of [commit] |
| **Tester** | Claude / human / both |
| **Session type** | verification / exploratory / regression |

## What was tested
[1-2 sentences]

## Strongest positives
- ...

## Strongest negatives
- ...

## Where they stopped
[Level reached, lives left, score, stars if applicable]

## One sentence verdict
[Did the pass land?]

## Recommended next
[What should happen next based on this evidence]
```

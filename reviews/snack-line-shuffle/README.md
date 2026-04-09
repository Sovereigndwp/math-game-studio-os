# reviews/snack-line-shuffle/

## Status: placeholder — review build deferred

This folder exists as a placeholder for the Snack Line Shuffle P1 review
build. **No prototype has been implemented yet.** There is no `current/`
subdirectory, no `index.html`, and no pass-record files.

Creating a stub build file here would violate the concept's "do not fake
the build" rule. Do not add `current/index.html` until P1 implementation
has been explicitly approved and begins.

## Why the folder exists now

Having the folder in git reserves the path so that:

- tooling and scripts that scan `reviews/*` recognize the concept slot
- the intended review path documented in the lane entry, status file,
  and family registry resolves to a real directory
- when P1 implementation is approved, `current/` and its files can be
  added here without a separate "create folder" commit cluttering the
  history

## Concept source of truth

See [`concepts/snack-line-shuffle/`](../../concepts/snack-line-shuffle/)
for the approved concept packet, P1 Definition of Done, locked approvals,
and misconception notes.

## Lane entry

See [`docs/concept_lanes.md`](../../docs/concept_lanes.md) for the
current pipeline lane entry. The lane entry prominently documents that
this is an approved concept only — not yet prototyped, not yet playtested.

## What will eventually live here

Once P1 implementation is approved, this folder will grow to match the
pattern used by the other games:

```
reviews/snack-line-shuffle/
  current/
    index.html
    pass-1.html
    pass-1-record.md
    (later: pass-2a.html, pass-2b.html, pass-3.html, etc.)
```

Until then: nothing but this README.

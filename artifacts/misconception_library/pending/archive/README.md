# pending/archive/

Pending misconception write-back files that were **archived rather than applied**.

Files are moved here (not deleted) when any of the following is true:

- The pending write-back has become stale enough that manual review is no longer worthwhile.
- The pending write-back was superseded by later library work.
- The pending write-back's originating playtest or pass context is no longer current.
- A policy decision was made to not apply the revision.

**Archiving does NOT apply the write-back.** The live misconception library at
`artifacts/misconception_library/<game>-misconceptions.json` is never touched
when a file is archived here. If you want to inspect an archived file's
proposed diff, read its `entries_to_update` field directly or consult git
history via `git log --follow pending/archive/<filename>`.

**Do not run `scripts/apply_library_writeback.py` against any file in this
directory.** Archived files are not eligible to be applied. If you believe an
archived file should actually be applied, first move it back to the parent
`pending/` directory via a separate commit with a clear rationale, then run
the write-back CLI from there.

See [`docs/pipeline_policy.md`](../../../../docs/pipeline_policy.md) for the
full policy context.

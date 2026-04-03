# Math Game Studio OS — Runbook

## Environment Setup

**Requirements:** The repo ships with a `.venv` provisioned for Python 3.14.3.
You do not need to install Python 3.14 system-wide — only the venv matters at runtime.

If the venv is missing or broken, recreate it:

```bash
python3.14 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Activate the Virtual Environment

```bash
# From repo root:
source .venv/bin/activate

# Verify:
which python        # should resolve to .../Master-Gaming-App-and-OS/.venv/bin/python
python --version    # should show Python 3.14.x
```

Alternatively, prefix every command with `.venv/bin/python` to skip activation.

## Run Stub Benchmarks

Stub mode is deterministic and requires no API key. Use it as the default regression check.

```bash
# From repo root:
.venv/bin/python scripts/run_benchmarks.py

# With a saved markdown report:
.venv/bin/python scripts/run_benchmarks.py --report
```

Reports are written to `reports/benchmark_regression_stub_<timestamp>.md`.

**Expected result:** `5/5 passed` with no `[FAIL]` lines.
**Expected runtime:** ~5–10 seconds (all five cases run deterministic stubs, no API calls).

## Run LLM Benchmarks

LLM mode drives all six pipeline agents through Claude. It requires `ANTHROPIC_API_KEY`
to be set.

```bash
# Ensure the key is exported in your shell session:
export ANTHROPIC_API_KEY=sk-ant-...

# Run LLM benchmarks (defaults to claude-sonnet-4-6):
.venv/bin/python scripts/run_benchmarks.py --llm --report

# Override the model:
.venv/bin/python scripts/run_benchmarks.py --llm --model claude-sonnet-4-6 --report
```

Reports are written to `reports/benchmark_regression_llm_<timestamp>.md`.

**Expected result:** `5/5 passed`. Any `[FAIL]` line is a regression.
**Expected runtime:** ~3–5 minutes for five cases (each runs six Claude API calls in sequence).

Interaction warnings (`! Interaction differs: ...`) are acceptable — the LLM may select a
valid but different primary interaction type. Investigate before treating a warned run as
a fully clean pass. Outcome and stop-stage mismatches are always failures.

## Troubleshooting

**`TypeError: Could not resolve authentication method`**
The `ANTHROPIC_API_KEY` environment variable is not set in the current shell session.
Run `export ANTHROPIC_API_KEY=sk-ant-...` and retry. Do not hard-code the key in any file.

**`ModuleNotFoundError: No module named 'anthropic'`**
The venv is not activated or the wrong Python is being used. Prefix the command with
`.venv/bin/python` explicitly.

**`[FAIL] bench_XX — Stop-stage mismatch: expected '...', got 'unknown'`**
This indicates a field name mismatch between the benchmark runner and PipelineResult.
The correct field is `final_artifact_name`. Check `scripts/run_benchmarks.py` line ~130.

**`ValidationError` or `AgentRunnerError` during a benchmark run**
An agent produced an artifact that failed JSON schema validation. The invalid payload is
saved to `memory/job_workspaces/<job_id>/<artifact>.INVALID_DEBUG.<timestamp>.json`.
Inspect that file to see what the agent returned and which schema fields failed.

**Stub benchmarks pass but LLM benchmarks fail on interaction type**
The LLM selected a valid but different interaction type than the benchmark expectation.
This is logged as a warning (`!`), not a failure, unless the outcome or stop stage also
differs. Review the `interaction_decision_memo` artifact in the job workspace.

## Rotate the Anthropic API Key Safely

1. **Generate a new key** in the Anthropic console before revoking the old one.
2. **Test the new key** locally before committing to rotation:
   ```bash
   ANTHROPIC_API_KEY=<new-key> .venv/bin/python scripts/run_benchmarks.py --llm
   ```
3. **Update your shell profile** (e.g., `~/.zshrc`):
   ```bash
   export ANTHROPIC_API_KEY=<new-key>
   ```
   Then reload: `source ~/.zshrc`
4. **Revoke the old key** in the Anthropic console only after confirming the new key
   passes benchmarks.
5. **Never commit a key to git.** The key lives only in your shell profile or a secrets
   manager. Confirm `.env` and `*.env` are in `.gitignore` (they are).

If a key is accidentally committed:
- Revoke it immediately in the Anthropic console.
- Rewrite the git history with `git filter-repo` or contact the repo owner for a
  force push. Treat the key as compromised the moment it appears in any commit.

## Upgrade Dependencies

If you need to upgrade a dependency (e.g., `anthropic`):

```bash
.venv/bin/pip install --upgrade anthropic
.venv/bin/pip freeze | grep -E "^(anthropic|jsonschema|PyYAML)==" > requirements.txt
```

Then run stub benchmarks to confirm nothing broke, and commit `requirements.txt`.

## What Counts as a V1 Pass

A pipeline run is a **V1 pass** if and only if all of the following are true:

| Criterion | Pass condition |
|---|---|
| **Outcome** | `PipelineResult.outcome == "approved"` OR `"rejected"` at the expected stage |
| **Stop stage** | `PipelineResult.final_artifact_name` matches the benchmark's `expected_stop` |
| **Interaction** | `primary_interaction_type` matches `expected_interaction` (warnings logged but permitted) |
| **All gates** | Every stage that ran returned `status == "pass"` before advancing |
| **No stalls** | `outcome != "stalled"` — stalled means a revision limit was exceeded unexpectedly |

**Benchmark-level pass:** All 5 cases satisfy all five criteria above. The suite exits
with code `0`. Any `[FAIL]` line in stdout is a regression.

Interaction type mismatches between stub and LLM runs are expected and do not constitute
a failure. Investigate any mismatch before promoting an LLM run as a clean regression
baseline.

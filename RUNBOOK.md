# Math Game Studio OS — Runbook

## Environment Setup

**Requirements:** Python 3.14 (the repo ships with a `.venv` already provisioned).

If the venv is missing or broken, recreate it:

```bash
python3.14 -m venv .venv
.venv/bin/pip install -r requirements.txt   # if a requirements file exists
# or: .venv/bin/pip install anthropic jsonschema
```

## Activate the Virtual Environment

```bash
# From repo root:
source .venv/bin/activate

# Verify:
which python    # should resolve to .venv/bin/python
python --version  # should show Python 3.14.x
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

**Expected result:** `5/5 passed` with no FAIL lines.

## Run LLM Benchmarks

LLM mode drives all six pipeline agents through Claude. It requires `ANTHROPIC_API_KEY` to be set.

```bash
# Ensure the key is exported in your shell session:
export ANTHROPIC_API_KEY=sk-ant-...

# Run LLM benchmarks (defaults to claude-sonnet-4-6):
.venv/bin/python scripts/run_benchmarks.py --llm --report

# Override the model:
.venv/bin/python scripts/run_benchmarks.py --llm --model claude-opus-4-6 --report
```

Reports are written to `reports/benchmark_regression_llm_<timestamp>.md`.

**Expected result:** `5/5 passed`. Interaction warnings are acceptable; outcome and stop-stage must both match.

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
4. **Revoke the old key** in the Anthropic console only after confirming the new key passes benchmarks.
5. **Never commit a key to git.** The key lives only in your shell profile or a secrets manager. Confirm `.env` and `*.env` are in `.gitignore`.

If a key is accidentally committed:
- Revoke it immediately in the Anthropic console.
- Rewrite the git history with `git filter-repo` or contact the repo owner for a force push.

## What Counts as a V1 Pass

A pipeline run is a **V1 pass** if and only if all of the following are true:

| Criterion | Pass condition |
|---|---|
| **Outcome** | `PipelineResult.outcome == "approved"` OR `"rejected"` at the expected stage |
| **Stop stage** | `PipelineResult.final_artifact_name` matches the benchmark's `expected_stop` |
| **Interaction** | `primary_interaction_type` in the `interaction_decision_memo` matches `expected_interaction` (warnings allowed; failures are not) |
| **All six gate decisions** | Every stage that ran returned `status == "pass"` before advancing |
| **No stalled jobs** | `outcome != "stalled"` — stalled means a revision limit was hit unexpectedly |

**Benchmark-level pass:** All 5 benchmark cases pass the three criteria above. The suite exits with code `0`. Any `FAIL` line in the output is a regression.

**Interaction mismatches** are logged as warnings, not failures — the pipeline may produce a valid but different interaction type in LLM mode. Investigate warnings before promoting to production.

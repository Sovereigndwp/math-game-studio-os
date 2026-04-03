"""
utils/llm_caller.py — LLM callable factory for Math Game Studio OS agents.

Provides make_claude_callable(), which returns a model_callable compatible with
SharedAgentRunner.run(). The callable formats agent context into a Claude prompt,
calls the Anthropic Messages API, extracts JSON from the response, and returns
the artifact dict.

Usage:
    from utils.llm_caller import make_claude_callable
    from agents.intake_framing.agent import run as run_intake

    callable = make_claude_callable(model="claude-sonnet-4-6")
    result = run_intake(repo_root, job_id, artifact_paths, model_callable=callable)

Requirements:
    - ANTHROPIC_API_KEY environment variable (or pass api_key= explicitly)
    - Either: `pip install anthropic` (preferred SDK path)
    - Or: `requests` (fallback HTTP path — already available in this environment)

Engine boundary note:
    Agents decide framing, interaction choice, family placement, loop design.
    This module only handles the I/O contract between the runner and the LLM.
    It does not interpret, filter, or transform artifact content.
"""
from __future__ import annotations

import json
import os
import re
import textwrap
from pathlib import Path
from typing import Any, Callable, Dict, Optional


# ---------------------------------------------------------------------------
# Prompt formatting
# ---------------------------------------------------------------------------


def format_user_message(context: Dict[str, Any]) -> str:
    """
    Format the user-turn message sent to Claude for a given agent context.

    The message includes:
    - Job metadata
    - All input artifacts as formatted JSON
    - Clear instruction to produce the output artifact as valid JSON
    """
    job_id = context["job_id"]
    expected_output = context["expected_output_artifact"]
    expected_produced_by = context["expected_produced_by"]
    artifact_inputs = context["artifact_inputs"]

    sections: list[str] = []

    sections.append(f"## Job context\nJob ID: `{job_id}`")

    if artifact_inputs:
        sections.append("## Input artifacts\n")
        for name, artifact in artifact_inputs.items():
            sections.append(
                f"### {name}\n```json\n{json.dumps(artifact, indent=2)}\n```"
            )

    output_schema = context.get("output_schema")

    output_block_lines = [
        f"## Output required",
        f"Produce a single valid JSON object for artifact `{expected_output}`.",
        f"",
        f"These three fields are injected by the runner after your response — do NOT omit them, but they will be overwritten with correct values regardless:",
        f'- `"artifact_name"`: `"{expected_output}"`',
        f'- `"produced_by"`: `"{expected_produced_by}"`',
        f'- `"job_id"`: `"{job_id}"`',
        f'- `"version"`: integer ≥ 1 (set to 1)',
        f"",
        f"Return ONLY the raw JSON object. No explanation, no markdown fences, no text before or after.",
        f"If you use a code block, use ```json ... ``` with nothing outside it.",
    ]

    if output_schema is not None:
        output_block_lines += [
            f"",
            f"### Exact output schema (validation is strict — `additionalProperties: false`)",
            f"Your JSON MUST conform to this schema exactly. Any field not listed under `properties` will cause a hard validation failure.",
            f"```json",
            json.dumps(output_schema, indent=2),
            f"```",
        ]

    sections.append("\n".join(output_block_lines))

    return "\n\n".join(sections)


# ---------------------------------------------------------------------------
# JSON extraction
# ---------------------------------------------------------------------------


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    Extract a JSON object from LLM response text.

    Handles:
    - Raw JSON response
    - JSON wrapped in ```json ... ``` code blocks
    - JSON wrapped in ``` ... ``` code blocks
    - Leading/trailing whitespace or commentary around the JSON
    """
    text = text.strip()

    # 1. Try direct parse first (clean responses)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Extract from ```json ... ``` code block
    match = re.search(r"```json\s*([\s\S]+?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # 3. Extract from generic ``` ... ``` code block
    match = re.search(r"```\s*([\s\S]+?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # 4. Find the first { ... } block spanning the full depth
    start = text.find("{")
    if start != -1:
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start : i + 1])
                    except json.JSONDecodeError:
                        break

    raise ValueError(
        f"Could not extract a valid JSON object from LLM response. "
        f"First 300 chars: {text[:300]!r}"
    )


# ---------------------------------------------------------------------------
# API caller: anthropic SDK path
# ---------------------------------------------------------------------------


def _call_via_sdk(
    system_prompt: str,
    user_message: str,
    model: str,
    api_key: Optional[str],
    max_tokens: int,
) -> str:
    import anthropic  # type: ignore

    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


# ---------------------------------------------------------------------------
# API caller: requests fallback path (no anthropic SDK needed)
# ---------------------------------------------------------------------------


def _call_via_requests(
    system_prompt: str,
    user_message: str,
    model: str,
    api_key: Optional[str],
    max_tokens: int,
) -> str:
    import requests  # type: ignore

    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. "
            "Export it before running LLM mode: export ANTHROPIC_API_KEY=sk-ant-..."
        )

    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_message}],
    }

    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=payload,
        timeout=120,
    )

    if resp.status_code != 200:
        raise RuntimeError(
            f"Anthropic API error {resp.status_code}: {resp.text[:500]}"
        )

    data = resp.json()
    return data["content"][0]["text"]


# ---------------------------------------------------------------------------
# Main factory
# ---------------------------------------------------------------------------


def make_claude_callable(
    model: str = "claude-sonnet-4-6",
    api_key: Optional[str] = None,
    max_tokens: int = 4096,
) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """
    Return a model_callable that drives a Math Game Studio OS agent via Claude.

    The callable:
    1. Formats the agent context (prompt.md + artifact inputs) into a prompt
    2. Calls the Anthropic Messages API (SDK if available, requests otherwise)
    3. Parses the JSON artifact from the response
    4. Injects job_id, artifact_name, produced_by (SharedAgentRunner also enforces these)

    Args:
        model:      Anthropic model string. Default: "claude-sonnet-4-6"
        api_key:    API key. Falls back to ANTHROPIC_API_KEY env var.
        max_tokens: Max tokens for the response. 4096 is sufficient for all V1 artifacts.

    Returns:
        Callable[[Dict[str, Any]], Dict[str, Any]] — compatible with SharedAgentRunner.run()

    Engine boundary:
        This function handles I/O only. It does not interpret artifact content,
        apply gate logic, or make routing decisions.
    """
    # Detect which call path is available
    try:
        import anthropic as _  # noqa: F401
        _use_sdk = True
    except ImportError:
        _use_sdk = False

    def callable(context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt: str = context["prompt_text"]
        user_message: str = format_user_message(context)

        if _use_sdk:
            raw_text = _call_via_sdk(system_prompt, user_message, model, api_key, max_tokens)
        else:
            raw_text = _call_via_requests(system_prompt, user_message, model, api_key, max_tokens)

        artifact = extract_json_from_text(raw_text)
        return artifact

    return callable


# ---------------------------------------------------------------------------
# Dry-run validator (no API call — verifies prompt formatting only)
# ---------------------------------------------------------------------------


def dry_run_format(context: Dict[str, Any]) -> Dict[str, str]:
    """
    Return the formatted system prompt and user message without making an API call.
    Use for prompt inspection, testing, and debugging.
    """
    return {
        "system_prompt": context["prompt_text"],
        "user_message": format_user_message(context),
    }


# ---------------------------------------------------------------------------
# CLI inspection tool
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    import sys

    repo_root = Path(__file__).resolve().parents[1]
    schema_dir = repo_root / "artifacts" / "schemas"

    print("LLM caller module loaded.")
    print(f"  SDK path available: {_use_sdk if '_use_sdk' in dir() else 'check import'}")  # type: ignore[name-defined]
    print(f"  API key set: {'yes' if os.environ.get('ANTHROPIC_API_KEY') else 'NO — set ANTHROPIC_API_KEY'}")
    print()
    print("To test: from utils.llm_caller import make_claude_callable, dry_run_format")

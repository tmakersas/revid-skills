"""
Tiny shared client for the Revid Public API v3.

All Python examples in this folder import from here so we don't repeat the
auth / polling logic.
"""
from __future__ import annotations

import os
import time
from typing import Any

import requests

API = "https://www.revid.ai/api/public/v3"


def _key() -> str:
    k = os.environ.get("REVID_API_KEY")
    if not k:
        raise RuntimeError("REVID_API_KEY not set")
    return k


def render(payload: dict[str, Any]) -> str:
    """POST /render — returns the project id (pid)."""
    r = requests.post(
        f"{API}/render",
        json=payload,
        headers={"key": _key(), "Content-Type": "application/json"},
        timeout=30,
    )
    r.raise_for_status()
    body = r.json()
    if body.get("success") != 1:
        raise RuntimeError(f"render failed: {body.get('error', body)}")
    return body["pid"]


def wait_for(pid: str, timeout_s: int = 600) -> dict[str, Any]:
    """Poll /status until ready/failed/timeout. Returns the final body."""
    deadline = time.time() + timeout_s
    delay = 5.0
    while time.time() < deadline:
        r = requests.get(
            f"{API}/status",
            params={"pid": pid},
            headers={"key": _key()},
            timeout=15,
        )
        r.raise_for_status()
        body = r.json()
        status = body.get("status")
        progress = body.get("progress", 0)
        print(f"  pid={pid} status={status} progress={progress}")
        if status == "ready":
            return body
        if status == "failed":
            raise RuntimeError(f"render failed: {body.get('error', body)}")
        time.sleep(delay)
        if progress > 30:
            delay = 8.0
    raise TimeoutError(f"pid {pid} not ready after {timeout_s}s")


def estimate_credits(payload: dict[str, Any]) -> dict[str, Any]:
    """POST /calculate-credits — returns the estimate without rendering."""
    r = requests.post(
        f"{API}/calculate-credits",
        json=payload,
        headers={"key": _key(), "Content-Type": "application/json"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()

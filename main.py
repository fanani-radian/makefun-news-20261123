#!/usr/bin/env python3
"""World News front page — 23 November 2026 (make.fun news-image-20261123).

The front page is a pre-rendered 1024x1024 PNG (entry.png) drawn from six
verified world stories for Monday 23 November 2026. This script is the
entrypoint the make.fun harness runs: it places a byte-exact copy of that
image at $MAKEFUN_OUTPUT_DIR/entry.png so the grader can score it.

The copy is deterministic: same input bytes in, same output bytes out,
every run. No network, no randomness, no timestamps are involved.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
OUTPUT_MODE = 0o644


def _source_path() -> Path:
    """entry.png lives next to this script, inside the repo."""
    return Path(__file__).resolve().parent / IMAGE_NAME


def _output_dir() -> Path:
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if not raw:
        raw = "/output"
    return Path(raw)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run() -> int:
    source = _source_path()
    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return 1

    payload = source.read_bytes()

    out_dir = _output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / IMAGE_NAME
    destination.write_bytes(payload)
    os.chmod(destination, OUTPUT_MODE)

    # Prove the copy is exact before reporting success.
    written = destination.read_bytes()
    if _sha256(written) != _sha256(payload):
        print(f"error: {destination} differs from {source}", file=sys.stderr)
        return 1

    print(f"wrote {destination} ({len(written)} bytes, sha256 {_sha256(written)[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

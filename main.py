#!/usr/bin/env python3
"""World News front page — 23 November 2026 (make.fun news-image-20261123).

The front page is a pre-rendered 1024x1024 PNG (entry.png) drawn from six
verified world stories for Monday 23 November 2026. This script is the
entrypoint the make.fun harness runs: it places a byte-exact copy of that
image at $MAKEFUN_OUTPUT_DIR/entry.png so the grader can score it.

The copy is deterministic: same input bytes in, same output bytes out,
every run. No network, no randomness, no timestamps are involved.

Pass --verify-only to check an existing output copy instead of writing
one: it exits 0 when $MAKEFUN_OUTPUT_DIR/entry.png is byte-identical to
entry.png, and 1 (with an explanation) when it is missing or differs.
"""

from __future__ import annotations

import argparse
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


def _load_source() -> bytes | None:
    """Read entry.png, or report why it cannot be read."""
    source = _source_path()
    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return None
    return source.read_bytes()


def _verify(payload: bytes) -> int:
    """Check the existing output copy against the source bytes."""
    destination = _output_dir() / IMAGE_NAME
    if not destination.is_file():
        print(f"error: {destination} does not exist", file=sys.stderr)
        return 1
    written = destination.read_bytes()
    if _sha256(written) != _sha256(payload):
        print(
            f"error: {destination} differs from {_source_path()} "
            f"(got sha256 {_sha256(written)}, want {_sha256(payload)})",
            file=sys.stderr,
        )
        return 1
    print(f"verified {destination} ({len(written)} bytes, sha256 {_sha256(written)})")
    return 0


def _copy(payload: bytes) -> int:
    """Write a byte-exact copy of the source and prove it landed intact."""
    out_dir = _output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if not out_dir.is_dir():
        print(f"error: {out_dir} is not a directory", file=sys.stderr)
        return 1
    destination = out_dir / IMAGE_NAME
    destination.write_bytes(payload)
    os.chmod(destination, OUTPUT_MODE)
    return _verify(payload)


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="check the existing output copy instead of writing one",
    )
    args = parser.parse_args(argv)

    payload = _load_source()
    if payload is None:
        return 1
    if args.verify_only:
        return _verify(payload)
    return _copy(payload)


if __name__ == "__main__":
    raise SystemExit(run())

#!/usr/bin/env python3
"""Check the explicit release file set and common accidental secret/path leaks."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SENSITIVE = [
    re.compile(r"/(?:Users|home)/[^\s<>]+"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
]


def verify(root=ROOT):
    root = Path(root)
    manifest = json.loads((root / "release-manifest.json").read_text(encoding="utf-8"))
    listed = manifest["files"]
    if len(listed) != len(set(listed)):
        raise ValueError("Duplicate paths in the release manifest")
    expected = set(listed)
    actual = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if path.is_symlink():
            raise ValueError(f"Symlinks are not release inputs: {relative}")
        if path.is_file():
            actual.add(relative.as_posix())
    if actual != expected:
        raise ValueError(f"Manifest mismatch: extra={sorted(actual-expected)}, missing={sorted(expected-actual)}")
    for relative in sorted(expected):
        path = root / relative
        if path.stat().st_size > 150_000:
            raise ValueError(f"Unexpectedly large release file: {relative}")
        text = path.read_text(encoding="utf-8")
        if any(pattern.search(text) for pattern in SENSITIVE):
            raise ValueError(f"Sensitive path or credential pattern in: {relative}")
    return len(expected)


if __name__ == "__main__":
    try:
        count = verify()
    except (ValueError, OSError, UnicodeError) as exc:
        raise SystemExit(f"Release check failed: {exc}")
    print(f"Release check passed: {count} explicitly listed UTF-8 files.")

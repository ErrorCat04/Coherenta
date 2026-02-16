#!/usr/bin/env python3
"""Verify a Coherenta release bundle using sha256 and a detached signature.

This script is intentionally minimal: it verifies only sha256.
Signature verification depends on your chosen crypto tool (gpg/age/minisign/sigstore).
"""

import hashlib, sys, pathlib

def sha256_file(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    if len(sys.argv) != 3:
        print("Usage: verify_sha256.py <bundle.zip> <bundle.sha256>")
        return 2
    bundle = pathlib.Path(sys.argv[1])
    sha_file = pathlib.Path(sys.argv[2])
    expected = sha_file.read_text(encoding="utf-8").strip().split()[0]
    actual = sha256_file(bundle)
    if actual.lower() == expected.lower():
        print("OK: sha256 matches")
        return 0
    print("FAIL: sha256 mismatch")
    print(" expected:", expected)
    print(" actual:  ", actual)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())

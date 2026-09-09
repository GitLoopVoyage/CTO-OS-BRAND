#!/usr/bin/env python3
"""
CTO OS Visual Canon v0.1 — product-shell.css derivation (deterministic)

product-shell.css is NOT an authored file. It is derived, byte for byte, from the
single <style> block of the frozen Day 2 artifact product-shell.html, whose
SHA-256 is pinned below. Any edit to product-shell.css that is not a re-run of
this script is a canon violation; `--check` proves the committed bytes equal the
derivation output.

Usage
  python3 derive-shell-css.py            # (re)write product-shell.css
  python3 derive-shell-css.py --check    # exit 0 iff committed bytes == derivation

No dependencies beyond the Python standard library. Output is independent of
platform, locale, time, and environment.
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "product-shell.html")
TARGET = os.path.join(HERE, "product-shell.css")

# Frozen Day 2 identity of the source artifact (CANON_FREEZE_PRODUCT_SHELL_DAY_2).
SOURCE_SHA256 = "1e54c7fa2616c5c6441660cbb7e7652505b4ef65b4552db56f034e141f62aa94"


def derive() -> bytes:
    src = open(SOURCE, "rb").read()
    actual = hashlib.sha256(src).hexdigest()
    if actual != SOURCE_SHA256:
        sys.stderr.write(
            "derive-shell-css: source identity mismatch\n"
            f"  expected {SOURCE_SHA256}\n  actual   {actual}\n"
            "  product-shell.html is frozen; refusing to derive from different bytes.\n"
        )
        sys.exit(2)
    text = src.decode("utf-8")
    blocks = re.findall(r"<style>(.*?)</style>", text, re.S)
    if len(blocks) != 1:
        sys.stderr.write(f"derive-shell-css: expected exactly one <style> block, found {len(blocks)}\n")
        sys.exit(2)
    header = (
        "/*!\n"
        " * CTO OS — Product Shell stylesheet  v0.1  (DERIVED ARTIFACT — do not edit)\n"
        " * Source: product-shell.html  sha256 " + SOURCE_SHA256 + "\n"
        " * Derivation: 04-product-shell/derive-shell-css.py (deterministic; run with --check to verify)\n"
        " * Content below is the source's single <style> block, byte for byte.\n"
        " * Load AFTER canon-tokens.css. Shipped because compositions (Command Center, Day 4)\n"
        " * need to link the shell without embedding the gallery page.\n"
        " */\n"
    )
    return (header + blocks[0]).encode("utf-8")


def main() -> int:
    out = derive()
    if "--check" in sys.argv[1:]:
        if not os.path.exists(TARGET):
            print("derive-shell-css: CHECK FAIL — product-shell.css missing")
            return 1
        cur = open(TARGET, "rb").read()
        if cur == out:
            print(f"derive-shell-css: CHECK OK — product-shell.css == derivation "
                  f"({len(out)} bytes, sha256 {hashlib.sha256(out).hexdigest()})")
            return 0
        print("derive-shell-css: CHECK FAIL — product-shell.css differs from derivation\n"
              f"  committed  sha256 {hashlib.sha256(cur).hexdigest()} ({len(cur)} bytes)\n"
              f"  derivation sha256 {hashlib.sha256(out).hexdigest()} ({len(out)} bytes)")
        return 1
    with open(TARGET, "wb") as f:
        f.write(out)
    print(f"derive-shell-css: wrote product-shell.css ({len(out)} bytes, sha256 {hashlib.sha256(out).hexdigest()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

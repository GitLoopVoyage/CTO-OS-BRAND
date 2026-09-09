# CTO OS Brand — Visual Canon

`CTO_OS_VISUAL_CANON_V0.1` · Phase A closed · Phase B in progress

Every artifact in this repository is subordinate to one rule:

> **No visual may imply more authority, certainty, verification, safety or runtime state than the underlying CTO OS model actually establishes.**

That rule is a build gate, not a sensibility. See `03-canon-lint/`.

## Contents

| Dir | Artifact | Status |
|---|---|---|
| `01-fractal-core-mark/` | Fractal Core mark — vector master v2, eight canonical SVGs, production board, mechanical audit | **VECTOR MASTER v2 · QA_2 31/31 PASS** |
| `02-fractal-pulse/` | Fractal Pulse motion system — five states, two masters, custom element + React wrapper | **BUILT · lint-clean** |
| `03-canon-lint/` | Canon Lint — the machine gate. Checks computed styles in a real browser against the model extract's vocabularies | **ACTIVE · R0–R11** |
| `04-product-shell/` | Product Shell — navigation, panel taxonomy, density, component set, token layer | **DAY 2 · PASS / FREEZE** |
| `05-freeze-records/` | Freeze records and hash-bound machine reports | — |
| `06-canon-program/` | Week-one programme plan | — |

## Verify

`MANIFEST.sha256` lists every file. Verify the tree:

```
sha256sum -c MANIFEST.sha256
```

The Day-2 freeze binds these identities (see `05-freeze-records/CANON_FREEZE_PRODUCT_SHELL_DAY_2.md`):

```
04-product-shell/product-shell.html   1e54c7fa2616c5c6441660cbb7e7652505b4ef65b4552db56f034e141f62aa94   46,536 bytes
04-product-shell/canon-tokens.css     3d944a6352cbf0c80b6964f06a3b8271a56a8edd9cd23bf13a8d730a4dd01dab    6,363 bytes
02-fractal-pulse/fractal-pulse.html   d3b6f8effb4314debe6d32055c4d148206de68641e33084287253f95e0d091b4   49,226 bytes
03-canon-lint/canon-lint.js           ce172f94626c169824ea9a1209022ed936c58c0500aeab54391c1d41e5966a57   20,691 bytes
03-canon-lint/canon-vocabulary.json   e18e14c3628c17be1327ac1db30b10b48f097afa9bcccd8e3c0203f36eacb632    3,295 bytes
```

## Run the gate

```
npm i playwright
node 03-canon-lint/canon-lint.js 04-product-shell/product-shell.html --json report.json
```

Exit 0 = no errors. The report embeds the SHA-256 of every target and of the ruleset that produced it. A report that names a filename is narrative; a report that names bytes is evidence.

## Regenerate the mark

```
cd 01-fractal-core-mark/source
python3 assets2.py     # eight canonical SVGs
python3 board2.py      # production board SVG
python3 audit.py       # 31-check mechanical audit
```

Geometry lives in `geom2.py`. Wordmark glyph paths (`wm_*.txt`) are frozen outlines; `wm.py` documents how they were derived and is not re-run.

## Doctrine sources

Structure and vocabulary trace to: `GF_R2_CORE_FORMAL_SPECIFICATION`, `00_CTO_OS_PRODUCT_CONSTITUTION` (Art. 21.2, 23.2, 26.4, 33, 35.2), `CTO_OS_VISUAL_CANON_MODEL_EXTRACT_V0.1`. Nothing here amends any governance artifact. Reference-tenant data (Meridian Logistics) is synthetic throughout and declared as such at each fixture root.

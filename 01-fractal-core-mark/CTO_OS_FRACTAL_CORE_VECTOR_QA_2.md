# CTO OS Fractal Core Mark — Mechanical Vector Audit 2

**Audit ID:** `CTO_OS_FRACTAL_CORE_VECTOR_QA_2`
**Audit date:** 2026-09-01
**Supersedes:** `CTO_OS_FRACTAL_CORE_VECTOR_QA_1`
**Scope:** `VECTOR_CORRECTION_1` — re-run of the exact QA_1 check set against the corrected master and all re-exported derivatives.
**Resolution applied:** **MODEL B** — the canonical vector was redrawn so three genuinely distinct nested open frames exist, each carrying exactly one canonical gate.

## Disposition

```text
CONCEPT:
PASS / FROZEN

CANONICAL THREE-FRAME CONSTRUCTION CLAIM:
PASS                      (VQA-01 CLOSED)

GATE-SEQUENCE DOCUMENTATION:
PASS                      (VQA-01 CLOSED)

VERTICAL LOCKUP VIEWBOX:
PASS                      (VQA-02 CLOSED)

PATH CONSISTENCY:
PASS

COLOR HIERARCHY:
PASS

WORDMARK PATH CONSISTENCY:
PASS / UNCHANGED

MONOCHROME:
PASS

FONT-INDEPENDENT CANONICAL MARK:
PASS

RASTER-FREE STANDALONE SVGs:
PASS

MASK / CLIP COMPLEXITY:
PASS

MICRO-MARK DOCUMENTATION:
PASS WITH DOCUMENTED 16 PX EXCEPTION

OVERALL:
PRODUCTION MASTER v1.0 — APPROVED
0 BLOCKING DEFECTS
```

# VQA-01 — closed

## What changed

The QA_1 finding was correct: the previous canonical path contained one `10X` outer frame and one `6X` inner frame that carried **both** the left and bottom gates. There was no third frame.

Under Model B the master was redrawn. Before redrawing, the constraint set was solved rather than guessed.

## Why the inter-frame gap had to change

Preserved without exception: `10X × 10X` master, `X` stroke on every frame, `2X × 2X` `#2563EB` core, neutral structural frames, existing wordmark paths.

Edge-to-core budget along either axis is `4X`, and must satisfy:

```text
X(f1) + g1 + X(f2) + g2 + X(f3) + clearance = 4X
=>  g1 + g2 + clearance = X
```

Enumerating integer-`X` assignments with both gaps non-zero:

```text
g1 = 0X  g2 = 0X  c = 1X   INVALID — f1/f2 and f2/f3 touch
g1 = 0X  g2 = 1X  c = 0X   INVALID — f1/f2 touch
g1 = 1X  g2 = 0X  c = 0X   INVALID — f2/f3 touch

integer solutions: NONE
```

**No integer-`X` master can carry three distinct frames.** The unique uniform solution is:

```text
g1 = g2 = X/2      clearance = 0
```

The master therefore resolves on a **half-X grid (20 × 20)** while every frame stroke remains exactly `X`. The inter-frame gap was the only free variable, and it is the only construction variable that changed. It was not on the preserve list.

## Corrected construction

```text
MASTER            10X x 10X
FRAME STROKE      X            (all three frames)
INTER-FRAME GAP   X/2          (uniform)
GATE WIDTH        2X           (all three gates)
CENTRAL CORE      2X x 2X      (flush inside f3)
CORE CLEARANCE    0

f1 OUTER    bbox 0.0 - 10.0 X    ring 0.0-1.0 / 9.0-10.0    GATE = TOP
f2 MIDDLE   bbox 1.5 -  8.5 X    ring 1.5-2.5 / 7.5- 8.5    GATE = LEFT
f3 INNER    bbox 3.0 -  7.0 X    ring 3.0-4.0 / 6.0- 7.0    GATE = BOTTOM
CORE             4.0 -  6.0 X
```

All three gates sit on the core axes (`x 4-6`, `y 4-6`).

## Corrected canonical structural path

```svg
M0 0h4v1h-4z
M6 0h4v1h-4z
M0 9h10v1h-10z
M0 1h1v8h-1z
M9 1h1v8h-1z

M1.5 1.5h7v1h-7z
M1.5 7.5h7v1h-7z
M1.5 2.5h1v1.5h-1z
M1.5 6h1v1.5h-1z
M7.5 2.5h1v5h-1z

M3 3h4v1h-4z
M3 4h1v2h-1z
M6 4h1v2h-1z
M3 6h1v1h-1z
M6 6h1v1h-1z
```

Core, unchanged:

```svg
M4 4h2v2h-2z
```

## Machine verification of the three-frame claim

The claim is no longer asserted in prose. It is derived from the path by 4-connected component labelling on the half-X grid, and each component's ring is tested for exactly one gap:

```text
components found ........ 3
f1  bbox [0.0, 0.0, 10.0, 10.0]   gates 1   side TOP      width 2X
f2  bbox [1.5, 1.5,  8.5,  8.5]   gates 1   side LEFT     width 2X
f3  bbox [3.0, 3.0,  7.0,  7.0]   gates 1   side BOTTOM   width 2X
```

## Centre-line equivalence

Each frame is also expressible as a single open centre-line path stroked at width `X`, butt caps, miter joins — one arc per frame, opened at that frame's own gate:

```text
f1 OUTER   M6 0.5 L9.5 0.5 L9.5 9.5 L0.5 9.5 L0.5 0.5 L4 0.5        len 34X
f2 MIDDLE  M2 4 L2 2 L8 2 L8 8 L2 8 L2 6                            len 22X
f3 INNER   M4 6.5 L3.5 6.5 L3.5 3.5 L6.5 3.5 L6.5 6.5 L6 6.5        len 10X
```

Rasterised at 800 x 800 against the filled-rectangle master:

```text
max pixel delta ......... 0
differing pixels ........ 0 of 640000
```

The stroked form and the filled form are the same object. This is what the Fractal Pulse motion system animates, so motion and mark cannot drift apart.

# VQA-02 — closed

Measured wordmark ink bounds (baseline at `y = 0`, cap height `6X`):

```text
ink x   0.4114  ->  34.1143
ink y  -6.0686  ->   0.0686
```

The `+0.0686X` overshoot below the baseline is confirmed exactly as reported.

**Correction applied:** the vertical lockup viewBox height was raised from `19.0000` to `19.5000`, adding a declared optical margin of `X/2` below the baseline. The frozen `3X` symbol-to-wordmark gap and the `6X` cap height are untouched — the wordmark did not move.

```text
VLOCK_H = 10X (symbol) + 3X (gap) + 6X (cap) + 0.5X (optical margin) = 19.5X
```

Rendered ink-bound containment, measured per file:

| File | viewBox | Margins (X) | Result |
|---|---|---|---|
| `ctoossymbolfullcolourdarkbg.svg` | `0 0 10 10` | L 0.0000  T 0.0000  R 0.0000  B 0.0000 | PASS |
| `ctoossymbolfullcolourlightbg.svg` | `0 0 10 10` | L 0.0000  T 0.0000  R 0.0000  B 0.0000 | PASS |
| `ctoossymbolmonochromepositive.svg` | `0 0 10 10` | L 0.0000  T 0.0000  R 0.0000  B 0.0000 | PASS |
| `ctoossymbolmonochromereversed.svg` | `0 0 10 10` | L 0.0000  T 0.0000  R 0.0000  B 0.0000 | PASS |
| `ctooslockuphorizontaldarkbg.svg` | `0 0 47.4656982421875 10` | L 0.0000  T 0.0000  R 0.3514  B 0.0000 | PASS |
| `ctooslockuphorizontallightbg.svg` | `0 0 47.4656982421875 10` | L 0.0000  T 0.0000  R 0.3514  B 0.0000 | PASS |
| `ctooslockupverticaldarkbg.svg` | `0 0 34.4656982421875 19.5` | L 0.4114  T 0.0000  R 0.3514  B 0.4314 | PASS |
| `ctooslockupverticallightbg.svg` | `0 0 34.4656982421875 19.5` | L 0.4114  T 0.0000  R 0.3514  B 0.4314 | PASS |

Bottom margin on the vertical lockup moved from `-0.0686` (overshoot, clipping) to `+0.4314`.

# Full check set

| Check | Result | Evidence |
|---|---|---|
| Three distinct structural frames (4-connected components) | PASS | 3 components found |
| f1 OUTER carries exactly one TOP gate of 2X | PASS | bbox [0.0, 0.0, 10.0, 10.0], gate TOP, width 2X |
| f2 MIDDLE carries exactly one LEFT gate of 2X | PASS | bbox [1.5, 1.5, 8.5, 8.5], gate LEFT, width 2X |
| f3 INNER carries exactly one BOTTOM gate of 2X | PASS | bbox [3.0, 3.0, 7.0, 7.0], gate BOTTOM, width 2X |
| Gate sequence outer=TOP / middle=LEFT / inner=BOTTOM | PASS | f1 OUTER=TOP / f2 MIDDLE=LEFT / f3 INNER=BOTTOM |
| Every structural rectangle is exactly 1X thick | PASS | 0 violations |
| Frame bounds f1 0-10, f2 1.5-8.5, f3 3-7 | PASS | f1 [0.0, 0.0, 10.0, 10.0]  f2 [1.5, 1.5, 8.5, 8.5]  f3 [3.0, 3.0, 7.0, 7.0] |
| Inter-frame gap uniform at X/2 | PASS | g1 = 0.5X, g2 = 0.5X |
| Central core exactly 2X x 2X | PASS | rect (4, 4, 2, 2) |
| Core clearance 0 (core flush inside f3) | PASS | clearance = 0X |
| Edge-to-core budget closes at 10X | PASS | X + X/2 + X + X/2 + X + 0, doubled, + 2X core = 10X |
| Canonical frame path identical in all 8 standalone assets | PASS | single shared path string |
| Core path identical in all 8 standalone assets | PASS | M4 4h2v2h-2z |
| Wordmark paths identical across all lockups | PASS | 4 lockups share one converted glyph set |
| Colour hierarchy ctoossymbolfullcolourdarkbg.svg | PASS | fills ['#EDF0F3', '#2563EB'] |
| Colour hierarchy ctoossymbolfullcolourlightbg.svg | PASS | fills ['#191C20', '#2563EB'] |
| Colour hierarchy ctoossymbolmonochromepositive.svg | PASS | fills ['#191C20', '#191C20'] |
| Colour hierarchy ctoossymbolmonochromereversed.svg | PASS | fills ['#EDF0F3', '#EDF0F3'] |
| Cobalt never fills a structural frame | PASS | frame fills: #191C20, #EDF0F3 |
| Wordmark OS set in #2563EB on full-colour lockups | PASS | #2563EB |
| ctoossymbolfullcolourdarkbg.svg free of live text / raster / clip machinery | PASS | paths only |
| ctoossymbolfullcolourlightbg.svg free of live text / raster / clip machinery | PASS | paths only |
| ctoossymbolmonochromepositive.svg free of live text / raster / clip machinery | PASS | paths only |
| ctoossymbolmonochromereversed.svg free of live text / raster / clip machinery | PASS | paths only |
| ctooslockuphorizontaldarkbg.svg free of live text / raster / clip machinery | PASS | paths only |
| ctooslockuphorizontallightbg.svg free of live text / raster / clip machinery | PASS | paths only |
| ctooslockupverticaldarkbg.svg free of live text / raster / clip machinery | PASS | paths only |
| ctooslockupverticallightbg.svg free of live text / raster / clip machinery | PASS | paths only |
| Symbol viewBox 0 0 10 10 | PASS | 0 0 10 10 |
| Horizontal lockup viewBox 0 0 47.4657 10 | PASS | 0 0 47.4657 10 |
| Vertical lockup viewBox raised to 0 0 34.4657 19.5000 (VQA-02) | PASS | was 0 0 34.4657 19.0000 |

**31 checks, 31 PASS, 0 FAIL.**

# Re-exported derivatives

All eight standalone assets were regenerated from the corrected master in a single pass, plus the production board.

```text
ctoossymbolfullcolourdarkbg.svg
ctoossymbolfullcolourlightbg.svg
ctoossymbolmonochromepositive.svg
ctoossymbolmonochromereversed.svg
ctooslockuphorizontaldarkbg.svg
ctooslockuphorizontallightbg.svg
ctooslockupverticaldarkbg.svg
ctooslockupverticallightbg.svg      (added — light-ground vertical lockup)
CTOOSProductionBoard.svg
CTOOSProductionBoard.png
```

The board defines one `frames` path, one `core` path and one wordmark path set, referenced by `<use>` 15 times each. Every literal copy of the canonical path string in the board is byte-identical to the master.

**One intentional exception:** the board contains exactly one instance of `href="#frames" fill="#2563EB"`. It is inside panel O, labelled `COBALT FRAMES — Cobalt may never fill a frame`. Verified as the sole occurrence.

# Micro-mark rule, restated for the three-frame master

The `X/2` gap means the full master only lands on whole pixels at an even `X`.

```text
40 px and above   X = size / 10, no snapping required
32 px             X = 3 px on a 30 px optical box; the X/2 gap renders at 1.5 px
24 px             X = 2 px on a 20 px optical box; every edge on a whole pixel
16 px             DOCUMENTED EXCEPTION — reduced 8X two-frame micro master,
                  X = 2 px, f3 and its BOTTOM gate omitted,
                  TOP and LEFT gates retained
```

# Non-blocking production notes, carried forward

The production board still uses live `<text>` for its own documentation labels with `Inter / Helvetica Neue / Arial` fallbacks. This does not touch the canonical mark or lockups, whose wordmarks are converted to paths. If the board itself must be archival, convert board labels to paths or distribute a PDF with embedded fonts.

Gradients appear only in the simulated physical-report cover and spine. The canonical mark and standalone lockups contain no gradients.

CMYK values on the board remain reference conversions. They should not be called exact until a print condition and ICC profile are specified. The binding digital identity is the hexadecimal / RGB values.

## Final gate

```text
PRODUCTION MASTER v1.0:
APPROVED

1. Three-frame doctrine reconciled with the vector path .... CLOSED, machine-verified
2. Vertical-lockup viewBox / overshoot boundary ............ CLOSED, measured
3. Affected SVGs re-exported ............................... DONE, 8 assets + board
4. Exact mechanical audit re-run ........................... DONE, 31/31 PASS
```

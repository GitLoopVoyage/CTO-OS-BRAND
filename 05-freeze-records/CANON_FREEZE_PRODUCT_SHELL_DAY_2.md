# CTO OS Visual Canon — Product Shell Day 2 Freeze Record

**Record ID:** `CANON_FREEZE_PRODUCT_SHELL_DAY_2`
**Date:** 2026-09-09
**Supersedes:** the machine report `report-fractal-pulse.json` (2 errors / 19 warnings) — that report was Canon Lint's deliberately-preserved *failing first run* against the Fractal Pulse page, delivered as evidence that the gate could find real defects. It was never superseded by a bound passing report until now. Its ruling as controlling was correct.
**Responds to:** `PRODUCT_SHELL_DAY_2_REVIEW` — visual pass with one narrow correction; machine hold pending current rerun.

## Disposition

```text
NARROW CORRECTION (ASSURED / amber):        APPLIED
MACHINE GATE (Canon Lint) ON FROZEN TARGET: ERRORS = 0
WARNINGS:                                   7, ADJUDICATED BELOW — none contradicts a canonical invariant
PRODUCT_SHELL_DAY_2:                        PASS / FREEZE
BROAD REDESIGN:                             NOT PERFORMED
```

## Naming, for the record

The controlling machine gate is **Canon Lint** (`canon-lint.js` + `canon-vocabulary.json`). Fractal Pulse is artifact 01, the motion system. The superseded report was Canon Lint *run against* the Fractal Pulse page; the gate itself was never Fractal Pulse.

## 1. The narrow correction

Finding accepted as stated: `ASSURED` on the display-stage axis was rendered in amber via `.stage span[data-halt="hold"]`. Amber is reserved for attention states. A stage borrowing it is an axis leak — display stage wearing attention semantics.

Correction, in two parts:
- the `data-halt` attribute was removed from the stage and **the CSS rule was deleted entirely**, so the leak cannot recur by re-use. The hold that stage was trying to express already lives where it belongs — the halt banner, which names the *kind* of hold.
- the finding was encoded as a permanent check. **R11 attention-hue-leak**: any declared state outside the attention set rendered in amber or signal is an ERROR. The attention set is data, in `canon-vocabulary.json`:

```text
CONFLICTED  STALE  HOLD  HELD  BLOCKED  FAILED  REJECT  ABORT_REQUESTED
RECONCILIATION_REQUIRED  SUSPENDED  REVOKED  EXPIRED
MULTIPLE_BOUNDARIES_HOLD  NOT_PROVIDED_FAIL_CLOSED
```

R11 was proven against a reconstruction of the defective shell before the fix was accepted: it returned exactly one error, at `span "ASSURED"`, axis `pipeline-stage`. Green for ASSURED remains prohibited by the absence of any green token in the layer.

## 2. Frozen target — exact bytes

| Artifact | SHA-256 | Bytes |
|---|---|---|
| `product-shell.html` | `1e54c7fa2616c5c6441660cbb7e7652505b4ef65b4552db56f034e141f62aa94` | 46,536 |
| `canon-tokens.css` | `3d944a6352cbf0c80b6964f06a3b8271a56a8edd9cd23bf13a8d730a4dd01dab` | 6,363 |
| `fractal-pulse.html` | `d3b6f8effb4314debe6d32055c4d148206de68641e33084287253f95e0d091b4` | 49,226 |

`canon-tokens.css` is byte-identical to the reviewer's `canon-tokens-1.css` (`3d944a63…`, 6,363 bytes). The token layer the review independently verified is the token layer frozen here.

## 3. Ruleset that produced the report — exact bytes

A report is meaningful only relative to the rules that produced it, so the ruleset is bound too.

| File | SHA-256 | Bytes |
|---|---|---|
| `canon-lint.js` | `ce172f94626c169824ea9a1209022ed936c58c0500aeab54391c1d41e5966a57` | 20,691 |
| `canon-vocabulary.json` | `e18e14c3628c17be1327ac1db30b10b48f097afa9bcccd8e3c0203f36eacb632` | 3,295 |

Ruleset changes in this cycle, all narrowing or additive, none silencing:
- **R11 added** — attention-hue leak (above).
- **R10 narrowed** — an unreached stage (`data-claimed="false"`) makes no time-sensitive claim and no longer warns for a missing as-of. This is the same principle already applied to R5 and R6 in the prior cycle.
- Every report now embeds the SHA-256 and byte count of each target and of the ruleset. A report that names a filename is a narrative; a report that names bytes is evidence.

## 4. Machine report

`CANON_LINT_REPORT_PRODUCT_SHELL_DAY_2.json`
SHA-256 `0020de63d035508154272d49185bba5f0072a53b842b0350183bd31cef7a42ef` · 4,327 bytes · generated 2026-09-09T11:13:27.973Z

```text
product-shell.html    ERRORS 0   WARN 5   INFO 1
fractal-pulse.html    ERRORS 0   WARN 2   INFO 0
CANON LINT PASSED     0 errors, 7 warnings
```

Regression check: Fractal Pulse re-run under the new ruleset returns 0 errors, unchanged.

## 5. Warnings — adjudicated individually

Standard applied: warning ≠ blocker by default, but no warning may contradict a canonical invariant. The invariant every warning below is tested against is axis non-collapse (extract §0), which governs **state claims**.

| # | File | Finding | Adjudication |
|---|---|---|---|
| 1–3 | shell | R0 · `Supplied`, `Unreviewed`, `Missing` as specimen-row labels | Labels inside a declared `component-documentation` scope, each sitting beside a fully-declared specimen carrying the same value on its correct axis. Not claims. **No contradiction.** Kept visible because formal vocabulary used as prose is worth seeing. |
| 4–5 | shell | R0 · `UNKNOWN`, `SUPPORTED` in the nesting-rule prose | Doctrine text explaining the summarisation rule, inside a declared documentation scope. Not claims. **No contradiction.** |
| 6–7 | pulse | R0 · loader variants named `Hold`, `Complete` | Component names, not state claims. `HOLD` is an AER decision and a disposition; `COMPLETE` is an effect-extent. **No contradiction** — but a naming collision with formal vocabulary in a canon that forbids axis collapse. Recommended hygiene, out of scope for this cycle: rename to `Held` / `Settled`. Left visible deliberately. |

The single INFO is `ASSURED` appearing in the explanatory sentence that says a load-bearing ASSURED stage requires an evidence reference. Prohibitive context; not a claim.

## 6. Invariants carried forward

```text
SYNTHETIC DEMONSTRATION      ≠   ORGANIZATIONAL STATE
VISUAL REVIEW PASS           ≠   MACHINE GATE PASS
REPORT NAMING A FILENAME     ≠   REPORT NAMING BYTES
```

## Final gate

```text
PRODUCT_SHELL_DAY_2:   PASS / FREEZE
CONTROLLING EVIDENCE:  CANON_LINT_REPORT_PRODUCT_SHELL_DAY_2.json, bound to the hashes above
NEXT:                  Day 4 — Command Center, composed only from frozen Day 2 components
```

# CTO_OS_CHANGE_CONTROL_PIPELINE_DAY_5_CORRECTION_1 — execution record

**Program:** CTO_OS_VISUAL_CANON_V0.1 · Phase B · Artifact 04 · Day 5
**Authorisation:** `CTO_OS_CHANGE_CONTROL_PIPELINE_DAY_5_CORRECTION_1` (founder, 2026-09-10)
**Base:** `GitLoopVoyage/CTO-OS-BRAND` · `canon/day-5-change-pipeline` @ `1b15d81ba9b735eaefaf82dcbcfac5717a257c8c` — verified as HEAD before the pass
**Standing:** ONE NARROW CORRECTION PASS · NO BROAD REDESIGN · NO DAY-5 FREEZE · NO MERGE · NO IMPLEMENTATION AUTHORITY · NO DEPLOYMENT · PRODUCTION ZERO
**Status:** candidate returned for fresh review. Nothing frozen, nothing merged.

This record supersedes, in part, `REVIEW_CHANGE_PIPELINE_DAY_5.md`: its "Withdrawn label, kept record" paragraph and its §4 gate name no longer describe the candidate. That file is left as the history of the prior candidate `f927cce6…`.

---

## 1. Result

| | sha256 | bytes |
|---|---|---|
| **`change-pipeline.html` — corrected candidate** | `6a23b08a51b072ddcbb129720a892538989a148c848ffcd0e3989d14cdb3aa6e` | 36 713 |
| `CANON_LINT_REPORT_CHANGE_PIPELINE_DAY_5.json` — bound to `6a23b08a…` | `39475fda0a921d58f79a4ebfc95c2db77dad499d9509e92cad1826e17d171c7a` | — |
| `CHG_0912_CONSISTENCY_PROOF_DAY_5.json` — §3 | `8cd0ec586c379c33e9f01da933b06cd4157bc3378a79003badb731569023718c` | — |
| `chg-0912-consistency.py` — the proof tool | `b49e4de5aff78a0747a2437e121d07371520a6d18901078f27dbe30ab7e16a7e` | — |
| `CANON_LINT_GATE_DAY_5_ALL_CANON_SURFACES.json` — §4 | `f5aa0adc72ef6625ee1e2cf2ad60a7281518a4b482482e4833d486a4f3736f85` | — |

Prior candidate: `f927cce6b41fe5e4cba63ac95c0324f0fcaef58ebd573a37bcf817eee3e0c58e`. The corrected candidate is byte-distinct.

Canon Lint on `6a23b08a…`: **0 ERROR · 0 WARN · 1 INFO** (R4 on the prohibitive label "Why ASSURED cannot be claimed"), frozen ruleset `ce172f94…` / `e18e14c3…`. Five frozen Day 2 identities unchanged; `derive-shell-css.py --check` OK. Render verified headless at 1440 px.

## 2. The corrections — exactly as authorised

**D5-F1 — chg-0912 stage event timestamps.** `AUTHORIZED` data-asof `2026-09-03T09:14:22Z` → **`2026-09-02T08:31:00Z`**; `IMPLEMENTED` data-asof `2026-09-03T09:14:22Z` → **`2026-09-03T07:55:00Z`**. Both now equal the controlling Command Center strip (`fd7958c3…`, Prove panel). `REQUEST` (`2026-09-01T14:02:00Z`) and the `auth-4471` reference already agreed. My error: I had stamped two stage events with the register-read time instead of the event time — the exact as-of confusion extract §10 exists to prevent.

**D5-F2 — chg-0915 AUTHORIZED preserved as history.** The stage cell is no longer struck and no longer `data-claimed="false"`. It is a reached stage bound to its authority record and time: `data-reached="true" data-authority-ref="auth-4390" data-asof="2026-09-02T11:05:00Z"`. The current interruption is the route beside it — `authority SUSPENDED` as of `2026-09-03T08:40:00Z` — unchanged. The `data-withdrawn` attribute and its strike-through CSS rule are removed from the artifact entirely; no other element used them. Prose row retitled "Stage history" and rewritten to say that history is not rewritten to fit the present state. *Stated for review:* the prior candidate carried no timestamp for this stage because it was unclaimed; `2026-09-02T11:05:00Z` is fixture data set in this pass (after the change's request at 10:20Z, before the suspension), synthetic like everything else on the screen.

**D5-F3 — invented runtime-uncertainty exit rule removed.** chg-0898's "Colour" row no longer says the route "stays a hold route until an observation exists or the change is withdrawn by a human act". It now ends: *What would resolve the route is not stated, because present evidence does not establish it.* Present-state statements (cannot advance; truth not establishable from the evidence held; not styled as alarm) are kept.

**Documentary.** The combined gate is renamed **ALL-CANON-SURFACE GATE**; `CANON_LINT_GATE_DAY_5_ALL_ARTIFACTS.json` is removed and `CANON_LINT_GATE_DAY_5_ALL_CANON_SURFACES.json` replaces it, with the five canon surfaces under `surfaces` and `week-one.html` under `outside_product_surface_scope` — six errors preserved verbatim, explicitly without gating effect and without exemption.

Nothing else in the artifact changed. `git diff 1b15d81 -- 08-change-pipeline/change-pipeline.html` is six hunks: two timestamps, one stage cell, one prose row, one CSS line, one sentence.

## 3. Cross-artifact chg-0912 consistency — proved by extraction, not by assertion

`chg-0912-consistency.py` reads both documents' **declared attributes** (`data-axis`, `data-status`, `data-asof`, `data-authority-ref`, `data-terminal`, `data-claimed`) — never prose — locates each fact by axis, value and row context, and requires every fact to be single-valued in each document and equal across them. A stage fact must sit inside a `.stage` strip, which excludes the Command Center's per-node stage cells (node facts, not chg-0912 facts).

Run: `python3 chg-0912-consistency.py command-center.html change-pipeline.html --json CHG_0912_CONSISTENCY_PROOF_DAY_5.json`

| fact | Command Center `fd7958c3…` | Pipeline `6a23b08a…` | |
|---|---|---|---|
| stage REQUEST as-of | 2026-09-01T14:02:00Z | same | OK |
| stage AUTHORIZED as-of · ref | 2026-09-02T08:31:00Z · auth-4471 | same | OK |
| stage IMPLEMENTED as-of | 2026-09-03T07:55:00Z | same | OK |
| ASSURED / RUNTIME / CLOSED | claimed=false ×3 | same | OK |
| att-1187 attempt | BLOCKED · 2026-09-02T07:58:00Z · terminal | same | OK |
| att-1187 boundary | NOT_PROVIDED_FAIL_CLOSED | same | OK |
| att-1190 attempt | HELD · 2026-09-03T09:14:22Z | same | OK |
| dec-0295 disposition | MODIFY · 2026-09-02T08:31:00Z | same | OK |
| dec-0301 disposition | HOLD · 2026-09-03T09:14:22Z | same | OK |
| evidence effects 4–5 | MISSING · UNREVIEWED · 2026-09-03T09:14:22Z | same | OK |
| AER decision | HOLD · 2026-09-03T09:14:22Z | same | OK |
| auth-4471 authority | ACTIVE · 2026-09-03T09:14:22Z | same | OK |

**15 facts, 15 agree, exit 0.** The same tool run against the prior candidate `f927cce6…` exits 1 with exactly the two D5-F1 disagreements (AUTHORIZED, IMPLEMENTED) and nothing else — which is both the proof that the tool sees the defect and the proof that the pass changed nothing further about chg-0912. Full extraction is in the JSON, which also binds both input hashes.

## 4. ALL-CANON-SURFACE GATE

Run on a **detached** scratch checkout (main `b16d59f3` + Day 4 branch `51bfc0c` + these candidate bytes), discarded after the run — the Day 5 process error (merging on the local `main` ref) is not repeated.

| surface | sha256 | result |
|---|---|---|
| 01 `fractal-pulse.html` | `d3b6f8ef…` | PASS · 0 E · 2 W (component-documentation, as at Day 2 freeze) |
| 02 `product-shell.html` | `1e54c7fa…` | PASS · 0 E · 5 W (as at Day 2 freeze) |
| 03 `command-center.html` | `fd7958c3…` | PASS · 0 E · 0 W |
| 04 `change-pipeline.html` | `6a23b08a…` | PASS · 0 E · 0 W · 1 INFO |
| `demo.html` | `b850347c…` | PASS · 0 E · 0 W |

Outside product-surface scope, preserved visibly, no gating effect: `week-one.html` `d8a12d2e…` — **6 ERROR** (R0 ×6), untouched, awaiting the reviewer's disposition as set out in the Day 5 review §4.

## 5. Noted, not corrected — outside this pass

Two other sentences on the screen predict how a route resolves, the same class of statement as D5-F3: chg-0912's "Supplying the missing evidence lifts the evidence cause only — the human hold (dec-0301) is a separate act and lifts separately", and the legend's "It lifts only by another human act, whatever the evidence does" under Human disposition. They rest on extract §5 (a disposition is an accountable-human act) rather than on invention, but they still state a future resolution rather than present evidence. The authorisation names D5-F3 exactly, so they stand; flagged for the reviewer to include in a later cycle or leave.

## 6. Push

```
cd ~/CTO-OS-BRAND
git fetch origin
git fetch "<LOGO-2>/CTO-OS-BRAND-day5-correction1.bundle" canon/day-5-change-pipeline:canon/day-5-change-pipeline
git push origin canon/day-5-change-pipeline
```

The bundle carries one commit on top of `1b15d81`; if the branch already exists locally from the Day 5 bundle, the fetch fast-forwards it.

# Change Control Pipeline — Day 5 candidate for review

> **Superseded in part by `CORRECTION_1_CHANGE_PIPELINE_DAY_5.md` (2026-09-10).** This file records the prior candidate `f927cce6…`. The "Withdrawn label, kept record" paragraph, the chg-0912 timestamps it implies, and the §4 gate name ("every artifact") no longer describe the current candidate; the gate is now the ALL-CANON-SURFACE GATE and `week-one.html` is reported outside product-surface scope.

**Program:** CTO_OS_VISUAL_CANON_V0.1 · Phase B · Artifact 04 · Day 5
**Base:** `main` @ `b16d59f3` · **Branch:** `canon/day-5-change-pipeline`
**Standing:** candidate. NO CONSTITUTIONAL EFFECT · NO IMPLEMENTATION AUTHORITY · NO DEPLOYMENT · PRODUCTION ZERO. Nothing here is frozen; the v0.1 freeze the Day 5 plan names is the reviewer's act, not this record's.

Governing rule: *no visual may imply more authority, certainty, verification, safety, or runtime state than the underlying CTO OS model actually establishes.*

---

## 1. Identities

| file | sha256 | bytes |
|---|---|---|
| **`08-change-pipeline/change-pipeline.html` — candidate** | `f927cce6b41fe5e4cba63ac95c0324f0fcaef58ebd573a37bcf817eee3e0c58e` | 36 763 |
| `08-change-pipeline/CANON_LINT_REPORT_CHANGE_PIPELINE_DAY_5.json` — bound to `f927cce6…` | `ac6b1573a0dbf3d8a74d01c90259fbfd32eb3fb8401152111bf96afea96ad135` | — |
| `08-change-pipeline/CANON_LINT_GATE_DAY_5_ALL_ARTIFACTS.json` — §4 | `a31a2cef8092ce91f3798f6c250e8ae911a4ea9ed394c713d2d6af5a45ae2451` | — |
| `04-product-shell/product-shell.css` — derived, identical bytes to the Day 4 branch | `967e3cf903f9a3e27f4a277319a350bd511f9ca3e5b652cd43a4b4a67b6a4a6e` | 16 689 |
| `04-product-shell/derive-shell-css.py` — identical to the Day 4 branch | `f79f029d8f8f046b8f0ddeef22ef3268c6e550bd7dbed3187a74fee0382c625e` | — |

Canon Lint on `f927cce6…`: **0 ERROR · 0 WARN · 1 INFO** under the frozen ruleset `canon-lint.js` `ce172f94…` / `canon-vocabulary.json` `e18e14c3…`. The INFO is R4 on the label "Why ASSURED cannot be claimed", recognised as prohibitive prose. Non-normative distribution: 2 epistemic claims, 1 settled, 1 unsettled — reported, not ruled (extract §11.10).

Five frozen Day 2 identities unchanged on this branch (`d3b6f8ef…`, `ce172f94…`, `e18e14c3…`, `1e54c7fa…`, `3d944a63…`); `derive-shell-css.py --check` → OK.

## 2. What the artifact establishes

**The strip is six labels.** `REQUEST → AUTHORIZED → IMPLEMENTED → ASSURED → RUNTIME → CLOSED`, exactly the extract §9 list, rendered with the frozen `.stage` component. Unreached stages carry `data-claimed="false"` and make no claim. Reached load-bearing stages expose the axis beneath: every claimed `AUTHORIZED` carries `data-authority-ref`, every `ASSURED` a `data-evidence` that resolves to a node on the page, every `RUNTIME` a `data-observation` plus as-of, every `CLOSED` a `data-closure-basis`. Lint R6 measures this; it is not asserted.

**A route is not a stage.** The one new structure is the route interrupt (`.route`). It sits between stage cells, it never uses a stage token, and its `data-axis`/`data-status` are the *underlying* axis and value — `aer-decision HOLD`, `authority SUSPENDED`, `effect-certainty UNKNOWN`, `aer-decision REJECT`, `attempt BLOCKED`. Beneath each route, the cause chips list every contributing axis with its own as-of. The screen never emits an "on hold" badge, because a hold with three causes lifts three separate ways (chg-0912 shows this).

**The route takes the colour of its cause.** Amber or signal appear only when the underlying state is itself an attention state (R11 list). The runtime-uncertainty route on chg-0898 is drawn in ink: `UNKNOWN` is not an alarm (R8). This is the design decision most likely to be "corrected" by a well-meaning designer later, and the linter will catch it if it is.

**Waiting is not a hold.** chg-0903 sits at `REQUEST` with `PENDING_VALIDITY` authority and `PENDING` evidence and no route marker, because no axis records an interruption. Drawing one would manufacture state.

**Withdrawn label, kept record.** chg-0915's `AUTHORIZED` was reached and is now struck (`data-withdrawn="true"`, `data-claimed="false"`): its basis auth-4390 is `SUSPENDED`. The record and history stand; only the label's claim is withdrawn.

**Closure is a reference, not a rule.** chg-0887's `CLOSED` resolves to dec-0288 (`ACCEPT`) and the screen says the rule by which ACCEPT closes a change is the tenant's, not the model's (extract §9, §12 do-not-invent). chg-0905 shows the converse: `RUNTIME` reached, effect `COMPLETE`/`CONFIRMED`, and `CLOSED` still unclaimed.

## 3. Fixture — synthetic, coverage-chosen, consistent with Day 4

Meridian Logistics remains invented and declared at the root (`data-fixture-root="synthetic"`). Seven of twelve register entries are shown, chosen so that each route class occurs once and the demo path runs end to end; the screen says so in its footer and disclaims any distribution claim. **chg-0912 is the same record as on the Command Center** (Day 4, under review) and agrees with it value for value: att-1187 `BLOCKED` under cap-117 with `NOT_PROVIDED_FAIL_CLOSED` prior to dec-0295; dec-0295 `MODIFY`; att-1190 `HELD`, the single attempt under cap-118; evidence `MISSING`/`UNREVIEWED` for effects 4–5; dec-0301 `HOLD`; no independent assurance of record. If the Day 4 review changes any of those values, this artifact changes with it — noted as a dependency, not hidden.

New fixture identifiers introduced here (all synthetic): chg-0887/0898/0903/0905/0915/0921, auth-4388/4402, att-1175, aer-2290, asr-0199/0207, obs-3290/3311, dec-0288. None introduces vocabulary; all values are from the extract.

## 4. Day 5 afternoon gate — every artifact, one ruleset

Run in a scratch merge of `main` + the Day 4 branch + this branch (merge commit `b924caa`, discarded, never a candidate), so the demo path is measured as one tree. Combined report: `CANON_LINT_GATE_DAY_5_ALL_ARTIFACTS.json` (`a31a2cef…`).

| artifact | sha256 | result |
|---|---|---|
| 01 `fractal-pulse.html` | `d3b6f8ef…` | PASS · 0 E · 2 W (R0, declared component-documentation — as at Day 2 freeze) |
| 02 `product-shell.html` | `1e54c7fa…` | PASS · 0 E · 5 W (R0 ×5 component-documentation, R4 INFO — as at Day 2 freeze) |
| 03 `command-center.html` | `fd7958c3…` | PASS · 0 E · 0 W |
| 04 `change-pipeline.html` | `f927cce6…` | PASS · 0 E · 0 W · 1 INFO |
| `demo.html` (pulse) | `b850347c…` | PASS · 0 E · 0 W |
| `week-one.html` (Day 0 plan) | `d8a12d2e…` | **FAIL · 6 E** — see below |

**`week-one.html` fails and is reported without exemption.** It is the programme plan, not a product surface, and was never claimed as a lint target; the six errors are R0 heuristics reading doctrine prose (`UNKNOWN`, `Hold`, `Complete` as component names) and the artifact table's phase column ("Evidence Graph — signature visual" → "C · System") as state claims. Two possible dispositions, for the reviewer: (a) declare plan documents outside the gate and record that scope; (b) authorise a narrow cycle to scope the doctrine sections as component documentation, which downgrades four findings and leaves two that only a markup reorder or a ruleset change would clear. I did not touch the plan on Day 5; it is a Day 0 artifact and the ruleset is frozen.

## 5. My own errors, named

- First draft rendered "HUMAN HUMAN HOLD": the cause-chip key "human" duplicated the `.disp` component's own "HUMAN " prefix. Fixed to "decision". Caught by looking at the render, not by lint — lint has no rule for redundancy, and should not.
- The first legend markup put the axis line directly after the title, which R0(b) reads as label→value ("Authority hold" → "authority · aer-decision"). I reordered the cell (title, description, axis) rather than exempting it. That is a real narrowing of what the heuristic sees, not a workaround: the axis line now follows prose, where no reader takes it as a state claim.
- A header label read simply "Closed", which is the formal `CLOSED` token with no axis (R0a). Renamed "Closed with basis" — which is also the more honest label.

- The gate worktree was checked out on `main` and I merged both branches into it, which moved the *local* `main` ref to the scratch merge commit. Nothing was pushed, but the first manifest delta and the first bundle were computed against the moved ref and were wrong. I reset local `main` to `b16d59f3`, regenerated the delta, amended the commit and rebuilt the bundle; the hashes in §1 and the delivered bundle are from the corrected state. A scratch merge belongs on a detached HEAD, not on `main`.

## 6. Not done, by design

- No freeze. The plan's "fix, freeze" step is the reviewer's ruling on this record plus Day 4's.
- No merge to `main`. Both branches sit on `b16d59f3`; they merge cleanly (proved by the gate tree).
- No compact-density or light-surface screenshots — the shell's own freeze covers those modes; this artifact adds no mode-specific rules.
- Shell erratum (svc-pricing `14 d` as-of in attention hue) still carried for the shell cycle.

## 7. Push

```
cd ~/CTO-OS-BRAND
git fetch origin main
git fetch "<LOGO-2>/CTO-OS-BRAND-day5.bundle" canon/day-5-change-pipeline:canon/day-5-change-pipeline
git push origin canon/day-5-change-pipeline
```

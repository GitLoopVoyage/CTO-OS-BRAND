# Command Center — Day 4 Review Package

**Record ID:** `CANON_REVIEW_COMMAND_CENTER_DAY_4`
**Status:** CANDIDATE — submitted for independent review. Not frozen.
**Origin:** Founder proposition (design canvas `command-center.dc.html`), corrected in one narrow cycle.
**Composition:** frozen Day-2 shell components only. No new vocabulary. Rail Art. 21.2 · panels Art. 35.2 · governing question Art. 21.3 · nesting rule Art. 33.1 · vocabularies Model Extract v0.1.

## Machine gate

```text
target   07-command-center/command-center.html
sha256   ebdd44f73b269ddda5be3090ea80fe025c99d721a6aad5a7372f64739151af95
bytes    21,977
ERRORS   0     WARNINGS   0     INFO   0
```

Linted **in the repository tree**, with the page linking the frozen shell files by relative path — not inlined copies. The report is bound to the ruleset that produced it:

```text
canon-lint.js          ce172f94626c169824ea9a1209022ed936c58c0500aeab54391c1d41e5966a57
canon-vocabulary.json  e18e14c3628c17be1327ac1db30b10b48f097afa9bcccd8e3c0203f36eacb632
```

## Corrections applied to the proposition (six, one class plus one)

Canon Lint returned four R0 errors on the proposition as submitted: row labels `Pending`, `Suspended`, `Supplied`, `Missing` are formal state words used as prose. On the Day-2 gallery this class was scoped as component documentation; on a product surface that scope does not apply, and the gate was right not to downgrade it.

Rule adopted: **on a product surface the label names the subject; the chip names the state.**

| Was | Now |
|---|---|
| `Pending` (authority row) | `Window 09-04` |
| `Suspended` (authority row) | `svc-inventory` |
| `Supplied` (evidence row) | `Effects 1–3` |
| `Missing` (evidence row) | `Effects 4–5` |
| `Adverse` (evidence row, not a formal value, same rule) | `svc-inventory` |
| `14 d` as-of cell in amber | neutral — a non-claim cell may not carry an attention hue; the STALE chip beside it already does |

## Errata this composition surfaced in the frozen set

1. **`product-shell.css` did not exist.** The shell's CSS lived only inside `product-shell.html`. Compositions need to link it. Extracted verbatim from the frozen page and shipped at `04-product-shell/product-shell.css` (`7153d783b5180c1b…`). `product-shell.html` bytes unchanged.
2. **`fractal-pulse.js` could not be inlined.** Its doc comment contained a literal `</script>`, which terminates any `<script>` element it is inlined into and dumps the remainder of the file as page text. One character changed in the comment (`<\/script>`); behaviour identical. `3315ca6ebe0fd03b…`
3. **Frozen `product-shell.html` carries the same amber as-of cell** corrected above (state table, `svc-pricing` row). Not reopened — recorded here for the Day-4 freeze as shell errata.

## Open for reviewer disposition — not resolved by the author

1. **`att-1187`: `AttemptState = BLOCKED` on boundary outcome `MULTIPLE_BOUNDARIES_HOLD`.** Extract §4: only `ALLOW` proceeds to `BEGIN_ATTEMPT`; a hold-class boundary outcome suggests `HELD` rather than `BLOCKED`. The legal transition is defined in `GF_R2_CORE_FORMAL_SPECIFICATION_V0.2`, not in the extract. **Model question. Needs the spec.**
2. **Command-bar copy under a decorative loop:** *"Reconstructing technical state for svc-routing…"* Fractal Pulse doctrine: generic copy is honest; specific copy is a claim and needs a source. Either bind to a fixture event or reduce to *"Working…"*.
3. **RISK is a stated omission.** Seven of the eight Command Center questions are on screen. No canonical risk vocabulary exists in the extract; Art. 32 is illustrative. Omitted under do-not-invent. Should the omission be visible on the surface, or is this record sufficient?

## Not on this screen, by design

Nothing invented. No green token. No stage asserted beyond `IMPLEMENTED`. Scope summary renders the panel's **weakest child** (`UNVERIFIABLE`), not its mode or average.

## Fixture

Meridian Logistics — synthetic, declared at `data-fixture-root="synthetic"`; every fixture node inside it. The fixture determines its own distribution: 6 epistemic claims, 1 settled, 5 unsettled. Reported, not enforced.

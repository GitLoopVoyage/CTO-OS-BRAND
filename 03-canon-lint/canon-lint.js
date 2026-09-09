#!/usr/bin/env node
/*!
 * CANON LINT  --  CTO_OS_VISUAL_CANON_V0.1
 *
 * Enforces, mechanically, the canon rule:
 *   No visual may imply more authority, certainty, verification, safety or
 *   runtime state than the underlying CTO OS model actually establishes.
 *
 * Rules implemented are those required by
 *   CTO_OS_VISUAL_CANON_MODEL_EXTRACT_V0.1_20260903.md, section 11,
 * plus the axis-collapse prohibition of section 0 and the as-of rule of
 * section 10. State vocabularies live in canon-vocabulary.json and are read
 * at run time -- they are not hardcoded here.
 *
 * The page is loaded in a real browser and checked against COMPUTED styles,
 * not source classes, so "visually distinct" and "not styled as an error"
 * are measured rather than asserted.
 *
 *   node canon-lint.js <file.html> [more.html ...] [--json report.json]
 *
 * Exit 0 = no ERRORs.  Exit 1 = at least one ERROR.  WARN never fails a build.
 *
 * Deliberately NOT implemented: any rule about the distribution of green vs
 * not-green. Extract section 11 rule 10 -- the fixture truth determines the
 * distribution. Distribution is reported as information only, marked
 * non-normative, and can never fail a build.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const crypto = require("crypto");
const sha = p => crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");

const VOCAB = JSON.parse(fs.readFileSync(path.join(__dirname, "canon-vocabulary.json"), "utf8"));

/* ------------------------------------------------------------------ *
 * The check suite. Runs inside the page.                              *
 * ------------------------------------------------------------------ */
function checkSuite(V) {
  const out = [];
  const seen = new WeakSet();
  const add = (rule, sev, msg, el, detail) => {
    out.push({
      rule, sev, msg,
      where: el ? describe(el) : "document",
      detail: detail || null
    });
  };
  function describe(el) {
    if (!el || !el.tagName) return "document";
    let s = el.tagName.toLowerCase();
    if (el.id) s += "#" + el.id;
    const c = (el.getAttribute("class") || "").trim().split(/\s+/).filter(Boolean).slice(0, 3);
    if (c.length) s += "." + c.join(".");
    const t = (el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 46);
    if (t) s += ' "' + t + '"';
    return s;
  }
  const norm = s => (s || "").trim().toUpperCase().replace(/[\s-]+/g, "_");
  const rgb = s => {
    const m = /rgba?\(([^)]+)\)/.exec(s || "");
    if (!m) return null;
    const p = m[1].split(",").map(x => parseFloat(x));
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const dist = (a, b) => a && b ? Math.sqrt((a.r-b.r)**2 + (a.g-b.g)**2 + (a.b-b.b)**2) : Infinity;
  const hexToRgb = h => ({ r: parseInt(h.slice(1,3),16), g: parseInt(h.slice(3,5),16), b: parseInt(h.slice(5,7),16), a:1 });

  const COBALT = hexToRgb(V.colors.cobalt);
  const SIGNAL = hexToRgb(V.colors.signal);
  const AMBERS = ["amber","amberLight","amberDark"].map(k => hexToRgb(V.colors[k]));
  const nearAttention = c => dist(c, SIGNAL) < 40 || AMBERS.some(a => dist(c, a) < 40);

  /* ---- collect every element making a state claim ---- */
  const claims = [...document.querySelectorAll("[data-status],[data-axis]")];

  /* R9 -- fixture must be declared synthetic at the root ------------- */
  const usesFixture = document.querySelector("[data-fixture-ref],[data-fixture-id]") ||
                      document.documentElement.hasAttribute("data-fixture");
  if (usesFixture) {
    const rootEl = document.querySelector("[data-fixture-root]");
    const root = document.documentElement.getAttribute("data-fixture") ||
                 document.body.getAttribute("data-fixture") ||
                 (rootEl && rootEl.getAttribute("data-fixture-root"));
    const covered = !rootEl || [...document.querySelectorAll("[data-fixture-ref],[data-fixture-id]")]
                                 .every(e => rootEl.contains(e));
    if (norm(root) !== "SYNTHETIC" || !covered) {
      add("R9-fixture-synthetic", "ERROR",
        'Page uses fixture data but the root does not declare data-fixture="synthetic".',
        null, "extract 11.9");
    }
  }

  /* ---- per-claim checks ---- */
  for (const el of claims) {
    const axis = (el.getAttribute("data-axis") || "").trim();
    const raw = el.getAttribute("data-status");
    const val = norm(raw);

    /* R1 -- every status claim declares a semantic axis -------------- */
    if (!axis) {
      add("R1-axis-declared", "ERROR",
        "State claim carries no data-axis. Every claim must declare which semantic axis it speaks on.",
        el, "allowed: " + V.axes.join(" | "));
      continue;
    }
    if (!V.axes.includes(axis)) {
      add("R1-axis-declared", "ERROR",
        'Unknown semantic axis "' + axis + '".', el, "allowed: " + V.axes.join(" | "));
      continue;
    }

    /* R2 / R3 -- value must be exact vocabulary for that axis --------- */
    const allowed = V.vocabulary[axis] || [];
    if (raw === null) {
      add("R3-exact-vocabulary", "ERROR",
        'Element declares axis "' + axis + '" but carries no data-status value.', el);
    } else if (!allowed.includes(val)) {
      const other = Object.keys(V.vocabulary).filter(a => a !== axis && V.vocabulary[a].includes(val));
      add(axis === "epistemic" ? "R2-epistemic-vocabulary" : "R3-exact-vocabulary", "ERROR",
        '"' + raw + '" is not a legal value on axis "' + axis + '".',
        el,
        other.length
          ? "AXIS COLLAPSE: that value belongs to axis " + other.join("/") + ". Extract section 0 forbids substituting one axis for another."
          : "allowed: " + allowed.join(", "));
    }

    /* R6 -- pipeline stage may not masquerade as a formal state ------- */
    if (axis === "pipeline-stage") {
      const formal = ["data-authority","data-attempt","data-effect","data-disposition"]
        .filter(a => el.hasAttribute(a));
      if (el.hasAttribute("data-formal-state")) {
        add("R6-no-stage-masquerade", "ERROR",
          "Pipeline display stage carries data-formal-state. Stages are product labels, not formal states.",
          el, "extract section 9");
      }
      /* stage assertions that are load-bearing must expose the axis beneath */
      const needsUnder = { AUTHORIZED: "data-authority-ref", ASSURED: "data-evidence",
                           RUNTIME: "data-observation", CLOSED: "data-closure-basis" };
      const need = needsUnder[val];
      const claimed = el.getAttribute("data-claimed") !== "false";
      if (need && claimed && !el.hasAttribute(need)) {
        add("R6-stage-resolves", "ERROR",
          'Pipeline stage "' + val + '" is load-bearing but does not expose ' + need + ".",
          el, "extract section 9: AUTHORIZED resolves to an AuthorityRecord; ASSURED needs an explicit assurance reference; RUNTIME needs an exact observation plus as_of; CLOSED needs a defined closure basis.");
      }
      if (formal.length) {
        add("R6-no-stage-masquerade", "WARN",
          "Pipeline stage also carries formal-axis attributes: " + formal.join(", ") +
          ". Legal, but the UI must keep them visibly separate.", el);
      }
    }

    /* R5 -- runtime claims need as-of and an observation reference ---- */
    if ((val === "RUNTIME" || axis === "effect-extent" || axis === "effect-certainty")
        && el.getAttribute("data-claimed") !== "false") {
      if (!el.hasAttribute("data-asof")) {
        add("R5-runtime-asof", "ERROR",
          "Runtime / execution-effect claim carries no data-asof.", el, "extract section 10");
      }
      if (val === "RUNTIME" && !el.hasAttribute("data-observation")) {
        add("R5-runtime-asof", "ERROR",
          "RUNTIME claim carries no data-observation reference.", el, "extract section 9");
      }
    }

    /* as-of on every time-sensitive axis ----------------------------- */
    if (V.timeSensitiveAxes.includes(axis) && !el.hasAttribute("data-asof")
        && el.getAttribute("data-claimed") !== "false") {   // an unreached stage makes no time-sensitive claim
      add("R10-asof", "WARN",
        'Claim on time-sensitive axis "' + axis + '" carries no data-asof.', el,
        "extract section 10: CURRENT CLAIM + AS-OF + EPISTEMIC STATE + SOURCE/EVIDENCE REF WHERE MATERIAL");
    }

    /* R8 -- uncertainty is not an error ------------------------------ */
    if (axis === "epistemic" && V.nonErrorEpistemic.includes(val)) {
      const cs = getComputedStyle(el);
      const c = rgb(cs.color), bc = rgb(cs.borderTopColor);
      if (dist(c, SIGNAL) < 40 || (cs.borderTopWidth !== "0px" && dist(bc, SIGNAL) < 40)) {
        add("R8-uncertainty-not-error", "ERROR",
          '"' + val + '" is styled with the signal/error colour. Uncertainty is a legitimate state, not a failure.',
          el, "computed colour " + cs.color);
      }
    }

    /* R11 -- attention hue only on attention-bearing states ------------ */
    if (raw !== null && !V.attentionStates.includes(val)) {
      const cs = getComputedStyle(el);
      const c = rgb(cs.color), bc = rgb(cs.borderTopColor);
      if (nearAttention(c) || (cs.borderTopWidth !== "0px" && nearAttention(bc))) {
        add("R11-attention-hue-leak", "ERROR",
          '"' + val + '" on axis "' + axis + '" is rendered in an attention hue, but it is not an attention state.',
          el, "amber/signal are reserved for: " + V.attentionStates.join(", ") + ". A stage or settled value borrowing them is an axis leak.");
      }
    }

    /* R7 -- authority treatment distinct from capability/access ------- */
    if (axis === "authority") el.setAttribute("data-lint-auth", "1");
    seen.add(el);
  }

  /* R0 -- UNDECLARED state claims -----------------------------------
   * The rules above only see claims that declared themselves. A claim made
   * in plain text with no attributes escapes every one of them, which is the
   * easier mistake to make and the more dangerous one. Detect label:value
   * pairs that read as system state and carry no axis.                     */
  const AXIS_LABELS = /^(authority|authorisation|authorization|assurance|evidence|runtime|attempt|disposition|state|state graph|execution|effect|closure|status|posture|health)\b/i;
  const ALL_VALUES = new Set(Object.values(V.vocabulary).flat());
  const NEAR = {}; // loose forms that read as a formal value but are not one
  for (const v of ALL_VALUES) {
    NEAR[v.replace(/_/g, " ")] = v;
    NEAR[v.split("_")[0]] = v;             // "PENDING" -> PENDING_VALIDITY etc.
  }
  const leaves = [...document.querySelectorAll("body *")].filter(e => e.children.length === 0);
  for (const el of leaves) {
    if (el.closest("[data-axis]") || el.closest("[data-lint-ignore]")) continue;
    if (el.closest("pre,code,kbd,samp")) continue;   // code samples are not surfaces
    const txt = (el.textContent || "").trim();
    if (!txt || txt.length > 40) continue;
    const key = norm(txt);

    // (a) the element's own text IS a formal state value
    if (ALL_VALUES.has(key)) {
      const axesWith = Object.keys(V.vocabulary).filter(a => V.vocabulary[a].includes(key));
      const docScope = el.closest('[data-lint-scope="component-documentation"]');
      add("R0-undeclared-claim", docScope ? "WARN" : "ERROR",
        'Renders the formal state value "' + txt + '" with no data-axis.', el,
        "value exists on axis: " + axesWith.join("/") +
        (docScope
          ? ". Downgraded: inside a declared component-documentation scope, so this is a component name, not a state claim. The collision with formal vocabulary is still worth knowing about."
          : ". Extract section 0: the UI may summarise axes but may not substitute one for another, and a value with no axis is unreadable as either."));
      continue;
    }

    // (b) previous sibling is an axis label, so this element is its value
    const prev = el.previousElementSibling;
    const prevIsHeading = prev && (/^H[1-6]$/.test(prev.tagName) || prev.tagName === "TH");
    if (el.tagName === "TH") continue;
    if (prev && !prevIsHeading && prev.children.length === 0 &&
        AXIS_LABELS.test((prev.textContent || "").trim())) {
      const label = (prev.textContent || "").trim();
      const near = NEAR[key] || NEAR[key.replace(/_/g, " ")];
      add("R0-undeclared-claim", "ERROR",
        'Reads as a state claim ("' + label + '" -> "' + txt + '") but declares no data-axis, no data-status and no data-asof.',
        el,
        near
          ? 'AXIS COLLAPSE RISK: "' + txt + '" resembles the formal value ' + near + ' but is not it. Loose forms of formal state names are the exact failure the extract prohibits.'
          : "extract section 10: CURRENT CLAIM + AS-OF + EPISTEMIC STATE + SOURCE/EVIDENCE REF WHERE MATERIAL");
    }
  }

  /* R4 -- assurance claims need a resolvable evidence reference ------ */
  const textNodes = [...document.querySelectorAll("body *")].filter(e => e.children.length === 0);
  for (const el of textNodes) {
    const t = norm(el.textContent);
    for (const claim of V.assuranceClaims) {
      if (new RegExp("(^|_)" + claim + "($|_)").test(t)) {
        if (el.getAttribute("data-claimed") === "false" ||
            el.closest('[data-claimed="false"]')) continue;   // stage exists, is not asserted
        const ctx = norm((el.closest("p,li,td,div") || el).textContent).slice(0, 400);
        const explanatory = /(MUST|REQUIRE|REQUIRES|NEVER|CANNOT|MAY_NOT|NOT_BE|FORBID|SOLELY_BECAUSE|EXPOSE)/.test(ctx);
        const holder = el.closest("[data-evidence]");
        if (!holder) {
          add("R4-assurance-needs-evidence", explanatory ? "INFO" : "ERROR",
            'Renders "' + claim + '" with no data-evidence reference in scope.' +
            (explanatory ? " (appears in an explanatory or prohibitive sentence)" : ""), el,
            "extract section 6: never render ASSURED / VERIFIED / PROVEN solely because evidence is SUPPLIED or REVIEWED");
        } else {
          const ref = holder.getAttribute("data-evidence");
          if (!document.getElementById(ref) && !document.querySelector('[data-evidence-id="' + ref + '"]')) {
            add("R4-assurance-needs-evidence", "ERROR",
              'Evidence reference "' + ref + '" does not resolve to any evidence node.', el);
          }
        }
      }
    }
  }

  /* R7 -- measured, not asserted: authority vs capability treatments -- */
  const auths = [...document.querySelectorAll('[data-axis="authority"]')];
  const caps = [...document.querySelectorAll("[data-capability],[data-access]")];
  if (auths.length && caps.length) {
    const sig = el => {
      const cs = getComputedStyle(el);
      return [cs.color, cs.backgroundColor, cs.borderTopColor, cs.borderTopStyle, cs.borderRadius].join("|");
    };
    const aSet = new Set(auths.map(sig));
    for (const c of caps) {
      if (aSet.has(sig(c))) {
        add("R7-authority-not-access", "ERROR",
          "A capability/access element renders with a treatment identical to an authority element. Permission and credential access may not share a visual token.",
          c, "extract section 2");
      }
    }
  }

  /* forbidden absolutes ---------------------------------------------- */
  const bodyText = (document.body.innerText || "").toLowerCase();
  for (const phrase of V.forbiddenAbsolutes) {
    let i = bodyText.indexOf(phrase);
    while (i !== -1) {
      const around = bodyText.slice(Math.max(0, i - 90), i + phrase.length + 90);
      const excused = /do not|never|must not|forbidden|cannot|prohibited|fails|failure|instead of|rather than|"|”/.test(around);
      add("R-absolutes", excused ? "INFO" : "ERROR",
        'Absolute claim "' + phrase + '"' + (excused ? " (appears in a prohibitive or quoted context)" : ""),
        null, "..." + around.replace(/\s+/g, " ").trim() + "...");
      i = bodyText.indexOf(phrase, i + 1);
    }
  }

  /* colour discipline: cobalt only in declared roles ------------------ */
  for (const el of document.querySelectorAll("body *")) {
    if (el.children.length) continue;
    const cs = getComputedStyle(el);
    for (const [prop, v] of [["color", cs.color], ["background-color", cs.backgroundColor], ["fill", cs.fill]]) {
      const c = rgb(v);
      if (c && c.a > 0.5 && dist(c, COBALT) < 26) {
        const role = el.getAttribute("data-role") || (el.closest("[data-role]") || {}).getAttribute?.("data-role");
        if (!role || !V.cobaltRoles.includes(role)) {
          add("R-colour-discipline", "WARN",
            "Cobalt used on " + prop + " outside a declared cobalt role.", el,
            "declared roles: " + V.cobaltRoles.join(", "));
        }
      }
    }
  }

  /* ---- NON-NORMATIVE observation. Never an ERROR. Extract 11.10. ---- */
  const epi = [...document.querySelectorAll('[data-axis="epistemic"]')]
    .map(e => norm(e.getAttribute("data-status")));
  const settled = epi.filter(v => v === "KNOWN" || v === "SUPPORTED").length;
  const distribution = epi.length
    ? { total: epi.length, settled, unsettled: epi.length - settled }
    : null;

  return { findings: out, distribution };
}

/* ------------------------------------------------------------------ *
 * Runner                                                              *
 * ------------------------------------------------------------------ */
(async () => {
  const args = process.argv.slice(2);
  const jsonAt = args.indexOf("--json");
  const jsonOut = jsonAt > -1 ? args[jsonAt + 1] : null;
  const files = args.filter((a, i) => !a.startsWith("--") && !(jsonAt > -1 && i === jsonAt + 1));
  if (!files.length) {
    console.error("usage: node canon-lint.js <file.html> [...] [--json report.json]");
    process.exit(2);
  }

  const browser = await chromium.launch();
  const report = {
    tool: "canon-lint",
    generated: new Date().toISOString(),
    ruleset: {
      "canon-lint.js":        { sha256: sha(__filename), bytes: fs.statSync(__filename).size },
      "canon-vocabulary.json":{ sha256: sha(path.join(__dirname, "canon-vocabulary.json")),
                                bytes: fs.statSync(path.join(__dirname, "canon-vocabulary.json")).size,
                                source: VOCAB._source }
    },
    files: []
  };
  let errors = 0, warns = 0;

  for (const f of files) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    await page.goto("file://" + path.resolve(f));
    await page.waitForTimeout(500);
    const res = await page.evaluate(checkSuite, VOCAB);
    await page.close();

    const e = res.findings.filter(x => x.sev === "ERROR");
    const w = res.findings.filter(x => x.sev === "WARN");
    const i = res.findings.filter(x => x.sev === "INFO");
    errors += e.length; warns += w.length;
    report.files.push({ file: path.basename(f), sha256: sha(f), bytes: fs.statSync(f).size,
                        errors: e.length, warns: w.length, findings: res.findings, distribution: res.distribution });

    console.log("\n\x1b[1m" + path.basename(f) + "\x1b[0m   sha256 " + sha(f).slice(0,16) + "\u2026  " + fs.statSync(f).size + " bytes");
    console.log("  " + e.length + " ERROR   " + w.length + " WARN   " + i.length + " INFO");
    const groups = {};
    for (const x of res.findings) (groups[x.rule] = groups[x.rule] || []).push(x);
    for (const rule of Object.keys(groups)) {
      const g = groups[rule];
      const sev = g[0].sev;
      const tag = sev === "ERROR" ? "\x1b[31mERROR\x1b[0m" : sev === "WARN" ? "\x1b[33mWARN \x1b[0m" : "\x1b[90mINFO \x1b[0m";
      console.log("\n  " + tag + "  " + rule + "  (" + g.length + ")");
      for (const x of g.slice(0, 4)) {
        console.log("    - " + x.msg);
        console.log("      at " + x.where);
        if (x.detail) console.log("      " + x.detail.slice(0, 150));
      }
      if (g.length > 4) console.log("    ... " + (g.length - 4) + " more");
    }
    if (res.distribution) {
      console.log("\n  \x1b[90mNON-NORMATIVE  epistemic claims: " + res.distribution.total +
        " (" + res.distribution.settled + " settled, " + res.distribution.unsettled +
        " unsettled). Reported only. No distribution rule exists and none may be added — extract 11.10.\x1b[0m");
    }
  }

  await browser.close();
  if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(report, null, 1));
  console.log("\n" + "-".repeat(62));
  console.log(errors ? "\x1b[31mCANON LINT FAILED\x1b[0m  " + errors + " error(s), " + warns + " warning(s)"
                     : "\x1b[32mCANON LINT PASSED\x1b[0m  0 errors, " + warns + " warning(s)");
  process.exit(errors ? 1 : 0);
})();

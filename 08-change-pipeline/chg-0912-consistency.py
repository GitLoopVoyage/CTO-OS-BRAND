#!/usr/bin/env python3
"""
Cross-artifact consistency proof for fixture record chg-0912.

The Command Center (Day 4) is the controlling fixture. The Change Pipeline
(Day 5) renders the same record. This tool extracts every shared fact from
BOTH documents by reading declared attributes (data-axis / data-status /
data-asof / refs) - never prose - and reports agreement fact by fact.

  python3 chg-0912-consistency.py <command-center.html> <change-pipeline.html> [--json out.json]

Exit 0 iff every fact is found exactly once-valued in each document and the
values agree. A fact found with two different values inside one document is a
failure of that document, reported as such. Standard library + beautifulsoup4.
"""
import hashlib, json, re, sys
from bs4 import BeautifulSoup

# Each fact: locator = (axis, status, id that must appear in the element's row
# context) ; fields = attributes compared. Row context = nearest ancestor that
# is a .specrow, .route, .halt, .chip, <tr>, or the .pipe/.panel container.
FACTS = [
  ("stage REQUEST (chg-0912)",      "pipeline-stage", "REQUEST",     "chg-0912", ["data-asof"]),
  ("stage AUTHORIZED (chg-0912)",   "pipeline-stage", "AUTHORIZED",  "chg-0912", ["data-asof", "data-authority-ref"]),
  ("stage IMPLEMENTED (chg-0912)",  "pipeline-stage", "IMPLEMENTED", "chg-0912", ["data-asof"]),
  ("stage ASSURED not claimed",     "pipeline-stage", "ASSURED",     "chg-0912", ["data-claimed"]),
  ("stage RUNTIME not claimed",     "pipeline-stage", "RUNTIME",     "chg-0912", ["data-claimed"]),
  ("stage CLOSED not claimed",      "pipeline-stage", "CLOSED",      "chg-0912", ["data-claimed"]),
  ("att-1187 attempt",              "attempt",        "BLOCKED",     "att-1187", ["data-asof", "data-terminal"]),
  ("att-1187 boundary",             "boundary",       "NOT_PROVIDED_FAIL_CLOSED", "att-1187", []),   # presence + value only; boundary carries no as-of
  ("att-1190 attempt",              "attempt",        "HELD",        "att-1190", ["data-asof"]),
  ("dec-0295 disposition",          "disposition",    "MODIFY",      "dec-0295", ["data-asof"]),
  ("dec-0301 disposition",          "disposition",    "HOLD",        "dec-0301", ["data-asof"]),
  ("evidence effects 4-5 presence", "evidence-presence", "MISSING",  "4",        ["data-asof"]),
  ("evidence effects 4-5 review",   "evidence-review",   "UNREVIEWED","4",       ["data-asof"]),
  ("AER decision on chg-0912",      "aer-decision",   "HOLD",        "",         ["data-asof"]),
  ("auth-4471 authority",           "authority",      "ACTIVE",      "auth-4471", ["data-asof"]),
]
CONTAINERS = {"specrow", "route", "halt", "chip", "pipe", "panel"}

def context_text(el):
    for anc in el.parents:
        if anc.name == "tr" or (anc.get("class") and CONTAINERS & set(anc.get("class"))):
            return anc.get_text(" ", strip=True)
    return el.get_text(" ", strip=True)

def extract(path):
    raw = open(path, "rb").read()
    soup = BeautifulSoup(raw.decode("utf-8"), "html.parser")
    out = {}
    for name, axis, status, needle, fields in FACTS:
        hits = []
        for el in soup.select(f'[data-axis="{axis}"][data-status="{status}"]'):
            ctx = context_text(el)
            if needle == "4":
                ok = re.search(r"[Ee]ffects 4", ctx) is not None
            elif needle == "chg-0912":
                # A change's stage strip is a .stage container. Per-node stage
                # cells in the technical-state table are node facts, not chg-0912
                # facts, and are excluded by that requirement. Pipeline: the strip
                # must sit inside the chg-0912 card; command center: the screen is
                # scoped to chg-0912 and its one strip is that change's.
                strip = el.find_parent(class_="stage")
                card = el.find_parent(class_="pipe")
                in_card = ("chg-0912" in card.get_text()) if card is not None else ("chg-0912" in soup.get_text())
                ok = strip is not None and in_card
            elif needle == "":
                ok = True
            else:
                ok = needle in ctx
            if ok:
                vals = {f: el.get(f) for f in fields}
                if el.get("data-claimed") == "false" and "data-claimed" not in fields:
                    continue  # an unreached copy of a stage token makes no claim
                hits.append(vals)
        distinct = {json.dumps(v, sort_keys=True) for v in hits}
        out[name] = {"found": len(hits), "values": [json.loads(d) for d in sorted(distinct)]}
    return hashlib.sha256(raw).hexdigest(), len(raw), out

def main():
    argv = sys.argv[1:]
    jpath = None
    if "--json" in argv:
        i = argv.index("--json"); jpath = argv[i + 1]; del argv[i:i + 2]
    cc_path, cp_path = argv
    cc_hash, cc_bytes, cc = extract(cc_path)
    cp_hash, cp_bytes, cp = extract(cp_path)
    rows, ok_all = [], True
    for name, *_ in FACTS:
        a, b = cc[name], cp[name]
        single_a = len(a["values"]) == 1 and a["found"] >= 1
        single_b = len(b["values"]) == 1 and b["found"] >= 1
        agree = single_a and single_b and a["values"][0] == b["values"][0]
        ok_all &= agree
        rows.append({"fact": name, "command_center": a, "change_pipeline": b, "agree": agree})
        flag = "OK " if agree else "XX "
        print(f"{flag}{name:34s} CC={a['values'] if single_a else ('AMBIGUOUS', a)}  CP={b['values'] if single_b else ('AMBIGUOUS', b)}")
    report = {"tool": "chg-0912-consistency", "controlling": {"file": cc_path, "sha256": cc_hash, "bytes": cc_bytes},
              "candidate": {"file": cp_path, "sha256": cp_hash, "bytes": cp_bytes},
              "facts": rows, "all_agree": ok_all}
    if jpath:
        open(jpath, "w").write(json.dumps(report, indent=1))
    print("\nALL FACTS AGREE" if ok_all else "\nDISAGREEMENT - see rows marked XX")
    return 0 if ok_all else 1

if __name__ == "__main__":
    sys.exit(main())

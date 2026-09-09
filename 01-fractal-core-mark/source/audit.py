# -*- coding: utf-8 -*-
"""Exact mechanical audit — CTO_OS_FRACTAL_CORE_VECTOR_QA_2 (re-run of QA_1)."""
import re, json, glob, sys
import numpy as np
import geom2 as geom

R = []
def check(name, ok, evidence):
    R.append((name, "PASS" if ok else "FAIL", evidence))
    return ok

# ---------------------------------------------------------------- grid model
K = 2                                   # half-X resolution
N = int(10 * K)
def cells(rects):
    g = np.zeros((N, N), dtype=int)
    for (x, y, w, h) in rects:
        g[int(round(y*K)):int(round((y+h)*K)), int(round(x*K)):int(round((x+w)*K))] = 1
    return g

def components(g):
    lab = np.zeros_like(g); cur = 0; out = []
    for i in range(N):
        for j in range(N):
            if g[i, j] and not lab[i, j]:
                cur += 1; stack = [(i, j)]; comp = []
                while stack:
                    a, b = stack.pop()
                    if a < 0 or b < 0 or a >= N or b >= N: continue
                    if not g[a, b] or lab[a, b]: continue
                    lab[a, b] = cur; comp.append((a, b))
                    stack += [(a+1,b),(a-1,b),(a,b+1),(a,b-1)]
                out.append(comp)
    return out

frames = geom.master_frames()
G = cells(frames)
comps = components(G)
check("Three distinct structural frames (4-connected components)",
      len(comps) == 3, "%d components found" % len(comps))

# --- per-frame ring analysis
info = []
for comp in sorted(comps, key=lambda c: -(max(b for a,b in c) - min(b for a,b in c))):
    ys = [a for a,b in comp]; xs = [b for a,b in comp]
    y0,y1,x0,x1 = min(ys), max(ys)+1, min(xs), max(xs)+1
    sub = G[y0:y1, x0:x1]
    th = 1*K                                        # stroke X -> K cells
    ring = np.zeros_like(sub); ring[:] = 0
    ring[:th,:] = 1; ring[-th:,:] = 1; ring[:,:th] = 1; ring[:,-th:] = 1
    missing = (ring == 1) & (sub == 0)
    my, mx = np.where(missing)
    side = None; length = 0
    if len(my):
        if my.max() < th: side, length = "TOP", (mx.max()-mx.min()+1)/K
        elif my.min() >= sub.shape[0]-th: side, length = "BOTTOM", (mx.max()-mx.min()+1)/K
        elif mx.max() < th: side, length = "LEFT", (my.max()-my.min()+1)/K
        elif mx.min() >= sub.shape[1]-th: side, length = "RIGHT", (my.max()-my.min()+1)/K
    solid = (ring == 1) | (sub == 0)
    info.append({"bbox": [x0/K, y0/K, x1/K, y1/K], "gate_side": side,
                 "gate_len": length, "gates": 1 if len(my) else 0,
                 "is_ring": bool(np.all(sub[th:-th, th:-th] == 0)) if sub.shape[0] > 2*th else True})

names = ["f1 OUTER", "f2 MIDDLE", "f3 INNER"]
expect = ["TOP", "LEFT", "BOTTOM"]
ok_seq = True
for n, exp, d in zip(names, expect, info):
    good = d["gate_side"] == exp and abs(d["gate_len"] - 2.0) < 1e-9 and d["gates"] == 1
    ok_seq &= good
    check("%s carries exactly one %s gate of 2X" % (n, exp), good,
          "bbox %s, gate %s, width %gX" % (d["bbox"], d["gate_side"], d["gate_len"]))
check("Gate sequence outer=TOP / middle=LEFT / inner=BOTTOM", ok_seq,
      " / ".join("%s=%s" % (n, d["gate_side"]) for n, d in zip(names, info)))

# --- stroke module
bad = [r for r in frames if not (abs(r[2]-1) < 1e-9 or abs(r[3]-1) < 1e-9)]
check("Every structural rectangle is exactly 1X thick", not bad, "%d violations" % len(bad))

# --- bounds / gaps / core
b = [d["bbox"] for d in info]
check("Frame bounds f1 0-10, f2 1.5-8.5, f3 3-7",
      b[0][:2]+b[0][2:] == [0.0,0.0,10.0,10.0] and b[1][:2]+b[1][2:] == [1.5,1.5,8.5,8.5]
      and b[2][:2]+b[2][2:] == [3.0,3.0,7.0,7.0],
      "f1 %s  f2 %s  f3 %s" % (b[0], b[1], b[2]))
g1 = b[1][0] - (b[0][0] + 1); g2 = b[2][0] - (b[1][0] + 1)
check("Inter-frame gap uniform at X/2", abs(g1-0.5) < 1e-9 and abs(g2-0.5) < 1e-9,
      "g1 = %gX, g2 = %gX" % (g1, g2))
core = geom.master_core()
clear = core[0] - (b[2][0] + 1)
check("Central core exactly 2X x 2X", core[2] == 2 and core[3] == 2, "rect %s" % (core,))
check("Core clearance 0 (core flush inside f3)", abs(clear) < 1e-9, "clearance = %gX" % clear)
check("Edge-to-core budget closes at 10X",
      abs((1 + g1 + 1 + g2 + 1 + clear) * 2 + 2 - 10) < 1e-9,
      "X + X/2 + X + X/2 + X + 0, doubled, + 2X core = 10X")

# ---------------------------------------------------------------- SVG files
FRAMES_D = geom.rects_to_path(geom.master_frames())
CORE_D   = geom.rects_to_path([geom.master_core()])
CTO_D    = open("wm_cto.txt").read().strip()
OS_D     = open("wm_os.txt").read().strip()

FILES = ["ctoossymbolfullcolourdarkbg.svg","ctoossymbolfullcolourlightbg.svg",
         "ctoossymbolmonochromepositive.svg","ctoossymbolmonochromereversed.svg",
         "ctooslockuphorizontaldarkbg.svg","ctooslockuphorizontallightbg.svg",
         "ctooslockupverticaldarkbg.svg","ctooslockupverticallightbg.svg"]
src = {f: open(f).read() for f in FILES}

check("Canonical frame path identical in all 8 standalone assets",
      all(FRAMES_D in s for s in src.values()), "single shared path string")
check("Core path identical in all 8 standalone assets",
      all(CORE_D in s for s in src.values()), CORE_D)

LOCK = [f for f in FILES if "lockup" in f]
check("Wordmark paths identical across all lockups",
      all(CTO_D in src[f] and OS_D in src[f] for f in LOCK),
      "%d lockups share one converted glyph set" % len(LOCK))

def fills(s):
    return re.findall(r'fill="(#[0-9A-Fa-f]{6})"', s)
COL = {
 "ctoossymbolfullcolourdarkbg.svg":  ["#EDF0F3","#2563EB"],
 "ctoossymbolfullcolourlightbg.svg": ["#191C20","#2563EB"],
 "ctoossymbolmonochromepositive.svg":["#191C20","#191C20"],
 "ctoossymbolmonochromereversed.svg":["#EDF0F3","#EDF0F3"],
}
for f, exp in COL.items():
    check("Colour hierarchy %s" % f, fills(src[f]) == exp, "fills %s" % fills(src[f]))

def frame_fill(s):
    m = re.search(re.escape(FRAMES_D) + r'" fill="(#[0-9A-Fa-f]{6})"', s)
    return m.group(1) if m else None
check("Cobalt never fills a structural frame",
      all(frame_fill(s) != "#2563EB" for s in src.values()),
      "frame fills: " + ", ".join(sorted(set(frame_fill(s) for s in src.values()))))
check("Wordmark OS set in #2563EB on full-colour lockups",
      all(re.search(re.escape(OS_D) + r'" fill="#2563EB"', src[f])
          for f in LOCK), "#2563EB")

for f in FILES:
    s = src[f]
    check("%s free of live text / raster / clip machinery" % f,
          "<text" not in s and "<image" not in s and "clipPath" not in s
          and "<mask" not in s and "font-family" not in s,
          "paths only")

def vb(s): return re.search(r'viewBox="([^"]+)"', s).group(1)
check("Symbol viewBox 0 0 10 10",
      all(vb(src[f]) == "0 0 10 10" for f in FILES if "symbol" in f), "0 0 10 10")
check("Horizontal lockup viewBox 0 0 47.4657 10",
      all(vb(src[f]) == "0 0 47.4657 10" for f in FILES if "lockuphorizontal" in f),
      "0 0 47.4657 10")
check("Vertical lockup viewBox raised to 0 0 34.4657 19.5000 (VQA-02)",
      all(vb(src[f]) == "0 0 34.4657 19.5000" for f in FILES if "lockupvertical" in f),
      "was 0 0 34.4657 19.0000")

json.dump({"frames": info, "results": R}, open("audit_result.json","w"), indent=1)
fails = [r for r in R if r[1] == "FAIL"]
w = max(len(r[0]) for r in R)
for n, v, ev in R:
    print("%-*s  %s   %s" % (w, n, v, ev))
print("\n%d checks, %d PASS, %d FAIL" % (len(R), len(R)-len(fails), len(fails)))
sys.exit(1 if fails else 0)

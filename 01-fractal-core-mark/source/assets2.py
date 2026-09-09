# -*- coding: utf-8 -*-
"""Re-export every canonical derivative from the corrected master (geom2)."""
import geom2 as geom

CTO_D = open("wm_cto.txt").read().strip()
OS_D  = open("wm_os.txt").read().strip()
CTO_W, OS_W, WM_W = [float(v) for v in open("wm_meta.txt").read().split()]

F = geom.rects_to_path(geom.master_frames())
C = geom.rects_to_path([geom.master_core()])

COB="#2563EB"; ICE="#EDF0F3"; DARK="#191C20"

CAP        = 6.0     # wordmark cap height, X
GAP_SW     = 3.0     # symbol -> wordmark gap, X   (frozen)
OPT_MARGIN = 0.5     # declared optical margin, X = X/2  (VQA-02 correction)
LOCKUP_W   = 10 + GAP_SW + WM_W          # 47.4657
VLOCK_H    = 10 + GAP_SW + CAP + OPT_MARGIN   # 19.5   (was 19.0 -> clipped)

def head(vb, w, h, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" width="%d" height="%d">'
            '<title>%s</title>' % (vb, w, h, title))

def symbol(frame, core, fn, title):
    s  = head("0 0 10 10", 1000, 1000, title)
    s += '<path d="%s" fill="%s"/><path d="%s" fill="%s"/></svg>' % (F, frame, C, core)
    open(fn,"w").write(s)

def lockup_h(frame, core, ink, fn, title):
    s  = head("0 0 %.4f 10" % LOCKUP_W, round(LOCKUP_W*100), 1000, title)
    s += '<path d="%s" fill="%s"/><path d="%s" fill="%s"/>' % (F, frame, C, core)
    s += ('<g transform="translate(%g %g)"><path d="%s" fill="%s"/><path d="%s" fill="%s"/></g></svg>'
          % (10+GAP_SW, 8, CTO_D, ink, OS_D, core))
    open(fn,"w").write(s)

def lockup_v(frame, core, ink, fn, title):
    s  = head("0 0 %.4f %.4f" % (WM_W, VLOCK_H), round(WM_W*50), round(VLOCK_H*50), title)
    s += ('<g transform="translate(%.4f 0)"><path d="%s" fill="%s"/><path d="%s" fill="%s"/></g>'
          % ((WM_W-10)/2.0, F, frame, C, core))
    s += ('<g transform="translate(0 %g)"><path d="%s" fill="%s"/><path d="%s" fill="%s"/></g></svg>'
          % (10+GAP_SW+CAP, CTO_D, ink, OS_D, core))
    open(fn,"w").write(s)

T = "CTO OS Fractal Core Mark"
symbol(ICE,  COB,  "ctoossymbolfullcolourdarkbg.svg",     T+" - full colour, dark ground")
symbol(DARK, COB,  "ctoossymbolfullcolourlightbg.svg",    T+" - full colour, light ground")
symbol(DARK, DARK, "ctoossymbolmonochromepositive.svg",   T+" - monochrome positive")
symbol(ICE,  ICE,  "ctoossymbolmonochromereversed.svg",   T+" - monochrome reversed")
lockup_h(ICE,  COB, ICE,  "ctooslockuphorizontaldarkbg.svg",  T+" - horizontal lockup, dark ground")
lockup_h(DARK, COB, DARK, "ctooslockuphorizontallightbg.svg", T+" - horizontal lockup, light ground")
lockup_v(ICE,  COB, ICE,  "ctooslockupverticaldarkbg.svg",    T+" - vertical lockup, dark ground")
lockup_v(DARK, COB, DARK, "ctooslockupverticallightbg.svg",   T+" - vertical lockup, light ground")
print("LOCKUP_W %.4f   VLOCK_H %.4f" % (LOCKUP_W, VLOCK_H))
print("re-exported 8 canonical SVGs")

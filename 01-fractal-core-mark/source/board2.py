# -*- coding: utf-8 -*-
import geom2 as geom

CTO_D = open("wm_cto.txt").read().strip()
OS_D  = open("wm_os.txt").read().strip()
CTO_W, OS_W, WM_W = [float(v) for v in open("wm_meta.txt").read().split()]
CAP = 6.0          # cap height in X units
GAP_SW = 3.0       # symbol -> wordmark gap (X)
LOCKUP_W = 10 + GAP_SW + WM_W
TAGLINE = "KNOW WHAT IS TRUE.  PROVE WHAT IS REAL.  CONTROL WHAT MATTERS."

# ---- colour system -------------------------------------------------------
COBALT = "#2563EB"
ICE    = "#EDF0F3"
STEEL  = "#8A93A0"
DARKN  = "#191C20"
BG     = "#141619"
PANEL  = "#1D2024"
PANEL2 = "#22262B"
LINE   = "#31373E"
MUTED  = "#98A1AC"
DIM    = "#6E7681"
LIGHTBG= "#F4F2EE"
RED    = "#E5484D"

W, H = 2800, 1700
out = []
def e(s): out.append(s)

# ---- helpers -------------------------------------------------------------
PLACEMENTS = []
WORDMARKS = []
CUR = "?"
def sym(x, y, size, frame=ICE, core=COBALT, extra=""):
    PLACEMENTS.append(dict(panel=CUR, x=x, y=y, size=size, frame=frame, core=core))
    """Canonical master symbol, single shared definition. size = full 10X box."""
    s = size / 10.0
    return ('<g transform="translate(%.4f %.4f) scale(%.6f)" %s>'
            '<use href="#frames" fill="%s"/><use href="#core" fill="%s"/></g>'
            % (x, y, s, extra, frame, core))

def wordmark(x, y_baseline, capsize, cto=ICE, os_=COBALT):
    """Canonical wordmark master. capsize = cap height in px."""
    WORDMARKS.append(dict(panel=CUR, x=x, y=y_baseline, cap=capsize, cto=cto, os=os_))
    s = capsize / CAP
    return ('<g transform="translate(%.4f %.4f) scale(%.6f)">'
            '<use href="#wm-cto" fill="%s"/><use href="#wm-os" fill="%s"/></g>'
            % (x, y_baseline, s, cto, os_))

def lockup_h(x, y, symsize, frame=ICE, core=COBALT, ink=ICE):
    """Horizontal lockup, frozen ratios. x,y = top-left of symbol box."""
    X = symsize / 10.0
    g  = sym(x, y, symsize, frame, core)
    g += wordmark(x + (10 + GAP_SW) * X, y + 8 * X, CAP * X, ink, core)
    return g

def lockup_h_w(symsize):  return LOCKUP_W * symsize / 10.0

def lockup_v(x, y, symsize, frame=ICE, core=COBALT, ink=ICE):
    """Vertical lockup: symbol centred over wordmark, gap 3X."""
    X = symsize / 10.0
    tw = WM_W * X
    g  = sym(x + (tw - symsize) / 2.0, y, symsize, frame, core)
    g += wordmark(x, y + symsize + (GAP_SW + CAP) * X, CAP * X, ink, core)
    return g

def panel(x, y, w, h, label, fill=PANEL, caption=None):
    global CUR
    CUR = label.split(".")[0].strip()
    e('<rect x="%g" y="%g" width="%g" height="%g" rx="3" fill="%s" stroke="%s"/>' % (x,y,w,h,fill,LINE))
    e('<text class="plabel" x="%g" y="%g">%s</text>' % (x+22, y+34, label))
    if caption:
        e('<text class="pcap" x="%g" y="%g">%s</text>' % (x+22, y+h-16, caption))

def txt(x, y, s, cls="lbl", anchor="start", extra=""):
    e('<text class="%s" x="%g" y="%g" text-anchor="%s" %s>%s</text>' % (cls,x,y,anchor,extra,s))

# ---- document ------------------------------------------------------------
e('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
e('''<style>
text{font-family:Inter,'Helvetica Neue',Arial,sans-serif;fill:%s}
.h1{font-size:40px;font-weight:700;fill:#F2F5F8;letter-spacing:.4px}
.h2{font-size:17px;font-weight:500;fill:%s;letter-spacing:.9px}
.plabel{font-size:17px;font-weight:600;fill:#DCE2E9;letter-spacing:1.1px}
.pcap{font-size:12px;font-weight:500;fill:%s;letter-spacing:1.2px}
.lbl{font-size:14px;font-weight:500;fill:%s}
.sm{font-size:12px;font-weight:500;fill:%s}
.dim{font-size:11.5px;font-weight:600;fill:%s;letter-spacing:.6px}
.bold{font-size:14px;font-weight:700;fill:#E6EBF1}
.mono{font-family:'DejaVu Sans Mono',monospace;font-size:12px;fill:%s}
.ok{font-size:13px;font-weight:700;fill:#3FB68B;letter-spacing:1px}
</style>''' % (MUTED, MUTED, DIM, MUTED, DIM, DIM, MUTED))

e('<defs>')
e('<g id="frames"><path d="%s"/></g>' % geom.rects_to_path(geom.master_frames()))
e('<g id="core"><path d="%s"/></g>' % geom.rects_to_path([geom.master_core()]))
e('<g id="wm-cto"><path d="%s"/></g>' % CTO_D)
e('<g id="wm-os"><path d="%s"/></g>' % OS_D)
e('<linearGradient id="cover" x1="0" y1="0" x2="1" y2="1">'
  '<stop offset="0" stop-color="#33383E"/><stop offset="0.5" stop-color="#282D33"/>'
  '<stop offset="1" stop-color="#1C2025"/></linearGradient>')
e('<linearGradient id="spine" x1="0" y1="0" x2="1" y2="0">'
  '<stop offset="0" stop-color="#14171A"/><stop offset="1" stop-color="#2E343A"/></linearGradient>')
e('</defs>')

e('<rect width="%d" height="%d" fill="%s"/>' % (W,H,BG))

# ---- header --------------------------------------------------------------
txt(48, 74, "CTO OS FRACTAL CORE MARK &#8212; VECTOR MASTER v2", "h1")
txt(48, 104, "VECTOR_CORRECTION_1 &#183; MODEL B &#183; THREE DISTINCT OPEN FRAMES, ONE GATE EACH &#183; CONCEPT UNCHANGED", "h2")
e('<line x1="48" y1="126" x2="%d" y2="126" stroke="%s"/>' % (W-48, LINE))

M=48; GUT=16; CW=664
C1,C2,C3,C4 = 48, 728, 1408, 2088
R1,R1H = 150, 560
R2,R2H = 726, 380
R3,R3H = 1122, 400

def arrow(x1,y1,x2,y2,col=DIM):
    e('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1" marker-start="url(#ar)" marker-end="url(#ar)"/>'%(x1,y1,x2,y2,col))

e('<defs><marker id="ar" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="6" markerHeight="6" orient="auto">'
  '<path d="M1 4 L7 1.6 L7 6.4 Z" fill="%s"/></marker>'
  '<marker id="arw" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="6" markerHeight="6" orient="auto">'
  '<path d="M1 4 L7 1.6 L7 6.4 Z" fill="%s"/></marker></defs>' % (DIM, MUTED))

# ===================== A. CANONICAL MASTER SYMBOL =========================
panel(C1, R1, CW, R1H, "A.  CANONICAL MASTER SYMBOL", PANEL, "VECTOR MASTER v2 &#183; THREE OPEN FRAMES + ACCOUNTABLE CORE")
S=356
e(sym(C1+(CW-S)/2, R1+118, S, ICE, COBALT))
txt(C1+CW/2, R1+R1H-52, "10X &#215; 10X  &#183;  3 FRAMES  &#183;  STROKE X  &#183;  GAP X/2  &#183;  GATE 2X  &#183;  CORE 2X", "sm", "middle")

# ===================== B. CONSTRUCTION GRID ===============================
panel(C2, R1, CW, R1H, "B.  EXACT MODULAR CONSTRUCTION GRID", PANEL, "EVERY MEASUREMENT RECONSTRUCTS THE VECTOR MASTER")
S=270; X=S/10.0; HX=X/2.0
gx = C2+150; gy = R1+156
for i in range(21):                                  # half-X grid, 20 x 20
    w  = 0.9 if i%2==0 else 0.55
    col = "#414A54" if i%2==0 else "#333A43"
    e('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g"/>'%(gx+i*HX,gy,gx+i*HX,gy+S,col,w))
    e('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g"/>'%(gx,gy+i*HX,gx+S,gy+i*HX,col,w))
e('<rect x="%g" y="%g" width="%g" height="%g" fill="none" stroke="#4F5964"/>'%(gx,gy,S,S))
e(sym(gx, gy, S, STEEL, COBALT))

# --- master width, below ---
arrow(gx, gy+S+30, gx+S, gy+S+30)
txt(gx+S/2, gy+S+47, "MASTER = 10X &#215; 10X", "dim", "middle")

# --- gate width, above ---
arrow(gx+4*X, gy-18, gx+6*X, gy-18)
txt(gx+3.6*X, gy-14, "GATE WIDTH = 2X (ALL THREE)", "dim", "end")

# --- right-hand dimension stack ---
ax = gx+S+16
for (y0,y1,lab) in [(0,1,"FRAME STROKE = X"),
                    (1,1.5,"INTER-FRAME GAP = X/2"),
                    (4,6,"CENTRAL CORE = 2X &#215; 2X")]:
    arrow(ax, gy+y0*X, ax, gy+y1*X)
    e('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#3E4650" stroke-width="0.8"/>'%(gx+S, gy+y0*X, ax, gy+y0*X))
    e('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#3E4650" stroke-width="0.8"/>'%(gx+S, gy+y1*X, ax, gy+y1*X))
    txt(ax+10, gy+(y0+y1)/2.0*X+4, lab, "dim")

# --- gate leaders, one per frame ---
def leader(x1,y1,x2,y2):
    e('<path d="M%g %g L%g %g" stroke="%s" stroke-width="1" fill="none"/>'%(x1,y1,x2,y2,MUTED))
    e('<circle cx="%g" cy="%g" r="2.6" fill="%s"/>'%(x1,y1,MUTED))
leader(gx+5*X, gy+0.5*X, gx+5*X, gy-34)
txt(gx+5*X, gy-42, "f1 OUTER GATE &#183; TOP", "dim", "middle", 'fill="%s"'%MUTED)
leader(gx+2*X, gy+5*X, gx-30, gy+5*X)
txt(gx-36, gy+5*X-5, "f2 MIDDLE GATE", "dim", "end", 'fill="%s"'%MUTED)
txt(gx-36, gy+5*X+9, "&#183; LEFT", "dim", "end", 'fill="%s"'%MUTED)
leader(gx+5*X, gy+6.5*X, gx+5*X, gy+S+8)
txt(gx+5*X, gy+S+21, "f3 INNER GATE &#183; BOTTOM", "dim", "middle", 'fill="%s"'%MUTED)

# --- frame bounds table, lower right ---
tb = gy+7.4*X
txt(ax+10, tb, "FRAME BOUNDS", "bold")
for i,(n,a,b2) in enumerate([("f1 OUTER","0.0","10.0"),("f2 MIDDLE","1.5","8.5"),
                             ("f3 INNER","3.0","7.0"),("CORE","4.0","6.0")]):
    txt(ax+10, tb+20+i*17, "%s" % n, "sm")
    txt(ax+186, tb+20+i*17, "%s &#8211; %s X" % (a,b2), "sm", "end")

# ===================== C. PRIMARY HORIZONTAL LOCKUP =======================
panel(C3, R1, CW, 272, "C.  PRIMARY HORIZONTAL LOCKUP", PANEL, "FULL COLOUR &#183; NEUTRAL FRAMES + COBALT CORE + COBALT OS")
ss = 500.0/LOCKUP_W*10
e(lockup_h(C3+(CW-lockup_h_w(ss))/2, R1+96, ss, ICE, COBALT, ICE))

# ===================== D. VERTICAL LOCKUP =================================
panel(C4, R1, CW, 272, "D.  VERTICAL LOCKUP", PANEL, "FULL COLOUR &#183; SAME MASTER, SAME WORDMARK")
vs = 82.0
vx = C4+(CW-WM_W*vs/10.0)/2
e(lockup_v(vx, R1+68, vs, ICE, COBALT, ICE))

# ===================== E. LIGHT VERSION ===================================
panel(C3, 438, CW, 272, "E.  LIGHT VERSION", PANEL)
e('<rect x="%g" y="%g" width="%g" height="%g" fill="%s"/>'%(C3+1, 438+52, CW-2, 272-52-30, LIGHTBG))
ss2 = 470.0/LOCKUP_W*10
e(lockup_h(C3+(CW-lockup_h_w(ss2))/2, 438+104, ss2, DARKN, COBALT, DARKN))
txt(C3+22, 438+272-14, "HORIZONTAL LOCKUP ON LIGHT &#183; DARK NEUTRAL FRAMES + COBALT CORE", "pcap")

# ===================== F. DARK VERSION ====================================
panel(C4, 438, CW, 272, "F.  DARK VERSION", PANEL)
e('<rect x="%g" y="%g" width="%g" height="%g" fill="#0C0E10"/>'%(C4+1, 438+52, CW-2, 272-52-30))
e(lockup_h(C4+(CW-lockup_h_w(ss2))/2, 438+104, ss2, ICE, COBALT, ICE))
txt(C4+22, 438+272-14, "HORIZONTAL LOCKUP ON DARK &#183; ICE FRAMES + COBALT CORE", "pcap")

# ===================== G. POSITIVE MONOCHROME =============================
panel(C1, R2, CW, R2H, "G.  POSITIVE MONOCHROME", PANEL)
e('<rect x="%g" y="%g" width="%g" height="%g" fill="#FFFFFF"/>'%(C1+1, R2+52, CW-2, R2H-52-30))
ms = 470.0/LOCKUP_W*10
e(lockup_h(C1+(CW-lockup_h_w(ms))/2, R2+150, ms, DARKN, DARKN, DARKN))
txt(C1+22, R2+R2H-14, "ONE INK &#183; 100% K &#183; NO COBALT, NO GREYSCALE STEPS", "pcap")

# ===================== H. REVERSED MONOCHROME =============================
panel(C2, R2, CW, R2H, "H.  REVERSED MONOCHROME", PANEL)
e('<rect x="%g" y="%g" width="%g" height="%g" fill="#0C0E10"/>'%(C2+1, R2+52, CW-2, R2H-52-30))
e(lockup_h(C2+(CW-lockup_h_w(ms))/2, R2+150, ms, ICE, ICE, ICE))
txt(C2+22, R2+R2H-14, "ONE INK &#183; KNOCK-OUT &#183; IDENTICAL PATHS TO PANEL G", "pcap")

# ===================== J. CLEAR-SPACE RULE ================================
panel(C3, R2, CW, R2H, "J.  CLEAR-SPACE RULE &amp; MINIMUM SIZE", PANEL)
js = 88.0
JX = js/10.0
lw = lockup_h_w(js); lh = js
lx = C3+(CW-lw)/2; ly = R2+112
e('<rect x="%g" y="%g" width="%g" height="%g" fill="#101317"/>'%(lx-2*JX, ly-2*JX, lw+4*JX, lh+4*JX))
e('<rect x="%g" y="%g" width="%g" height="%g" fill="none" stroke="%s" stroke-dasharray="5 4"/>'%(lx-2*JX, ly-2*JX, lw+4*JX, lh+4*JX, "#5A636D"))
e('<rect x="%g" y="%g" width="%g" height="%g" fill="none" stroke="%s" stroke-dasharray="2 3"/>'%(lx, ly, lw, lh, "#454E58"))
e(lockup_h(lx, ly, js, ICE, COBALT, ICE))
arrow(lx-2*JX, ly-2*JX-14, lx, ly-2*JX-14); txt(lx-JX, ly-2*JX-20, "2X", "dim", "middle")
arrow(lx-2*JX-14, ly-2*JX, lx-2*JX-14, ly); txt(lx-2*JX-20, ly-JX+4, "2X", "dim", "end")
txt(C3+24, R2+250, "CLEAR SPACE", "bold")
txt(C3+24, R2+272, "2X on all four sides, measured from the lockup", "sm")
txt(C3+24, R2+292, "bounding box. No type, rule or image may enter it.", "sm")
txt(C3+360, R2+250, "MINIMUM SIZE", "bold")
txt(C3+360, R2+272, "Digital &#8212; 16 px symbol height", "sm")
txt(C3+360, R2+292, "Print &#8212; 0.75 in (19 mm) lockup width", "sm")
txt(C3+360, R2+312, "Below 32 px use panel I micro-masters", "sm")

# ===================== O. INCORRECT USE ===================================
panel(C4, R2, CW, R2H, "O.  INCORRECT USE", PANEL)
items = [
 ("ROTATION",       "Do not rotate the symbol."),
 ("GATE CHANGE",    "Do not move or re-order gates."),
 ("ADDED LAYER",    "Do not add recursion layers."),
 ("COBALT FRAMES",  "Cobalt may never fill a frame."),
 ("ALTERNATE BLUE", "No blue other than #2563EB."),
 ("WORDMARK EDIT",  "Do not stretch or re-space."),
]
ox = C4+26; oy = R2+64; cwid = 206; chg = 152; bw_ = cwid-14; bh_ = chg-16
for i,(t,d) in enumerate(items):
    px = ox + (i%3)*cwid; py = oy + (i//3)*chg
    e('<rect x="%g" y="%g" width="%g" height="%g" rx="2" fill="#15181C" stroke="#2B3138"/>'%(px,py,bw_,bh_))
    cx = px+bw_/2.0; cy = py+48; s = 52
    if i==0:
        e('<g transform="translate(%g %g) rotate(45)">%s</g>'%(cx,cy,sym(-s/2,-s/2,s,STEEL,COBALT)))
    elif i==1:
        r=[(0,0,10,1),(0,9,10,1),(0,1,1,8),(9,1,1,3),(9,6,1,3),
           (2,2,2,1),(6,2,2,1),(2,3,1,4),(7,3,1,4),(2,7,6,1)]
        e('<g transform="translate(%g %g) scale(%g)"><path d="%s" fill="%s"/><path d="%s" fill="%s"/></g>'
          %(cx-s/2, cy-s/2, s/10.0, geom.rects_to_path(r), STEEL, geom.rects_to_path([(4,4,2,2)]), COBALT))
    elif i==2:
        base = geom.outer_frame()+geom.middle_frame()+[(2.6,2.6,4.8,0.4),(2.6,7,4.8,0.4),(2.6,2.6,0.4,4.8),(7,2.6,0.4,4.8)]+geom.inner_frame()
        e('<g transform="translate(%g %g) scale(%g)"><path d="%s" fill="%s"/><path d="%s" fill="%s"/></g>'
          %(cx-s/2, cy-s/2, s/10.0, geom.rects_to_path(base), STEEL, geom.rects_to_path([(4,4,2,2)]), COBALT))
    elif i==3:
        e(sym(cx-s/2, cy-s/2, s, COBALT, ICE))
    elif i==4:
        e(sym(cx-s/2, cy-s/2, s, STEEL, "#00B4FF"))
    else:
        capm = 15.0; wdt = WM_W*(capm/CAP)*1.45
        e('<g transform="translate(%g %g) scale(1.45,1)">%s</g>'%(cx-wdt/2.0, cy+capm/2.0, wordmark(0,0,capm,STEEL,COBALT)))
    # red incorrect badge
    e('<g stroke="%s" stroke-width="2" stroke-linecap="round" opacity="0.95">'
      '<circle cx="%g" cy="%g" r="9" fill="none"/><path d="M%g %g L%g %g"/></g>'
      %(RED, px+bw_-18, py+18, px+bw_-24, py+12, px+bw_-12, py+24))
    e('<text class="dim" x="%g" y="%g" text-anchor="middle" fill="%s">%s</text>'%(cx, py+96, RED, t))
    e('<text class="sm" x="%g" y="%g" text-anchor="middle" font-size="10.5">%s</text>'%(cx, py+114, d))

# ===================== I. MICRO-MARK ======================================
panel(C1, R3, CW, R3H, "I.  MICRO-MARK MASTERS &#8212; 16 / 24 / 32 px", PANEL)

MICRO = {
 32: (3.0, 1.0, geom.master_frames(), [geom.master_core()]),
 24: (2.0, 2.0, geom.master_frames(), [geom.master_core()]),
 16: (2.0, 0.0,
      [(0,0,3,1),(5,0,3,1),(0,7,8,1),(0,1,1,6),(7,1,1,6),
       (2,2,4,1),(2,3,1,1),(2,5,1,1),(5,3,1,3),(2,6,4,1)],
      [(3,3,2,2)]),
}
def micro(x, y, px, ink=ICE):
    Xp, off, rects, core = MICRO[px]
    e('<g transform="translate(%g %g) scale(%g)"><path d="%s" fill="%s"/><path d="%s" fill="%s"/></g>'
      % (x+off, y+off, Xp, geom.rects_to_path(rects), ink, geom.rects_to_path(core), COBALT))

# actual-size row
ay = R3+104
for i, p in enumerate([16, 24, 32]):
    bx = C1+52 + i*96
    e('<rect x="%g" y="%g" width="%g" height="%g" fill="#101317" stroke="#2B3138"/>' % (bx-18, ay-18, p+36, p+36))
    micro(bx, ay, p)
    txt(bx+p/2.0, ay+p+38, "%d px" % p, "dim", "middle")
txt(C1+52, R3+72, "ACTUAL SIZE", "dim")

# magnified row
txt(C1+360, R3+72, "MAGNIFIED", "dim")
mx = C1+360
for p, sc in [(16, 4.0), (24, 3.0), (32, 2.5)]:
    side = p*sc
    e('<rect x="%g" y="%g" width="%g" height="%g" fill="#101317" stroke="#2B3138"/>' % (mx-6, R3+90-6, side+12, side+12))
    e('<g transform="translate(%g %g) scale(%g)">' % (mx, R3+90, sc))
    micro(0, 0, p)
    e('</g>')
    txt(mx+side/2.0, R3+90+side+22, "%d px &#215; %g" % (p, sc), "dim", "middle")
    mx += side + 40

txt(C1+52, R3+R3H-112, "DOCUMENTED OPTICAL CORRECTIONS", "bold")
txt(C1+52, R3+R3H-90, "32 px &#8212; full canonical master; X = 3 px on a 30 px optical box (X/2 gap renders at 1.5 px).", "sm")
txt(C1+52, R3+R3H-70, "24 px &#8212; full canonical master; X = 2 px on a 20 px optical box, every edge on a whole pixel.", "sm")
txt(C1+52, R3+R3H-50, "16 px &#8212; DOCUMENTED EXCEPTION. Reduced 8X two-frame micro master, X = 2 px;", "sm")
txt(C1+52, R3+R3H-30, "&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160; f3 and its BOTTOM gate omitted. TOP and LEFT gates retained.", "sm")
txt(C1+52, R3+R3H-10, "The full master requires an even X so the X/2 gap lands on whole pixels.", "sm")

# ===================== L. EXACT COLOUR VALUES =============================
panel(C2, R3, CW, R3H, "L.  EXACT COLOUR VALUES", PANEL)
cols = [("COBALT BLUE",  COBALT, "37, 99, 235",   "84, 58, 0, 8",  "CORE + OS ONLY"),
        ("ICE NEUTRAL",  ICE,    "237, 240, 243", "2, 1, 0, 5",    "FRAMES / TYPE ON DARK"),
        ("STEEL NEUTRAL",STEEL,  "138, 147, 160", "14, 8, 0, 37",  "GRID / TINTED UI"),
        ("DARK NEUTRAL", DARKN,  "25, 28, 32",    "22, 13, 0, 87", "FRAMES / TYPE ON LIGHT")]
cy0 = R3+74
for i,(n,hexv,rgb,cmyk,use) in enumerate(cols):
    y = cy0 + i*74
    e('<rect x="%g" y="%g" width="56" height="56" rx="2" fill="%s" stroke="#3A4149"/>'%(C2+24, y, hexv))
    txt(C2+94, y+18, n, "bold")
    txt(C2+94, y+36, "HEX %s &#160;&#160; RGB %s" % (hexv.upper(), rgb), "sm")
    txt(C2+94, y+52, "CMYK %s &#160;&#160; &#183; &#160;&#160; %s" % (cmyk, use), "sm")
e('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s"/>'%(C2+24, R3+R3H-58, C2+CW-24, R3+R3H-58, LINE))
txt(C2+24, R3+R3H-34, "BINDING: BLUE IS USED ONLY FOR THE CENTRAL CORE AND THE &#8220;OS&#8221; WORDMARK.", "dim", "start", 'fill="%s"'%ICE)
txt(C2+24, R3+R3H-16, "STRUCTURAL FRACTAL FRAMES ARE NEVER COBALT, IN ANY APPLICATION.", "dim")

# ===================== M. TAGLINE LOCKUP ==================================
panel(C3, R3, CW, R3H, "M.  OPTIONAL TAGLINE LOCKUP", PANEL, "TAGLINE SET IN NEUTRAL ONLY &#183; NEVER COBALT")
ts = 380.0/LOCKUP_W*10
tx = C3+(CW-lockup_h_w(ts))/2
e(lockup_h(tx, R3+108, ts, ICE, COBALT, ICE))
TX = ts/10.0
e('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s"/>'%(tx, R3+108+13*TX, tx+lockup_h_w(ts), R3+108+13*TX, "#3A4149"))
txt(C3+CW/2, R3+108+13*TX+34, "KNOW WHAT IS TRUE.", "lbl", "middle", 'letter-spacing="2.2" font-size="15" fill="%s"'%ICE)
txt(C3+CW/2, R3+108+13*TX+58, "PROVE WHAT IS REAL.", "lbl", "middle", 'letter-spacing="2.2" font-size="15" fill="%s"'%ICE)
txt(C3+CW/2, R3+108+13*TX+82, "CONTROL WHAT MATTERS.", "lbl", "middle", 'letter-spacing="2.2" font-size="15" fill="%s"'%ICE)

# ===================== N. PHYSICAL GOVERNANCE REPORT ======================
panel(C4, R3, CW, R3H, "N.  PHYSICAL GOVERNANCE REPORT", PANEL, "EXACT CANONICAL MASTER &#183; DEBOSS + FOIL")
bx0 = C4+330; by0 = R3+60; bw=262; bh=288
e('<rect x="%g" y="%g" width="%g" height="%g" rx="2" fill="#0A0C0E" opacity="0.6"/>'%(bx0+9, by0+11, bw, bh))
e('<rect x="%g" y="%g" width="%g" height="%g" rx="2" fill="url(#cover)" stroke="#3B434C"/>'%(bx0, by0, bw, bh))
e('<rect x="%g" y="%g" width="13" height="%g" fill="url(#spine)"/>'%(bx0, by0, bh))
nvs = 60.0
nvx = bx0 + 13 + (bw-13-WM_W*nvs/10.0)/2.0
e('<g opacity="0.5">%s</g>' % lockup_v(nvx+1.4, by0+58+1.4, nvs, "#0D0F12", "#0D0F12", "#0D0F12"))
e(lockup_v(nvx, by0+58, nvs, ICE, COBALT, ICE))
e('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#5A636D"/>'%(bx0+40, by0+216, bx0+bw-28, by0+216))
e('<text class="dim" x="%g" y="%g" fill="#C9D1D9">GOVERNANCE REPORT</text>'%(bx0+40, by0+240))
txt(bx0+40, by0+258, "ANNUAL EDITION", "dim")
txt(C4+24, R3+82, "PERMITTED", "bold")
for i,s in enumerate(["Emboss / deboss","Foil / ink","Material texture"]):
    txt(C4+24, R3+104+i*20, "&#183; "+s, "sm")
txt(C4+24, R3+186, "NOT PERMITTED", "bold")
for i,s in enumerate(["Geometry change","Gate re-orientation","Extra / fewer frames","Core repositioning","Colour-hierarchy change"]):
    txt(C4+24, R3+208+i*20, "&#183; "+s, "sm")
txt(C4+24, R3+312, "FULL COLOUR: NEUTRAL FRAMES", "sm")
txt(C4+24, R3+330, "+ COBALT CORE.", "sm")
txt(C4+24, R3+350, "MONOCHROME: ONE INK ONLY.", "sm")

# ===================== STATUS STRIP =======================================
sy = 1538
e('<rect x="48" y="%g" width="%g" height="114" rx="3" fill="%s" stroke="%s"/>'%(sy, W-96, PANEL2, LINE))
txt(72, sy+40, "CTO OS FRACTAL CORE MARK &#8212; VECTOR MASTER v2 &#183; VQA-01 / VQA-02 CLOSED", "plabel", "start", 'font-size="20"')
st = [("CONCEPT","FROZEN"),("THREE FRAMES","VERIFIED"),("GATE SEQUENCE","VERIFIED"),
      ("WORDMARK","UNCHANGED"),("VERTICAL LOCKUP","BOUNDED"),("MONOCHROME","DOCUMENTED")]
for i,(k,v) in enumerate(st):
    x = 72 + i*440
    txt(x, sy+78, k, "dim")
    txt(x, sy+98, v, "ok")
e('</svg>')
open("CTOOSProductionBoard.svg","w").write("\n".join(out))
import json
json.dump({"symbols":PLACEMENTS,"wordmarks":WORDMARKS}, open("placements.json","w"), indent=1)
print("written", len("\n".join(out)))

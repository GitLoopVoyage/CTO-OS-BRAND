from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

FP = "/usr/share/fonts/opentype/montserrat/Montserrat-Medium.otf"
import os
if not os.path.exists(FP):
    FP = "/usr/share/fonts/truetype/montserrat/Montserrat-Medium.ttf"
f = TTFont(FP)
upm = f['head'].unitsPerEm
cap = f['OS/2'].sCapHeight
gs = f.getGlyphSet()
cmap = f.getBestCmap()
hmtx = f['hmtx']
print("upm",upm,"cap",cap)

CAP_X = 6.0            # cap height in X units
TRACK = 0.02           # em tracking
s = CAP_X / cap        # scale: font units -> X units

def word(text, x0):
    """returns (pathdata, advance_end_x) in X units, baseline y=0, y-up flipped to SVG y-down"""
    pen_out = []
    x = x0
    for ch in text:
        gname = cmap[ord(ch)]
        adv = hmtx[gname][0]
        spp = SVGPathPen(gs)
        # transform: scale s, flip y, translate x
        t = Transform(s, 0, 0, -s, x, 0)
        tp = TransformPen(spp, t)
        gs[gname].draw(tp)
        d = spp.getCommands()
        if d: pen_out.append(d)
        x += adv * s + TRACK * upm * s
    x -= TRACK * upm * s   # remove trailing tracking
    return " ".join(pen_out), x

cto_d, cto_end = word("CTO", 0.0)
SPACE = 3.0
os_d, os_end = word("OS", cto_end + SPACE)
print("CTO width", round(cto_end,4))
print("total wordmark width", round(os_end,4))
open("wm_cto.txt","w").write(cto_d)
open("wm_os.txt","w").write(os_d)
open("wm_meta.txt","w").write("%.6f %.6f %.6f\n" % (cto_end, os_end - (cto_end+SPACE), os_end))

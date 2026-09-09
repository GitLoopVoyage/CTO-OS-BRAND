# -*- coding: utf-8 -*-
"""
CTO OS FRACTAL CORE MARK - CANONICAL VECTOR MASTER v2
Corrected under CTO_OS_FRACTAL_CORE_VECTOR_QA_1, finding VQA-01, MODEL B.

Three genuinely distinct nested open frames, each carrying exactly one gate.

CONSTRUCTION VARIABLES
  MASTER              10X x 10X
  FRAME STROKE        X            (all three frames)
  INTER-FRAME GAP     X/2          (uniform; see note)
  GATE WIDTH          2X           (all three gates)
  CENTRAL CORE        2X x 2X      (flush inside the inner frame)
  GATE ORIENTATION    outer = TOP, middle = LEFT, inner = BOTTOM

NOTE ON THE GAP
  Edge-to-core budget is 4X and must satisfy
      X(f1) + g1 + X(f2) + g2 + X(f3) + clearance = 4X
      => g1 + g2 + clearance = X
  No integer-X assignment leaves both gaps non-zero, so no integer-X master can
  carry three distinct frames. g1 = g2 = X/2, clearance = 0 is the unique
  uniform solution. The master therefore resolves on a half-X grid (20 x 20)
  while every frame stroke remains exactly X.

FRAME BOUNDS
  f1 OUTER   bbox 0.0 .. 10.0   ring 0.0-1.0 / 9.0-10.0
  f2 MIDDLE  bbox 1.5 ..  8.5   ring 1.5-2.5 / 7.5- 8.5
  f3 INNER   bbox 3.0 ..  7.0   ring 3.0-4.0 / 6.0- 7.0
  CORE       4.0 ..  6.0
"""

X            = 1.0
MASTER       = 10.0
STROKE       = X
GAP          = X / 2.0
GATE         = 2 * X
CORE         = 2 * X

def outer_frame():
    """f1, bbox 0..10, GATE = TOP (x 4..6)."""
    return [(0,0,4,1), (6,0,4,1),        # top run, split by the TOP gate
            (0,9,10,1),                  # bottom run
            (0,1,1,8), (9,1,1,8)]        # left / right runs

def middle_frame():
    """f2, bbox 1.5..8.5, GATE = LEFT (y 4..6)."""
    return [(1.5,1.5,7,1),               # top run
            (1.5,7.5,7,1),               # bottom run
            (1.5,2.5,1,1.5), (1.5,6,1,1.5),   # left run, split by the LEFT gate
            (7.5,2.5,1,5)]               # right run

def inner_frame():
    """f3, bbox 3..7, GATE = BOTTOM (x 4..6)."""
    return [(3,3,4,1),                   # top run
            (3,4,1,2), (6,4,1,2),        # left / right runs
            (3,6,1,1), (6,6,1,1)]        # bottom run, split by the BOTTOM gate

def master_frames():
    return outer_frame() + middle_frame() + inner_frame()

def master_core():
    return (4,4,2,2)

# centre-line arcs: one per frame, stroke X, butt caps, miter joins.
# Each arc is the frame's ring opened at its own gate.
ARCS = {
  "outer":  ("M6 0.5 L9.5 0.5 L9.5 9.5 L0.5 9.5 L0.5 0.5 L4 0.5", 34.0, "TOP"),
  "middle": ("M2 4 L2 2 L8 2 L8 8 L2 8 L2 6",                     22.0, "LEFT"),
  "inner":  ("M4 6.5 L3.5 6.5 L3.5 3.5 L6.5 3.5 L6.5 6.5 L6 6.5", 10.0, "BOTTOM"),
}

def fmt(v):
    return ("%g" % v)

def rects_to_path(rects):
    return " ".join("M%s %sh%sv%sh%sz" % (fmt(x), fmt(y), fmt(w), fmt(h), fmt(-w))
                    for (x,y,w,h) in rects)

if __name__ == "__main__":
    print(rects_to_path(master_frames()))
    print(rects_to_path([master_core()]))

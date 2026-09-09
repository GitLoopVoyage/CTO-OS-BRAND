/*!
 * CTO OS — Fractal Pulse
 * Loading / progression motion system for the Fractal Core mark.
 *
 * Geometry is locked to Fractal Core VECTOR MASTER v2 (VECTOR_CORRECTION_1,
 * Model B): three genuinely distinct nested open frames, stroke X, uniform X/2
 * inter-frame gap, 2X core flush inside f3. The three stroked arcs below
 * reproduce the canonical frame set at zero pixel difference; each arc is one
 * frame, opened at that frame's own gate (f1 = TOP, f2 = LEFT, f3 = BOTTOM).
 * Cobalt #2563EB is permitted on the central core only, and only while the
 * core is accountable.
 *
 * Usage:
 *   <script src="fractal-pulse.js"></script>
 *   <fractal-pulse state="working" size="120"></fractal-pulse>
 *   <fractal-pulse state="hold" hold-at="inner"></fractal-pulse>
 *   <fractal-pulse state="error" hold-at="middle" ink="#191C20"></fractal-pulse>
 *
 * Attributes
 *   state    idle | working | hold | complete | error      (default working)
 *   size     px, drives the master used (<32 px = micro)    (default 96)
 *   hold-at  outer | middle | inner   — required by hold and error
 *   ink      structural frame colour   (default #EDF0F3, use #191C20 on light)
 *
 * No dependencies. Honours prefers-reduced-motion by rendering the settled frame.
 */
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var CORE_COLOR = "#2563EB";
  var SIGNAL = "#E5484D";
  var IDLE = 0.65, ACTIVE = 0.90, CORE_IDLE = 0.85;

  /* ---- canonical master v2, 10X box ---------------------------------- */
  var MASTER = {
    box: 10, loop: 1750,
    arcs: [
      { id: "outer",  d: "M6 0.5 L9.5 0.5 L9.5 9.5 L0.5 9.5 L0.5 0.5 L4 0.5", len: 34 },
      { id: "middle", d: "M2 4 L2 2 L8 2 L8 8 L2 8 L2 6",                     len: 22 },
      { id: "inner",  d: "M4 6.5 L3.5 6.5 L3.5 3.5 L6.5 3.5 L6.5 6.5 L6 6.5", len: 10 }
    ],
    core: { x: 4, y: 4, w: 2, h: 2 },
    bars: [
      { w: 2,    h: 0.28, x: 4, axis: "y", from: 0.10, to: 1.25 },
      { w: 0.28, h: 2,    y: 4, axis: "x", from: 1.60, to: 2.95 },
      { w: 2,    h: 0.28, x: 4, axis: "y", from: 6.62, to: 6.02 }
    ],
    marks: {
      ignite: [0, 300],
      sweeps: [[300, 600], [600, 900], [900, 1200]],
      arrive: [1200, 1350], ack: [1350, 1600], settle: [1600, 1750]
    }
  };

  /* ---- micro master, 8X box, documented exception below 32 px --------- */
  var MICRO = {
    box: 8, loop: 1450,
    arcs: [
      { id: "outer",  d: "M5 0.5 L7.5 0.5 L7.5 7.5 L0.5 7.5 L0.5 0.5 L3 0.5", len: 26 },
      { id: "middle", d: "M2.5 5 L2.5 5.5 L5.5 5.5 L5.5 2.5 L2.5 2.5 L2.5 3", len: 10 }
    ],
    core: { x: 3, y: 3, w: 2, h: 2 },
    bars: [
      { w: 2,   h: 0.3, x: 3, axis: "y", from: 0.10, to: 1.70 },
      { w: 0.3, h: 2,   y: 3, axis: "x", from: 2.10, to: 2.90 }
    ],
    marks: {
      ignite: [0, 300],
      sweeps: [[300, 600], [600, 900]],
      arrive: [900, 1050], ack: [1050, 1300], settle: [1300, 1450]
    }
  };

  /* ---- cubic-bezier(0.4, 0, 0.2, 1) ----------------------------------- */
  function bezier(p1x, p1y, p2x, p2y) {
    function A(a, b) { return 1 - 3 * b + 3 * a; }
    function B(a, b) { return 3 * b - 6 * a; }
    function C(a) { return 3 * a; }
    function calc(t, a, b) { return ((A(a, b) * t + B(a, b)) * t + C(a)) * t; }
    function slope(t, a, b) { return 3 * A(a, b) * t * t + 2 * B(a, b) * t + C(a); }
    return function (x) {
      if (x <= 0) return 0;
      if (x >= 1) return 1;
      var t = x;
      for (var i = 0; i < 8; i++) {
        var s = slope(t, p1x, p2x);
        if (s === 0) break;
        t -= (calc(t, p1x, p2x) - x) / s;
      }
      return calc(t, p1y, p2y);
    };
  }
  var EASE = bezier(0.4, 0, 0.2, 1);
  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }
  function seg(t, a, b) { return clamp((t - a) / (b - a), 0, 1); }
  function svgEl(n, attrs) {
    var e = document.createElementNS(NS, n);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }

  /* ---- shared clock: every instance on the page stays in phase -------- */
  var subscribers = [];
  var ticking = false;
  var origin = null;
  function tick(ts) {
    if (origin === null) origin = ts;
    var e = ts - origin;
    for (var i = 0; i < subscribers.length; i++) subscribers[i](e);
    if (subscribers.length) requestAnimationFrame(tick);
    else ticking = false;
  }
  function subscribe(fn) {
    subscribers.push(fn);
    if (!ticking) { ticking = true; requestAnimationFrame(tick); }
    return function () {
      var i = subscribers.indexOf(fn);
      if (i > -1) subscribers.splice(i, 1);
    };
  }

  /* ---- renderer -------------------------------------------------------- */
  function Renderer(root, opts) {
    this.size = opts.size || 96;
    this.state = opts.state || "working";
    this.holdAt = opts.holdAt || null;
    this.ink = opts.ink || "#EDF0F3";
    this.G = this.size < 32 ? MICRO : MASTER;
    this.loop = this.G.loop;
    this.marks = this.G.marks;
    this.build(root);
  }

  Renderer.prototype.build = function (root) {
    var G = this.G, self = this;
    var svg = svgEl("svg", {
      viewBox: "0 0 " + G.box + " " + G.box,
      width: this.size, height: this.size,
      "aria-hidden": "true", focusable: "false"
    });
    svg.style.display = "block";
    var g = svgEl("g", {
      fill: "none", stroke: this.ink, "stroke-width": 1,
      "stroke-linecap": "butt", "stroke-linejoin": "miter", "stroke-miterlimit": 10
    });
    this.base = []; this.swept = []; this.comet = [];
    G.arcs.forEach(function (a) {
      var b = svgEl("path", { d: a.d, opacity: IDLE });
      g.appendChild(b); self.base.push(b);

      var w = svgEl("path", { d: a.d, opacity: 0, "stroke-dasharray": "0 " + (a.len + 1) });
      g.appendChild(w); self.swept.push(w);

      // three stacked dashes make the comet: long faint tail -> short bright head
      self.comet.push([[3.2, 0.20], [1.2, 0.45], [0.42, 1]].map(function (cfg) {
        var c = svgEl("path", {
          d: a.d, opacity: 0,
          "stroke-dasharray": cfg[0] + " " + (a.len + cfg[0] + 1)
        });
        c._seg = cfg[0]; c._max = cfg[1];
        g.appendChild(c);
        return c;
      }));
    });
    svg.appendChild(g);

    this.bars = G.bars.map(function (b) {
      var r = svgEl("rect", { width: b.w, height: b.h, fill: self.ink, opacity: 0 });
      if (b.axis === "y") r.setAttribute("x", b.x); else r.setAttribute("y", b.y);
      svg.appendChild(r);
      return r;
    });

    var c = G.core;
    this.core = svgEl("rect", { x: c.x, y: c.y, width: c.w, height: c.h, fill: CORE_COLOR, opacity: CORE_IDLE });
    this.core.style.transformBox = "view-box";
    this.core.style.transformOrigin = (c.x + c.w / 2) + "px " + (c.y + c.h / 2) + "px";
    svg.appendChild(this.core);

    root.appendChild(svg);
    this.svg = svg;
  };

  Renderer.prototype.stopIndex = function () {
    if ((this.state !== "hold" && this.state !== "error") || !this.holdAt) return -1;
    for (var k = 0; k < this.G.arcs.length; k++) if (this.G.arcs[k].id === this.holdAt) return k;
    return this.G.arcs.length - 1;
  };
  Renderer.prototype.haltTime = function () {
    var i = this.stopIndex();
    return i < 0 ? this.loop : this.marks.sweeps[i][1];
  };
  Renderer.prototype.setSwept = function (i, p) {
    var L = this.G.arcs[i].len, v = p * L;
    this.swept[i].setAttribute("stroke-dasharray", v + " " + (L + 1));
    this.swept[i].setAttribute("opacity", v > 0.001 ? ACTIVE : 0);
  };
  Renderer.prototype.setComet = function (i, p, vis, color) {
    var L = this.G.arcs[i].len, ink = color || this.ink;
    this.comet[i].forEach(function (c) {
      c.setAttribute("stroke-dashoffset", c._seg - p * L);
      c.setAttribute("opacity", vis * c._max);
      c.setAttribute("stroke", ink);
    });
  };
  Renderer.prototype.clearComet = function (i) {
    this.comet[i].forEach(function (c) { c.setAttribute("opacity", 0); });
  };
  Renderer.prototype.setBar = function (i, p, vis) {
    var b = this.G.bars[i], r = this.bars[i];
    var pos = b.from + (b.to - b.from) * EASE(p);
    if (b.axis === "y") r.setAttribute("y", pos); else r.setAttribute("x", pos);
    r.setAttribute("opacity", vis);
    r.setAttribute("fill", this.ink);
  };
  Renderer.prototype.settled = function () {
    var self = this;
    this.G.arcs.forEach(function (a, i) { self.setSwept(i, 1); self.clearComet(i); });
    this.bars.forEach(function (r) { r.setAttribute("opacity", 0); });
    this.core.setAttribute("fill", CORE_COLOR);
    this.core.setAttribute("opacity", 1);
    this.core.style.transform = "scale(1)";
  };

  Renderer.prototype.render = function (t, now) {
    if (now === undefined) now = t;
    var self = this, M = this.marks, G = this.G, n = G.arcs.length;
    var stopAt = this.stopIndex();

    if (this.state === "idle") {
      G.arcs.forEach(function (a, i) { self.setSwept(i, 0); self.clearComet(i); });
      this.bars.forEach(function (r) { r.setAttribute("opacity", 0); });
      this.core.setAttribute("fill", CORE_COLOR);
      this.core.setAttribute("opacity", 0.85 + 0.08 * (0.5 - 0.5 * Math.cos(now / 4000 * Math.PI * 2)));
      this.core.style.transform = "scale(1)";
      return;
    }

    // 1. core ignition — the request has arrived, nothing is evaluated yet
    var ig = seg(t, M.ignite[0], M.ignite[1]);
    var accountable = (this.state !== "hold" && this.state !== "error");
    var op, sc = 1;
    if (accountable) {
      op = 0.45 + 0.55 * EASE(ig);
      sc = 0.92 + 0.08 * EASE(ig);
      this.core.setAttribute("fill", CORE_COLOR);
    } else {
      op = IDLE;
      this.core.setAttribute("fill", this.ink); // never cobalt while nothing is accountable
    }

    // 2. inward governance sweep — one arc per gate, in gate order
    for (var i = 0; i < n; i++) {
      if (stopAt >= 0 && i > stopAt) { this.setSwept(i, 0); this.clearComet(i); continue; }
      var raw = seg(t, M.sweeps[i][0], M.sweeps[i][1]);
      var p = EASE(raw);
      var partial = (stopAt === i) ? 0.55 : 1;
      var pp = Math.min(p, partial);
      this.setSwept(i, pp);
      if (stopAt === i && p >= partial) {
        var breath = 0.55 + 0.45 * (0.5 - 0.5 * Math.cos((now / 1200) * Math.PI * 2));
        this.setComet(i, partial, breath, this.state === "error" ? SIGNAL : null);
      } else if (raw > 0 && raw < 1) {
        this.setComet(i, pp, 1, null);
      } else this.clearComet(i);
    }

    // gate passage bars — suppressed on the micro master and past a halt
    for (var b = 0; b < this.bars.length; b++) {
      var bp = seg(t, M.sweeps[b][1] - 40, M.sweeps[b][1] + 170);
      var show = (stopAt < 0 || b < stopAt) && this.size >= 32;
      if (show && bp > 0 && bp < 1) this.setBar(b, bp, Math.sin(bp * Math.PI) * 0.95);
      else this.bars[b].setAttribute("opacity", 0);
    }

    // 3. core acknowledgement — one restrained pulse, then settle
    if (accountable) {
      if (t >= M.ack[0] && t <= M.ack[1]) {
        var ap = seg(t, M.ack[0], M.ack[1]);
        var tri = ap < 0.5 ? EASE(ap * 2) : EASE(1 - (ap - 0.5) * 2);
        sc = 1 + 0.07 * tri;
        op = 1 - 0.18 * tri;
      } else if (t > M.ack[1] && this.state !== "complete") {
        op = 1 - (1 - CORE_IDLE) * EASE(seg(t, M.settle[0], M.settle[1]));
        sc = 1;
      }
      if (this.state === "complete" && t >= M.ack[1]) { op = 1; sc = 1; }
    }
    if (this.state !== "complete" && t >= M.settle[0] && accountable) {
      var dp = EASE(seg(t, M.settle[0], M.settle[1]));
      for (var j = 0; j < n; j++) this.setSwept(j, 1 - dp);
    }
    this.core.setAttribute("opacity", op);
    this.core.style.transform = "scale(" + sc + ")";
  };

  /* ---- custom element -------------------------------------------------- */
  var REDUCED = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function FractalPulse() { return Reflect.construct(HTMLElement, [], FractalPulse); }
  FractalPulse.prototype = Object.create(HTMLElement.prototype);
  FractalPulse.prototype.constructor = FractalPulse;
  Object.setPrototypeOf(FractalPulse, HTMLElement);

  FractalPulse.observedAttributes = ["state", "size", "hold-at", "ink"];

  FractalPulse.prototype.connectedCallback = function () {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    this.mount();
  };
  FractalPulse.prototype.disconnectedCallback = function () {
    if (this._unsub) this._unsub();
    this._unsub = null;
  };
  FractalPulse.prototype.attributeChangedCallback = function () {
    if (this.shadowRoot) this.mount();
  };

  FractalPulse.prototype.mount = function () {
    if (this._unsub) this._unsub();
    this.shadowRoot.innerHTML = "<style>:host{display:inline-block;line-height:0}</style>";

    var r = new Renderer(this.shadowRoot, {
      size: parseInt(this.getAttribute("size"), 10) || 96,
      state: this.getAttribute("state") || "working",
      holdAt: this.getAttribute("hold-at"),
      ink: this.getAttribute("ink")
    });
    this._renderer = r;

    if (REDUCED) { r.settled(); return; }

    var halted = (r.state === "hold" || r.state === "error");
    this._unsub = subscribe(function (e) {
      var t;
      if (halted) t = Math.min(e, r.haltTime());
      else if (r.state === "complete") t = Math.min(e % (r.loop + 900), r.loop);
      else t = e % r.loop;
      r.render(t, e);
    });
  };

  if (!window.customElements.get("fractal-pulse")) {
    window.customElements.define("fractal-pulse", FractalPulse);
  }

  window.FractalPulse = { Renderer: Renderer, MASTER: MASTER, MICRO: MICRO, EASE: EASE, subscribe: subscribe };
})();

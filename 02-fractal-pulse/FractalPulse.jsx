/*!
 * CTO OS — Fractal Pulse (React)
 *
 * Thin wrapper over the framework-agnostic renderer in fractal-pulse.js.
 * Import that file once (side-effect import registers <fractal-pulse> and
 * publishes window.FractalPulse), then use this component anywhere.
 *
 *   import './fractal-pulse.js';
 *   import FractalPulse from './FractalPulse';
 *
 *   <FractalPulse state="working" size={120} />
 *   <FractalPulse state="hold" holdAt="inner" label="Waiting for required evidence" />
 *
 * Props
 *   state    'idle' | 'working' | 'hold' | 'complete' | 'error'   default 'working'
 *   size     number, px. Below 32 the micro master is used.        default 96
 *   holdAt   'outer' | 'middle' | 'inner'  — required by hold and error
 *   ink      structural frame colour. '#EDF0F3' on dark, '#191C20' on light.
 *   label    optional visible caption; also becomes the accessible name.
 *
 * Honesty rule: `state` and `holdAt` are assertions about the system. Drive them
 * from real events, or leave state at 'working' with generic copy. Never animate
 * stage names the backend has not reported.
 */
import React, { useEffect, useRef } from 'react';

const REDUCED =
  typeof window !== 'undefined' &&
  window.matchMedia &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export default function FractalPulse({
  state = 'working',
  size = 96,
  holdAt = null,
  ink = '#EDF0F3',
  label = null,
  className,
  style,
}) {
  const hostRef = useRef(null);

  useEffect(() => {
    const host = hostRef.current;
    if (!host || !window.FractalPulse) return;
    host.innerHTML = '';

    const r = new window.FractalPulse.Renderer(host, { size, state, holdAt, ink });

    if (REDUCED) {
      r.settled();
      return () => { host.innerHTML = ''; };
    }

    const halted = state === 'hold' || state === 'error';
    const unsub = window.FractalPulse.subscribe((e) => {
      let t;
      if (halted) t = Math.min(e, r.haltTime());
      else if (state === 'complete') t = Math.min(e % (r.loop + 900), r.loop);
      else t = e % r.loop;
      r.render(t, e);
    });

    return () => { unsub(); host.innerHTML = ''; };
  }, [state, size, holdAt, ink]);

  return (
    <span
      className={className}
      style={{ display: 'inline-flex', flexDirection: 'column', alignItems: 'center', gap: 14, ...style }}
      role="status"
      aria-live="polite"
      aria-label={label || (state === 'working' ? 'Working' : state)}
    >
      <span ref={hostRef} aria-hidden="true" style={{ lineHeight: 0 }} />
      {label ? (
        <span
          style={{
            fontFamily: 'IBM Plex Mono, ui-monospace, monospace',
            fontSize: 11,
            letterSpacing: '0.15em',
            textTransform: 'uppercase',
            color: ink === '#EDF0F3' ? '#7C8794' : '#5D6874',
          }}
        >
          {label}
        </span>
      ) : null}
    </span>
  );
}

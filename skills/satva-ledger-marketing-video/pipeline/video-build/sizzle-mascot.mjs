// Satva agent mascot: an original SVG character in the brand palette only
// (#1d83b8 blue, white, #6d6d6d grey, #111 ink). Returns markup + GSAP-line helpers bound to a timeline-lines array.
export function makeMascot(tw) {
  const mascot = (p, x, y, w) => `<svg id="${p}" class="abs mas" viewBox="0 0 200 230" style="left:${x}px;top:${y}px;width:${w}px;height:${Math.round(w * 1.15)}px;overflow:visible">
  <ellipse cx="100" cy="218" rx="58" ry="8" fill="rgba(17,17,17,.10)"/>
  <g id="${p}-all">
    <ellipse cx="72" cy="200" rx="22" ry="10" fill="#6d6d6d"/><ellipse cx="128" cy="200" rx="22" ry="10" fill="#6d6d6d"/>
    <line x1="100" y1="34" x2="100" y2="58" stroke="#6d6d6d" stroke-width="6" stroke-linecap="round"/>
    <circle cx="100" cy="26" r="13" fill="#fff" stroke="#1d83b8" stroke-width="6"/>
    <g id="${p}-armL"><ellipse cx="20" cy="142" rx="15" ry="11" fill="#1d83b8"/></g>
    <g id="${p}-armR"><ellipse cx="180" cy="142" rx="15" ry="11" fill="#1d83b8"/></g>
    <rect x="28" y="56" width="144" height="142" rx="46" fill="#1d83b8"/>
    <rect x="44" y="80" width="112" height="78" rx="30" fill="#fff"/>
    <g id="${p}-eyesN"><ellipse cx="78" cy="114" rx="9" ry="12" fill="#111"/><ellipse cx="122" cy="114" rx="9" ry="12" fill="#111"/><circle cx="81" cy="109" r="3" fill="#fff"/><circle cx="125" cy="109" r="3" fill="#fff"/></g>
    <g id="${p}-eyesH" class="hide"><path d="M66 118 q12 -18 24 0" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M110 118 q12 -18 24 0" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/></g>
    <circle cx="62" cy="136" r="8" fill="#1d83b8" opacity=".22"/><circle cx="138" cy="136" r="8" fill="#1d83b8" opacity=".22"/>
    <path id="${p}-smile" d="M88 136 q12 12 24 0" stroke="#111" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path id="${p}-open" class="hide" d="M86 132 q14 24 28 0 z" fill="#111" stroke="#111" stroke-width="4" stroke-linejoin="round"/>
    <ellipse id="${p}-o" class="hide" cx="100" cy="139" rx="7" ry="9" fill="#111"/>
    <path id="${p}-flat" class="hide" d="M90 141 h20" stroke="#111" stroke-width="6" stroke-linecap="round"/>
    <circle cx="100" cy="176" r="12" fill="#fff"/><text x="100" y="182" text-anchor="middle" font-family="Mulish" font-weight="700" font-size="17" fill="#111">S</text>
    <g id="${p}-q" class="hide"><circle cx="160" cy="42" r="22" fill="#fff" stroke="#1d83b8" stroke-width="5"/><text x="160" y="52" text-anchor="middle" font-family="Mulish" font-weight="700" font-size="30" fill="#1d83b8">?</text></g>
  </g></svg>`;

  // mood -> opacity of [smile, open, o, flat, eyesN, eyesH, q] plus eye y-offset
  const MOOD = { idle: [1, 0, 0, 0, 1, 0, 0, 0], work: [1, 0, 0, 0, 1, 0, 0, 5], happy: [0, 1, 0, 0, 0, 1, 0, 0], surprise: [0, 0, 1, 0, 1, 0, 0, 0], puzzled: [0, 0, 0, 1, 1, 0, 1, 0] };
  const parts = ["smile", "open", "o", "flat", "eyesN", "eyesH", "q"];
  const r = (t) => +t.toFixed(3);
  const mMood = (p, t, m) => {
    const v = MOOD[m];
    parts.forEach((g, i) => tw.push(`tl.set("#${p}-${g}",{opacity:${v[i]}},${r(t)});`));
    tw.push(`tl.set("#${p}-eyesN",{y:${v[7]}},${r(t)});`);
  };
  const mIn = (p, t) => tw.push(`tl.from("#${p}",{scale:.3,opacity:0,transformOrigin:"50% 100%",duration:.5,ease:"back.out(2)"},${r(t)});`);
  const mBob = (p, t0, t1) => tw.push(`tl.to("#${p}-all",{y:-9,duration:.522,yoyo:true,repeat:${Math.max(1, Math.round((t1 - t0) / 0.522) - 1)},ease:"sine.inOut"},${r(t0)});`);
  const mBlink = (p, ts) => ts.forEach((t) => tw.push(`tl.to("#${p}-eyesN",{scaleY:.1,svgOrigin:"100 114",duration:.07,yoyo:true,repeat:1},${r(t)});`));
  const mWave = (p, t) => tw.push(`tl.to("#${p}-armR",{rotation:-60,svgOrigin:"172 134",duration:.26,yoyo:true,repeat:5,ease:"sine.inOut"},${r(t)});`);
  const mHop = (p, t) => tw.push(`tl.fromTo("#${p}",{y:0},{y:-26,duration:.18,yoyo:true,repeat:1,ease:"power2.out"},${r(t)});`);
  return { mascot, mMood, mIn, mBob, mBlink, mWave, mHop };
}

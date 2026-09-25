// Original SVG mascot character, brand-palette-parameterized (no fixed colors, no copyrighted assets).
// Used only by themes that opt into `useMascot: true`. Returns markup + GSAP-line helpers bound to a
// timeline-lines array (`tw`), same contract build-sizzle.mjs proved out for the Satva Ledger video.
//
// `variant`: "default" (antenna, no gender markers) | "bow" (a bow instead of an antenna tip, plus
// eyelashes) | "spark" (a lightning-bolt tip + a star chest badge, energetic/confident read) —
// three distinct original designs, not recolors of the same character. `ribbon` picks the bow's
// or spark's accent color; defaults to a warm coral (bow) / amber (spark).
export function makeMascot(tw, accent = "#1d83b8", ink = "#111111", grey = "#6d6d6d", variant = "default", ribbon) {
  const bow = variant === "bow";
  const spark = variant === "spark";
  ribbon = ribbon || (spark ? "#f5a623" : "#ef5da8");
  const tip = bow
    ? `<g transform="translate(100,24)"><path d="M0 0 L-16 -9 Q-20 0 -16 9 Z" fill="${ribbon}"/><path d="M0 0 L16 -9 Q20 0 16 9 Z" fill="${ribbon}"/><circle r="5" fill="${ribbon}" stroke="#fff" stroke-width="1.5"/></g>`
    : spark
    ? `<path transform="translate(84,10)" d="M20 0 L4 18 H14 L0 38 L26 14 H15 Z" fill="${ribbon}" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/>`
    : `<circle cx="100" cy="26" r="13" fill="#fff" stroke="${accent}" stroke-width="6"/>`;
  const lashes = bow
    ? `<path d="M70 100 l-6 -6M78 97 l-3 -8M86 97 l1 -8" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>
       <path d="M130 100 l6 -6M122 97 l3 -8M114 97 l-1 -8" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>`
    : "";
  const chestMark = spark
    ? `<path d="M100 168 l3.5 7.5 8 .8 -6 5.6 1.8 8 -7.3 -4.3 -7.3 4.3 1.8-8 -6-5.6 8-.8z" fill="${ribbon}"/>`
    : `<text x="100" y="182" text-anchor="middle" font-family="inherit" font-weight="700" font-size="17" fill="${ink}">•</text>`;
  const mascot = (p, x, y, w) => `<svg id="${p}" class="abs mas" viewBox="0 0 200 230" style="left:${x}px;top:${y}px;width:${w}px;height:${Math.round(w * 1.15)}px;overflow:visible">
  <ellipse cx="100" cy="218" rx="58" ry="8" fill="rgba(17,17,17,.10)"/>
  <g id="${p}-all">
    <ellipse cx="72" cy="200" rx="22" ry="10" fill="${grey}"/><ellipse cx="128" cy="200" rx="22" ry="10" fill="${grey}"/>
    <line x1="100" y1="34" x2="100" y2="58" stroke="${grey}" stroke-width="6" stroke-linecap="round"/>
    ${tip}
    <g id="${p}-armL"><ellipse cx="20" cy="142" rx="15" ry="11" fill="${accent}"/></g>
    <g id="${p}-armR"><ellipse cx="180" cy="142" rx="15" ry="11" fill="${accent}"/></g>
    <rect x="28" y="56" width="144" height="142" rx="46" fill="${accent}"/>
    <rect x="44" y="80" width="112" height="78" rx="30" fill="#fff"/>
    <g id="${p}-eyesN"><ellipse cx="78" cy="114" rx="9" ry="12" fill="${ink}"/><ellipse cx="122" cy="114" rx="9" ry="12" fill="${ink}"/><circle cx="81" cy="109" r="3" fill="#fff"/><circle cx="125" cy="109" r="3" fill="#fff"/>${lashes}</g>
    <g id="${p}-eyesH" class="hide"><path d="M66 118 q12 -18 24 0" stroke="${ink}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M110 118 q12 -18 24 0" stroke="${ink}" stroke-width="6" fill="none" stroke-linecap="round"/></g>
    <circle cx="62" cy="136" r="8" fill="${(bow || spark) ? ribbon : accent}" opacity=".22"/><circle cx="138" cy="136" r="8" fill="${(bow || spark) ? ribbon : accent}" opacity=".22"/>
    <path id="${p}-smile" d="M88 136 q12 12 24 0" stroke="${ink}" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path id="${p}-open" class="hide" d="M86 132 q14 24 28 0 z" fill="${ink}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>
    <ellipse id="${p}-o" class="hide" cx="100" cy="139" rx="7" ry="9" fill="${ink}"/>
    <path id="${p}-flat" class="hide" d="M90 141 h20" stroke="${ink}" stroke-width="6" stroke-linecap="round"/>
    <circle cx="100" cy="176" r="12" fill="#fff"/>${chestMark}
    <g id="${p}-q" class="hide"><circle cx="160" cy="42" r="22" fill="#fff" stroke="${accent}" stroke-width="5"/><text x="160" y="52" text-anchor="middle" font-family="inherit" font-weight="700" font-size="30" fill="${accent}">?</text></g>
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

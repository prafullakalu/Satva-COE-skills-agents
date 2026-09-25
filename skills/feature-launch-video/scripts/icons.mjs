// Generic outline icon set (product-agnostic shapes) shared by every theme's intro icon-wall.
// Original strokes, no external icon library — pick names by what the flow step is about.
export const ICON = {
  tray: '<svg viewBox="0 0 24 24"><path d="M12 3v11m0 0l-4-4m4 4l4-4M4 15v4h16v-4"/></svg>',
  scale: '<svg viewBox="0 0 24 24"><path d="M12 4v16M6 20h12M5 8h14M5 8l-3 7a3.5 3.5 0 007 0zM19 8l-3 7a3.5 3.5 0 007 0z"/></svg>',
  users: '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 3-6 6.5-6s6.5 2.4 6.5 6M16 5a3.5 3.5 0 010 7M18 14c2.5.6 4 2.6 4 6"/></svg>',
  tag: '<svg viewBox="0 0 24 24"><path d="M3 12V4h8l10 10-8 8zM7.5 8.5h.01"/></svg>',
  chart: '<svg viewBox="0 0 24 24"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
  shield: '<svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM8.5 12l2.5 2.5 4.5-5"/></svg>',
  link: '<svg viewBox="0 0 24 24"><path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/></svg>',
  clock: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>',
  bell: '<svg viewBox="0 0 24 24"><path d="M6 10a6 6 0 0112 0c0 5 2 6 2 6H4s2-1 2-6zM10 20a2 2 0 004 0"/></svg>',
  check: '<svg viewBox="0 0 24 24"><path d="M4 12l6 6L20 6"/></svg>',
  bolt: '<svg viewBox="0 0 24 24"><path d="M13 2L3 14h7l-1 8 11-14h-7l0-6z"/></svg>',
};
export const WALL = Object.keys(ICON);

// visual -> a sensible default icon when a flow step doesn't name one
export const VISUAL_ICON = { card: "tray", stat: "chart", approval: "shield", chat: "users", list: "tag", compare: "scale" };

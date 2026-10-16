/**
 * Tekken 8 Movepedia - Interactive Vanilla JavaScript Application.
 * Powers the design-matched UI:
 * - 43 Character Roster Carousel with smooth navigation
 * - Sidebar Quick Fighter selection & Featured Moves
 * - Stages showcase with photorealistic & vector battlegrounds
 * - 4-Mode Real-Time Notation Engine (Arrows, English, Numpad, Controller)
 * - Dynamic Move Reference & Frame Data Table
 * - Data Quality Coverage & Sources Audit
 */

// Session Token Management for User Preferences
function getOrCreateSessionToken() {
  let token = localStorage.getItem('tekken8_session_token');
  if (!token) {
    token = 't8_sess_' + Math.random().toString(36).substring(2, 10) + '_' + Date.now();
    localStorage.setItem('tekken8_session_token', token);
  }
  return token;
}

// XSS Safe HTML String Escaper
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// Global State
const state = {
  characters: [],
  selectedCharacter: null,
  activeFilter: 'ALL',
  controllerLayout: 'PLAYSTATION',
  currentNotation: 'df+2',
  moves: [],
  movesPagination: {
    currentPage: 1,
    pageSize: 10,
    filteredMoves: []
  },
  sources: [],
  coverage: null,
  sessionToken: getOrCreateSessionToken(),
  matchup: {
    player: null,
    opponent: null,
    stage: null,
    conditions: {
      wall_position: 'OPEN',
      heat_state: 'AVAILABLE',
      starting_distance: 'MID',
      player_side: 'P1'
    },
    matchupPerspective: 'P1_VS_P2',
    matchupStartupFilter: 'ALL',
    matchupStanceFilter: 'ALL',
    usefulMovesPerspective: 'p1'
  },
  stageStrategy: {
    currentReport: null,
    comboFilter: {
      type: 'ALL',
      requiresHeat: false,
      requiresCH: false,
      difficulty: 'ALL'
    }
  },
  combosPhase5: {
    recommendations: null,
    activeCategory: 'ALL',
    activeDifficulty: 'ALL',
    activeHurtbox: 'ALL',
    searchQuery: '',
    requiresHeat: false,
    requiresCH: false,
    currentModalCombo: null,
    sandboxHits: [
      { raw: 25, notation: 'Hit 1 (Starter)' },
      { raw: 18, notation: 'Hit 2' },
      { raw: 22, notation: 'Hit 3 (Tornado)' },
      { raw: 15, notation: 'Hit 4' },
      { raw: 20, notation: 'Hit 5 (Ender)' },
    ]
  },
  comboFinder: {
    perspective: 'P1', // 'P1', 'P2', 'DUAL'
    p1Slug: 'jin',
    p2Slug: 'kazuya',
    stageId: 1,
    category: 'ALL',
    starterType: 'ALL',
    difficulty: 'ALL',
    wallFilter: 'ALL',
    stanceFilter: 'ALL',
    minDamage: null,
    maxDamage: null,
    search: '',
    p1Combos: [],
    p2Combos: [],
    p1Report: null,
    p2Report: null,
    expandedSteps: new Set(),
    compareList: []
  },
  roster: {
    viewMode: 'grid',
    searchQuery: '',
    sortOrder: 'NAME_ASC',
    activeFilter: 'ALL'
  },
  movesSafetyFilter: 'ALL',
  activeMatchupTab: 'panel-overview',
  viewAllMatchup: false,
  admin: {
    key: 'tekken8-fyp-admin-secret-2026',
    user: 'Lead Lab Architect',
    currentTab: 'tabIssues',
    dashboardData: null,
    previewResponse: null
  },
  stages: [
    {
      id: 1,
      slug: "the-arena",
      name: "The Arena",
      location: "Mishima Zaibatsu Stadium",
      image: "/assets/img/stages/arena.jpg",
      hazards: ["Wall Bound", "Floor Blast"],
      gimmick: "Octagonal championship cage with giant jumbotron screens"
    },
    {
      id: "urban-square",
      name: "Urban Square",
      location: "Times Square, New York",
      image: "/assets/img/stages/urban-square.jpg",
      hazards: ["Wall Break", "Balcony Break"],
      gimmick: "Rain-slicked neon metropolitan streets with breakable glass barriers"
    },
    {
      id: "yakushima",
      name: "Yakushima",
      location: "Sacred Misty Forest, Japan",
      image: "/assets/img/stages/yakushima.jpg",
      hazards: ["Hard Wall Break"],
      gimmick: "Ancient mystical mossy cedar forest with morning fog and sacred shrines"
    },
    {
      id: "rebel-hangar",
      name: "Rebel Hangar",
      location: "Yggdrasil Military Base",
      image: "/assets/img/stages/rebel-hangar.jpg",
      hazards: ["Wall Blast", "Floor Break"],
      gimmick: "High-tech military fortress with combat mechs and attack jets"
    },
    {
      id: "sanctum",
      name: "Sanctum",
      location: "Subterranean Magma Ruins",
      image: "/assets/img/stages/sanctum.jpg",
      hazards: ["Floor Break", "Hard Wall Break"],
      gimmick: "Ancient volcanic sacrificial temple with cascading lava pools"
    },
    {
      id: "stratosphere",
      name: "Into the Stratosphere",
      location: "Outer Atmosphere Orbit",
      image: "/assets/img/stages/stratosphere.jpg",
      hazards: ["Wall Blast", "Floor Blast"],
      gimmick: "Zero-gravity cataclysmic battle atop orbital meteor debris"
    },
    {
      id: "ortiz-farm",
      name: "Ortiz Farm",
      location: "Andes Coffee Valley, Peru",
      image: "/assets/img/stages/ortiz-farm.jpg",
      hazards: ["Balcony Break", "Floor Break"],
      gimmick: "Sunlit Peruvian mountain terrace coffee plantation"
    },
    {
      id: "coliseum",
      name: "Colosseum",
      location: "Ancient Imperial Arena, Italy",
      image: "/assets/img/stages/coliseum.jpg",
      hazards: ["Wall Break"],
      gimmick: "Timeless Roman amphitheater bathed in golden sunset glow"
    },
    {
      id: "celebration-on-the-seine",
      name: "Celebration on the Seine",
      location: "River Seine Cruise, France",
      image: "/assets/img/stages/celebration-on-the-seine.jpg",
      hazards: ["Balcony Break"],
      gimmick: "Parisian festival riverboat with Eiffel Tower fireworks in the night sky"
    },
    {
      id: "midnight-siege",
      name: "Midnight Siege",
      location: "G Corp Skyscraper Rooftop",
      image: "/assets/img/stages/midnight-siege.jpg",
      hazards: ["Wall Blast", "Floor Break"],
      gimmick: "Thunderstorm siege on G Corporation executive headquarters"
    },
    {
      id: "urban-square-evening",
      name: "Urban Square (Evening)",
      location: "Times Square Evening, New York",
      image: "/assets/img/stages/urban-square-evening.svg",
      hazards: ["Wall Break", "Balcony Break"],
      gimmick: "Evening dusk neon metropolitan crossing with intense advertising billboards"
    },
    {
      id: "arena-underground",
      name: "The Arena (Underground)",
      location: "Subterranean Fighting Pit",
      image: "/assets/img/stages/arena-underground.svg",
      hazards: ["Floor Blast", "Wall Bound"],
      gimmick: "Subterranean brutal cage fighting ring with reinforced steel boundaries"
    },
    {
      id: "elegant-palace",
      name: "Elegant Palace",
      location: "European Chateau Courtyard",
      image: "/assets/img/stages/elegant-palace.svg",
      hazards: ["Balcony Break", "Hard Wall Break"],
      gimmick: "Baroque European chateau garden with multi-tiered destructible marble balconies"
    },
    {
      id: "descent-into-subconscious",
      name: "Descent into Subconscious",
      location: "Abyss of the Mind",
      image: "/assets/img/stages/descent-into-subconscious.svg",
      hazards: ["Floor Break", "Floor Blast"],
      gimmick: "Surreal metaphysical void with shattering crystalline pathways"
    },
    {
      id: "secluded-training-ground",
      name: "Secluded Training Ground",
      location: "Mountain Dojo, Japan",
      image: "/assets/img/stages/secluded-training-ground.svg",
      hazards: ["Wall Break"],
      gimmick: "Isolated mountain dojo surrounded by bamboo forests and wooden palisades"
    },
    {
      id: "genmaji-temple",
      name: "Genmaji Temple",
      location: "Autumn Mountain Sanctuary, Japan",
      image: "/assets/img/stages/genmaji-temple.svg",
      hazards: ["Hard Wall Break", "Wall Break"],
      gimmick: "Ancient mountain temple courtyard flanked by fiery red autumn maple leaves"
    }
  ]
};

// Martial Art Subtitles
const FIGHTING_STYLES = {
  'jin': 'Mishima-Style Karate',
  'kazuya': 'Mishima Style Fighting Karate',
  'reina': 'Taido / Mishima-Style',
  'jun': 'Kazama-Style Traditional Martial Arts',
  'king': 'Pro Wrestling',
  'paul': 'Integrated Martial Arts based on Judo',
  'hwoarang': 'Taekwondo',
  'alisa': 'Thruster-Based High Mobility Combat',
  'asuka': 'Kazama-Style Traditional Martial Arts',
  'azucena': 'Rumi Maki',
  'bryan': 'Kickboxing',
  'claudio': 'Sirius Exorcism Sorcery',
  'devil-jin': 'Advanced Mishima Style',
  'dragunov': 'Commando Sambo',
  'feng': 'Chinese Martial Arts (God Fist)',
  'heihachi': 'Original Mishima-Style Karate',
  'jack-8': 'Brute Force / Firepower',
  'lars': 'Tekken Forces Martial Arts',
  'law': 'Martial Arts (Jeet Kune Do)',
  'lee': 'Martial Arts / Hitman Style',
  'leo': 'Baji Quan',
  'leroy': 'Wing Chun',
  'lidia': 'Traditional Karate',
  'lili': 'Street Gymnastics & Ballet',
  'nina': 'Assassination Martial Arts',
  'panda': 'Heihachi-Style Advanced Kuma Shin Ken',
  'kuma': 'Heihachi-Style Advanced Kuma Shin Ken',
  'raven': 'Ninjutsu',
  'shaheen': 'Military Close Quarters Combat',
  'steve': 'Boxing',
  'victor': 'Super Spy CQB & Tactical Blade',
  'xiaoyu': 'Bagua Zhang & Pigua Quan',
  'yoshimitsu': 'Manji Ninjutsu',
  'zafina': 'Ancient Assassination Arts',
  'eddy': 'Capoeira',
  'clive': 'Rosarian Swordplay',
  'anna': 'Assassination Martial Arts',
  'armor-king': 'Lucha Libre & Pro Wrestling',
  'bob': 'Freestyle Karate',
  'fahkumram': 'Muay Thai',
  'kunimitsu': 'Manji Clan Ninjutsu',
  'miary-zo': 'Savate / Kickboxing',
  'mokujin': 'Mokujin-Ken (Mimicry)'
};

// In-Memory API Cache & In-Flight Request Deduplication (Phase 8 Performance)
// Dynamic API Base URL — supports direct file://, local dev servers (5500, 3000), and FastAPI (8000)
const API_BASE = (typeof window !== 'undefined' && window.location && (window.location.protocol === 'file:' || (window.location.port !== '8000' && window.location.port !== '')))
  ? 'http://127.0.0.1:8000/api/v1'
  : '/api/v1';

const apiCache = new Map();
const inflightRequests = new Map();

async function fetchAPI(endpoint, useCache = false) {
  if (useCache && apiCache.has(endpoint)) {
    return apiCache.get(endpoint);
  }

  if (inflightRequests.has(endpoint)) {
    return await inflightRequests.get(endpoint);
  }

  const reqPromise = (async () => {
    try {
      const res = await fetch(`${API_BASE}${endpoint}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      if (useCache) {
        apiCache.set(endpoint, data);
      }
      return data;
    } catch (err) {
      console.warn(`API call failed for ${endpoint}:`, err);
      return null;
    } finally {
      inflightRequests.delete(endpoint);
    }
  })();

  inflightRequests.set(endpoint, reqPromise);
  return await reqPromise;
}

function invalidateApiCache() {
  apiCache.clear();
}

/**
 * Tekken 8 Notation Breakdown & Arcade Button Mapping Engine
 * Transforms raw string commands into authentic arcade/gamepad visual button chips:
 * Directions (➡ ↘ ⬇ ↙ ⬅ ↗ ↖ ⬆ ★), Buttons (1=Cyan, 2=Yellow, 3=Green, 4=Pink),
 * Stances/States (WS, FC, WR, SS, BT, HEAT, RAGE), Connectors (›, +, ~).
 */
function formatTekkenNotation(raw) {
  if (!raw || typeof raw !== 'string') return '';
  const trimmed = raw.trim();
  if (!trimmed) return '';
  if (trimmed.startsWith('<div class="tk-') || trimmed.startsWith('<span class="tk-')) return trimmed;

  // Split sequence by major combo step separators (">", "->", "=>", "→")
  if (trimmed.includes('>') || trimmed.includes('→') || trimmed.includes('->')) {
    const steps = trimmed.split(/\s*(?:>|->|=>|→)\s*/);
    return `<div class="tk-combo-sequence">${steps.map(s => formatSingleStep(s)).join('<span class="tk-next-arrow tk-break-btn" title="Combo Link Step">➔</span>')}</div>`;
  }

  return formatSingleStep(trimmed);
}

function formatSingleStep(step) {
  step = step.trim();
  if (!step) return '';

  // Separate space-delimited annotations (like "(T!)", "(W!)", "dash", etc.)
  const words = step.split(/\s+/);
  return `<span class="tk-step-wrapper">${words.map(w => formatWord(w)).join(' ')}</span>`;
}

function formatWord(w) {
  w = w.trim();
  if (!w) return '';

  // Special tags in parentheses
  if (w.startsWith('(') && w.endsWith(')')) {
    const tag = w.slice(1, -1).trim();
    if (tag.toUpperCase() === 'T!') return '<span class="tk-tag-tornado">TORNADO</span>';
    if (tag.toUpperCase() === 'W!') return '<span class="tk-tag-wall">WALL SPLAT</span>';
    if (tag.toUpperCase() === 'FB!') return '<span class="tk-tag-break">FLOOR BREAK</span>';
    if (tag.toUpperCase() === 'WB!') return '<span class="tk-tag-break">WALL BREAK</span>';
    if (tag.toLowerCase() === 'heat') return '<span class="tk-tag-heat">HEAT</span>';
    return `<span class="tk-tag-generic">${tag}</span>`;
  }

  // Common movement words
  const lower = w.toLowerCase();
  if (lower === 'dash') return '<span class="tk-move-action">DASH</span>';
  if (lower === 'microdash') return '<span class="tk-move-action">MICRODASH</span>';
  if (lower === 'run') return '<span class="tk-move-action">RUN</span>';

  // Check prefixes like R. or H.
  let prefixHtml = '';
  if (w.startsWith('R.') || w.startsWith('r.')) {
    prefixHtml = '<span class="tk-state-chip tk-rage-badge">RAGE</span> ';
    w = w.slice(2);
  } else if (w.startsWith('H.') || w.startsWith('h.')) {
    prefixHtml = '<span class="tk-state-chip tk-heat-badge">HEAT</span> ';
    w = w.slice(2);
  }

  // Check state prefixes: WS, FC, WR, SSL, SSR, SS, BT
  const stateMatch = w.match(/^(ws|fc|wr|ssl|ssr|ss|bt)(.*)$/i);
  let stateHtml = '';
  if (stateMatch) {
    const st = stateMatch[1].toUpperCase();
    stateHtml = `<span class="tk-state-chip">${st}</span> `;
    w = stateMatch[2];
  }

  // Subtokens split by commas or tildes (e.g. "1,2" or "df+1,2" or "f,n,d,df+2")
  const subTokens = w.split(/([,~])/);
  let bodyHtml = '<span class="tk-notation-chain">';
  for (let t of subTokens) {
    if (t === ',') {
      bodyHtml += '<span class="tk-sep-chip tk-break-btn" title="Sequence Break (,)">,</span>';
    } else if (t === '~') {
      bodyHtml += '<span class="tk-sep-chip tk-break-btn" title="Slide Input (~)">~</span>';
    } else if (t.trim()) {
      bodyHtml += formatAtom(t.trim());
    }
  }
  bodyHtml += '</span>';

  return `${prefixHtml}${stateHtml}${bodyHtml}`;
}

function formatAtom(atom) {
  // Check if atom is pure button expression (e.g. "1", "2", "1+2", "3+4", "2+3")
  const btnOnly = formatButtons(atom);
  if (btnOnly) return btnOnly;

  // If atom has '+', split into direction and buttons
  if (atom.includes('+')) {
    const parts = atom.split('+');
    const dirPart = parts[0].trim();
    const btnPart = parts.slice(1).join('+').trim();

    const dirHtml = dirPart ? formatDirection(dirPart) : '';
    const btnHtml = btnPart ? (formatButtons(btnPart) || `<span class="tk-btn-chip tk-btn-multi">${btnPart}</span>`) : '';

    if (dirHtml && btnHtml) {
      return `${dirHtml}<span class="tk-plus-chip">+</span>${btnHtml}`;
    } else if (dirHtml) {
      return dirHtml;
    } else if (btnHtml) {
      return btnHtml;
    }
  }

  // Check if direction
  const dirOnly = formatDirection(atom, true);
  if (dirOnly) return dirOnly;

  return `<span class="tk-raw-text">${atom}</span>`;
}

function formatDirection(dirStr, strict = false) {
  const map = {
    'f': '➡', 'b': '⬅', 'u': '⬆', 'd': '⬇',
    'df': '↘', 'd/f': '↘', 'db': '↙', 'd/b': '↙',
    'uf': '↗', 'u/f': '↗', 'ub': '↖', 'u/b': '↖',
    'n': '★', '★': '★'
  };

  const lower = dirStr.toLowerCase();
  if (map[lower]) {
    const isHold = (dirStr === dirStr.toUpperCase()) && dirStr !== 'N' && dirStr !== '★';
    const isStar = lower === 'n' || lower === '★';
    return `<span class="tk-dir-chip ${isHold ? 'tk-hold' : ''} ${isStar ? 'tk-dir-star' : ''}">${map[lower]}</span>`;
  }

  // Quarter / Half circle motions
  if (lower === 'qcf') return '<span class="tk-dir-chip">⬇</span><span class="tk-dir-chip">↘</span><span class="tk-dir-chip">➡</span>';
  if (lower === 'qcb') return '<span class="tk-dir-chip">⬇</span><span class="tk-dir-chip">↙</span><span class="tk-dir-chip">⬅</span>';
  if (lower === 'hcf') return '<span class="tk-dir-chip">⬅</span><span class="tk-dir-chip">↙</span><span class="tk-dir-chip">⬇</span><span class="tk-dir-chip">↘</span><span class="tk-dir-chip">➡</span>';
  if (lower === 'hcb') return '<span class="tk-dir-chip">➡</span><span class="tk-dir-chip">↘</span><span class="tk-dir-chip">⬇</span><span class="tk-dir-chip">↙</span><span class="tk-dir-chip">⬅</span>';

  if (strict) return null;
  return `<span class="tk-raw-text">${dirStr}</span>`;
}

function formatButtons(btnStr) {
  const norm = btnStr.replace(/\s+/g, '');
  const layout = state.controllerLayout || 'ARCADE';

  // Authentic Tekken button mappings with tactile arcade styling
  const mapping = {
    ARCADE: {
      '1': { text: '1', title: '1 (Left Punch)', cls: 'tk-btn-1' },
      '2': { text: '2', title: '2 (Right Punch)', cls: 'tk-btn-2' },
      '3': { text: '3', title: '3 (Left Kick)', cls: 'tk-btn-3' },
      '4': { text: '4', title: '4 (Right Kick)', cls: 'tk-btn-4' },
      '1+2': { text: '1+2', title: '1+2 (LP+RP)', cls: 'tk-btn-1-2' },
      '3+4': { text: '3+4', title: '3+4 (LK+RK)', cls: 'tk-btn-3-4' },
      '1+3': { text: '1+3', title: '1+3 (Throw)', cls: 'tk-btn-1-2' },
      '2+4': { text: '2+4', title: '2+4 (Throw)', cls: 'tk-btn-3-4' },
      '1+4': { text: '1+4', title: '1+4 (LP+RK)', cls: 'tk-btn-multi' },
      '2+3': { text: '2+3', title: '2+3 (RP+LK)', cls: 'tk-btn-multi' },
      '1+2+3': { text: '1+2+3', title: '1+2+3', cls: 'tk-btn-multi' },
      '1+2+4': { text: '1+2+4', title: '1+2+4', cls: 'tk-btn-multi' },
      '1+2+3+4': { text: 'Ki', title: 'Ki Charge (1+2+3+4)', cls: 'tk-btn-ki' },
    },
    PLAYSTATION: {
      '1': { text: '□', title: 'Square (Left Punch)', cls: 'tk-btn-1 tk-btn-ps' },
      '2': { text: '△', title: 'Triangle (Right Punch)', cls: 'tk-btn-2 tk-btn-ps' },
      '3': { text: '✕', title: 'Cross (Left Kick)', cls: 'tk-btn-3 tk-btn-ps' },
      '4': { text: '○', title: 'Circle (Right Kick)', cls: 'tk-btn-4 tk-btn-ps' },
      '1+2': { text: '□+△', title: 'Square + Triangle (LP+RP)', cls: 'tk-btn-1-2 tk-btn-ps' },
      '3+4': { text: '✕+○', title: 'Cross + Circle (LK+RK)', cls: 'tk-btn-3-4 tk-btn-ps' },
      '1+3': { text: '□+✕', title: 'Throw (Square + Cross)', cls: 'tk-btn-1-2 tk-btn-ps' },
      '2+4': { text: '△+○', title: 'Throw (Triangle + Circle)', cls: 'tk-btn-3-4 tk-btn-ps' },
      '1+4': { text: '□+○', title: 'Square + Circle', cls: 'tk-btn-multi tk-btn-ps' },
      '2+3': { text: '△+✕', title: 'Triangle + Cross', cls: 'tk-btn-multi tk-btn-ps' },
      '1+2+3+4': { text: 'Ki', title: 'Ki Charge', cls: 'tk-btn-ki tk-btn-ps' },
    },
    XBOX: {
      '1': { text: 'X', title: 'X Button (Left Punch)', cls: 'tk-btn-1 tk-btn-xb' },
      '2': { text: 'Y', title: 'Y Button (Right Punch)', cls: 'tk-btn-2 tk-btn-xb' },
      '3': { text: 'A', title: 'A Button (Left Kick)', cls: 'tk-btn-3 tk-btn-xb' },
      '4': { text: 'B', title: 'B Button (Right Kick)', cls: 'tk-btn-4 tk-btn-xb' },
      '1+2': { text: 'X+Y', title: 'X + Y Buttons (LP+RP)', cls: 'tk-btn-1-2 tk-btn-xb' },
      '3+4': { text: 'A+B', title: 'A + B Buttons (LK+RK)', cls: 'tk-btn-3-4 tk-btn-xb' },
      '1+3': { text: 'X+A', title: 'Throw (X + A)', cls: 'tk-btn-1-2 tk-btn-xb' },
      '2+4': { text: 'Y+B', title: 'Throw (Y + B)', cls: 'tk-btn-3-4 tk-btn-xb' },
      '1+4': { text: 'X+B', title: 'X + B Buttons', cls: 'tk-btn-multi tk-btn-xb' },
      '2+3': { text: 'Y+A', title: 'Y + A Buttons', cls: 'tk-btn-multi tk-btn-xb' },
      '1+2+3+4': { text: 'Ki', title: 'Ki Charge', cls: 'tk-btn-ki tk-btn-xb' },
    }
  };

  const currentMap = mapping[layout] || mapping.ARCADE;
  if (currentMap[norm]) {
    const item = currentMap[norm];
    return `<span class="tk-btn-chip ${item.cls}" title="${item.title}">${item.text}</span>`;
  }

  if (/^[1-4\+]+$/.test(norm)) {
    if (layout === 'PLAYSTATION') {
      const psCustom = norm.replace(/1/g, '□').replace(/2/g, '△').replace(/3/g, '✕').replace(/4/g, '○');
      return `<span class="tk-btn-chip tk-btn-multi tk-btn-ps">${psCustom}</span>`;
    } else if (layout === 'XBOX') {
      const xbCustom = norm.replace(/1/g, 'X').replace(/2/g, 'Y').replace(/3/g, 'A').replace(/4/g, 'B');
      return `<span class="tk-btn-chip tk-btn-multi tk-btn-xb">${xbCustom}</span>`;
    }
    return `<span class="tk-btn-chip tk-btn-multi">${norm}</span>`;
  }
  return null;
}

// Universal Button Mapping Switcher (Re-renders all notation in real-time)
function setControllerLayout(layout) {
  state.controllerLayout = layout;
  try {
    localStorage.setItem('tekken8_controller_layout', layout);
  } catch (e) {}

  // Synchronize all toggle buttons across navbar and notation section
  document.querySelectorAll('.ctl-btn, .nav-ctl-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.layout === layout);
  });

  // Re-render move tables, combos, punishes, and featured moves
  if (state.movesPagination && state.movesPagination.filteredMoves) {
    renderMovesTable(state.movesPagination.filteredMoves, false);
  }
  renderFeaturedMoves();
  if (state.lastMatchupData) {
    renderMatchupDashboard(state.lastMatchupData);
  }
  renderComboRecommendations();
  updateNotationDisplay();
}

// 1. Initial Load
document.addEventListener('DOMContentLoaded', async () => {
  setupEventListeners();
  setupRosterControls();
  initMatchupTabs();
  setupMovesSafetyFilters();
  await loadCharacters();
  await loadStages();
  await loadCoverageData();
  await loadSourcesData();
  updateNotationDisplay();
  await initMatchupAnalyzer();
  initPunishAssistant();
  await loadPunishmentOptions();
  initAdminHub();
  renderFeaturedMoves();
  populateHeroCombatTriad();
  initComboLab();
  initPunishQuiz();
  setupStageFilters();
  updateFavoritesBadges();
  initGlobalSearch();
  updateNotesCountBadge();
  restoreStateFromUrl();
});


// Event Listeners Setup
function setupEventListeners() {
  // Restore saved controller layout (Arcade, PlayStation, Xbox)
  const savedLayout = localStorage.getItem('tekken8_controller_layout') || 'ARCADE';
  state.controllerLayout = savedLayout;
  document.querySelectorAll('.ctl-btn, .nav-ctl-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.layout === savedLayout);
    btn.addEventListener('click', (e) => {
      const layout = e.currentTarget.dataset.layout;
      if (layout) setControllerLayout(layout);
    });
  });

  // Mobile Menu Toggle
  const mobileToggle = document.getElementById('navMobileToggle');
  const mainNav = document.getElementById('mainNavLinks');
  if (mobileToggle && mainNav) {
    mobileToggle.addEventListener('click', () => {
      mainNav.classList.toggle('mobile-open');
      mobileToggle.classList.toggle('active');
    });
    mainNav.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        mainNav.classList.remove('mobile-open');
        mobileToggle.classList.remove('active');
      });
    });
  }

  // Notation Input
  const notInput = document.getElementById('notationInput');
  if (notInput) {
    notInput.addEventListener('input', debounce(updateNotationDisplay, 150));
  }

  // Carousel & Roster Category Filter Pills
  document.querySelectorAll('#carouselFilterPills .filter-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('#carouselFilterPills .filter-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      state.activeFilter = e.target.dataset.filter;
      state.roster.activeFilter = e.target.dataset.filter;
      renderRosterGrid();
      renderCarousel();
      const track = document.getElementById('carouselTrack');
      if (track) track.scrollTo({ left: 0, behavior: 'smooth' });
    });
  });

  // Sidebar Filters
  document.querySelectorAll('#sidebarFilterPills .filter-btn-mini').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('#sidebarFilterPills .filter-btn-mini').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      renderSidebarQuickFighters(e.target.dataset.filter);
    });
  });

  // Initialize Robust Carousel Sliding & Touch/Mouse Drag
  initCarouselNavigation();

  // Quick Search Box
  const searchInput = document.getElementById('searchQuickInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (!q) {
        state.activeFilter = 'ALL';
        renderCarousel();
        return;
      }
      const match = state.characters.find(c => c.name.toLowerCase().includes(q) || c.slug.toLowerCase().includes(q));
      if (match) {
        selectCharacter(match.slug);
      }
    });
  }

  // Moves Table Filter
  const tableFilter = document.getElementById('movesTableFilter');
  if (tableFilter) {
    tableFilter.addEventListener('input', (e) => {
      filterMovesTable(e.target.value.toLowerCase().trim());
    });
  }

  // Moves Table Pagination Buttons (Phase 8 Performance)
  const movesPrevBtn = document.getElementById('movesPrevBtn');
  const movesNextBtn = document.getElementById('movesNextBtn');
  if (movesPrevBtn) {
    movesPrevBtn.addEventListener('click', () => changeMovesPage(-1));
  }
  if (movesNextBtn) {
    movesNextBtn.addEventListener('click', () => changeMovesPage(1));
  }

  // Move Detail Inspector Modal Dismissal
  const moveModal = document.getElementById('moveDetailModal');
  if (moveModal) {
    moveModal.addEventListener('click', (e) => {
      if (e.target === moveModal) closeMoveDetailModal();
    });
  }
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (typeof closeGlobalSearch === 'function') closeGlobalSearch();
      if (typeof closeMoveDetailModal === 'function') closeMoveDetailModal();
      if (typeof closeFavoritesModal === 'function') closeFavoritesModal();
      if (typeof closeSettingsModal === 'function') closeSettingsModal();
      if (typeof closePracticeNotesModal === 'function') closePracticeNotesModal();
      if (typeof closePracticeNoteEditModal === 'function') closePracticeNoteEditModal();
      if (typeof closeNotationGuideModal === 'function') closeNotationGuideModal();
      if (typeof closeDamageScalingModal === 'function') closeDamageScalingModal();
      if (typeof closePracticeModal === 'function') closePracticeModal();
      if (typeof closeStageDetailModal === 'function') closeStageDetailModal();
    }
  });

}

// Carousel Navigation, Step Scrolling & Touch/Mouse Swipe
function updateCarouselNavButtons() {
  const prevBtn = document.getElementById('carouselPrevBtn');
  const nextBtn = document.getElementById('carouselNextBtn');
  const track = document.getElementById('carouselTrack');
  if (!track || !prevBtn || !nextBtn) return;
  const maxScroll = Math.max(0, track.scrollWidth - track.clientWidth - 4);
  prevBtn.classList.toggle('is-disabled', track.scrollLeft <= 4);
  nextBtn.classList.toggle('is-disabled', track.scrollLeft >= maxScroll);
}

function initCarouselNavigation() {
  const prevBtn = document.getElementById('carouselPrevBtn');
  const nextBtn = document.getElementById('carouselNextBtn');
  const track = document.getElementById('carouselTrack');
  if (!track) return;

  function stepCarousel(direction) {
    // Dynamic paging step: ~72% of visible track width (or at least 260px)
    const step = Math.max(260, Math.floor(track.clientWidth * 0.72));
    const target = track.scrollLeft + (direction * step);
    track.scrollTo({
      left: target,
      behavior: 'smooth'
    });
    setTimeout(updateCarouselNavButtons, 350);
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', (e) => {
      e.preventDefault();
      stepCarousel(-1);
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', (e) => {
      e.preventDefault();
      stepCarousel(1);
    });
  }

  // Update button states on scroll
  track.addEventListener('scroll', debounce(updateCarouselNavButtons, 50), { passive: true });

  // Mouse wheel horizontal side-scrolling
  track.addEventListener('wheel', (e) => {
    if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
      e.preventDefault();
      track.scrollLeft += e.deltaY * 1.5;
      updateCarouselNavButtons();
    }
  }, { passive: false });

  // POINTER DRAG & SWIPE SUPPORT (Mouse, Pen & Touch)
  let isPointerDown = false;
  let startX = 0;
  let initialScrollLeft = 0;
  let dragDistance = 0;

  track.addEventListener('pointerdown', (e) => {
    if (e.button !== 0 && e.pointerType === 'mouse') return;
    isPointerDown = true;
    dragDistance = 0;
    startX = e.clientX;
    initialScrollLeft = track.scrollLeft;
    track.classList.add('is-dragging');
    try {
      track.setPointerCapture(e.pointerId);
    } catch (_) {}
  });

  track.addEventListener('pointermove', (e) => {
    if (!isPointerDown) return;
    const deltaX = e.clientX - startX;
    dragDistance = Math.max(dragDistance, Math.abs(deltaX));
    track.scrollLeft = initialScrollLeft - deltaX;
  });

  const finishDrag = (e) => {
    if (!isPointerDown) return;
    isPointerDown = false;
    track.classList.remove('is-dragging');
    try {
      track.releasePointerCapture(e.pointerId);
    } catch (_) {}
    updateCarouselNavButtons();
  };

  track.addEventListener('pointerup', finishDrag);
  track.addEventListener('pointercancel', finishDrag);

  // Capture phase click interceptor: if user was dragging/swiping, do NOT trigger character selection
  track.addEventListener('click', (e) => {
    if (dragDistance > 6) {
      e.preventDefault();
      e.stopPropagation();
      dragDistance = 0;
    }
  }, true);

  // Update button states initially and on window resize
  window.addEventListener('resize', debounce(updateCarouselNavButtons, 100));
  setTimeout(updateCarouselNavButtons, 150);
}

// Hurtbox archetype resolver for 43 fighters
function getCharacterHurtboxProfile(slug) {
  const bears = ['kuma', 'panda'];
  const big = ['jack-8', 'king', 'armor-king', 'bob', 'fahkumram'];
  const compact = [
    'alisa', 'asuka', 'azucena', 'jun', 'lili', 'nina', 
    'reina', 'xiaoyu', 'zafina', 'lidia', 'anna', 'kunimitsu', 'miary-zo'
  ];
  if (bears.includes(slug)) return { label: 'Bears', type: 'BEARS', badgeClass: 'hb-bear' };
  if (big.includes(slug)) return { label: 'Big / Heavy', type: 'BIG', badgeClass: 'hb-big' };
  if (compact.includes(slug)) return { label: 'Compact / Female', type: 'FEMALE_COMPACT', badgeClass: 'hb-compact' };
  return { label: 'Male Standard', type: 'MALE_STANDARD', badgeClass: 'hb-standard' };
}

// Quick Summary Drawer Sync
function updateSelectedFighterSummary(char) {
  if (!char) return;
  const nameEl = document.getElementById('selectedFighterName');
  const archEl = document.getElementById('selectedFighterArchetype');
  const hurtEl = document.getElementById('selectedFighterHurtbox');
  const hb = getCharacterHurtboxProfile(char.slug);

  if (nameEl) nameEl.textContent = char.name;
  if (archEl) archEl.textContent = `${char.archetype || 'Tekken 8 Fighter'}${char.is_dlc ? ' • DLC' : ''}`;
  if (hurtEl) hurtEl.textContent = `Hurtbox: ${hb.label}`;
}

// Setup Roster Controls (Search, Sort, Filters, View Modes)
function setupRosterControls() {
  const gridBtn = document.getElementById('viewModeGridBtn');
  const ribbonBtn = document.getElementById('viewModeRibbonBtn');
  const gridContainer = document.getElementById('rosterGridContainer');
  const ribbonContainer = document.getElementById('rosterRibbonContainer');

  function setViewMode(mode) {
    state.roster.viewMode = mode;
    if (gridBtn && ribbonBtn) {
      gridBtn.classList.toggle('active', mode === 'grid');
      ribbonBtn.classList.toggle('active', mode === 'ribbon');
    }
    if (gridContainer && ribbonContainer) {
      gridContainer.style.display = mode === 'grid' ? 'block' : 'none';
      ribbonContainer.style.display = mode === 'ribbon' ? 'flex' : 'none';
    }
    if (mode === 'ribbon') {
      updateCarouselNavButtons();
    }
  }

  if (gridBtn) gridBtn.addEventListener('click', () => setViewMode('grid'));
  if (ribbonBtn) ribbonBtn.addEventListener('click', () => setViewMode('ribbon'));

  const searchInput = document.getElementById('rosterSearchInput');
  const clearBtn = document.getElementById('rosterSearchClearBtn');

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      state.roster.searchQuery = e.target.value.toLowerCase().trim();
      if (clearBtn) {
        clearBtn.style.display = state.roster.searchQuery ? 'block' : 'none';
      }
      renderRosterGrid();
      renderCarousel();
    });
  }

  if (clearBtn && searchInput) {
    clearBtn.addEventListener('click', () => {
      searchInput.value = '';
      state.roster.searchQuery = '';
      clearBtn.style.display = 'none';
      renderRosterGrid();
      renderCarousel();
      searchInput.focus();
    });
  }

  const sortSelect = document.getElementById('rosterSortSelect');
  if (sortSelect) {
    sortSelect.addEventListener('change', (e) => {
      state.roster.sortOrder = e.target.value;
      renderRosterGrid();
      renderCarousel();
    });
  }
}

function resetRosterFilters() {
  state.roster.searchQuery = '';
  state.roster.activeFilter = 'ALL';
  state.activeFilter = 'ALL';
  const searchInput = document.getElementById('rosterSearchInput');
  if (searchInput) searchInput.value = '';
  const clearBtn = document.getElementById('rosterSearchClearBtn');
  if (clearBtn) clearBtn.style.display = 'none';
  document.querySelectorAll('.roster-filter-pills .filter-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.filter === 'ALL');
  });
  renderRosterGrid();
  renderCarousel();
}

function getFilteredAndSortedCharacters() {
  let list = [...state.characters];

  const filter = state.roster.activeFilter || state.activeFilter || 'ALL';
  if (filter !== 'ALL') {
    list = list.filter(c => {
      if (filter === 'MISHIMA') return c.archetype && c.archetype.includes('Mishima');
      if (filter === 'ALLIES') return c.archetype && c.archetype.includes('Allies');
      if (filter === 'REBELS') return c.archetype && c.archetype.includes('Rebels');
      if (filter === 'NEWCOMERS') return c.archetype && c.archetype.includes('Newcomers');
      if (filter === 'GRAPPLER') return (c.archetype && c.archetype.includes('Grappler')) || c.slug === 'king' || c.slug === 'armor-king';
      if (filter === 'DLC') return c.is_dlc === true || (c.archetype && c.archetype.toLowerCase().includes('dlc'));
      return true;
    });
  }

  const q = state.roster.searchQuery;
  if (q) {
    list = list.filter(c => 
      c.name.toLowerCase().includes(q) ||
      c.slug.toLowerCase().includes(q) ||
      (c.archetype && c.archetype.toLowerCase().includes(q)) ||
      (FIGHTING_STYLES[c.slug] && FIGHTING_STYLES[c.slug].toLowerCase().includes(q))
    );
  }

  const sort = state.roster.sortOrder || 'NAME_ASC';
  if (sort === 'NAME_ASC') {
    list.sort((a, b) => a.name.localeCompare(b.name));
  } else if (sort === 'NAME_DESC') {
    list.sort((a, b) => b.name.localeCompare(a.name));
  } else if (sort === 'ARCHETYPE') {
    list.sort((a, b) => (a.archetype || '').localeCompare(b.archetype || '') || a.name.localeCompare(b.name));
  } else if (sort === 'BASE_FIRST') {
    list.sort((a, b) => (a.is_dlc === b.is_dlc ? a.name.localeCompare(b.name) : (a.is_dlc ? 1 : -1)));
  } else if (sort === 'DLC_FIRST') {
    list.sort((a, b) => (a.is_dlc === b.is_dlc ? a.name.localeCompare(b.name) : (a.is_dlc ? -1 : 1)));
  }

  return list;
}

function renderRosterGrid() {
  const container = document.getElementById('rosterGrid');
  if (!container) return;

  const filtered = getFilteredAndSortedCharacters();

  const countBadge = document.getElementById('rosterCountBadge');
  if (countBadge) {
    countBadge.textContent = `${filtered.length} Warriors`;
  }

  if (filtered.length === 0) {
    const term = state.roster.searchQuery || state.activeFilter || '';
    container.innerHTML = `
      <div class="empty-state-card" style="grid-column: 1 / -1;">
        <div class="empty-icon">🥊</div>
        <h3 class="empty-title">No Fighters Found</h3>
        <p class="empty-desc">No warriors matched "<strong>${escapeHtml(term)}</strong>". Try clearing your search keyword or switching filter categories.</p>
        <button type="button" class="btn btn-secondary empty-action" onclick="resetRosterFilters()">Clear Filters &amp; Show All</button>
      </div>
    `;
    return;
  }

  const favs = getFavorites();

  container.innerHTML = filtered.map(c => {
    const isSelected = state.selectedCharacter && state.selectedCharacter.slug === c.slug;
    const isFav = (favs.fighters || []).includes(c.slug);
    const hb = getCharacterHurtboxProfile(c.slug);
    const style = FIGHTING_STYLES[c.slug] || c.archetype || 'Tekken 8';
    return `
      <div class="roster-fighter-card ${isSelected ? 'active' : ''}"
           id="gridCard_${c.slug}"
           tabindex="0"
           role="button"
           aria-pressed="${isSelected}"
           aria-label="Select ${c.name}"
           onclick="selectCharacter('${c.slug}')"
           onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();selectCharacter('${c.slug}');}">
        <div class="roster-avatar-wrap">
          <img class="roster-avatar"
               src="${c.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp'}"
               alt="${c.name}"
               loading="lazy"
               onerror="this.src='/assets/avatars/jin-brand-256-C1-oe_x3.webp'"/>
          ${c.is_dlc ? '<span class="roster-dlc-tag">DLC</span>' : ''}
          ${isSelected ? '<span class="roster-active-indicator">SELECTED</span>' : ''}
          <button type="button" class="btn-roster-fav ${isFav ? 'active' : ''}" onclick="event.stopPropagation(); toggleCharacterFavorite('${c.slug}')" title="Favorite ${c.name}">
            ${isFav ? '★' : '☆'}
          </button>
        </div>
        <div class="roster-card-info">
          <div class="roster-card-name">${c.name}</div>
          <div class="roster-card-style">${style}</div>
          <div class="roster-card-chips">
            <span class="roster-chip ${hb.badgeClass}">${hb.label}</span>
            <button type="button" class="btn-roster-profile-link" onclick="event.stopPropagation(); openCharacterProfile('${c.slug}')" title="View 17-Section Deep Dive Profile">
              📖 Profile
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// Progressive Disclosure: Matchup Tab Navigation
function initMatchupTabs() {
  const tabsBar = document.getElementById('matchupTabsBar');
  if (!tabsBar) return;

  const tabButtons = tabsBar.querySelectorAll('.matchup-tab-btn:not(.view-all)');
  const viewAllBtn = document.getElementById('btnToggleViewAllMatchup');
  const panels = document.querySelectorAll('.matchup-tab-panel');
  const dashboardContent = document.getElementById('matchupDashboardContent');

  function switchTab(tabId) {
    state.activeMatchupTab = tabId;
    state.viewAllMatchup = false;

    if (dashboardContent) dashboardContent.classList.remove('view-all-mode');
    if (viewAllBtn) viewAllBtn.classList.remove('active');

    tabButtons.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabId);
    });

    panels.forEach(panel => {
      panel.classList.toggle('active', panel.id === tabId);
    });
  }

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.dataset.tab;
      if (tabId) switchTab(tabId);
    });
  });

  if (viewAllBtn) {
    viewAllBtn.addEventListener('click', () => {
      state.viewAllMatchup = !state.viewAllMatchup;
      viewAllBtn.classList.toggle('active', state.viewAllMatchup);
      if (dashboardContent) {
        dashboardContent.classList.toggle('view-all-mode', state.viewAllMatchup);
      }
      if (state.viewAllMatchup) {
        panels.forEach(panel => panel.classList.add('active'));
        tabButtons.forEach(btn => btn.classList.remove('active'));
      } else {
        switchTab(state.activeMatchupTab || 'panel-overview');
      }
    });
  }
}

// Move Explorer Frame Safety Filter Buttons Setup
function setupMovesSafetyFilters() {
  const container = document.getElementById('movesSafetyFilters');
  if (!container) return;

  const buttons = container.querySelectorAll('.safety-pill');
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.movesSafetyFilter = btn.dataset.safety || 'ALL';
      const searchVal = document.getElementById('movesTableFilter')?.value.toLowerCase().trim() || '';
      filterMovesTable(searchVal);
    });
  });
}

// 2. Load & Render Characters
async function loadCharacters() {
  const data = await fetchAPI('/characters', true);
  if (data && Array.isArray(data)) {
    state.characters = data;
    renderRosterGrid();
    renderCarousel();
    renderSidebarQuickFighters('ALL');
    initMoveExplorer();
    
    // Select default fighter (Jin Kazama)
    const defaultFighter = data.find(c => c.slug === 'jin') || data[0];
    if (defaultFighter) {
      selectCharacter(defaultFighter.slug);
    }
  }
}

// Render Main Carousel
function renderCarousel() {
  const track = document.getElementById('carouselTrack');
  if (!track) return;

  const filtered = getFilteredAndSortedCharacters();

  if (filtered.length === 0) {
    track.innerHTML = '<div style="color:var(--text-muted); padding:1rem;">No fighters in this category.</div>';
    updateCarouselNavButtons();
    return;
  }

  track.innerHTML = filtered.map(c => {
    const isSelected = state.selectedCharacter && state.selectedCharacter.slug === c.slug;
    return `
      <div class="carousel-fighter-card ${isSelected ? 'active' : ''}" 
           id="card_${c.slug}"
           onclick="selectCharacter('${c.slug}')"
           title="${c.name} (${c.archetype || 'Tekken 8'})">
        <div class="carousel-avatar-wrap">
          <img class="carousel-avatar" 
               src="${c.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp'}" 
               alt="${c.name}"
               loading="lazy"
               draggable="false"
               onerror="this.src='/assets/avatars/jin-brand-256-C1-oe_x3.webp'"/>
        </div>
        <div class="carousel-name">${c.name}</div>
      </div>
    `;
  }).join('');

  setTimeout(updateCarouselNavButtons, 80);
}

// Render Sidebar Quick Fighters
function renderSidebarQuickFighters(filterCategory = 'ALL') {
  const container = document.getElementById('sidebarQuickFighters');
  if (!container) return;

  const featuredSlugs = ['jin', 'king', 'reina', 'paul', 'hwoarang', 'kazuya', 'jun', 'bryan', 'eddy', 'feng'];
  
  const pool = state.characters.filter(c => {
    if (filterCategory === 'ALL') return true;
    if (filterCategory === 'NEWCOMERS') return c.archetype && c.archetype.includes('Newcomers');
    if (filterCategory === 'MISHIMA') return c.archetype && c.archetype.includes('Mishima');
    if (filterCategory === 'ALLIES') return c.archetype && c.archetype.includes('Allies');
    if (filterCategory === 'REBELS') return c.archetype && c.archetype.includes('Rebels');
    return true;
  });

  // Pick top 5 matching fighters
  const displayFighters = pool.filter(c => featuredSlugs.includes(c.slug)).slice(0, 5);
  const finalFighters = displayFighters.length === 5 ? displayFighters : pool.slice(0, 5);

  container.innerHTML = finalFighters.map(c => {
    const isSelected = state.selectedCharacter && state.selectedCharacter.slug === c.slug;
    return `
      <div class="quick-fighter-card ${isSelected ? 'active' : ''}" onclick="selectCharacter('${c.slug}')" title="${c.name}">
        <img src="${c.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp'}" alt="${c.name}">
        <span>${c.name.split(' ')[0]}</span>
      </div>
    `;
  }).join('');
}

// Render Dynamic Featured Moves & Combos with authentic Arcade Button Mapping
function renderFeaturedMoves() {
  const container = document.getElementById('featuredMovesList');
  if (!container) return;

  const featured = [
    {
      characterSlug: 'jin',
      characterName: 'Jin',
      avatar: '/assets/avatars/jin-brand-256-C1-oe_x3.webp',
      moveName: 'Electric Wind Hook Fist',
      input: 'f,n,d,df+2',
      damage: '23',
      badges: [
        { text: 'LAUNCHER', cls: 'badge-launcher' },
        { text: '+5 OB', cls: 'badge-block-plus' }
      ]
    },
    {
      characterSlug: 'kazuya',
      characterName: 'Kazuya',
      avatar: '/assets/avatars/kazuya-brand-256-BInk9tTm.webp',
      moveName: 'Spinning Demon (Hell Sweep)',
      input: 'f,n,d,df+4,1',
      damage: '33',
      badges: [
        { text: 'HIGH CRUSH', cls: 'badge-crush' },
        { text: '-23 OB', cls: 'badge-block-neg' }
      ]
    },
    {
      characterSlug: 'reina',
      characterName: 'Reina',
      avatar: '/assets/avatars/reina-brand-256-DDc7iMts.webp',
      moveName: 'Wind God Fist',
      input: 'f,n,df+2',
      damage: '22',
      badges: [
        { text: 'LAUNCHER', cls: 'badge-launcher' },
        { text: '+5 OB', cls: 'badge-block-plus' }
      ]
    },
    {
      characterSlug: 'king',
      characterName: 'King',
      avatar: '/assets/avatars/king-brand-256-Dq_98Qq3.webp',
      moveName: 'Giant Swing',
      input: 'f,b,db,d,df,f+1',
      damage: '65',
      badges: [
        { text: 'THROW', cls: 'badge-throw' },
        { text: '1 BREAK', cls: 'badge-crush' }
      ]
    },
    {
      characterSlug: 'feng',
      characterName: 'Feng',
      avatar: '/assets/avatars/feng-brand-256-Cfyw5tOe.webp',
      moveName: 'Iron Fortress',
      input: 'b+1+2',
      damage: '25',
      badges: [
        { text: 'POWER CRUSH', cls: 'badge-crush' },
        { text: '-13 OB', cls: 'badge-block-neg' }
      ]
    },
    {
      characterSlug: 'jun',
      characterName: 'Jun',
      avatar: '/assets/avatars/jun-brand-256-eieDvySl.webp',
      moveName: 'White Heron Dance',
      input: '1+4,2,4',
      damage: '38',
      badges: [
        { text: 'NATURAL COMBO', cls: 'badge-block' },
        { text: 'M-H-L', cls: 'badge-crush' }
      ]
    }
  ];

  container.innerHTML = featured.map(m => {
    const formattedInput = formatTekkenNotation(m.input);
    const badgesHtml = m.badges.map(b => `<span class="feat-badge ${b.cls}">${b.text}</span>`).join('');
    return `
      <div class="featured-move-row" onclick="onFeaturedMoveClick('${m.characterSlug}', '${m.moveName.replace(/'/g, "\\'")}')" title="${m.characterName}: ${m.moveName}">
        <img class="feat-char-avatar" src="${m.avatar}" alt="${m.characterName}" loading="lazy" onerror="this.src='/assets/avatars/jin-brand-256-C1-oe_x3.webp'">
        <div class="feat-meta-wrap">
          <div class="feat-move-title">${m.characterName}: ${m.moveName}</div>
          <div class="feat-notation-wrap">${formattedInput}</div>
        </div>
        <div class="feat-damage">${m.damage}</div>
        <div class="feat-badge-group">
          ${badgesHtml}
        </div>
      </div>
    `;
  }).join('');
}

function onFeaturedMoveClick(slug, moveName) {
  selectCharacter(slug);
  filterByMoveText(moveName);
}


// Select Character Action
async function selectCharacter(slug) {
  const char = state.characters.find(c => c.slug === slug);
  if (!char) return;

  state.selectedCharacter = char;

  // Update active state in carousel
  document.querySelectorAll('.carousel-fighter-card').forEach(el => el.classList.remove('active'));
  const card = document.getElementById(`card_${slug}`);
  if (card) {
    card.classList.add('active');
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  }

  // Update active state in roster grid
  document.querySelectorAll('.roster-fighter-card').forEach(el => {
    el.classList.remove('active');
    el.setAttribute('aria-pressed', 'false');
  });
  const gridCard = document.getElementById(`gridCard_${slug}`);
  if (gridCard) {
    gridCard.classList.add('active');
    gridCard.setAttribute('aria-pressed', 'true');
  }

  // Update Selected Fighter Quick Summary Drawer
  updateSelectedFighterSummary(char);

  // Update active state in sidebar
  document.querySelectorAll('.quick-fighter-card').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.quick-fighter-card').forEach(el => {
    if (el.getAttribute('title') === char.name) {
      el.classList.add('active');
    }
  });

  // Update title
  const titleEl = document.getElementById('currentFighterTitle');
  if (titleEl) {
    titleEl.textContent = `${char.name.toUpperCase()} — MOVES & FRAME DATA`;
  }

  // Synchronize Move Explorer Fighter Bar
  const meSelect = document.getElementById('moveExplorerFighterSelect');
  if (meSelect && meSelect.value !== char.slug) {
    meSelect.value = char.slug;
  }
  const meAvatar = document.getElementById('moveExplorerFighterAvatar');
  if (meAvatar && char.avatar_url) {
    meAvatar.src = char.avatar_url;
    meAvatar.alt = char.name;
  }

  // Synchronize Player 1 in Matchup Analyzer
  const pSelect = document.getElementById('playerSelect');
  if (pSelect && pSelect.value != char.id) {
    pSelect.value = char.id;
    updatePlayerPreview();
  }

  // Fetch moves for this fighter
  await loadMovesForCharacter(char.id);
}

// ==========================================================================
// 3. Move Explorer & Verified Frame Data Engine (Phase 4)
// ==========================================================================

function initMoveExplorer() {
  const select = document.getElementById('moveExplorerFighterSelect');
  if (!select) return;

  const currentSlug = state.selectedCharacter?.slug || 'jin';
  select.innerHTML = (state.characters || []).map(c => `
    <option value="${c.slug}" ${c.slug === currentSlug ? 'selected' : ''}>${c.name}</option>
  `).join('');

  const avatar = document.getElementById('moveExplorerFighterAvatar');
  if (avatar && state.selectedCharacter?.avatar_url) {
    avatar.src = state.selectedCharacter.avatar_url;
    avatar.alt = state.selectedCharacter.name;
  }
}

function onMoveExplorerFighterChange(slug) {
  playSfx('click');
  const char = (state.characters || []).find(c => c.slug === slug);
  if (!char) return;

  const avatar = document.getElementById('moveExplorerFighterAvatar');
  if (avatar && char.avatar_url) {
    avatar.src = char.avatar_url;
    avatar.alt = char.name;
  }

  selectCharacter(slug);
}

async function loadMovesForCharacter(characterId) {
  const data = await fetchAPI(`/moves?character_id=${characterId}&limit=500`, true);
  state.moves = data || [];

  // Update Move Explorer Header Badges
  const totalBadge = document.getElementById('moveExplorerTotalMovesBadge');
  if (totalBadge) totalBadge.textContent = `${state.moves.length} Moves`;

  const verifiedBadge = document.getElementById('moveExplorerVerifiedBadge');
  if (verifiedBadge) {
    const total = state.moves.length;
    const verifiedCount = state.moves.filter(m => m.verification_status === 'VERIFIED' || m.is_verified).length;
    const pct = total > 0 ? Math.round((verifiedCount / total) * 100) : 100;
    verifiedBadge.textContent = `${pct}% VERIFIED`;
  }

  const patchBadge = document.getElementById('moveExplorerPatchBadge');
  if (patchBadge) {
    const pVer = state.moves.find(m => m.patch_version)?.patch_version || '3.00.02';
    patchBadge.textContent = `v${pVer}`;
  }

  // Synchronize fighter select dropdown
  const meSelect = document.getElementById('moveExplorerFighterSelect');
  if (meSelect && state.selectedCharacter && meSelect.value !== state.selectedCharacter.slug) {
    meSelect.value = state.selectedCharacter.slug;
  }

  // Filter and render table
  filterMovesTable();
}

function changeMovesPage(delta) {
  state.movesPagination.currentPage += delta;
  renderMovesTable(state.movesPagination.filteredMoves, false);
}

function renderMovesTable(movesList, resetPage = true) {
  const tbody = document.getElementById('movesTableBody');
  const emptyState = document.getElementById('movesEmptyState');
  const paginationBar = document.getElementById('movesPaginationBar');
  const paginationInfo = document.getElementById('movesPaginationInfo');
  const pageNumberEl = document.getElementById('movesPageNumber');
  const prevBtn = document.getElementById('movesPrevBtn');
  const nextBtn = document.getElementById('movesNextBtn');
  if (!tbody) return;

  if (resetPage) {
    state.movesPagination.currentPage = 1;
    state.movesPagination.filteredMoves = movesList || [];
  }

  const list = state.movesPagination.filteredMoves;

  if (!list || list.length === 0) {
    tbody.innerHTML = '';
    if (emptyState) emptyState.style.display = 'block';
    if (paginationBar) paginationBar.style.display = 'none';
    const countPill = document.getElementById('moveExplorerCountPill');
    if (countPill) countPill.textContent = '0 Moves';
    return;
  }

  if (emptyState) emptyState.style.display = 'none';
  if (paginationBar) paginationBar.style.display = 'flex';

  const totalMoves = list.length;
  const pageSize = state.movesPagination.pageSize;
  const totalPages = Math.ceil(totalMoves / pageSize) || 1;

  if (state.movesPagination.currentPage > totalPages) {
    state.movesPagination.currentPage = totalPages;
  }
  if (state.movesPagination.currentPage < 1) {
    state.movesPagination.currentPage = 1;
  }

  const curPage = state.movesPagination.currentPage;
  const startIdx = (curPage - 1) * pageSize;
  const endIdx = Math.min(startIdx + pageSize, totalMoves);
  const pagedMoves = list.slice(startIdx, endIdx);

  if (paginationInfo) {
    paginationInfo.textContent = `Showing ${startIdx + 1}–${endIdx} of ${totalMoves} moves`;
  }
  if (pageNumberEl) {
    pageNumberEl.textContent = `Page ${curPage} of ${totalPages}`;
  }
  if (prevBtn) prevBtn.disabled = curPage <= 1;
  if (nextBtn) nextBtn.disabled = curPage >= totalPages;

  const countPill = document.getElementById('moveExplorerCountPill');
  if (countPill) countPill.textContent = `${totalMoves} Moves`;

  tbody.innerHTML = pagedMoves.map(m => {
    const isStance = m.frame_state_type === 'NOT_APPLICABLE' || (m.hit_level || '').toLowerCase() === 's' || (m.name || '').toLowerCase().includes('stance');
    const isThrow = (m.hit_level_type === 'THROW') || (m.hit_level || '').toLowerCase() === 't' || (m.properties || []).some(p => (typeof p === 'string' ? p : p.property_type || '').toLowerCase().includes('throw'));

    // Startup display (explicit state: never ambiguous dash or fake zero)
    let startupStr = '—';
    if (isStance) {
      startupStr = '<span class="frame-stance-text">N/A</span>';
    } else if (m.startup_raw) {
      startupStr = m.startup_raw;
    } else if (m.startup_frames !== null) {
      startupStr = `i${m.startup_frames}`;
    } else {
      startupStr = '<span class="frame-null">Unknown</span>';
    }

    // Block Advantage styling
    let blockStr = '—';
    let blockClass = 'frame-null';
    if (isStance) {
      blockStr = 'N/A';
      blockClass = 'frame-stance-text';
    } else if (isThrow) {
      blockStr = 'Duck / Break';
      blockClass = 'frame-throw-text';
    } else if (m.block_advantage_raw) {
      blockStr = m.block_advantage_raw;
      if (m.is_plus_on_block || (m.block_advantage !== null && m.block_advantage > 0)) {
        blockClass = 'frame-plus';
      } else if (m.is_launch_punishable || (m.block_advantage !== null && m.block_advantage <= -15)) {
        blockClass = 'frame-minus';
      } else if (m.block_advantage !== null) {
        blockClass = m.block_advantage === 0 ? 'frame-zero' : 'frame-minus';
      }
    } else if (m.block_advantage !== null) {
      blockStr = m.block_advantage > 0 ? `+${m.block_advantage}` : (m.block_advantage === 0 ? '±0' : `${m.block_advantage}`);
      blockClass = m.block_advantage > 0 ? 'frame-plus' : (m.block_advantage === 0 ? 'frame-zero' : 'frame-minus');
    } else {
      blockStr = 'Unknown';
      blockClass = 'frame-null';
    }

    // Hit Advantage styling
    let hitStr = '—';
    let hitClass = 'frame-null';
    if (isStance) {
      hitStr = 'N/A';
      hitClass = 'frame-stance-text';
    } else if (m.hit_advantage_raw) {
      hitStr = m.hit_advantage_raw;
      if (m.hit_advantage !== null) {
        hitClass = m.hit_advantage > 0 ? 'frame-plus' : (m.hit_advantage < 0 ? 'frame-minus' : 'frame-zero');
      }
    } else if (m.hit_advantage !== null) {
      hitStr = m.hit_advantage > 0 ? `+${m.hit_advantage}` : (m.hit_advantage === 0 ? '±0' : `${m.hit_advantage}`);
      hitClass = m.hit_advantage > 0 ? 'frame-plus' : (m.hit_advantage < 0 ? 'frame-minus' : 'frame-zero');
    } else {
      hitStr = 'Unknown';
      hitClass = 'frame-null';
    }

    // Counter Hit Advantage styling
    let chStr = '—';
    let chClass = 'frame-null';
    if (isStance) {
      chStr = 'N/A';
      chClass = 'frame-stance-text';
    } else if (m.counter_hit_advantage_raw) {
      chStr = m.counter_hit_advantage_raw;
      chClass = (chStr.toLowerCase().includes('launch') || chStr.toLowerCase().includes('knd')) ? 'frame-plus' : '';
    } else if (m.counter_hit_advantage !== null) {
      chStr = m.counter_hit_advantage > 0 ? `+${m.counter_hit_advantage}` : `${m.counter_hit_advantage}`;
      chClass = m.counter_hit_advantage > 0 ? 'frame-plus' : 'frame-minus';
    } else if (m.is_counter_hit_launcher) {
      chStr = 'Launch';
      chClass = 'frame-plus';
    } else {
      chStr = '<span style="color:var(--text-dim); font-size:0.75rem;">Same as Hit</span>';
    }

    // Damage
    let dmgStr = '—';
    if (isStance) {
      dmgStr = '—';
    } else if (m.damage !== null) {
      dmgStr = `${m.damage}`;
    } else {
      dmgStr = '<span class="frame-null">Unknown</span>';
    }

    // Hit Level Badge
    let hitLevelHtml = '';
    const hlType = (m.hit_level_type || '').toUpperCase();
    const rawHl = (m.hit_level || '').toUpperCase();
    if (isStance || hlType === 'STANCE' || rawHl === 'S') {
      hitLevelHtml = '<span class="move-level-badge stance">STANCE</span>';
    } else if (isThrow || hlType === 'THROW' || rawHl === 'T') {
      hitLevelHtml = '<span class="move-level-badge throw">THROW</span>';
    } else if (hlType === 'SPECIAL_MID' || rawHl === 'SM' || rawHl === 'SPECIAL MID') {
      hitLevelHtml = '<span class="move-level-badge special-mid">S.MID</span>';
    } else if (hlType === 'HIGH' || rawHl.startsWith('H')) {
      hitLevelHtml = `<span class="move-level-badge high">${rawHl || 'HIGH'}</span>`;
    } else if (hlType === 'LOW' || rawHl.startsWith('L')) {
      hitLevelHtml = `<span class="move-level-badge low">${rawHl || 'LOW'}</span>`;
    } else {
      hitLevelHtml = `<span class="move-level-badge mid">${rawHl || 'MID'}</span>`;
    }

    // Safety & Punish Column
    let safetyHtml = '';
    const sType = m.block_safety || (m.block_advantage !== null ? (m.block_advantage >= 1 ? 'PLUS' : (m.block_advantage >= -9 ? 'SAFE' : (m.block_advantage <= -15 ? 'LAUNCH_PUNISH' : 'UNSAFE'))) : (isStance ? 'NOT_APPLICABLE' : 'UNKNOWN'));
    if (sType === 'PLUS') {
      safetyHtml = '<span class="move-safety-badge plus">+ ADVANTAGE</span>';
    } else if (sType === 'SAFE') {
      safetyHtml = '<span class="move-safety-badge safe">SAFE (≤ -9)</span>';
    } else if (sType === 'UNSAFE') {
      safetyHtml = `<span class="move-safety-badge unsafe">UNSAFE</span>`;
      if (m.punish_window_frames) {
        safetyHtml += `<div class="punish-window-chip">i${m.punish_window_frames} Window</div>`;
      }
      if (m.has_pushback) {
        safetyHtml += `<div class="pushback-warning-tag" title="${escapeHtml(m.pushback_warning || 'Pushback spacing risk')}">⚠️ Pushback</div>`;
      }
      if (m.is_stance_transition) {
        safetyHtml += `<div class="stance-chip stance-chip-trans">➔ ${escapeHtml(m.stance_name || 'Stance')}</div>`;
      } else if (m.is_from_stance) {
        safetyHtml += `<div class="stance-chip stance-chip-from">${escapeHtml(m.stance_name || 'Stance')}</div>`;
      }
      if (m.punish_recommendation) {
        safetyHtml += `<div style="font-size:0.68rem; color:#fca5a5; margin-top:2px;">🥊 ${m.punish_recommendation}</div>`;
      }
    } else if (sType === 'LAUNCH_PUNISH') {
      safetyHtml = `<span class="move-safety-badge launch">LAUNCH PUNISH</span>`;
      if (m.punish_window_frames) {
        safetyHtml += `<div class="punish-window-chip launch">i${m.punish_window_frames}+ Launch</div>`;
      }
      if (m.has_pushback) {
        safetyHtml += `<div class="pushback-warning-tag" title="${escapeHtml(m.pushback_warning || 'Pushback spacing risk')}">⚠️ Pushback</div>`;
      }
      if (m.is_stance_transition) {
        safetyHtml += `<div class="stance-chip stance-chip-trans">➔ ${escapeHtml(m.stance_name || 'Stance')}</div>`;
      } else if (m.is_from_stance) {
        safetyHtml += `<div class="stance-chip stance-chip-from">${escapeHtml(m.stance_name || 'Stance')}</div>`;
      }
      if (m.punish_recommendation) {
        safetyHtml += `<div style="font-size:0.68rem; color:#fca5a5; margin-top:2px;">🥊 ${m.punish_recommendation}</div>`;
      }
    } else if (sType === 'NOT_APPLICABLE') {
      safetyHtml = '<span class="move-safety-badge na">STANCE TRANS</span>';
      if (m.is_stance_transition) {
        safetyHtml += `<div class="stance-chip stance-chip-trans">➔ ${escapeHtml(m.stance_name || 'Stance')}</div>`;
      }
    } else {
      safetyHtml = '<span class="move-safety-badge na">UNKNOWN</span>';
    }


    // Move Property Badges
    const props = m.properties || [];
    const propBadges = props.map(p => {
      const rawName = typeof p === 'string' ? p : (p.property_type || p.property_name || p.name || '');
      const pName = (rawName || '').toLowerCase();
      if (!pName) return '';
      if (pName.includes('heat')) return `<span class="feat-badge badge-launcher" style="padding:0.15rem 0.4rem; font-size:0.65rem;">HEAT</span>`;
      if (pName.includes('rage')) return `<span class="feat-badge badge-crush" style="padding:0.15rem 0.4rem; font-size:0.65rem;">RAGE</span>`;
      if (pName.includes('crush') || pName.includes('power')) return `<span class="feat-badge badge-crush" style="padding:0.15rem 0.4rem; font-size:0.65rem;">CRUSH</span>`;
      if (pName.includes('launcher') || pName.includes('launch')) return `<span class="feat-badge badge-launcher" style="padding:0.15rem 0.4rem; font-size:0.65rem;">LAUNCH</span>`;
      if (pName.includes('tornado')) return `<span class="feat-badge badge-block" style="padding:0.15rem 0.4rem; font-size:0.65rem;">TORNADO</span>`;
      if (pName.includes('homing')) return `<span class="feat-badge badge-block" style="padding:0.15rem 0.4rem; font-size:0.65rem; background:rgba(6,182,212,0.2); border-color:#06b6d4; color:#67e8f9;">HOMING</span>`;
      return `<span class="hazard-pill">${rawName.replace(/-/g, ' ').toUpperCase()}</span>`;
    }).filter(Boolean).join(' ');

    return `
      <tr onclick="testNotationString('${m.original_notation}')" style="cursor:pointer;" title="Click to test in Notation Engine">
        <td style="font-weight:700; color:#fff;">
          <div style="display:flex; align-items:center; gap:0.4rem;">
            <button type="button" class="btn-fav-move-star" onclick="event.stopPropagation(); toggleMoveFavorite('${m.original_notation}', '${(m.name || m.original_notation).replace(/'/g, "\\'")}')" title="Bookmark Move">⭐</button>
            <span>${m.name}</span>
          </div>
        </td>
        <td>${formatTekkenNotation(m.original_notation)}</td>
        <td>${hitLevelHtml}</td>
        <td><span style="font-weight:700;">${startupStr}</span></td>
        <td><span class="${blockClass}">${blockStr}</span></td>
        <td><span class="${hitClass}">${hitStr}</span></td>
        <td><span class="${chClass}">${chStr}</span></td>
        <td><span style="font-weight:800; color:var(--accent-gold);">${dmgStr}</span></td>
        <td>${safetyHtml}</td>
        <td><div style="display:flex; gap:0.25rem; flex-wrap:wrap;">${propBadges || '—'}</div></td>
        <td style="text-align:center;">
          <button type="button" class="btn-inspect-move" onclick="event.stopPropagation(); openMoveDetailModal(${m.id})" title="Inspect complete technical data & advice">
            🔍 Inspect
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function filterMovesTable(query = undefined) {
  const q = (query !== undefined && query !== null ? query : (document.getElementById('movesTableFilter')?.value || '')).toLowerCase().trim();
  const safety = state.movesSafetyFilter || 'ALL';
  const hitLevelFilter = document.getElementById('moveFilterHitLevel')?.value || 'ALL';
  const startupMin = parseInt(document.getElementById('moveFilterStartupMin')?.value, 10);
  const startupMax = parseInt(document.getElementById('moveFilterStartupMax')?.value, 10);
  const punishFilter = document.getElementById('moveFilterPunish')?.value || 'ALL';
  const stanceFilter = document.getElementById('moveFilterStance')?.value || 'ALL';
  const verFilter = document.getElementById('moveFilterVerification')?.value || 'ALL';

  let filtered = state.moves || [];

  // Quick Safety Pill
  if (safety !== 'ALL') {
    filtered = filtered.filter(m => {
      const blk = m.block_advantage;
      const hitLvl = (m.hit_level || '').toLowerCase();
      const props = (m.properties || []).map(p => (typeof p === 'string' ? p : (p.property_name || p.property_type || '')).toLowerCase());
      const name = (m.name || '').toLowerCase();
      const isStance = m.frame_state_type === 'NOT_APPLICABLE' || hitLvl === 's' || name.includes('stance') || m.is_stance_move;

      if (safety === 'SAFE') return (m.block_safety === 'SAFE' || (blk !== null && blk >= -9)) && !isStance;
      if (safety === 'UNSAFE') return (m.block_safety === 'UNSAFE' || (blk !== null && blk <= -10 && blk >= -14)) && !isStance;
      if (safety === 'LAUNCH_PUNISH') return (m.block_safety === 'LAUNCH_PUNISH' || m.is_launch_punishable || (blk !== null && blk <= -15)) && !isStance;
      if (safety === 'PLUS') return (m.is_plus_on_block || (blk !== null && blk >= 1)) && !isStance;
      if (safety === 'HIGH') return m.hit_level_type === 'HIGH' || hitLvl.startsWith('h');
      if (safety === 'MID') return m.hit_level_type === 'MID' || hitLvl.startsWith('m');
      if (safety === 'LOW') return m.hit_level_type === 'LOW' || hitLvl.startsWith('l');
      if (safety === 'HEAT') return m.is_heat_engager || props.some(p => p.includes('heat')) || name.includes('heat');
      if (safety === 'POWER_CRUSH') return m.is_power_crush || props.some(p => p.includes('crush') || p.includes('power'));
      if (safety === 'HOMING') return m.is_homing || props.some(p => p.includes('homing'));
      if (safety === 'TORNADO') return m.is_tornado || props.some(p => p.includes('tornado'));
      if (safety === 'STANCE') return isStance;
      return true;
    });
  }

  // Hit Level
  if (hitLevelFilter !== 'ALL') {
    filtered = filtered.filter(m => {
      const hl = (m.hit_level_type || m.hit_level || '').toUpperCase();
      if (hitLevelFilter === 'HIGH') return hl.includes('HIGH') || hl === 'H';
      if (hitLevelFilter === 'MID') return (hl.includes('MID') && !hl.includes('SPECIAL')) || hl === 'M';
      if (hitLevelFilter === 'LOW') return hl.includes('LOW') || hl === 'L';
      if (hitLevelFilter === 'SPECIAL_MID') return hl.includes('SPECIAL') || hl.includes('SM');
      if (hitLevelFilter === 'THROW') return hl.includes('THROW') || hl === 'T';
      if (hitLevelFilter === 'STANCE') return hl.includes('STANCE') || hl === 'S' || m.frame_state_type === 'NOT_APPLICABLE';
      return true;
    });
  }

  // Startup Range
  if (!isNaN(startupMin)) {
    filtered = filtered.filter(m => m.startup_frames !== null && m.startup_frames >= startupMin);
  }
  if (!isNaN(startupMax)) {
    filtered = filtered.filter(m => m.startup_frames !== null && m.startup_frames <= startupMax);
  }

  // Punishability Filter
  if (punishFilter !== 'ALL') {
    filtered = filtered.filter(m => {
      const blk = m.block_advantage;
      const isStance = m.frame_state_type === 'NOT_APPLICABLE' || (m.hit_level || '').toLowerCase() === 's';
      if (isStance) return false;
      if (punishFilter === 'SAFE') return m.block_safety === 'SAFE' || (blk !== null && blk >= -9);
      if (punishFilter === 'PUNISHABLE_10') return (m.punish_startup_min !== null && m.punish_startup_min <= 10) || (blk !== null && blk <= -10);
      if (punishFilter === 'PUNISHABLE_12') return (m.punish_startup_min !== null && m.punish_startup_min <= 12) || (blk !== null && blk <= -12);
      if (punishFilter === 'PUNISHABLE_14') return (m.punish_startup_min !== null && m.punish_startup_min <= 14) || (blk !== null && blk <= -14);
      if (punishFilter === 'LAUNCH_PUNISHABLE') return m.is_launch_punishable || m.block_safety === 'LAUNCH_PUNISH' || (blk !== null && blk <= -15);
      return true;
    });
  }

  // Stance Context Filter
  if (stanceFilter !== 'ALL') {
    filtered = filtered.filter(m => {
      const isStance = m.is_stance_move || m.frame_state_type === 'NOT_APPLICABLE' || (m.hit_level || '').toLowerCase() === 's' || (m.name || '').toLowerCase().includes('stance');
      if (stanceFilter === 'NEUTRAL_ONLY') return !isStance;
      if (stanceFilter === 'STANCE_ONLY') return isStance;
      return true;
    });
  }

  // Verification Status Filter
  if (verFilter !== 'ALL') {
    filtered = filtered.filter(m => {
      const status = (m.verification_status || 'VERIFIED').toUpperCase();
      return status === verFilter;
    });
  }

  // Search Query
  if (q) {
    filtered = filtered.filter(m => {
      const name = (m.name || '').toLowerCase();
      const not = (m.original_notation || '').toLowerCase();
      const hl = (m.hit_level || '').toLowerCase();
      const trans = (m.transition_stance || '').toLowerCase();
      const props = (m.properties || []).map(p => (typeof p === 'string' ? p : (p.property_name || p.property_type || '')).toLowerCase()).join(' ');
      return name.includes(q) || not.includes(q) || hl.includes(q) || trans.includes(q) || props.includes(q);
    });
  }

  renderMovesTable(filtered, true);
}

function resetMovesFilter() {
  state.movesSafetyFilter = 'ALL';
  const filterInput = document.getElementById('movesTableFilter');
  if (filterInput) filterInput.value = '';

  const hl = document.getElementById('moveFilterHitLevel');
  if (hl) hl.value = 'ALL';
  const minEl = document.getElementById('moveFilterStartupMin');
  if (minEl) minEl.value = '';
  const maxEl = document.getElementById('moveFilterStartupMax');
  if (maxEl) maxEl.value = '';
  const pun = document.getElementById('moveFilterPunish');
  if (pun) pun.value = 'ALL';
  const st = document.getElementById('moveFilterStance');
  if (st) st.value = 'ALL';
  const ver = document.getElementById('moveFilterVerification');
  if (ver) ver.value = 'ALL';

  document.querySelectorAll('#movesSafetyFilters .safety-pill').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.safety === 'ALL');
  });

  filterMovesTable('');
  showToast('Move Explorer filters reset to all data', 'info');
}

async function openMoveDetailModal(moveId) {
  playSfx('click');
  let move = (state.moves || []).find(m => m.id === moveId);
  if (!move) {
    move = await fetchAPI(`/moves/${moveId}`, true);
  }
  if (!move) {
    showToast('Unable to load move details', 'error');
    return;
  }

  const modal = document.getElementById('moveDetailModal');
  if (!modal) return;

  const char = (state.characters || []).find(c => c.slug === move.character_slug || c.id === move.character_id) || state.selectedCharacter;

  // Title & Header
  const titleEl = document.getElementById('miMoveTitle');
  if (titleEl) titleEl.textContent = move.name.toUpperCase();
  const avatarEl = document.getElementById('miCharAvatar');
  if (avatarEl) {
    avatarEl.src = (char && char.avatar_url) ? char.avatar_url : '/assets/avatars/jin-brand-256-C1-oe_x3.webp';
    avatarEl.alt = char ? char.name : 'Character';
  }
  const nameEl = document.getElementById('miCharName');
  if (nameEl) nameEl.textContent = move.character_name || (char ? char.name : 'Tekken 8 Fighter');
  const notEl = document.getElementById('miMoveNotation');
  if (notEl) {
    notEl.innerHTML = `${formatTekkenNotation(move.original_notation)} <span style="color:var(--text-muted); font-size:0.8rem; margin-left:0.4rem;">(${move.original_notation})</span>`;
  }

  // Hit Level Badge
  const hitLevelEl = document.getElementById('miHitLevelBadge');
  if (hitLevelEl) {
    const lvl = (move.hit_level_type || move.hit_level || 'MID').toUpperCase();
    let lvlClass = 'mid';
    if (lvl.includes('HIGH') || lvl === 'H') lvlClass = 'high';
    else if (lvl.includes('LOW') || lvl === 'L') lvlClass = 'low';
    else if (lvl.includes('SPECIAL') || lvl.includes('SM')) lvlClass = 'special-mid';
    else if (lvl.includes('THROW') || lvl === 'T') lvlClass = 'throw';
    else if (lvl.includes('STANCE') || lvl === 'S') lvlClass = 'stance';
    hitLevelEl.className = `move-level-badge ${lvlClass}`;
    hitLevelEl.textContent = lvl;
  }

  // Safety Badge
  const safetyEl = document.getElementById('miSafetyBadge');
  if (safetyEl) {
    const s = move.block_safety || (move.block_advantage !== null ? (move.block_advantage >= 1 ? 'PLUS' : (move.block_advantage >= -9 ? 'SAFE' : (move.block_advantage <= -15 ? 'LAUNCH_PUNISH' : 'UNSAFE'))) : 'UNKNOWN');
    let sClass = 'safe';
    let sText = 'SAFE (≤ -9)';
    if (s === 'PLUS') { sClass = 'plus'; sText = '+ ADVANTAGE'; }
    else if (s === 'UNSAFE') { sClass = 'unsafe'; sText = 'UNSAFE (-10 to -14)'; }
    else if (s === 'LAUNCH_PUNISH') { sClass = 'launch'; sText = 'LAUNCH PUNISHABLE'; }
    else if (s === 'NOT_APPLICABLE') { sClass = 'na'; sText = 'STANCE TRANSITION'; }
    else if (s === 'UNKNOWN') { sClass = 'na'; sText = 'UNKNOWN SAFETY'; }
    safetyEl.className = `move-safety-badge ${sClass}`;
    safetyEl.textContent = sText;
  }

  // Verification Badge
  const verEl = document.getElementById('miVerificationBadge');
  if (verEl) {
    verEl.textContent = (move.verification_status || 'VERIFIED').toUpperCase();
  }

  // Stats Grid
  const isStance = move.frame_state_type === 'NOT_APPLICABLE' || (move.hit_level || '').toLowerCase() === 's';

  // Startup
  const startupEl = document.getElementById('miStartupVal');
  if (startupEl) {
    startupEl.textContent = isStance ? 'N/A' : (move.startup_raw || (move.startup_frames !== null ? `i${move.startup_frames}` : 'Unknown'));
  }

  // Block
  const blockEl = document.getElementById('miBlockVal');
  if (blockEl) {
    if (isStance) {
      blockEl.textContent = 'N/A';
      blockEl.style.color = '#a855f7';
    } else if (move.block_advantage_raw) {
      blockEl.textContent = move.block_advantage_raw;
      blockEl.style.color = move.is_plus_on_block ? '#00e676' : (move.is_launch_punishable ? '#f43f5e' : (move.block_advantage < 0 ? '#fb7185' : '#e2e8f0'));
    } else if (move.block_advantage !== null) {
      blockEl.textContent = move.block_advantage > 0 ? `+${move.block_advantage}` : `${move.block_advantage}`;
      blockEl.style.color = move.block_advantage > 0 ? '#00e676' : (move.block_advantage <= -15 ? '#f43f5e' : (move.block_advantage < 0 ? '#fb7185' : '#e2e8f0'));
    } else {
      blockEl.textContent = 'Unknown';
      blockEl.style.color = 'var(--text-muted)';
    }
  }

  // Hit
  const hitEl = document.getElementById('miHitVal');
  if (hitEl) {
    if (isStance) {
      hitEl.textContent = 'N/A';
      hitEl.style.color = '#a855f7';
    } else if (move.hit_advantage_raw) {
      hitEl.textContent = move.hit_advantage_raw;
      hitEl.style.color = move.hit_advantage > 0 ? '#00e676' : '#e2e8f0';
    } else if (move.hit_advantage !== null) {
      hitEl.textContent = move.hit_advantage > 0 ? `+${move.hit_advantage}` : `${move.hit_advantage}`;
      hitEl.style.color = move.hit_advantage > 0 ? '#00e676' : '#e2e8f0';
    } else {
      hitEl.textContent = 'Unknown';
      hitEl.style.color = 'var(--text-muted)';
    }
  }

  // CH
  const chEl = document.getElementById('miCHVal');
  if (chEl) {
    if (isStance) {
      chEl.textContent = 'N/A';
    } else if (move.counter_hit_advantage_raw) {
      chEl.textContent = move.counter_hit_advantage_raw;
    } else if (move.counter_hit_advantage !== null) {
      chEl.textContent = move.counter_hit_advantage > 0 ? `+${move.counter_hit_advantage}` : `${move.counter_hit_advantage}`;
    } else if (move.is_counter_hit_launcher) {
      chEl.textContent = 'Launch';
      chEl.style.color = '#f43f5e';
    } else {
      chEl.textContent = 'Same as Hit';
      chEl.style.color = 'var(--text-muted)';
    }
  }

  // Damage
  const dmgEl = document.getElementById('miDamageVal');
  if (dmgEl) {
    dmgEl.textContent = move.damage !== null ? `${move.damage}` : (isStance ? '—' : 'Unknown');
  }

  // Tracking
  const trackEl = document.getElementById('miTrackingVal');
  if (trackEl) {
    trackEl.textContent = move.tracking_property || (move.is_homing ? 'Homing (Tracks Both Sides)' : 'Linear (Step Left)');
  }

  // Punish Recommendation Box
  const punishEl = document.getElementById('miPunishDesc');
  if (punishEl) {
    punishEl.textContent = move.punish_recommendation || (isStance ? 'Stance transition: No direct block punish applies. Interrupt during startup or contest transition frames.' : 'Safe on block (≤ -9). No guaranteed punish available.');
  }

  // Defensive Response Box
  const defEl = document.getElementById('miDefensiveDesc');
  if (defEl) {
    defEl.textContent = move.defensive_response || 'Standard guard position. Observe hit level properties.';
  }

  // Pushback Spacing Alert (Phase 6 QoL)
  const pbWrap = document.getElementById('miPushbackWrap');
  const pbDesc = document.getElementById('miPushbackDesc');
  if (pbWrap && pbDesc) {
    if (move.has_pushback || move.pushback_warning) {
      pbDesc.textContent = move.pushback_warning || 'Pushback detected on block. Standard close-range jabs may whiff; use range-extended punishers.';
      pbWrap.style.display = 'block';
    } else {
      pbWrap.style.display = 'none';
    }
  }

  // User Practice Note Box (Phase 6 QoL)
  const noteWrap = document.getElementById('miUserNoteWrap');
  const noteDesc = document.getElementById('miUserNoteDesc');
  const noteBtn = document.getElementById('miBtnEditNote');
  if (noteWrap && noteDesc) {
    const targetKey = `${move.character_slug || char?.slug || 'jin'}__${move.original_notation}`;
    const allNotes = getPracticeNotes();
    const existingNote = allNotes.find(n => n.targetKey === targetKey || (n.targetType === 'MOVE' && n.targetLabel?.includes(move.original_notation)));
    if (existingNote) {
      noteDesc.innerHTML = `<strong>[${escapeHtml(existingNote.category || 'Practice')}]</strong> ${escapeHtml(existingNote.content)}`;
      if (noteBtn) {
        noteBtn.textContent = 'Edit Note';
        noteBtn.onclick = () => {
          openPracticeNoteEditModal(existingNote.id);
        };
      }
    } else {
      noteDesc.textContent = 'No personal practice notes added for this move yet.';
      if (noteBtn) {
        noteBtn.textContent = '+ Add Note';
        noteBtn.onclick = () => {
          openPracticeNoteEditModal(null, {
            key: targetKey,
            type: 'MOVE',
            label: `${char ? char.name : 'Fighter'}: ${move.original_notation} (${move.name || 'Move'})`,
            characterSlug: move.character_slug || char?.slug || 'jin',
            category: 'Execution Tip'
          });
        };
      }
    }
  }

  // Conditional Notes
  const condWrap = document.getElementById('miConditionalWrap');
  const condDesc = document.getElementById('miConditionalDesc');
  if (condWrap && condDesc) {
    if (move.conditional_notes) {
      condDesc.textContent = move.conditional_notes;
      condWrap.style.display = 'block';
    } else {
      condWrap.style.display = 'none';
    }
  }


  // Provenance Bar
  const patchEl = document.getElementById('miPatchVer');
  if (patchEl) patchEl.textContent = move.patch_version || '3.00.02';
  const sourceEl = document.getElementById('miSourceName');
  if (sourceEl) sourceEl.textContent = move.source_name || 'wavu.wiki';
  const dateEl = document.getElementById('miVerifiedDate');
  if (dateEl) dateEl.textContent = move.last_verified_date || '2026-05-25';

  // Test Notation Button
  const testBtn = document.getElementById('miBtnTestNotation');
  if (testBtn) {
    testBtn.onclick = () => {
      closeMoveDetailModal();
      testNotationString(move.original_notation);
    };
  }

  modal.style.display = 'flex';
}

function closeMoveDetailModal() {
  playSfx('click');
  const modal = document.getElementById('moveDetailModal');
  if (modal) modal.style.display = 'none';
}

// 4. Render Stages Showcase
async function loadStages() {
  const data = await fetchAPI('/stages', true);
  if (data && Array.isArray(data) && data.length > 0) {
    state.stages = data;
  }
  renderStages();
}

async function setGlobalStage(stageId, options = {}) {
  const idNum = parseInt(stageId);
  if (!idNum || isNaN(idNum)) return;
  state.selectedStageId = idNum;
  if (!state.comboFinder) state.comboFinder = {};
  state.comboFinder.stageId = idNum;

  const stg = state.stages?.find(s => String(s.id) === String(idNum));
  if (!stg) return;

  // 1. Sync dropdowns across all modules
  ['stageSelect', 'comboLabStageSelect', 'heroStageSelect'].forEach(selId => {
    const el = document.getElementById(selId);
    if (el && String(el.value) !== String(idNum)) {
      el.value = idNum;
    }
  });

  // 2. Sync Stage Showcase Cards in #stagesGrid
  document.querySelectorAll('.stage-card').forEach(c => c.classList.remove('active'));
  const sc = document.getElementById(`stage_card_${idNum}`);
  if (sc) sc.classList.add('active');

  // 3. Update Matchup Analyzer stage preview
  updateStagePreview();

  // 4. Update Combo Lab stage hazard thumbnail and chip
  const thumb = document.getElementById('comboLabStageThumb');
  if (thumb) {
    thumb.src = stg.image_url || stg.image || '/assets/img/stages/arena.jpg';
    thumb.alt = stg.name;
  }
  const hazardsEl = document.getElementById('comboLabStageHazards');
  if (hazardsEl) {
    const parts = [];
    if (stg.has_walls === false || stg.boundary_shape === 'Infinite') parts.push('Infinite (No Walls)');
    else parts.push(`Walled Arena (${stg.boundary_shape || 'Enclosed'})`);
    if (stg.wall_break) parts.push('Wall Break');
    if (stg.floor_break) parts.push('Floor Break');
    if (stg.floor_blast) parts.push('Floor Blast');
    if (stg.wall_blast) parts.push('Wall Blast');
    if (stg.balcony_break) parts.push('Balcony Break');
    hazardsEl.textContent = parts.join(' • ');
  }

  // 5. Update Matchup Stage Strategy if characters selected (preserves character identities)
  const pChar = state.matchup?.player;
  const oChar = state.matchup?.opponent;
  if (pChar && oChar) {
    loadStageStrategy(idNum, pChar.id, oChar.id);
  }

  // 6. Refresh P1 and P2 Combo Lab recommendations asynchronously
  if (options.skipComboLabRefresh !== true) {
    try {
      await Promise.all([
        loadComboFinderFighter('p1'),
        loadComboFinderFighter('p2')
      ]);
      renderComboLab();
    } catch (e) {
      console.warn('Error refreshing Combo Lab for stage:', e);
    }
  }

  // 7. Optional scroll to target section
  if (options.scrollToSection) {
    const el = document.getElementById(options.scrollToSection);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function selectStage(stageId) {
  playSfx('click');
  setGlobalStage(stageId, { scrollToSection: 'analyzer' });
}

function renderStages() {
  const container = document.getElementById('stagesGrid');
  if (!container) return;

  const currentSelect = document.getElementById('stageSelect');
  const activeStageId = currentSelect ? parseInt(currentSelect.value) : (state.selectedStageId || 1);

  container.innerHTML = state.stages.map(s => {
    const hazardsList = s.hazards || [];
    const imgSrc = s.image_url || s.image || '/assets/img/stages/arena.jpg';
    const fallbackSvg = '/assets/img/stages/arena.svg';
    const locationStr = s.location || 'Official Arena';
    const gimmickStr = s.notes || s.special_mechanics || s.gimmick || (s.has_walls ? 'Walled tournament battleground' : 'Infinite arena');
    const isSelected = s.id === activeStageId;
    const boundaryStr = s.has_walls ? (s.boundary_shape || 'Walled') : 'Infinite';
    const distStr = s.wall_distance || (s.has_walls ? '24m' : 'Unbounded');

    // Destructible Hazard Badges with full verified hazard recognition
    const hazardBadges = [];
    if (imgSrc.endsWith('.svg')) hazardBadges.push('<span class="stage-overlay-badge badge-blueprint" style="background:rgba(14,165,233,0.9); color:#fff; border:1px solid #38bdf8; font-weight:800;">TACTICAL BLUEPRINT</span>');
    if (!s.has_walls) hazardBadges.push('<span class="stage-overlay-badge badge-infinite">INFINITE</span>');
    if (s.wall_break) hazardBadges.push('<span class="stage-overlay-badge badge-wallbreak">WALL BREAK</span>');
    if (s.hard_wall_break) hazardBadges.push('<span class="stage-overlay-badge badge-wallbreak">HARD WALL BREAK</span>');
    if (s.wall_blast) hazardBadges.push('<span class="stage-overlay-badge badge-wallbreak">WALL BLAST</span>');
    if (s.wall_bound) hazardBadges.push('<span class="stage-overlay-badge badge-wallbreak">WALL BOUND</span>');
    if (s.floor_break) hazardBadges.push('<span class="stage-overlay-badge badge-floorbreak">FLOOR BREAK</span>');
    if (s.floor_blast) hazardBadges.push('<span class="stage-overlay-badge badge-floorbreak">FLOOR BLAST</span>');
    if (s.balcony_break) hazardBadges.push('<span class="stage-overlay-badge badge-balcony">BALCONY BREAK</span>');

    const altText = imgSrc.endsWith('.svg') ? `Tactical Blueprint Vector: ${s.name}` : `Arena Photograph: ${s.name}`;

    return `
      <div class="stage-card ${isSelected ? 'active' : ''}" 
           id="stage_card_${s.id}" 
           onclick="selectStage(${s.id})"
           onkeydown="if(event.key==='Enter'||event.key===' ')selectStage(${s.id})"
           role="button"
           tabindex="0"
           aria-label="Select stage ${s.name}: ${boundaryStr}, ${distStr}"
           title="${gimmickStr}">
        <div class="stage-img-wrap">
          <img class="stage-img" src="${imgSrc}" alt="${altText}" loading="lazy" onerror="this.src='${fallbackSvg}'">
          <div class="stage-img-overlay-badges">
            ${hazardBadges.join('')}
          </div>
          ${isSelected ? '<div class="stage-selected-indicator"><span>ACTIVE ARENA</span></div>' : ''}
        </div>
        <div class="stage-meta">
          <div class="stage-meta-header">
            <div>
              <div class="stage-name">${s.name}</div>
              <div class="stage-location">${locationStr} • <span style="color:var(--text-muted); font-size:0.7rem;">${boundaryStr} (${distStr})</span></div>
            </div>
            <button class="stage-select-btn ${isSelected ? 'selected' : ''}" type="button" aria-pressed="${isSelected}">
              ${isSelected ? 'Selected' : 'Select'}
            </button>
          </div>
          <div class="stage-hazards">
            ${hazardsList.map(h => `<span class="hazard-pill">${h}</span>`).join('')}
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// 5. Notation Engine Real-Time Translation
async function updateNotationDisplay() {
  const inputEl = document.getElementById('notationInput');
  const inputVal = inputEl ? inputEl.value.trim() || 'df+2' : 'df+2';
  state.currentNotation = inputVal;

  // Server-side conversion call
  try {
    const res = await fetch(`${API_BASE}/notation/convert`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        notation: inputVal,
        controller_layout: state.controllerLayout
      })
    });
    if (res.ok) {
      const data = await res.json();
      renderNotationCards(data);
      return;
    }
  } catch (e) {
    // Graceful fallback
  }

  // Client-side instant display fallback
  renderClientNotation(inputVal);
}

function renderNotationCards(data) {
  document.getElementById('modeArrow').textContent = data.arrow_display || '—';
  document.getElementById('modeEnglish').textContent = data.english_display || '—';
  document.getElementById('modeNumpad').textContent = data.numpad_display || '—';
  document.getElementById('modeController').textContent = data.controller_display || '—';

  const unsAlert = document.getElementById('unsupportedAlert');
  if (unsAlert) {
    if (data.has_unsupported_syntax) {
      unsAlert.style.display = 'block';
      unsAlert.textContent = `Unsupported syntax flagged for review: ${data.unsupported_tokens.join(', ')}`;
    } else {
      unsAlert.style.display = 'none';
    }
  }
}

function renderClientNotation(inputStr) {
  let arrow = inputStr;
  let eng = inputStr;
  let numpad = inputStr;
  let ctl = inputStr;

  if (inputStr.toLowerCase() === 'df+2') {
    arrow = '↘ + 2';
    eng = 'Down Forward + Right Punch';
    numpad = '3 + 2';
    ctl = state.controllerLayout === 'PLAYSTATION' ? '↘ + △' : (state.controllerLayout === 'XBOX' ? '↘ + Y' : '↘ + 2');
  }

  document.getElementById('modeArrow').textContent = arrow;
  document.getElementById('modeEnglish').textContent = eng;
  document.getElementById('modeNumpad').textContent = numpad;
  document.getElementById('modeController').textContent = ctl;
}

function insertNotationToken(token) {
  const inputEl = document.getElementById('notationInput');
  if (!inputEl) return;
  const current = inputEl.value.trim();
  if (!current) {
    inputEl.value = token;
  } else if (['1', '2', '3', '4', '1+2'].includes(token) && !current.endsWith('+') && !current.endsWith(',')) {
    inputEl.value = `${current}+${token}`;
  } else {
    inputEl.value = `${current},${token}`;
  }
  updateNotationDisplay();
}

function testNotationString(notation) {
  const inputEl = document.getElementById('notationInput');
  if (inputEl) {
    inputEl.value = notation;
    updateNotationDisplay();
    document.getElementById('notation').scrollIntoView({ behavior: 'smooth' });
  }
}

function filterByMoveText(text) {
  const tableFilter = document.getElementById('movesTableFilter');
  if (tableFilter) {
    tableFilter.value = text;
    filterMovesTable(text.toLowerCase());
    document.getElementById('moves').scrollIntoView({ behavior: 'smooth' });
  }
}

// 6. Coverage & Sources Data
async function loadCoverageData() {
  const data = await fetchAPI('/coverage/summary', true);
  if (data) {
    state.coverage = data;
    const rosterEl = document.getElementById('covRosterCount');
    const rosterPctEl = document.getElementById('covRosterPct');
    const totalMovesEl = document.getElementById('covTotalMoves');
    const overallPctEl = document.getElementById('covOverallPct');

    if (rosterEl) rosterEl.textContent = `${data.characters_found} / ${data.characters_expected}`;
    if (rosterPctEl) rosterPctEl.textContent = `${data.character_coverage_pct}% Ingested`;
    if (totalMovesEl) totalMovesEl.textContent = `${data.total_moves_cataloged}`;
    if (overallPctEl) overallPctEl.textContent = `${data.overall_field_completeness_pct}%`;
  }
}

async function loadSourcesData() {
  const data = await fetchAPI('/sources', true);
  if (data && Array.isArray(data)) {
    state.sources = data;
    const grid = document.getElementById('sourcesGrid');
    if (!grid) return;

    grid.innerHTML = data.map(s => {
      let badgeClass = 'badge-approved';
      if (s.approval_status === 'APPROVED_WITH_RESTRICTIONS') badgeClass = 'badge-restrictions';
      if (s.approval_status === 'RESEARCH_ONLY') badgeClass = 'badge-research';
      if (s.approval_status === 'BLOCKED_PENDING_PERMISSION') badgeClass = 'badge-blocked';

      return `
        <div class="source-item-card">
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div class="source-item-name">${s.name}</div>
            <span class="feat-badge ${badgeClass}">${s.approval_status.replace(/_/g, ' ')}</span>
          </div>
          <div style="font-size:0.75rem; color:var(--text-muted);">
            License: <span style="color:#fff; font-weight:700;">${s.license_type || 'Unspecified'}</span>
          </div>
          <div style="font-size:0.75rem; color:var(--text-muted);">
            Policy: <span style="color:var(--accent-cyan);">${s.rate_limit_policy || 'Standard'}</span>
          </div>
          <a href="${s.base_url}" target="_blank" style="font-size:0.75rem; color:var(--accent-cyan); text-decoration:none; margin-top:0.25rem;">
            ${s.base_url} &rarr;
          </a>
        </div>
      `;
    }).join('');
  }
}

// Utility: Debounce
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ==========================================================================
// 7. Matchup Analyzer & Selection System
// ==========================================================================

async function initMatchupAnalyzer() {
  populateMatchupDropdowns();
  setupMatchupControls();
  await restoreUserPreferences();
  await runMatchupAnalysis();
}

function populateMatchupDropdowns() {
  const pSelect = document.getElementById('playerSelect');
  const oSelect = document.getElementById('opponentSelect');
  const sSelect = document.getElementById('stageSelect');

  if (!pSelect || !oSelect || !sSelect) return;

  // Populate Characters with local portraits and archetypes
  const charOptions = state.characters.map(c => {
    const avatar = c.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp';
    const archetype = c.archetype || 'Tekken Fighter';
    return `<option value="${c.id}" data-slug="${c.slug}" data-avatar="${avatar}" data-archetype="${archetype}">${c.name}</option>`;
  }).join('');

  pSelect.innerHTML = charOptions;
  oSelect.innerHTML = charOptions;

  // Set default: Player = Jin, Opponent = Kazuya
  const jin = state.characters.find(c => c.slug === 'jin');
  const kazuya = state.characters.find(c => c.slug === 'kazuya');

  if (jin) pSelect.value = jin.id;
  if (kazuya) oSelect.value = kazuya.id;
  else if (state.characters.length > 1) oSelect.value = state.characters[1].id;

  // Populate Stages with real database verified records
  sSelect.innerHTML = state.stages.map(st => {
    const shape = st.boundary_shape || (st.has_walls ? 'Walled' : 'Infinite');
    const img = st.image_url || st.image || '/assets/img/stages/arena.jpg';
    return `<option value="${st.id}" data-slug="${st.slug}" data-image="${img}">${st.name} (${shape})</option>`;
  }).join('');

  if (state.stages.length > 0) {
    sSelect.value = state.stages[0].id;
  }

  updatePlayerPreview();
  updateOpponentPreview();
  updateStagePreview();
}

function setupMatchupControls() {
  const pSelect = document.getElementById('playerSelect');
  const oSelect = document.getElementById('opponentSelect');
  const sSelect = document.getElementById('stageSelect');
  const pSearch = document.getElementById('playerSearchInput');
  const oSearch = document.getElementById('opponentSearchInput');
  const btnSwap = document.getElementById('btnSwapFighters');
  const btnRandP = document.getElementById('btnRandomPlayer');
  const btnRandO = document.getElementById('btnRandomOpponent');
  const btnRun = document.getElementById('btnRunAnalysis');

  // Change events
  if (pSelect) {
    pSelect.addEventListener('change', () => {
      updatePlayerPreview();
      runMatchupAnalysis();
      const pId = parseInt(pSelect.value);
      const char = state.characters?.find(c => c.id === pId);
      if (char && state.comboFinder) {
        state.comboFinder.p1Slug = char.slug;
        const fSelect = document.getElementById('comboLabFighterSelect');
        if (fSelect && fSelect.value !== char.slug) fSelect.value = char.slug;
        if (typeof loadComboFinderFighter === 'function') {
          loadComboFinderFighter('p1').then(() => {
            if (typeof renderComboLab === 'function') renderComboLab();
          }).catch(e => console.warn(e));
        }
      }
    });
  }

  if (oSelect) {
    oSelect.addEventListener('change', () => {
      updateOpponentPreview();
      runMatchupAnalysis();
      const oId = parseInt(oSelect.value);
      const char = state.characters?.find(c => c.id === oId);
      if (char && state.comboFinder) {
        state.comboFinder.p2Slug = char.slug;
        const oSelectCL = document.getElementById('comboLabOpponentSelect');
        if (oSelectCL && oSelectCL.value !== char.slug) oSelectCL.value = char.slug;
        if (typeof loadComboFinderFighter === 'function') {
          loadComboFinderFighter('p2').then(() => {
            if (typeof renderComboLab === 'function') renderComboLab();
          }).catch(e => console.warn(e));
        }
      }
    });
  }


  if (sSelect) {
    sSelect.addEventListener('change', () => {
      setGlobalStage(sSelect.value);
      runMatchupAnalysis();
    });
  }

  // Filter player select options
  if (pSearch && pSelect) {
    pSearch.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      filterSelectOptions(pSelect, q);
    });
  }

  // Filter opponent select options
  if (oSearch && oSelect) {
    oSearch.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      filterSelectOptions(oSelect, q);
    });
  }

  // Random Buttons
  if (btnRandP) {
    btnRandP.addEventListener('click', () => {
      pickRandomFighter('player');
    });
  }

  if (btnRandO) {
    btnRandO.addEventListener('click', () => {
      pickRandomFighter('opponent');
    });
  }

  // 1-Click Swap Button
  if (btnSwap) {
    btnSwap.addEventListener('click', () => {
      swapFighters();
    });
  }

  // Run Button
  if (btnRun) {
    btnRun.addEventListener('click', () => {
      runMatchupAnalysis();
    });
  }

  // Tactical Conditions Pill Toggles
  const conditionGroups = [
    { id: 'wallPositionGroup', key: 'wall_position' },
    { id: 'heatStateGroup', key: 'heat_state' },
    { id: 'distanceGroup', key: 'starting_distance' },
    { id: 'playerSideGroup', key: 'player_side' }
  ];

  conditionGroups.forEach(grp => {
    const el = document.getElementById(grp.id);
    if (!el) return;
    el.querySelectorAll('.cond-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        el.querySelectorAll('.cond-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.matchup.conditions[grp.key] = pill.dataset.val;
        runMatchupAnalysis();
      });
    });
  });

  // Phase 5: Character-Specific Combo & Juggle Compatibility Controls
  const comboTypePills = document.getElementById('comboTypePills');
  if (comboTypePills) {
    comboTypePills.querySelectorAll('.combo-filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        comboTypePills.querySelectorAll('.combo-filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.combosPhase5.activeCategory = btn.dataset.cat || 'ALL';
        renderComboRecommendations();
      });
    });
  }

  const comboSearch = document.getElementById('comboSearchInput');
  if (comboSearch) {
    comboSearch.addEventListener('input', debounce((e) => {
      state.combosPhase5.searchQuery = e.target.value.toLowerCase().trim();
      renderComboRecommendations();
    }, 150));
  }

  const checkHeat = document.getElementById('comboCheckHeat');
  if (checkHeat) {
    checkHeat.addEventListener('change', (e) => {
      state.combosPhase5.requiresHeat = e.target.checked;
      renderComboRecommendations();
    });
  }

  const checkCH = document.getElementById('comboCheckCH');
  if (checkCH) {
    checkCH.addEventListener('change', (e) => {
      state.combosPhase5.requiresCH = e.target.checked;
      renderComboRecommendations();
    });
  }

  const diffSelect = document.getElementById('comboDiffSelect');
  if (diffSelect) {
    diffSelect.addEventListener('change', (e) => {
      state.combosPhase5.activeDifficulty = e.target.value;
      renderComboRecommendations();
    });
  }

  const hurtboxSelect = document.getElementById('comboHurtboxFilter');
  if (hurtboxSelect) {
    hurtboxSelect.addEventListener('change', (e) => {
      state.combosPhase5.activeHurtbox = e.target.value;
      renderComboRecommendations();
    });
  }
}

function filterSelectOptions(selectEl, query) {
  let firstMatch = null;
  Array.from(selectEl.options).forEach(opt => {
    const text = opt.textContent.toLowerCase();
    const match = !query || text.includes(query);
    opt.style.display = match ? '' : 'none';
    if (match && !firstMatch) firstMatch = opt;
  });
  if (firstMatch && query) {
    selectEl.value = firstMatch.value;
    selectEl.dispatchEvent(new Event('change'));
  }
}

function formatHurtboxLabel(hb) {
  if (!hb) return 'Male Standard';
  const clean = String(hb).replace(/_/g, ' ').toLowerCase();
  return clean.replace(/\b\w/g, c => c.toUpperCase());
}

function updatePlayerPreview() {
  const pSelect = document.getElementById('playerSelect');
  const avatarImg = document.getElementById('playerAvatarPreview');
  const badge = document.getElementById('playerArchetypeBadge');
  const hurtboxChip = document.getElementById('playerHurtboxChip');
  const styleChip = document.getElementById('playerStyleChip');
  if (!pSelect) return;

  const charId = parseInt(pSelect.value);
  const char = state.characters.find(c => c.id === charId);
  const selectedOpt = (pSelect.selectedOptions && pSelect.selectedOptions.length > 0) ? pSelect.selectedOptions[0] : null;

  const avatar = (char && char.avatar_url) || (selectedOpt && selectedOpt.dataset && selectedOpt.dataset.avatar) || '/assets/avatars/jin-brand-256-C1-oe_x3.webp';
  const archetype = (char && char.archetype) || (selectedOpt && selectedOpt.dataset && selectedOpt.dataset.archetype) || 'Mishima / Allies';

  if (avatarImg) {
    avatarImg.src = avatar;
    avatarImg.onerror = () => { avatarImg.src = '/assets/avatars/jin-brand-256-C1-oe_x3.webp'; };
  }
  if (badge) badge.textContent = archetype;
  if (hurtboxChip) {
    hurtboxChip.textContent = `Hurtbox: ${formatHurtboxLabel(char && char.hurtbox_class)}`;
  }
  if (styleChip) {
    styleChip.textContent = archetype;
  }
}

function updateOpponentPreview() {
  const oSelect = document.getElementById('opponentSelect');
  const avatarImg = document.getElementById('opponentAvatarPreview');
  const badge = document.getElementById('opponentArchetypeBadge');
  const hurtboxChip = document.getElementById('opponentHurtboxChip');
  const styleChip = document.getElementById('opponentStyleChip');
  if (!oSelect) return;

  const charId = parseInt(oSelect.value);
  const char = state.characters.find(c => c.id === charId);
  const selectedOpt = (oSelect.selectedOptions && oSelect.selectedOptions.length > 0) ? oSelect.selectedOptions[0] : null;

  const avatar = (char && char.avatar_url) || (selectedOpt && selectedOpt.dataset && selectedOpt.dataset.avatar) || '/assets/avatars/kazuya-brand-256-BInk9tTm.webp';
  const archetype = (char && char.archetype) || (selectedOpt && selectedOpt.dataset && selectedOpt.dataset.archetype) || 'Mishima';

  if (avatarImg) {
    avatarImg.src = avatar;
    avatarImg.onerror = () => { avatarImg.src = '/assets/avatars/kazuya-brand-256-BInk9tTm.webp'; };
  }
  if (badge) badge.textContent = archetype;
  if (hurtboxChip) {
    hurtboxChip.textContent = `Hurtbox: ${formatHurtboxLabel(char && char.hurtbox_class)}`;
  }
  if (styleChip) {
    styleChip.textContent = archetype;
  }
}

function viewFighterMoves(playerKey) {
  const selectId = playerKey === 'p1' ? 'playerSelect' : 'opponentSelect';
  const sel = document.getElementById(selectId);
  if (!sel) return;
  const charId = parseInt(sel.value);
  const char = state.characters.find(c => c.id === charId);
  if (!char) return;

  if (typeof selectCharacter === 'function') {
    selectCharacter(char.slug);
  }
  const movesEl = document.getElementById('moves');
  if (movesEl) {
    movesEl.scrollIntoView({ behavior: 'smooth' });
  }
  showToast(`Viewing frame data & moves for ${char.name}`, 'info');
}

function updateStagePreview() {
  const sSelect = document.getElementById('stageSelect');
  const thumb = document.getElementById('selectedStageThumb');
  const hazardsBox = document.getElementById('stageHazardsMini');
  if (!sSelect) return;

  const stageId = parseInt(sSelect.value);
  const stage = state.stages.find(s => s.id === stageId);
  if (stage) {
    const stageImgSrc = stage.image_url || stage.image || '/assets/img/stages/arena.jpg';
    if (thumb) {
      thumb.src = stageImgSrc;
      thumb.onerror = () => { thumb.src = '/assets/img/stages/arena.jpg'; };
    }
    const dashStageImg = document.getElementById('dashStageImg');
    if (dashStageImg) {
      dashStageImg.src = stageImgSrc;
      dashStageImg.onerror = () => { dashStageImg.src = '/assets/img/stages/arena.jpg'; };
    }
    const faceoffBanner = document.getElementById('faceoffHeroBanner');
    if (faceoffBanner) {
      faceoffBanner.style.backgroundImage = `linear-gradient(180deg, rgba(14, 17, 24, 0.78) 0%, rgba(10, 12, 18, 0.94) 100%), radial-gradient(circle at 50% 50%, rgba(255, 30, 56, 0.12), transparent 70%), url('${stageImgSrc}')`;
      faceoffBanner.style.backgroundSize = 'cover';
      faceoffBanner.style.backgroundPosition = 'center';
    }
    const stagePhotoImg = document.getElementById('stageTacticalPhotoImg');
    if (stagePhotoImg) {
      stagePhotoImg.src = stageImgSrc;
      stagePhotoImg.onerror = () => { stagePhotoImg.src = '/assets/img/stages/arena.jpg'; };
    }
    const stagePhotoName = document.getElementById('stageTacticalPhotoName');
    if (stagePhotoName) {
      stagePhotoName.textContent = stage.name.toUpperCase();
    }
    const stagePhotoLoc = document.getElementById('stageTacticalPhotoLoc');
    if (stagePhotoLoc) {
      stagePhotoLoc.textContent = stage.location || 'Official Arena';
    }

    if (hazardsBox) {
      const hazards = stage.hazards || [];
      if (hazards.length === 0) {
        hazardsBox.innerHTML = '<span class="mini-hazard-pill safe">Standard Walled</span>';
      } else {
        hazardsBox.innerHTML = hazards.slice(0, 3).map(h => {
          const isSafe = h.includes('Infinite') || h.includes('Standard');
          return `<span class="mini-hazard-pill ${isSafe ? 'safe' : ''}">${h}</span>`;
        }).join('');
      }
    }

    // Highlight active card in stages showcase
    document.querySelectorAll('.stage-card').forEach(c => c.classList.remove('active'));
    const sc = document.getElementById(`stage_card_${stageId}`);
    if (sc) sc.classList.add('active');
  }
}

function pickRandomFighter(target) {
  if (!state.characters || state.characters.length === 0) return;
  const pSelect = document.getElementById('playerSelect');
  const oSelect = document.getElementById('opponentSelect');

  const randomChar = state.characters[Math.floor(Math.random() * state.characters.length)];
  if (target === 'player' && pSelect) {
    pSelect.value = randomChar.id;
    updatePlayerPreview();
  } else if (target === 'opponent' && oSelect) {
    oSelect.value = randomChar.id;
    updateOpponentPreview();
  }
  runMatchupAnalysis();
}

function swapFighters() {
  const pSelect = document.getElementById('playerSelect');
  const oSelect = document.getElementById('opponentSelect');
  if (!pSelect || !oSelect) return;

  const tempVal = pSelect.value;
  pSelect.value = oSelect.value;
  oSelect.value = tempVal;

  updatePlayerPreview();
  updateOpponentPreview();

  const p1Char = state.characters.find(c => c.id === parseInt(pSelect.value));
  const p2Char = state.characters.find(c => c.id === parseInt(oSelect.value));
  if (p1Char && p2Char) {
    showToast(`Swapped: P1 is now ${p1Char.name}, P2 is now ${p2Char.name}`, 'info');
    if (state.comboFinder) {
      state.comboFinder.p1Slug = p1Char.slug;
      state.comboFinder.p2Slug = p2Char.slug;
      const fSelect = document.getElementById('comboLabFighterSelect');
      const oSelectCL = document.getElementById('comboLabOpponentSelect');
      if (fSelect) fSelect.value = p1Char.slug;
      if (oSelectCL) oSelectCL.value = p2Char.slug;
      if (typeof loadComboFinderFighter === 'function') {
        Promise.all([
          loadComboFinderFighter('p1'),
          loadComboFinderFighter('p2')
        ]).then(() => {
          if (typeof renderComboLab === 'function') renderComboLab();
        }).catch(e => console.warn(e));
      }
    }
  }

  runMatchupAnalysis();
}


async function restoreUserPreferences() {
  const pSelect = document.getElementById('playerSelect');
  const oSelect = document.getElementById('opponentSelect');
  const sSelect = document.getElementById('stageSelect');

  // Try fetching saved preferences from backend
  try {
    const prefData = await fetchAPI(`/matchup/preferences?session_token=${state.sessionToken}`);
    if (prefData && prefData.player_character_id && prefData.opponent_character_id) {
      if (pSelect) pSelect.value = prefData.player_character_id;
      if (oSelect) oSelect.value = prefData.opponent_character_id;
      if (sSelect && prefData.stage_id) sSelect.value = prefData.stage_id;
      
      if (prefData.conditions) {
        state.matchup.conditions = { ...state.matchup.conditions, ...prefData.conditions };
        applyConditionsToUI(state.matchup.conditions);
      }
      updatePlayerPreview();
      updateOpponentPreview();
      updateStagePreview();
      return;
    }
  } catch (e) {
    // Fall back to localStorage
  }

  const localPref = localStorage.getItem('tekken8_matchup_pref');
  if (localPref) {
    try {
      const p = JSON.parse(localPref);
      if (pSelect && p.player_id) pSelect.value = p.player_id;
      if (oSelect && p.opponent_id) oSelect.value = p.opponent_id;
      if (sSelect && p.stage_id) sSelect.value = p.stage_id;
      if (p.conditions) {
        state.matchup.conditions = { ...state.matchup.conditions, ...p.conditions };
        applyConditionsToUI(state.matchup.conditions);
      }
      updatePlayerPreview();
      updateOpponentPreview();
      updateStagePreview();
    } catch (e) {}
  }
}

function applyConditionsToUI(conds) {
  const map = {
    'wall_position': 'wallPositionGroup',
    'heat_state': 'heatStateGroup',
    'starting_distance': 'distanceGroup',
    'player_side': 'playerSideGroup'
  };

  Object.entries(map).forEach(([key, grpId]) => {
    const val = conds[key];
    const grp = document.getElementById(grpId);
    if (grp && val) {
      grp.querySelectorAll('.cond-pill').forEach(p => {
        p.classList.toggle('active', p.dataset.val === val);
      });
    }
  });
}

function saveUserPreferencesLocally(playerId, opponentId, stageId, conditions) {
  const payload = {
    player_id: playerId,
    opponent_id: opponentId,
    stage_id: stageId,
    conditions: conditions
  };
  localStorage.setItem('tekken8_matchup_pref', JSON.stringify(payload));
}

async function runMatchupAnalysis() {
  invalidateApiCache();
  const pSelect = document.getElementById('playerSelect');
  const oSelect = document.getElementById('opponentSelect');
  const sSelect = document.getElementById('stageSelect');

  if (!pSelect || !oSelect || !sSelect) return;

  const playerId = parseInt(pSelect.value);
  const opponentId = parseInt(oSelect.value);
  const stageId = parseInt(sSelect.value);

  if (isNaN(playerId) || isNaN(opponentId) || isNaN(stageId)) return;

  saveUserPreferencesLocally(playerId, opponentId, stageId, state.matchup.conditions);

  const loadingEl = document.getElementById('matchupLoading');
  const errorEl = document.getElementById('matchupError');
  const dashEl = document.getElementById('matchupDashboardContent');

  if (loadingEl) loadingEl.style.display = 'flex';
  if (errorEl) errorEl.style.display = 'none';
  if (dashEl) dashEl.style.display = 'none';

  try {
    const response = await fetch(`${API_BASE}/matchup/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        player_character_id: playerId,
        opponent_character_id: opponentId,
        stage_id: stageId,
        conditions: state.matchup.conditions,
        session_token: state.sessionToken
      })
    });

    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}`);
    }

    const data = await response.json();
    renderMatchupDashboard(data);
    loadPunishmentOptions();
  } catch (err) {
    console.error('Matchup analysis error:', err);
    if (loadingEl) loadingEl.style.display = 'none';
    if (errorEl) {
      errorEl.style.display = 'block';
      const msg = document.getElementById('matchupErrorMessage');
      if (msg) msg.textContent = `Error loading matchup analysis: ${err.message}`;
    }
  }
}

function renderMatchupDashboard(data) {
  const loadingEl = document.getElementById('matchupLoading');
  const errorEl = document.getElementById('matchupError');
  const dashEl = document.getElementById('matchupDashboardContent');

  if (loadingEl) loadingEl.style.display = 'none';
  if (errorEl) errorEl.style.display = 'none';
  if (dashEl) dashEl.style.display = 'block';

  state.lastMatchupData = data;

  // 1. Face-off Hero Banner (Stage Image Backdrop & Fighter Cards)
  const p1 = data.player_character;
  const p2 = data.opponent_character;
  const st = data.stage;

  document.getElementById('dashP1Img').src = p1.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp';
  document.getElementById('dashP1Name').textContent = p1.name;
  document.getElementById('dashP1Archetype').textContent = p1.archetype || 'Fighter';

  document.getElementById('dashP2Img').src = p2.avatar_url || '/assets/avatars/kazuya-brand-256-BInk9tTm.webp';
  document.getElementById('dashP2Name').textContent = p2.name;
  document.getElementById('dashP2Archetype').textContent = p2.archetype || 'Fighter';

  const stageImgSrc = (st && st.image_url) ? st.image_url : '/assets/img/stages/arena.jpg';
  const dashStageImg = document.getElementById('dashStageImg');
  if (dashStageImg) {
    dashStageImg.src = stageImgSrc;
    dashStageImg.onerror = () => { dashStageImg.src = '/assets/img/stages/arena.jpg'; };
  }
  const faceoffBanner = document.getElementById('faceoffHeroBanner');
  if (faceoffBanner) {
    faceoffBanner.style.backgroundImage = `linear-gradient(180deg, rgba(14, 17, 24, 0.78) 0%, rgba(10, 12, 18, 0.94) 100%), radial-gradient(circle at 50% 50%, rgba(255, 30, 56, 0.12), transparent 70%), url('${stageImgSrc}')`;
    faceoffBanner.style.backgroundSize = 'cover';
    faceoffBanner.style.backgroundPosition = 'center';
  }

  document.getElementById('dashStageName').textContent = st.name;
  document.getElementById('dashStageLocation').textContent = st.location || 'Tekken 8 Arena';

  const hazardsBox = document.getElementById('dashStageHazards');
  if (hazardsBox) {
    hazardsBox.innerHTML = (st.hazards || []).map(h => `<span class="hazard-pill">${h}</span>`).join('');
  }

  // 2. SECTION 1: Overall Matchup Assessment Banner
  const oa = data.overall_assessment;
  const prov = data.directional_provenance;

  const dirTextEl = document.getElementById('provenanceDirectionText');
  if (dirTextEl) dirTextEl.textContent = prov.direction;

  const ratingBadge = document.getElementById('matchupRatingBadge');
  const ratingText = document.getElementById('matchupRatingText');
  if (ratingBadge && ratingText) {
    ratingBadge.className = `rating-badge ${oa.rating.toLowerCase()}`;
    ratingText.textContent = `${oa.rating_label.toUpperCase()} MATCHUP`;
  }

  const confPill = document.getElementById('matchupConfidencePill');
  const confFill = document.getElementById('matchupConfidenceFill');
  if (confPill && confFill) {
    confPill.className = `confidence-pill ${oa.confidence_level.toLowerCase()}`;
    confPill.textContent = `${oa.confidence_level} CONFIDENCE (${oa.confidence_score}%)`;
    confFill.style.width = `${oa.confidence_score}%`;
  }

  const reasoningPara = document.getElementById('matchupReasoningText');
  if (reasoningPara) {
    reasoningPara.textContent = oa.reasoning;
  }

  const evidenceList = document.getElementById('matchupEvidenceList');
  if (evidenceList) {
    evidenceList.innerHTML = (oa.evidence_sources || []).map(e => `
      <span class="evidence-tag-pill">${e}</span>
    `).join('');
  }

  const unknownsList = document.getElementById('matchupUnknownsList');
  if (unknownsList) {
    if (!oa.unknowns || oa.unknowns.length === 0) {
      unknownsList.innerHTML = '<span class="unknown-tag-pill safe">No unresolved laboratory discrepancies</span>';
    } else {
      unknownsList.innerHTML = oa.unknowns.map(u => `
        <span class="unknown-tag-pill">${u}</span>
      `).join('');
    }
  }

  // Phase 8: Tactical Stat Attributes & Side-by-Side Move Specification
  renderMatchupStatBars(p1, p2);
  setupMoveComparison(state.moves, []);

  // Master Compendium Pro Tactics Relativity (Parts 5, 8, 14, 19, 22, 23)
  renderProTacticsRelativityCard(data);

  // 3. SECTION 7: Guaranteed Punish Matrix Table & Defensive Tactics
  renderPunishMatrix();

  // Defensive Tactics (Fuzzy Guard, Interrupts, Low Defense)
  const dt = data.defensive_tactics || {};
  const fuzzyEl = document.getElementById('fuzzyGuardText');
  const interruptEl = document.getElementById('interruptText');
  const lowDefEl = document.getElementById('lowDefenseText');
  if (fuzzyEl) fuzzyEl.textContent = dt.fuzzy_guard_notes || 'Fuzzy guard against strings with high extensions.';
  if (interruptEl) interruptEl.textContent = dt.interrupt_opportunities || 'Use fastest jab check to break stance transitions.';
  if (lowDefEl) lowDefEl.textContent = dt.low_defense_priority || 'Stay standing by default; react to launch-punishable sweeps.';

  // 4. SECTION 4: Useful Moves (vs Rival)
  renderUsefulMovesSection();

  // 5. SECTION 5: Opponent Dangerous Moves Requiring Special Attention
  const dangerList = document.getElementById('dangerousMovesList');
  const threatAlert = document.getElementById('threatAlertPill');
  if (threatAlert) threatAlert.textContent = `${data.dangerous_moves.length} Major Threats`;

  if (dangerList) {
    if (!data.dangerous_moves || data.dangerous_moves.length === 0) {
      dangerList.innerHTML = '<div style="color:var(--text-muted); padding:1rem;">No high-risk opponent moves flagged in current dataset.</div>';
    } else {
      dangerList.innerHTML = data.dangerous_moves.map(dm => {
        const riskCls = (dm.risk_level || 'HIGH').toLowerCase();
        const blk = dm.block_advantage !== null ? `${dm.block_advantage}` : 'N/A';
        const stp = dm.startup_frames ? `i${dm.startup_frames}` : '';

        return `
          <div class="danger-move-card ${riskCls}">
            <div class="dm-header">
              <div class="dm-title-col">
                <span class="dm-name">${dm.move_name}</span>
                <div style="margin-top:0.2rem;">${formatTekkenNotation(dm.input)}</div>
              </div>
              <span class="dm-risk-badge ${riskCls}">${dm.risk_level} (${blk} on block ${stp})</span>
            </div>
            <div class="dm-desc">${dm.threat_description}</div>
            <div class="dm-counter">
              <strong>Recommended Counter:</strong> ${dm.recommended_counter}
            </div>
          </div>
        `;
      }).join('');
    }
  }

  // 6. SECTION 6: Range, Spacing & Movement
  const sm = data.spacing_and_movement;
  const optRange = document.getElementById('optimalRangePill');
  const neutralStrat = document.getElementById('neutralStrategyText');
  const approachAdv = document.getElementById('approachAdviceText');
  const retreatSpc = document.getElementById('retreatSpacingText');

  if (optRange) optRange.textContent = sm.optimal_range;
  if (neutralStrat) neutralStrat.textContent = sm.neutral_strategy;
  if (approachAdv) approachAdv.textContent = sm.approach_advice;
  if (retreatSpc) retreatSpc.textContent = sm.retreat_spacing;

  // 7. SECTION 8: Side-Step & Tracking Evasion
  const st_evasion = data.sidestep_and_tracking;
  const sideBadge = document.getElementById('sidestepBadge');
  const sideReason = document.getElementById('sidestepReasoningText');
  const linearList = document.getElementById('linearMovesList');
  const homingList = document.getElementById('homingMovesList');

  if (sideBadge) {
    sideBadge.textContent = st_evasion.side_label;
    sideBadge.className = `sidestep-badge-pill ${st_evasion.recommended_side.toLowerCase()}`;
  }
  if (sideReason) sideReason.textContent = st_evasion.reasoning;
  if (linearList) {
    linearList.innerHTML = (st_evasion.linear_moves_to_step || []).map(m => `<li>${m}</li>`).join('');
  }
  if (homingList) {
    homingList.innerHTML = (st_evasion.opponent_homing_moves || []).map(m => `<li>${m}</li>`).join('');
  }

  // 8. SECTION 9: Heat Mechanics & Stance Dynamics
  const hm = data.heat_and_mechanics;
  const pHeat = document.getElementById('playerHeatFocus');
  const oHeat = document.getElementById('opponentHeatThreats');
  const hSmash = document.getElementById('heatSmashDynamics');

  if (pHeat) pHeat.textContent = hm.player_heat_focus;
  if (oHeat) oHeat.textContent = hm.opponent_heat_threats;
  if (hSmash) hSmash.textContent = `${hm.heat_smash_interaction} • ${hm.stance_and_install_dynamics}`;

  // 9. SECTION 10: Stage-Aware Strategy Engine & Character-Specific Juggle Compatibility
  loadStageStrategy(st.id, p1.id, p2.id);
  loadComboRecommendations(p1.id, p2.id, st.id);
  const stageAdvantageBox = document.getElementById('characterStageAdvantage');
  const sms = data.stage_matchup_synergy || {};
  if (stageAdvantageBox && sms.character_stage_advantage) {
    stageAdvantageBox.innerHTML = `<strong>Stage Win-Condition:</strong> ${sms.character_stage_advantage}`;
  }

  // 10. SECTIONS 2 & 3: Matchup Factors (Advantages vs Threats)
  const strList = document.getElementById('playerStrengthsList');
  const weakList = document.getElementById('playerWeaknessesList');
  if (strList) {
    strList.innerHTML = (data.player_strengths || []).map(s => `<li>${s}</li>`).join('');
  }
  if (weakList) {
    weakList.innerHTML = (data.opponent_strengths || []).map(w => `<li>${w}</li>`).join('');
  }

  // 11. SECTION 11: Directional Provenance Footer
  const provDir = document.getElementById('provDirectionText');
  const provStatus = document.getElementById('provStatusText');
  const provContrib = document.getElementById('provContributorText');
  const provDate = document.getElementById('provLastReviewedText');
  const provMoves = document.getElementById('provMovesAnalyzed');
  const provPatch = document.getElementById('provPatchVersion');

  if (provDir) provDir.textContent = prov.direction;
  if (provStatus) provStatus.textContent = prov.verification_status;
  if (provContrib) provContrib.textContent = prov.contributor;
  if (provDate) provDate.textContent = `Reviewed: ${prov.last_reviewed || '2026-03-15'}`;
  if (provMoves) {
    const comp = data.data_completeness;
    provMoves.textContent = `${comp.player_moves_analyzed + comp.opponent_moves_analyzed} Moves Evaluated`;
  }
  if (provPatch) provPatch.textContent = `Patch ${prov.patch_version}`;
}

// ==========================================================================
// Phase 2: P1 vs P2 Dual Matchup & Punish Matrix Engine
// ==========================================================================

function filterPunishList(list) {
  if (!Array.isArray(list)) return [];
  const sFilter = state.matchup.matchupStartupFilter || 'ALL';
  const posFilter = state.matchup.matchupStanceFilter || 'ALL';

  return list.filter(p => {
    // Startup filter
    if (sFilter === 'I10_12') {
      if (p.punish_startup > 12) return false;
    } else if (sFilter === 'I13_14') {
      if (p.punish_startup < 13 || p.punish_startup > 14) return false;
    } else if (sFilter === 'LAUNCH') {
      const isLaunch = (p.punish_startup >= 15) || (p.punish_tier && p.punish_tier.toLowerCase().includes('launch'));
      if (!isLaunch) return false;
    }

    // Stance / Position filter
    if (posFilter !== 'ALL') {
      const stance = p.stance_requirement || 'STANDING';
      if (stance !== posFilter) return false;
    }

    return true;
  });
}

function renderPunishRow(p) {
  let tierClass = 'jab';
  if (p.punish_tier && p.punish_tier.includes('Launch')) tierClass = 'launch';
  else if (p.punish_tier && (p.punish_tier.includes('Intermediate') || p.punish_tier.includes('i14'))) tierClass = 'intermediate';

  // Verification badge
  let verifHtml = '';
  const vStat = (p.verification_status || 'GUARANTEED').toUpperCase();
  if (vStat === 'GUARANTEED') {
    verifHtml = '<span class="verif-badge guaranteed">✓ Guaranteed</span>';
  } else if (vStat === 'CONDITIONAL') {
    verifHtml = '<span class="verif-badge conditional">⚡ Conditional</span>';
  } else {
    verifHtml = '<span class="verif-badge unverified">? Unverified</span>';
  }

  // Stance requirement badge
  let stanceHtml = '';
  if (p.stance_requirement === 'WHILE_STANDING') {
    stanceHtml = '<span class="stance-badge ws">🧎 WS / Crouch</span>';
  } else {
    stanceHtml = '<span class="stance-badge standing">🧍 Standing</span>';
  }

  // Hit level indicator
  const hlBadge = p.hit_level ? `<span class="fighter-meta-chip" style="padding:1px 6px; font-size:0.7rem; text-transform:uppercase;">${escapeHtml(p.hit_level)}</span>` : '';

  // Conditions note / Pushback risk
  let condHtml = '';
  if (p.conditions_note) {
    condHtml = `<div class="punish-condition-text">${escapeHtml(p.conditions_note)}</div>`;
  }

  return `
    <tr>
      <td>
        <div style="display:flex; align-items:center; gap:0.4rem;">
          <div style="font-weight:700; color:#fff;">${escapeHtml(p.opponent_move_name)}</div>
          ${hlBadge}
        </div>
        <div style="font-family:monospace; font-size:0.75rem; color:var(--text-muted); margin-top:2px;">${formatTekkenNotation(p.opponent_move_input)}</div>
      </td>
      <td>
        <span class="frame-disadvantage-badge">${p.opponent_block_advantage}</span>
      </td>
      <td>
        <div style="font-weight:700; color:#fff;">${escapeHtml(p.recommended_punish_name)}</div>
        <span class="km-input-badge">${formatTekkenNotation(p.recommended_punish_input)}</span>
      </td>
      <td>
        <span class="punish-startup-badge">i${p.punish_startup}</span>
      </td>
      <td>
        <span style="font-weight:800; color:var(--accent-gold);">${p.damage !== null && p.damage !== undefined ? p.damage : '—'}</span>
        <div style="margin-top:2px;"><span class="punish-tier-badge ${tierClass}">${escapeHtml(p.punish_type || p.punish_tier)}</span></div>
        ${(tierClass === 'launch' || (p.punish_tier && p.punish_tier.toLowerCase().includes('launch')) || p.is_launcher) ? `
          <button type="button" class="btn-punish-combo-link" onclick="openComboFinderForStarter('${escapeHtml(p.recommended_punish_input)}')" title="Open combos for starter ${escapeHtml(p.recommended_punish_input)}">
            🥊 Combos
          </button>
        ` : ''}
      </td>
      <td>
        <div style="display:flex; flex-wrap:wrap; gap:0.35rem; align-items:center;">
          ${verifHtml}
          ${stanceHtml}
        </div>
        ${condHtml}
      </td>
    </tr>
  `;
}

function openComboFinderForStarter(starterInput) {
  playSfx('click');
  const searchInput = document.getElementById('comboLabSearchInput');
  if (searchInput) {
    searchInput.value = starterInput || '';
  }
  if (typeof renderComboLab === 'function') {
    renderComboLab();
  }
  const comboLabEl = document.getElementById('combo-lab');
  if (comboLabEl) {
    comboLabEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  showToast(`Showing combo routes for starter: ${starterInput}`, 'info');
}


function renderDualColumn(title, fighterName, colorClass, items) {
  const badgeColor = colorClass === 'p1' ? 'var(--btn-lp-cyan)' : 'var(--btn-rk-pink)';
  if (!items || items.length === 0) {
    return `
      <div class="dual-column">
        <div class="dual-col-header ${colorClass}">
          <div style="font-weight:700; color:${badgeColor}; font-size:0.9rem;">${title}</div>
          <div style="font-size:0.75rem; color:var(--text-muted);">${escapeHtml(fighterName)} • 0 windows match filters</div>
        </div>
        <div style="color:var(--text-muted); padding:1rem; font-size:0.85rem; text-align:center; border:1px dashed var(--border-subtle); border-radius:6px;">
          No matching punishes in current filter criteria.
        </div>
      </div>
    `;
  }

  const rowsHtml = items.map(p => {
    let tierClass = 'jab';
    if (p.punish_tier && p.punish_tier.includes('Launch')) tierClass = 'launch';
    else if (p.punish_tier && (p.punish_tier.includes('Intermediate') || p.punish_tier.includes('i14'))) tierClass = 'intermediate';

    const vStat = (p.verification_status || 'GUARANTEED').toUpperCase();
    const verifBadge = vStat === 'GUARANTEED' 
      ? '<span class="verif-badge guaranteed">✓ Guaranteed</span>' 
      : '<span class="verif-badge conditional">⚡ Cond.</span>';

    const stanceBadge = p.stance_requirement === 'WHILE_STANDING'
      ? '<span class="stance-badge ws">🧎 WS</span>'
      : '<span class="stance-badge standing">🧍 Stand</span>';

    return `
      <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:6px; padding:0.65rem 0.85rem; margin-bottom:0.6rem;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.35rem;">
          <div>
            <span style="font-weight:700; color:#fff; font-size:0.85rem;">${escapeHtml(p.opponent_move_name)}</span>
            <span style="font-family:monospace; font-size:0.75rem; color:var(--text-muted); margin-left:0.3rem;">${p.opponent_move_input}</span>
          </div>
          <span class="frame-disadvantage-badge" style="font-size:0.75rem;">${p.opponent_block_advantage}</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
          <div style="display:flex; align-items:center; gap:0.4rem;">
            <span class="km-input-badge" style="font-size:0.75rem;">${p.recommended_punish_input}</span>
            <span class="punish-startup-badge" style="font-size:0.7rem;">i${p.punish_startup}</span>
            <span style="font-weight:700; color:var(--accent-gold); font-size:0.8rem;">${p.damage ? p.damage + ' dmg' : ''}</span>
          </div>
          <span class="punish-tier-badge ${tierClass}" style="font-size:0.7rem;">${escapeHtml(p.punish_tier)}</span>
        </div>
        <div style="display:flex; gap:0.4rem; align-items:center; flex-wrap:wrap;">
          ${verifBadge}
          ${stanceBadge}
          ${p.conditions_note ? `<span style="font-size:0.7rem; color:var(--text-muted);">${escapeHtml(p.conditions_note)}</span>` : ''}
        </div>
      </div>
    `;
  }).join('');

  return `
    <div class="dual-column">
      <div class="dual-col-header ${colorClass}">
        <div style="font-weight:700; color:${badgeColor}; font-size:0.9rem;">${title}</div>
        <div style="font-size:0.75rem; color:var(--text-muted);">${escapeHtml(fighterName)} • ${items.length} punish opportunities</div>
      </div>
      <div>${rowsHtml}</div>
    </div>
  `;
}

function renderPunishMatrix() {
  const data = state.lastMatchupData;
  if (!data) return;

  const p1 = data.player_character || {};
  const p2 = data.opponent_character || {};

  const p1Matrix = data.p1_punish_matrix || data.punish_matrix || [];
  const p2Matrix = data.p2_punish_matrix || [];

  // Update counts on perspective buttons
  const p1CountEl = document.getElementById('punishP1Count');
  const p2CountEl = document.getElementById('punishP2Count');
  if (p1CountEl) p1CountEl.textContent = p1Matrix.length;
  if (p2CountEl) p2CountEl.textContent = p2Matrix.length;

  const persp = state.matchup.matchupPerspective || 'P1_VS_P2';
  const tableWrap = document.getElementById('punishSingleTable');
  const dualWrap = document.getElementById('punishDualContainer');
  const tbody = document.getElementById('punishMatrixBody');
  const emptyState = document.getElementById('punishEmptyState');
  const countPill = document.getElementById('punishCountPill');
  const tabPunish = document.getElementById('tabPunishCount');

  if (persp === 'DUAL') {
    if (tableWrap) tableWrap.style.display = 'none';
    if (dualWrap) dualWrap.style.display = 'grid';

    const p1Filtered = filterPunishList(p1Matrix);
    const p2Filtered = filterPunishList(p2Matrix);

    const totalFiltered = p1Filtered.length + p2Filtered.length;
    if (countPill) countPill.textContent = `${totalFiltered} Verified Windows (Dual)`;
    if (tabPunish) tabPunish.textContent = totalFiltered;

    if (totalFiltered === 0) {
      if (emptyState) emptyState.style.display = 'block';
      if (dualWrap) dualWrap.style.display = 'none';
    } else {
      if (emptyState) emptyState.style.display = 'none';
      if (dualWrap) {
        dualWrap.style.display = 'grid';
        dualWrap.innerHTML = `
          ${renderDualColumn(`P1 (${p1.name}) Punishing P2`, p1.name, 'p1', p1Filtered)}
          ${renderDualColumn(`P2 (${p2.name}) Punishing P1`, p2.name, 'p2', p2Filtered)}
        `;
      }
    }
  } else {
    if (dualWrap) dualWrap.style.display = 'none';
    if (tableWrap) tableWrap.style.display = 'table';

    const targetList = (persp === 'P2_VS_P1') ? p2Matrix : p1Matrix;
    const defenderName = (persp === 'P2_VS_P1') ? p2.name : p1.name;
    const attackerName = (persp === 'P2_VS_P1') ? p1.name : p2.name;

    const filtered = filterPunishList(targetList);

    if (countPill) countPill.textContent = `${filtered.length} Verified Windows (${defenderName} vs ${attackerName})`;
    if (tabPunish) tabPunish.textContent = filtered.length;

    if (filtered.length === 0) {
      if (tbody) tbody.innerHTML = '';
      if (emptyState) emptyState.style.display = 'block';
      if (tableWrap) tableWrap.style.display = 'none';
    } else {
      if (emptyState) emptyState.style.display = 'none';
      if (tableWrap) tableWrap.style.display = 'table';
      if (tbody) {
        tbody.innerHTML = filtered.map(p => renderPunishRow(p)).join('');
      }
    }
  }
}

function setPunishPerspective(persp) {
  state.matchup.matchupPerspective = persp;
  const p1Btn = document.getElementById('btnPunishPerspP1');
  const p2Btn = document.getElementById('btnPunishPerspP2');
  const dualBtn = document.getElementById('btnPunishPerspDual');

  if (p1Btn) {
    p1Btn.classList.toggle('active', persp === 'P1_VS_P2');
    p1Btn.classList.toggle('p1-active', persp === 'P1_VS_P2');
  }
  if (p2Btn) {
    p2Btn.classList.toggle('active', persp === 'P2_VS_P1');
    p2Btn.classList.toggle('p2-active', persp === 'P2_VS_P1');
  }
  if (dualBtn) {
    dualBtn.classList.toggle('active', persp === 'DUAL');
  }

  renderPunishMatrix();
}

function setPunishStartupFilter(val) {
  state.matchup.matchupStartupFilter = val;
  const container = document.getElementById('punishStartupPills');
  if (container) {
    container.querySelectorAll('button').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.val === val);
    });
  }
  renderPunishMatrix();
}

function setPunishStanceFilter(val) {
  state.matchup.matchupStanceFilter = val;
  const container = document.getElementById('punishStancePills');
  if (container) {
    container.querySelectorAll('button').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.val === val);
    });
  }
  renderPunishMatrix();
}

function resetPunishFilters() {
  state.matchup.matchupStartupFilter = 'ALL';
  state.matchup.matchupStanceFilter = 'ALL';
  const startGrp = document.getElementById('punishStartupPills');
  if (startGrp) {
    startGrp.querySelectorAll('button').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.val === 'ALL');
    });
  }
  const stanceGrp = document.getElementById('punishStancePills');
  if (stanceGrp) {
    stanceGrp.querySelectorAll('button').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.val === 'ALL');
    });
  }
  renderPunishMatrix();
}

function setUsefulMovesPerspective(pKey) {
  state.matchup.usefulMovesPerspective = pKey;
  const p1Btn = document.getElementById('btnUsefulP1');
  const p2Btn = document.getElementById('btnUsefulP2');
  if (p1Btn) p1Btn.classList.toggle('active', pKey === 'p1');
  if (p2Btn) p2Btn.classList.toggle('active', pKey === 'p2');
  renderUsefulMovesSection();
}

function renderUsefulMovesSection() {
  const data = state.lastMatchupData;
  if (!data) return;

  const usefulGrid = document.getElementById('usefulMovesGrid');
  const usefulPill = document.getElementById('usefulMovesCountPill');
  const p1 = data.player_character || {};
  const p2 = data.opponent_character || {};

  const pKey = state.matchup.usefulMovesPerspective || 'p1';
  const p1Btn = document.getElementById('btnUsefulP1');
  const p2Btn = document.getElementById('btnUsefulP2');

  if (p1Btn) {
    p1Btn.classList.toggle('active', pKey === 'p1');
    p1Btn.textContent = `${p1.name || 'P1'} Moves`;
  }
  if (p2Btn) {
    p2Btn.classList.toggle('active', pKey === 'p2');
    p2Btn.textContent = `${p2.name || 'P2'} Moves`;
  }

  let movesList = [];
  if (pKey === 'p1') {
    movesList = data.useful_moves && data.useful_moves.length > 0 ? data.useful_moves : (data.player_key_moves || []);
  } else {
    movesList = data.opponent_key_moves && data.opponent_key_moves.length > 0 ? data.opponent_key_moves : [];
  }

  const currentFighterName = pKey === 'p1' ? p1.name : p2.name;
  if (usefulPill) {
    usefulPill.textContent = `${movesList.length} Recommended Tools (${currentFighterName})`;
  }

  if (usefulGrid) {
    if (!movesList || movesList.length === 0) {
      usefulGrid.innerHTML = `<div style="color:var(--text-muted); padding:1rem;">No specific moves cataloged for ${escapeHtml(currentFighterName)} yet.</div>`;
    } else {
      usefulGrid.innerHTML = movesList.map(m => {
        const stp = m.startup_frames ? `i${m.startup_frames}` : '—';
        const blk = m.block_advantage !== null && m.block_advantage !== undefined ? (m.block_advantage > 0 ? `+${m.block_advantage}` : `${m.block_advantage}`) : '—';
        const blkCls = m.block_advantage !== null && m.block_advantage !== undefined ? (m.block_advantage >= 0 ? 'frame-plus' : 'frame-minus') : '';
        const dmg = m.damage ? `${m.damage} DMG` : '—';
        const purpose = m.tactical_purpose || m.role || 'Signature tool in neutral';

        return `
          <div class="useful-move-card" onclick="testNotationString('${escapeHtml(m.input)}')" title="Click to test in Notation Engine">
            <div class="um-header">
              <div>
                <span class="um-name">${escapeHtml(m.move_name)}</span>
                <div style="margin-top:0.2rem;">${formatTekkenNotation(m.input)}</div>
              </div>
              <span class="um-role-tag">${escapeHtml(m.role || 'Tactical Poke')}</span>
            </div>
            <div class="um-stats-row">
              <span>Startup: <strong>${stp}</strong></span>
              <span class="${blkCls}">Block: <strong>${blk}</strong></span>
              <span style="color:var(--accent-gold);"><strong>${dmg}</strong></span>
            </div>
            <div class="um-purpose">${escapeHtml(purpose)}</div>
          </div>
        `;
      }).join('');
    }
  }
}

// Global window exposure for inline event handlers
window.setPunishPerspective = setPunishPerspective;
window.setPunishStartupFilter = setPunishStartupFilter;
window.setPunishStanceFilter = setPunishStanceFilter;
window.resetPunishFilters = resetPunishFilters;
window.setUsefulMovesPerspective = setUsefulMovesPerspective;
window.viewFighterMoves = viewFighterMoves;


// ==========================================================================
// Phase 4: Stage-Aware Strategy Engine & Blueprint Visualization
// ==========================================================================

async function loadStageStrategy(stageId, playerId, opponentId) {
  if (!stageId || !playerId) return;

  const wallPos = state.matchup.conditions.wall_position || 'OPEN';
  const heatSt = state.matchup.conditions.heat_state || 'AVAILABLE';

  try {
    const report = await fetchAPI(
      `/stages/${stageId}/strategy?player_character_id=${playerId}&opponent_character_id=${opponentId || ''}&wall_position=${wallPos}&heat_state=${heatSt}`,
      true
    );
    if (!report) return;

    state.stageStrategy.currentReport = report;
    renderStageStrategyUI(report);
    renderComboRecommendations();
  } catch (err) {
    console.warn('Error loading stage strategy:', err);
  }
}

function renderStageStrategyUI(report) {
  const dimPill = document.getElementById('stageDimensionsPill');
  const boundaryDesc = document.getElementById('stageBoundaryDescription');
  const dangerBadge = document.getElementById('wallDangerBadge');
  const blueprintContainer = document.getElementById('stageBlueprintContainer');
  const alertsContainer = document.getElementById('stageUnavailableAlerts');
  const cornerPressureEl = document.getElementById('cornerPressureStrategyText');
  const wallPositioningEl = document.getElementById('wallPositioningAdviceText');
  const hazardList = document.getElementById('stageHazardInteractionsList');

  const stageObj = (report && report.stage) ? report.stage : {};

  // Stage Real Artwork Photo Banner
  const stagePhotoImg = document.getElementById('stageTacticalPhotoImg');
  const isSvgStage = (stageObj.image_url || '').endsWith('.svg');
  if (stagePhotoImg) {
    stagePhotoImg.src = stageObj.image_url || '/assets/img/stages/arena.jpg';
    stagePhotoImg.alt = isSvgStage ? `Tactical Blueprint Vector: ${stageObj.name || 'Selected Arena'}` : `Arena Photograph: ${stageObj.name || 'Selected Arena'}`;
    stagePhotoImg.onerror = () => { stagePhotoImg.src = '/assets/img/stages/arena.jpg'; };
  }
  const stagePhotoName = document.getElementById('stageTacticalPhotoName');
  if (stagePhotoName) {
    stagePhotoName.textContent = (stageObj.name || 'Selected Arena').toUpperCase();
  }
  const stagePhotoLoc = document.getElementById('stageTacticalPhotoLoc');
  if (stagePhotoLoc) {
    stagePhotoLoc.textContent = stageObj.location || 'Official Arena';
  }
  const stagePhotoHazards = document.getElementById('stageTacticalPhotoHazards');
  if (stagePhotoHazards) {
    const badges = [];
    if (isSvgStage) badges.push('<span class="stage-overlay-badge badge-blueprint" style="background:rgba(14,165,233,0.9); color:#fff; border:1px solid #38bdf8; font-weight:800;">TACTICAL BLUEPRINT</span>');
    if (stageObj.wall_break) badges.push('<span class="stage-overlay-badge badge-wallbreak">WALL BREAK</span>');
    if (stageObj.floor_break) badges.push('<span class="stage-overlay-badge badge-floorbreak">FLOOR BREAK</span>');
    if (stageObj.balcony_break) badges.push('<span class="stage-overlay-badge badge-balcony">BALCONY BREAK</span>');
    if (!stageObj.has_walls) badges.push('<span class="stage-overlay-badge badge-infinite">INFINITE</span>');
    stagePhotoHazards.innerHTML = badges.join('');
  }

  // Danger Badge
  if (dangerBadge) {
    if (!stageObj.has_walls) {
      dangerBadge.textContent = 'SAFE (INFINITE)';
      dangerBadge.className = 'danger-level-badge safe';
    } else if (stageObj.wall_blast || (stageObj.wall_break && stageObj.balcony_break)) {
      dangerBadge.textContent = 'HIGH HAZARD STAGE';
      dangerBadge.className = 'danger-level-badge extreme';
    } else {
      dangerBadge.textContent = 'STANDARD WALLED';
      dangerBadge.className = 'danger-level-badge moderate';
    }
  }

  // Tactical Blueprint / Geometry Map
  if (blueprintContainer) {
    if (report.geometry_available && report.geometry_data) {
      const geo = report.geometry_data;
      let svgMarkup = `
        <div class="stage-blueprint-svg-wrap">
          <svg viewBox="${geo.canvas_viewbox || '0 0 400 400'}" width="100%" height="100%" style="overflow:visible;">
            <defs>
              <pattern id="gridPattern" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#gridPattern)" rx="6" />
      `;

      (geo.elements || []).forEach(elem => {
        if (elem.points) {
          svgMarkup += `
            <polygon points="${elem.points}" fill="rgba(255,30,56,0.08)" stroke="${elem.color || 'var(--accent-red)'}" stroke-width="3" class="stage-svg-element">
              <title>${elem.label} - ${elem.notes || ''}</title>
            </polygon>
          `;
        } else if (elem.radius) {
          const isSpawn = elem.element_type === 'spawn';
          svgMarkup += `
            <circle cx="${elem.x}" cy="${elem.y}" r="${elem.radius}" fill="${isSpawn ? 'rgba(56,189,248,0.1)' : 'rgba(249,115,22,0.15)'}" stroke="${elem.color || '#38bdf8'}" stroke-width="2" stroke-dasharray="${isSpawn ? '5,5' : 'none'}" class="stage-svg-element">
              <title>${elem.label} - ${elem.notes || ''}</title>
            </circle>
          `;
        } else if (elem.width && elem.height) {
          const rx = elem.x - elem.width / 2;
          const ry = elem.y - elem.height / 2;
          svgMarkup += `
            <rect x="${rx}" y="${ry}" width="${elem.width}" height="${elem.height}" rx="3" fill="${elem.color || '#475569'}" stroke="rgba(255,255,255,0.25)" stroke-width="1" class="stage-svg-element">
              <title>${elem.label} - ${elem.notes || ''}</title>
            </rect>
          `;
        }
      });

      svgMarkup += `
            <text x="200" y="204" text-anchor="middle" fill="#94a3b8" font-size="9" font-family="'Segoe UI', sans-serif" font-weight="700" letter-spacing="1">ENGAGEMENT AXIS</text>
          </svg>
        </div>
        <div class="stage-blueprint-legend">
          <div class="stage-legend-item"><span class="stage-legend-dot" style="background:var(--accent-red);"></span> Boundary Perimeter</div>
          <div class="stage-legend-item"><span class="stage-legend-dot" style="background:#38bdf8;"></span> Center Standoff (${geo.width_meters}m)</div>
          ${stageObj.wall_break ? '<div class="stage-legend-item"><span class="stage-legend-dot" style="background:#ef4444;"></span> Wall Break</div>' : ''}
          ${stageObj.floor_break ? '<div class="stage-legend-item"><span class="stage-legend-dot" style="background:#f97316;"></span> Floor Break</div>' : ''}
          ${stageObj.balcony_break ? '<div class="stage-legend-item"><span class="stage-legend-dot" style="background:#f59e0b;"></span> Balcony Rail</div>' : ''}
        </div>
      `;
      blueprintContainer.innerHTML = svgMarkup;
    } else {
      // Unmapped / Infinite Stage panel (Zero Fabricated Geometry)
      const stageName = stageObj.name || 'Selected Stage';
      blueprintContainer.innerHTML = `
        <div class="stage-unmapped-panel">
          <div class="stage-unmapped-header">
            <svg viewBox="0 0 24 24" width="16" height="16" stroke="#f59e0b" stroke-width="2.5" fill="none"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <span>${stageName} • UNBOUNDED / INFINITE BATTLEGROUND</span>
          </div>
          <p class="stage-unmapped-text">
            ⚠️ <strong>Zero Fabricated Geometry Rule:</strong> ${stageName} features unbounded open terrain with no perimeter wall bounds. Movement is unrestricted; no artificial polygonal boundary mesh is displayed.
          </p>
          <div class="stage-unmapped-metrics-grid">
            <div class="stage-unmapped-metric-cell">
              <div class="label">Boundary Shape</div>
              <div class="value">${stageObj.boundary_shape || 'Infinite'}</div>
            </div>
            <div class="stage-unmapped-metric-cell">
              <div class="label">Wall Distance</div>
              <div class="value">${report.wall_distance || 'Standard'}</div>
            </div>
            <div class="stage-unmapped-metric-cell">
              <div class="label">Wall Splat Status</div>
              <div class="value" style="color:#ef4444;">${report.wall_availability_status || 'Unavailable'}</div>
            </div>
            <div class="stage-unmapped-metric-cell">
              <div class="label">Environmental Break</div>
              <div class="value" style="color:#38bdf8;">None (Solid Floor)</div>
            </div>
          </div>
        </div>
      `;
    }
  }

  // Unavailable Mechanics Alert Banner
  if (alertsContainer) {
    if (report.unavailable_mechanics_warning && report.unavailable_mechanics_warning.length > 0) {
      alertsContainer.innerHTML = report.unavailable_mechanics_warning.map(w => `
        <div class="stage-unavailable-item">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="#ef4444" stroke-width="2.5" fill="none"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <div>${w}</div>
        </div>
      `).join('');
    } else {
      alertsContainer.innerHTML = '';
    }
  }

  // Corner Pressure & Spacing Advice
  if (cornerPressureEl) cornerPressureEl.textContent = report.corner_pressure_strategy;
  if (wallPositioningEl) wallPositioningEl.textContent = report.wall_positioning_notes;

  // Hazard Interactions List
  if (hazardList) {
    const items = [];
    if (report.wall_break_interaction) {
      items.push(`
        <div class="st-hazard-interaction-row">
          <span class="st-hazard-tag wall-break">Wall Break</span>
          <div>${report.wall_break_interaction}</div>
        </div>
      `);
    }
    if (report.balcony_break_interaction) {
      items.push(`
        <div class="st-hazard-interaction-row">
          <span class="st-hazard-tag balcony-break">Balcony Break</span>
          <div>${report.balcony_break_interaction}</div>
        </div>
      `);
    }
    if (report.floor_break_interaction) {
      items.push(`
        <div class="st-hazard-interaction-row">
          <span class="st-hazard-tag floor-break">Floor Break</span>
          <div>${report.floor_break_interaction}</div>
        </div>
      `);
    }
    if (items.length === 0) {
      items.push(`
        <div class="st-hazard-interaction-row">
          <span class="st-hazard-tag" style="background:rgba(255,255,255,0.06); color:var(--text-muted);">No Breaks</span>
          <div>This arena has solid, unbreakable foundations and boundaries. Standard wall splats only.</div>
        </div>
      `);
    }
    hazardList.innerHTML = items.join('');
  }
}

// ==========================================================================
// Phase 5: Character-Specific Juggle Compatibility & Damage Scaling Engine
// ==========================================================================

async function loadComboRecommendations(playerId, opponentId, stageId) {
  if (!playerId) return;

  const wallPos = state.matchup.conditions.wall_position || 'OPEN';
  const heatSt = state.matchup.conditions.heat_state || 'AVAILABLE';

  const container = document.getElementById('suitableCombosContainer');
  if (container) {
    container.innerHTML = `
      <div class="skeleton-card" style="margin-bottom:0.75rem;">
        <div class="skeleton-text heading skeleton-shimmer"></div>
        <div class="skeleton-text sub skeleton-shimmer"></div>
        <div class="skeleton-text skeleton-shimmer" style="width:75%; margin-top:0.4rem;"></div>
      </div>
      <div class="skeleton-card">
        <div class="skeleton-text heading skeleton-shimmer"></div>
        <div class="skeleton-text sub skeleton-shimmer"></div>
        <div class="skeleton-text skeleton-shimmer" style="width:60%; margin-top:0.4rem;"></div>
      </div>
    `;
  }

  try {
    let url = `/combos/recommendations?player_id=${playerId}&wall_position=${wallPos}&heat_state=${heatSt}`;
    if (opponentId) url += `&opponent_id=${opponentId}`;
    if (stageId) url += `&stage_id=${stageId}`;

    const report = await fetchAPI(url, true);
    if (!report) return;

    state.combosPhase5.recommendations = report;
    renderOpponentHurtboxBanner(report.opponent_hurtbox);
    renderComboRecommendations();
  } catch (err) {
    console.warn('Error loading combo recommendations:', err);
  }
}

function resetComboFilters() {
  state.combosPhase5.searchQuery = '';
  state.combosPhase5.requiresHeat = false;
  state.combosPhase5.requiresCH = false;
  state.combosPhase5.activeDifficulty = 'ALL';
  state.combosPhase5.activeHurtbox = 'ALL';
  state.combosPhase5.activeCategory = 'ALL';
  const sInput = document.getElementById('comboSearchInput');
  if (sInput) sInput.value = '';
  const heatToggle = document.getElementById('comboHeatToggle');
  if (heatToggle) heatToggle.checked = false;
  const chToggle = document.getElementById('comboCHToggle');
  if (chToggle) chToggle.checked = false;
  const diffSelect = document.getElementById('comboDifficultyFilter');
  if (diffSelect) diffSelect.value = 'ALL';
  const hurtSelect = document.getElementById('comboHurtboxFilter');
  if (hurtSelect) hurtSelect.value = 'ALL';
  document.querySelectorAll('.cl-cat-tab').forEach(t => t.classList.toggle('active', t.dataset.cat === 'ALL'));
  if (typeof renderComboRecommendations === 'function') {
    renderComboRecommendations();
  }

  // Phase 3 Combo Lab Reset
  if (state.comboFinder) {
    state.comboFinder.category = 'ALL';
  }
  const labStarter = document.getElementById('comboLabStarterTypeFilter');
  if (labStarter) labStarter.value = 'ALL';
  const labDiff = document.getElementById('comboLabDifficultyFilter');
  if (labDiff) labDiff.value = 'ALL';
  const labWall = document.getElementById('comboLabWallFilter');
  if (labWall) labWall.value = 'ALL';
  const labStance = document.getElementById('comboLabStanceFilter');
  if (labStance) labStance.value = 'ALL';
  const minDmg = document.getElementById('comboLabMinDamage');
  if (minDmg) minDmg.value = '';
  const maxDmg = document.getElementById('comboLabMaxDamage');
  if (maxDmg) maxDmg.value = '';
  const labSearch = document.getElementById('comboLabSearchInput');
  if (labSearch) labSearch.value = '';
  document.querySelectorAll('#comboLabCategoryPills .combo-cat-pill').forEach(b => b.classList.toggle('active', b.dataset.cat === 'ALL'));

  if (typeof renderComboLab === 'function') {
    renderComboLab();
  }
  showToast('Combo filters reset to show all routes', 'info');
}

function renderOpponentHurtboxBanner(hurtbox) {
  if (!hurtbox) return;

  const badgeEl = document.getElementById('oppHurtboxClassBadge');
  const targetNameEl = document.getElementById('oppHurtboxTargetName');
  const descEl = document.getElementById('oppHurtboxDesc');
  const quirksListEl = document.getElementById('oppHurtboxQuirksList');

  const hClass = (hurtbox.hurtbox_class || 'MALE_STANDARD').toLowerCase();

  if (badgeEl) {
    badgeEl.textContent = `${hurtbox.hurtbox_class} PROFILE`;
    badgeEl.className = `hurtbox-badge-tag ${hClass}`;
  }

  if (targetNameEl) {
    targetNameEl.textContent = `Target: ${hurtbox.character_name}`;
  }

  if (descEl) {
    descEl.textContent = hurtbox.description || 'Standard hurtbox baseline.';
  }

  if (quirksListEl) {
    const quirks = hurtbox.known_quirks || [];
    quirksListEl.innerHTML = quirks.map(q => `
      <span class="hurtbox-quirk-pill">⚡ ${q}</span>
    `).join('');
  }
}

function renderComboRecommendations() {
  const report = state.combosPhase5.recommendations;
  const container = document.getElementById('suitableCombosContainer');
  const countPill = document.getElementById('comboCountPill');
  if (!container || !report) return;

  const activeCat = state.combosPhase5.activeCategory;
  const f = state.combosPhase5;

  let pool = [];
  if (activeCat === 'ALL') {
    // Gather all 10 categories
    const categories = [
      'beginner_friendly', 'standard_launch', 'high_damage_optimal',
      'wall_carry', 'wall_combo', 'heat_dependent', 'counter_hit',
      'character_specific', 'stage_break', 'alternative_routes'
    ];
    const seen = new Set();
    categories.forEach(cat => {
      (report[cat] || []).forEach(c => {
        if (!seen.has(c.id)) {
          seen.add(c.id);
          pool.push(c);
        }
      });
    });
  } else {
    pool = report[activeCat] || [];
  }

  // Filter pool
  const filtered = pool.filter(c => {
    // Search query
    if (f.searchQuery) {
      const q = f.searchQuery;
      const titleMatch = (c.title || '').toLowerCase().includes(q);
      const notMatch = (c.notation_sequence || '').toLowerCase().includes(q);
      const starterMatch = (c.starter_move_name || '').toLowerCase().includes(q) || (c.starter_move_input || '').toLowerCase().includes(q);
      if (!titleMatch && !notMatch && !starterMatch) return false;
    }

    // Heat
    if (f.requiresHeat && !c.uses_heat) return false;

    // Counter Hit
    if (f.requiresCH && !c.requires_counter_hit && c.launcher_type !== 'COUNTER_HIT') return false;

    // Difficulty
    if (f.activeDifficulty !== 'ALL' && (c.difficulty || '').toUpperCase() !== f.activeDifficulty.toUpperCase()) {
      return false;
    }

    // Target Hurtbox
    if (f.activeHurtbox !== 'ALL' && (c.target_hurtbox_class || '').toUpperCase() !== f.activeHurtbox.toUpperCase()) {
      return false;
    }

    return true;
  });

  if (countPill) countPill.textContent = `${filtered.length} Recommended Combos`;
  const tabCombo = document.getElementById('tabComboCount');
  if (tabCombo) tabCombo.textContent = filtered.length;

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="empty-state-card">
        <div class="empty-icon">🥊</div>
        <h4 class="empty-title">No Combo Routes Found</h4>
        <p class="empty-desc">No juggle routes match your active difficulty, counter-hit, or hurtbox filters for this character matchup.</p>
        <button type="button" class="btn btn-secondary empty-action" onclick="resetComboFilters()">Clear Combo Filters</button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(c => {
    const ctype = (c.combo_type || 'MIDSCREEN').toUpperCase();
    let typeClass = 'type-midscreen';
    if (ctype === 'WALL_CARRY') typeClass = 'type-wall-carry';
    else if (ctype === 'WALL_COMBO') typeClass = 'type-wall-combo';
    else if (ctype === 'WALL_BREAK') typeClass = 'type-wall-break';
    else if (ctype === 'FLOOR_BREAK') typeClass = 'type-floor-break';
    else if (ctype === 'BALCONY_BREAK') typeClass = 'type-balcony-break';

    // 5-Tier dynamic compatibility badge
    let compatBadgeHtml = '';
    const status = c.compatibility_status || 'UNKNOWN_COMPATIBILITY';
    if (status === 'VERIFIED_FOR_OPPONENT') {
      compatBadgeHtml = `<span class="compat-pill verified" title="Tested directly against this opponent hurtbox profile in Practice Lab">✓ Verified For Opponent</span>`;
    } else if (status === 'TESTED_UNDER_CONDITIONS') {
      const cond = c.timing_adjustment || 'Conditions Apply';
      compatBadgeHtml = `<span class="compat-pill tested" title="${cond}">⚡ Tested: ${cond}</span>`;
    } else if (status === 'REPORTED_UNTESTED') {
      compatBadgeHtml = `<span class="compat-pill reported" title="Reported by tournament players; pending lab re-verification">📋 Reported Community Route</span>`;
    } else if (status === 'INCOMPATIBLE_DOCUMENTED') {
      compatBadgeHtml = `<span class="compat-pill incompatible" title="${c.incompatibility_reason || 'Drops on this hurtbox'}">⚠️ Incompatible Documented</span>`;
    } else {
      compatBadgeHtml = `<span class="compat-pill unknown" title="Untested on this specific character profile - lab verification recommended">❓ Unknown (Default)</span>`;
    }

    // Damage type tag
    const isEst = c.is_damage_estimate || c.damage_type === 'ESTIMATED';
    const dmgTypeClass = isEst ? 'estimated' : 'tested';
    const dmgTypeLabel = isEst ? 'SCALED ESTIMATE' : 'TESTED IN LAB';

    const stageTag = c.is_stage_dependent
      ? `<span class="combo-tag stage-dep">Stage Specific: ${c.stage_section || (report.stage ? report.stage.name : 'Hazard')}</span>`
      : `<span class="combo-tag universal">Universal Stage</span>`;

    const heatTag = c.uses_heat
      ? `<span class="combo-tag" style="background:rgba(255,0,127,0.15); border:1px solid rgba(255,0,127,0.3); color:#ff007f;">Heat Required</span>`
      : '';

    const chTag = (c.requires_counter_hit || c.launcher_type === 'COUNTER_HIT')
      ? `<span class="combo-tag" style="background:rgba(255,215,0,0.15); border:1px solid rgba(255,215,0,0.3); color:var(--accent-gold);">Counter Hit (120%)</span>`
      : '';

    const stanceTag = (c.required_stance && c.required_stance !== 'NONE')
      ? `<span class="combo-tag" style="background:rgba(168,85,247,0.15); border:1px solid rgba(168,85,247,0.3); color:#c084fc;">Stance: ${c.required_stance}</span>`
      : '';

    const targetHurtboxTag = (c.target_hurtbox_class && c.target_hurtbox_class !== 'UNIVERSAL')
      ? `<span class="combo-tag" style="background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.3); color:#fbbf24;">Target: ${c.target_hurtbox_class} Only</span>`
      : '';

    const wallPositionTag = c.uses_wall
      ? `<span class="combo-tag" style="background:rgba(56,189,248,0.15); border:1px solid rgba(56,189,248,0.3); color:#38bdf8;">Wall: ${c.stage_section || (c.combo_type === 'WALL_COMBO' ? 'Wall Splat' : 'Wall Carry')}</span>`
      : `<span class="combo-tag" style="background:rgba(148,163,184,0.1); border:1px solid rgba(148,163,184,0.2); color:#94a3b8;">Position: Open Ground</span>`;

    const starterEnder = (c.starter_move_name || c.ender_move_name)
      ? `
        <div class="combo-starter-ender-row">
          ${c.starter_move_name ? `<span>Starter: <strong>${c.starter_move_name}</strong> (${formatTekkenNotation(c.starter_move_input)})</span>` : ''}
          ${c.ender_move_name ? `<span>• Ender: <strong>${c.ender_move_name}</strong> (${formatTekkenNotation(c.ender_move_input)})</span>` : ''}
          ${c.launcher_type ? `<span>• Launcher: <strong style="color:var(--accent-gold);">${c.launcher_type}</strong></span>` : ''}
        </div>
      `
      : '';

    const notes = c.conditions_notes
      ? `<div class="combo-synergy-note">🎯 ${c.conditions_notes}</div>`
      : '';

    const execNotes = c.execution_notes
      ? `<div class="combo-synergy-note" style="border-color:#38bdf8;">⚙️ <strong>Execution Tip:</strong> ${c.execution_notes}</div>`
      : '';

    const dropAlert = (status === 'INCOMPATIBLE_DOCUMENTED' && c.incompatibility_reason)
      ? `
        <div class="combo-incompat-warning">
          <span>⚠️ <strong>Drop Condition:</strong> ${c.incompatibility_reason}</span>
        </div>
      `
      : '';

    const easierAltHtml = (c.easier_alternative_id && c.easier_alternative_title)
      ? `
        <div class="combo-easier-callout">
          <div class="combo-easier-info">
            🔀 <strong>Easier Alternative Available:</strong> ${c.easier_alternative_title}
            <div style="font-size:0.68rem; color:#cbd5e1; margin-top:0.15rem;">${c.easier_alternative_notes || 'Consistent tournament execution route'}</div>
          </div>
          <button type="button" class="btn-swap-combo-alt" onclick="selectComboById(${c.easier_alternative_id})">
            Switch to Alternative &rarr;
          </button>
        </div>
      `
      : '';

    return `
      <div class="combo-card" id="combo_card_${c.id}">
        <div class="combo-card-header">
          <div class="combo-card-title-group">
            <span class="combo-title">${c.title}</span>
            <div class="combo-tags-group">
              ${compatBadgeHtml}
              <span class="combo-tag ${typeClass}">${c.combo_type}</span>
              ${stageTag}
              ${heatTag}
              ${chTag}
              ${stanceTag}
              ${targetHurtboxTag}
              ${wallPositionTag}
            </div>
          </div>
          <div class="combo-metrics-group">
            <span class="combo-dmg-badge">${c.total_damage} DMG (${c.hit_count} Hits)</span>
            <span class="damage-type-pill ${dmgTypeClass}">${dmgTypeLabel}</span>
            <span class="feat-badge badge-approved" style="font-size:0.65rem;">${c.difficulty}</span>
          </div>
        </div>

        <div class="combo-notation-box" title="Click to test in notation engine" onclick="testNotationString('${(c.notation_sequence || '').replace(/'/g, "\\'")}')">
          ${formatTekkenNotation(c.notation_sequence)}
        </div>

        ${starterEnder}
        ${notes}
        ${execNotes}
        ${dropAlert}
        ${easierAltHtml}

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.4rem; flex-wrap:wrap; gap:0.4rem;">
          <button type="button" class="btn-scaling-breakdown" onclick="openDamageScalingModal(${c.id})">
            📊 View Scaling Breakdown (${c.hit_count} hits) &rarr;
          </button>
          <button type="button" class="btn-reset-record" style="font-size:0.7rem; padding:0.25rem 0.6rem;" onclick="testNotationString('${(c.notation_sequence || '').replace(/'/g, "\\'")}')">
            ⚡ Test in Notation Engine &rarr;
          </button>
        </div>

        <div class="combo-provenance-meta" style="font-size:0.68rem; color:#94a3b8; display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(255,255,255,0.06); padding-top:0.35rem; margin-top:0.45rem;">
          <span>🛡️ <strong style="color:#38bdf8;">${c.verification_status}</strong> • Patch: <strong style="color:#e2e8f0;">${c.patch_version}</strong></span>
          <span>Source: <em>${c.source}</em></span>
        </div>
      </div>
    `;
  }).join('');
}

function selectComboById(comboId) {
  const card = document.getElementById(`combo_card_${comboId}`);
  if (card) {
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    card.style.outline = '2px solid var(--accent-gold)';
    card.style.boxShadow = '0 0 15px rgba(255, 215, 0, 0.4)';
    setTimeout(() => {
      card.style.outline = '';
      card.style.boxShadow = '';
    }, 2500);
  } else {
    state.combosPhase5.activeCategory = 'ALL';
    document.querySelectorAll('#comboTypePills .combo-filter-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.cat === 'ALL');
    });
    renderComboRecommendations();
    setTimeout(() => {
      const c = document.getElementById(`combo_card_${comboId}`);
      if (c) {
        c.scrollIntoView({ behavior: 'smooth', block: 'center' });
        c.style.outline = '2px solid var(--accent-gold)';
        setTimeout(() => { c.style.outline = ''; }, 2500);
      }
    }, 100);
  }
}

// ==========================================================================
// Phase 5: Damage Scaling Modal & Interactive Sandbox
// ==========================================================================

function openDamageScalingModal(comboId) {
  let combo = null;
  let report = state.combosPhase5?.recommendations || state.comboFinder?.p1Report || state.comboFinder?.p2Report;

  // Search in state.comboFinder p1Combos and p2Combos first
  if (state.comboFinder) {
    combo = (state.comboFinder.p1Combos || []).find(c => String(c.id) === String(comboId)) ||
            (state.comboFinder.p2Combos || []).find(c => String(c.id) === String(comboId));
  }

  // If not found yet, search in recommendations categories
  if (!combo) {
    const searchReports = [state.combosPhase5?.recommendations, state.comboFinder?.p1Report, state.comboFinder?.p2Report].filter(Boolean);
    const categories = [
      'beginner_friendly', 'standard_launch', 'high_damage_optimal',
      'wall_carry', 'wall_combo', 'heat_dependent', 'counter_hit',
      'character_specific', 'stage_break', 'alternative_routes'
    ];
    for (const r of searchReports) {
      for (const cat of categories) {
        const found = (r[cat] || []).find(c => String(c.id) === String(comboId));
        if (found) {
          combo = found;
          report = r;
          break;
        }
      }
      if (combo) break;
    }
  }

  if (!combo) return;
  state.combosPhase5.currentModalCombo = combo;

  const modal = document.getElementById('damageScalingModal');
  const titleEl = document.getElementById('scalingModalComboTitle');
  const explEl = document.getElementById('scalingModalExplanation');
  const rawSumEl = document.getElementById('scalingRawSumVal');
  const scaledValEl = document.getElementById('scalingScaledVal');
  const testedValEl = document.getElementById('scalingTestedVal');
  const dmgTypeBadge = document.getElementById('scalingDamageTypeBadge');
  const overestEl = document.getElementById('scalingOverestimationVal');
  const tbody = document.getElementById('scalingTableBody');

  const dmgVal = combo.total_damage || combo.damage || 65;
  if (titleEl) titleEl.textContent = `${combo.title || 'Verified Juggle'} (${dmgVal} DMG)`;
  if (explEl) explEl.textContent = (report && report.damage_scaling_rules_explanation) ? report.damage_scaling_rules_explanation : 'Tekken 8 Damage Decay Formula: Hit 1 at 100% (120% on Counter-Hit), Hit 2 at 70%, Hit 3 at 50%, Hit 4 at 40%, Hit 5+ at 30% floor.';

  let hits = combo.scaling_breakdown || [];
  if (hits.length === 0 && combo.notation_sequence) {
    const steps = (combo.notation_sequence || '').split(/\s*(?:>|->|=>)\s*/).filter(Boolean);
    const scalePercents = [100, 70, 50, 40, 30];
    hits = steps.map((st, i) => {
      const pct = i >= scalePercents.length ? 30 : scalePercents[i];
      const raw = Math.round(dmgVal / Math.max(1, steps.length) * (100 / pct));
      const sc = Math.round(raw * (pct / 100));
      return {
        hit_number: i + 1,
        move_notation: st.trim(),
        raw_damage: raw,
        scaling_percent: pct,
        scaled_damage: sc,
        notes: i === 0 ? 'Launcher confirm' : (pct === 30 ? 'Scaling floor reached' : 'Aerial decay')
      };
    });
  }

  const rawSum = combo.raw_damage_sum || hits.reduce((acc, h) => acc + (h.raw_damage || 0), 0);
  const scaledTotal = hits.reduce((acc, h) => acc + (h.scaled_damage || 0), 0) || dmgVal;
  const avoidedOverest = Math.max(0, rawSum - scaledTotal);

  if (rawSumEl) rawSumEl.textContent = `${rawSum} DMG`;
  if (scaledValEl) scaledValEl.textContent = `${scaledTotal} DMG`;
  if (testedValEl) testedValEl.textContent = `${dmgVal} DMG`;
  if (dmgTypeBadge) dmgTypeBadge.textContent = combo.damage_type === 'TESTED' ? 'TESTED IN PRACTICE LAB' : 'VERIFIED SCALED';
  if (overestEl) overestEl.textContent = `+${avoidedOverest} DMG`;

  if (tbody) {
    if (hits.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:var(--text-muted); padding:1rem;">Hit-by-hit scaling details calculated dynamically from Tekken 8 decay curve.</td></tr>`;
    } else {
      tbody.innerHTML = hits.map(h => `
        <tr>
          <td><strong>Hit ${h.hit_number}</strong></td>
          <td style="font-family:'Consolas',monospace; color:#38bdf8;">${h.move_notation || '—'}</td>
          <td>${h.raw_damage} dmg</td>
          <td><span style="font-weight:700; color:${h.scaling_percent === 100 || h.scaling_percent === 120 ? '#00e676' : (h.scaling_percent === 30 ? '#ef4444' : 'var(--accent-gold)')};">${h.scaling_percent}%</span></td>
          <td style="font-weight:800; color:#fff;">${h.scaled_damage} dmg</td>
          <td style="color:var(--text-dim);">${h.notes || (h.hit_number === 1 ? 'Launcher confirm' : (h.scaling_percent === 30 ? 'Scaling floor reached' : 'Aerial decay'))}</td>
        </tr>
      `).join('');
    }
  }

  // Populate sandbox with combo hits
  if (hits.length > 0) {
    state.combosPhase5.sandboxHits = hits.map((h, i) => ({
      raw: h.raw_damage,
      notation: h.move_notation || `Hit ${i + 1}`
    }));
  }
  renderSandboxHits();
  recalculateSandbox();

  if (modal) modal.style.display = 'flex';
}

function closeDamageScalingModal() {
  const modal = document.getElementById('damageScalingModal');
  if (modal) modal.style.display = 'none';
}

function openDamageCalculatorSandbox() {
  const modal = document.getElementById('damageScalingModal');
  const titleEl = document.getElementById('scalingModalComboTitle');
  if (titleEl) titleEl.textContent = 'INTERACTIVE DAMAGE SCALING SANDBOX';
  renderSandboxHits();
  recalculateSandbox();
  if (modal) modal.style.display = 'flex';
}

function renderSandboxHits() {
  const container = document.getElementById('sandboxHitsContainer');
  if (!container) return;

  const hits = state.combosPhase5.sandboxHits;
  container.innerHTML = hits.map((h, i) => `
    <div class="sandbox-hit-chip">
      <span>Hit ${i + 1}:</span>
      <input type="number" class="sandbox-hit-input" value="${h.raw}" min="1" max="120"
             onchange="updateSandboxHit(${i}, this.value)" oninput="updateSandboxHit(${i}, this.value)">
      <span style="cursor:pointer; color:#ef4444; font-weight:bold; margin-left:2px;" onclick="removeSandboxHit(${i})" title="Remove Hit">&times;</span>
    </div>
  `).join('');
}

function updateSandboxHit(index, value) {
  const val = parseInt(value) || 0;
  if (state.combosPhase5.sandboxHits[index]) {
    state.combosPhase5.sandboxHits[index].raw = val;
    recalculateSandbox();
  }
}

function addSandboxHit() {
  const cnt = state.combosPhase5.sandboxHits.length + 1;
  state.combosPhase5.sandboxHits.push({ raw: 15, notation: `Hit ${cnt}` });
  renderSandboxHits();
  recalculateSandbox();
}

function removeSandboxHit(index) {
  if (state.combosPhase5.sandboxHits.length <= 1) return;
  state.combosPhase5.sandboxHits.splice(index, 1);
  renderSandboxHits();
  recalculateSandbox();
}

function resetSandboxHits() {
  state.combosPhase5.sandboxHits = [
    { raw: 25, notation: 'Hit 1 (Starter)' },
    { raw: 18, notation: 'Hit 2' },
    { raw: 22, notation: 'Hit 3 (Tornado)' },
    { raw: 15, notation: 'Hit 4' },
    { raw: 20, notation: 'Hit 5 (Ender)' },
  ];
  const chBox = document.getElementById('sandboxCheckCH');
  if (chBox) chBox.checked = false;
  renderSandboxHits();
  recalculateSandbox();
}

function recalculateSandbox() {
  const hits = state.combosPhase5.sandboxHits;
  const isCH = document.getElementById('sandboxCheckCH') ? document.getElementById('sandboxCheckCH').checked : false;

  let rawSum = 0;
  let scaledTotal = 0;

  hits.forEach((h, idx) => {
    const raw = h.raw || 0;
    rawSum += raw;
    let pct = 30;
    if (idx === 0) pct = isCH ? 120 : 100;
    else if (idx === 1) pct = 70;
    else if (idx === 2) pct = 50;
    else if (idx === 3) pct = 40;
    else pct = 30;

    scaledTotal += Math.floor(raw * pct / 100.0);
  });

  const resEl = document.getElementById('sandboxLiveResult');
  if (resEl) {
    const avoided = Math.max(0, rawSum - scaledTotal);
    resEl.innerHTML = `Scaled: <strong>${scaledTotal} DMG</strong> | Raw Sum: <span style="text-decoration:line-through; color:#f87171;">${rawSum} DMG</span> (Avoided Overstatement: +${avoided} DMG)`;
  }
}


// ==========================================================================
// 8. Phase 3: Smart Punishment Assistant & Interactive Practice Lab
// ==========================================================================

state.punishment = {
  options: [],
  filters: {
    query: '',
    blockFilter: 'ALL',
    hitLevel: 'ALL',
    stance: 'ALL',
    minDamage: 0
  },
  currentPracticeMove: null,
  drillTimer: null,
  drillStartTime: 0,
  drillWaitingForInput: false
};

function initPunishAssistant() {
  setupPunishControls();
}

function setupPunishControls() {
  const searchInput = document.getElementById('punishSearchInput');
  const blockFilter = document.getElementById('punishBlockFilter');
  const hitLevelFilter = document.getElementById('punishHitLevelFilter');
  const stanceFilter = document.getElementById('punishStanceFilter');
  const minDamageInput = document.getElementById('punishMinDamage');
  const resetBtn = document.getElementById('btnResetPunishFilters');
  const swapBtn = document.getElementById('btnSwapPunish');
  const modalCloseBtn = document.getElementById('btnPracticeModalClose');
  const startDrillBtn = document.getElementById('btnStartDrill');
  const executePunishBtn = document.getElementById('btnExecutePunish');
  const logSuccessBtn = document.getElementById('btnLogSuccess');
  const logFailBtn = document.getElementById('btnLogFail');
  const resetModalRecordBtn = document.getElementById('btnResetModalRecord');

  if (searchInput) {
    searchInput.addEventListener('input', debounce(() => {
      state.punishment.filters.query = searchInput.value.trim();
      loadPunishmentOptions();
    }, 200));
  }

  if (blockFilter) {
    blockFilter.addEventListener('change', () => {
      state.punishment.filters.blockFilter = blockFilter.value;
      loadPunishmentOptions();
    });
  }

  if (hitLevelFilter) {
    hitLevelFilter.addEventListener('change', () => {
      state.punishment.filters.hitLevel = hitLevelFilter.value;
      loadPunishmentOptions();
    });
  }

  if (stanceFilter) {
    stanceFilter.addEventListener('change', () => {
      state.punishment.filters.stance = stanceFilter.value;
      loadPunishmentOptions();
    });
  }

  if (minDamageInput) {
    minDamageInput.addEventListener('input', debounce(() => {
      state.punishment.filters.minDamage = parseInt(minDamageInput.value) || 0;
      loadPunishmentOptions();
    }, 200));
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      if (searchInput) searchInput.value = '';
      if (blockFilter) blockFilter.value = 'ALL';
      if (hitLevelFilter) hitLevelFilter.value = 'ALL';
      if (stanceFilter) stanceFilter.value = 'ALL';
      if (minDamageInput) minDamageInput.value = '';
      state.punishment.filters = {
        query: '',
        blockFilter: 'ALL',
        hitLevel: 'ALL',
        stance: 'ALL',
        minDamage: 0
      };
      loadPunishmentOptions();
    });
  }

  if (swapBtn) {
    swapBtn.addEventListener('click', () => {
      swapFighters();
    });
  }

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closePracticeModal);
  }

  const modalBackdrop = document.getElementById('practiceModal');
  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) closePracticeModal();
    });
  }

  if (startDrillBtn) {
    startDrillBtn.addEventListener('click', startReactionDrill);
  }

  if (executePunishBtn) {
    executePunishBtn.addEventListener('click', handlePunishExecution);
  }

  if (logSuccessBtn) {
    logSuccessBtn.addEventListener('click', () => recordPracticeTrial('SUCCESS'));
  }

  if (logFailBtn) {
    logFailBtn.addEventListener('click', () => recordPracticeTrial('FAIL'));
  }

  if (resetModalRecordBtn) {
    resetModalRecordBtn.addEventListener('click', resetSessionPracticeProgress);
  }

  // Keyboard shortcut for reaction drill: pressing Space or Enter triggers punish
  window.addEventListener('keydown', (e) => {
    const modal = document.getElementById('practiceModal');
    if (modal && modal.style.display !== 'none' && state.punishment.drillWaitingForInput) {
      if (['Space', 'Enter', 'KeyJ', 'Digit1', 'Digit2'].includes(e.code) || e.key === ' ') {
        e.preventDefault();
        handlePunishExecution();
      }
    }
  });
}

async function loadPunishmentOptions() {
  const pSelect = document.getElementById('playerSelect');
  const oSelect = document.getElementById('opponentSelect');
  if (!pSelect || !oSelect) return;

  const playerId = parseInt(pSelect.value);
  const opponentId = parseInt(oSelect.value);
  if (isNaN(playerId) || isNaN(opponentId)) return;

  // Update fighter display tags in punishment assistant
  const pChar = state.characters.find(c => c.id === playerId);
  const oChar = state.characters.find(c => c.id === opponentId);

  const pAvatar = document.getElementById('punishP1Avatar');
  const pName = document.getElementById('punishP1Name');
  const oAvatar = document.getElementById('punishP2Avatar');
  const oName = document.getElementById('punishP2Name');

  if (pAvatar && pChar) {
    pAvatar.src = pChar.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp';
    pAvatar.onerror = () => { pAvatar.src = '/assets/avatars/jin-brand-256-C1-oe_x3.webp'; };
  }
  if (pName && pChar) pName.textContent = pChar.name;

  if (oAvatar && oChar) {
    oAvatar.src = oChar.avatar_url || '/assets/avatars/kazuya-brand-256-BInk9tTm.webp';
    oAvatar.onerror = () => { oAvatar.src = '/assets/avatars/kazuya-brand-256-BInk9tTm.webp'; };
  }
  if (oName && oChar) oName.textContent = oChar.name;

  // Build query string
  const params = new URLSearchParams({
    player_character_id: playerId,
    opponent_character_id: opponentId
  });

  const f = state.punishment.filters;
  if (f.query) params.append('query', f.query);
  if (f.blockFilter && f.blockFilter !== 'ALL') params.append('block_filter', f.blockFilter);
  if (f.hitLevel && f.hitLevel !== 'ALL') params.append('hit_level', f.hitLevel);
  if (f.stance && f.stance !== 'ALL') params.append('stance', f.stance);
  if (f.minDamage > 0) params.append('min_damage', f.minDamage);

  try {
    const data = await fetchAPI(`/punishment/options?${params.toString()}`, true);
    if (!data) return;
    state.punishment.options = data.options || [];

    // Update KPI metrics
    const totalEl = document.getElementById('pmTotalMoves');
    const punEl = document.getElementById('pmPunishable');
    const launchEl = document.getElementById('pmLaunch');
    const safeEl = document.getElementById('pmSafe');
    const countPill = document.getElementById('punishFilteredCount');

    if (totalEl) totalEl.textContent = data.total_opponent_moves;
    if (punEl) punEl.textContent = data.punishable_moves_count;
    if (launchEl) launchEl.textContent = data.launch_punishable_count;
    if (safeEl) safeEl.textContent = data.safe_moves_count;
    if (countPill) countPill.textContent = `${state.punishment.options.length} Moves Listed`;

    renderPunishTable(state.punishment.options);
    await loadGlobalPracticeProgress();
  } catch (err) {
    console.error('Failed to load punishment options:', err);
  }
}

function renderPunishTable(options) {
  const tbody = document.getElementById('punishTableBody');
  const emptyBox = document.getElementById('punishTableEmpty');
  if (!tbody) return;

  if (!options || options.length === 0) {
    tbody.innerHTML = '';
    if (emptyBox) emptyBox.style.display = 'block';
    return;
  }

  if (emptyBox) emptyBox.style.display = 'none';

  tbody.innerHTML = options.map((opt, idx) => {
    // Block Advantage Pill
    const blk = opt.opponent_block_advantage;
    let blkClass = 'safe';
    let blkText = 'N/A';
    if (blk !== null) {
      if (blk <= -15) {
        blkClass = 'launch';
        blkText = `${blk}`;
      } else if (blk <= -10) {
        blkClass = 'punishable';
        blkText = `${blk}`;
      } else if (blk > 0) {
        blkClass = 'plus';
        blkText = `+${blk}`;
      } else {
        blkClass = 'safe';
        blkText = `${blk}`;
      }
    }

    // Recovery State Pill (Standing vs Crouching)
    const recState = opt.opponent_recovery_state || 'STANDING';
    const recClass = recState.toLowerCase();
    const recLabel = recState === 'CROUCHING' ? 'CROUCH GUARD (WS Only)' : 'STANDING GUARD';

    // Status Reach Badge
    const status = opt.punish_status || 'UNVERIFIED';
    let statusClass = 'unverified';
    let statusIcon = 'ℹ️';
    let statusLabel = status;
    if (status === 'GUARANTEED') {
      statusClass = 'guaranteed';
      statusIcon = '✅';
      statusLabel = 'GUARANTEED';
    } else if (status === 'CONDITIONAL') {
      statusClass = 'conditional';
      statusIcon = '⚠️';
      statusLabel = 'CONDITIONAL (Pushback)';
    } else if (status === 'SAFE') {
      statusClass = 'safe';
      statusIcon = '🛡️';
      statusLabel = 'SAFE ATTACK';
    } else {
      statusClass = 'unverified';
      statusIcon = '❓';
      statusLabel = 'UNVERIFIED';
    }

    // Recommended Punish details
    const punName = opt.recommended_punish_name || (opt.is_safe ? 'Neutral Guard' : 'No option found');
    const punInput = opt.recommended_punish_input ? formatTekkenNotation(opt.recommended_punish_input) : '—';
    const punStp = opt.punish_startup ? `i${opt.punish_startup}` : '—';
    const punDmg = opt.punish_damage ? `<span style="color:var(--accent-gold); font-weight:800;">${opt.punish_damage} DMG</span>` : '—';
    const punTier = opt.punish_tier ? `<span class="punish-tier-badge ${opt.punish_tier.toLowerCase().includes('launch') ? 'launch' : (opt.punish_tier.toLowerCase().includes('ws') ? 'intermediate' : 'jab')}">${opt.punish_tier}</span>` : '';

    return `
      <tr>
        <td>
          <div style="font-weight:700; color:#fff;">${opt.opponent_move_name}</div>
          <div style="display:flex; align-items:center; gap:0.4rem; margin-top:0.25rem;">
            ${formatTekkenNotation(opt.opponent_move_input)}
            <span class="step-tag">${opt.opponent_hit_level ? opt.opponent_hit_level.toUpperCase() : 'M'}</span>
          </div>
        </td>
        <td>
          <span class="punish-startup-badge">i${opt.opponent_startup || '—'}</span>
        </td>
        <td>
          <span class="frame-disadvantage-badge ${blkClass}">${blkText}</span>
        </td>
        <td>
          <span class="recovery-badge ${recClass}" title="${recState === 'CROUCHING' ? 'Defending low moves forces crouching recovery; requires While Standing (WS) moves' : 'Normal standing guard'}">${recLabel}</span>
        </td>
        <td>
          <div style="font-weight:700; color:#fff;">${punName}</div>
          <div style="margin-top:0.25rem; display:flex; align-items:center; gap:0.35rem;">
            ${punInput}
            ${punTier}
          </div>
        </td>
        <td>
          <span class="punish-startup-badge">${punStp}</span>
        </td>
        <td>
          ${punDmg}
        </td>
        <td>
          <span class="status-reach-badge ${statusClass}">
            <span>${statusIcon}</span>
            <span>${statusLabel}</span>
          </span>
          ${opt.opponent_pushback === 'HIGH' ? '<div style="font-size:0.68rem; color:#ff7043; margin-top:0.2rem;">Pushback warning: jab whiffs</div>' : ''}
        </td>
        <td>
          <div class="punish-explanation-text">${opt.why_it_works}</div>
        </td>
        <td>
          <button class="btn-practice-trigger" type="button" onclick="openPracticeModalByIndex(${idx})">
            <span>⚡ Practise</span>
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function openPracticeModalByIndex(idx) {
  const opt = state.punishment.options[idx];
  if (!opt) return;

  state.punishment.currentPracticeMove = opt;

  const modal = document.getElementById('practiceModal');
  const title = document.getElementById('practiceModalTitle');
  if (!modal) return;

  if (title) {
    title.textContent = `${opt.opponent_move_name} (${opt.opponent_move_input}) vs ${opt.recommended_punish_name || 'Punish Check'}`;
  }

  // Step 1: Learn Opponent Move
  document.getElementById('stepOppName').textContent = opt.opponent_move_name;
  document.getElementById('stepOppInput').textContent = opt.opponent_move_input;
  document.getElementById('stepOppStartup').textContent = opt.opponent_startup ? `i${opt.opponent_startup}` : 'i—';
  document.getElementById('stepOppHitLevel').textContent = opt.opponent_hit_level ? opt.opponent_hit_level.toUpperCase() : 'M';
  const oppBlkEl = document.getElementById('stepOppBlock');
  if (oppBlkEl) {
    oppBlkEl.textContent = opt.opponent_block_advantage !== null ? `${opt.opponent_block_advantage} on block` : 'Unknown frames';
  }

  // Step 2: Recovery State Recognition
  const recDisplay = document.getElementById('stepRecoveryDisplay');
  const recNote = document.getElementById('stepRecoveryNote');
  if (opt.opponent_recovery_state === 'CROUCHING') {
    recDisplay.textContent = 'CROUCHING GUARD (WS ONLY)';
    recDisplay.style.color = 'var(--accent-gold)';
    recDisplay.style.borderColor = 'rgba(255, 190, 11, 0.4)';
    recDisplay.style.background = 'rgba(255, 190, 11, 0.1)';
    recNote.textContent = 'Blocking a low attack forces crouching recovery. Standing 1,2 jabs cannot be performed; you must use a While Standing (WS) move!';
  } else {
    recDisplay.textContent = 'STANDING GUARD (STANDARD)';
    recDisplay.style.color = 'var(--accent-cyan)';
    recDisplay.style.borderColor = 'rgba(0, 229, 255, 0.4)';
    recDisplay.style.background = 'rgba(0, 229, 255, 0.1)';
    recNote.textContent = 'Opponent attack recovered standing. You can use standard standing attacks or launchers to punish.';
  }

  // Step 3: Punish Execution
  document.getElementById('stepPunishName').textContent = opt.recommended_punish_name || 'Standing 1,2 Jab Check';
  document.getElementById('stepPunishInput').textContent = opt.recommended_punish_input || '1,2';
  document.getElementById('stepPunishStartup').textContent = opt.punish_startup ? `i${opt.punish_startup}` : 'i10';
  document.getElementById('stepPunishDamage').textContent = opt.punish_damage ? `${opt.punish_damage} DMG` : '17 DMG';

  // Step 4: Reset Reaction Trainer
  resetReactionDrillDisplay();

  // Step 5: Load Move Mastery Progress
  loadMovePracticeProgress(opt.opponent_move_name);

  modal.style.display = 'flex';
}

function closePracticeModal() {
  const modal = document.getElementById('practiceModal');
  if (modal) modal.style.display = 'none';

  if (state.punishment.drillTimer) {
    clearTimeout(state.punishment.drillTimer);
    state.punishment.drillTimer = null;
  }
  state.punishment.drillWaitingForInput = false;
}

function resetReactionDrillDisplay() {
  const stage = document.getElementById('trainerStage');
  const prompt = document.getElementById('trainerPrompt');
  const timer = document.getElementById('trainerTimer');
  const status = document.getElementById('trainerStatusIndicator');
  const punishBtn = document.getElementById('btnExecutePunish');

  if (stage) stage.className = 'trainer-display-stage';
  if (prompt) prompt.textContent = 'Press "Start Reaction Drill" when ready to test your punish execution!';
  if (timer) {
    timer.style.display = 'none';
    timer.textContent = '0 ms';
  }
  if (status) {
    status.className = 'trainer-status ready';
    status.textContent = 'READY TO DRILL';
  }
  if (punishBtn) punishBtn.disabled = true;

  state.punishment.drillWaitingForInput = false;
  if (state.punishment.drillTimer) {
    clearTimeout(state.punishment.drillTimer);
    state.punishment.drillTimer = null;
  }
}

function startReactionDrill() {
  const stage = document.getElementById('trainerStage');
  const prompt = document.getElementById('trainerPrompt');
  const timer = document.getElementById('trainerTimer');
  const status = document.getElementById('trainerStatusIndicator');
  const punishBtn = document.getElementById('btnExecutePunish');

  resetReactionDrillDisplay();

  if (status) {
    status.className = 'trainer-status active';
    status.textContent = 'DRILL IN PROGRESS...';
  }
  if (prompt) {
    prompt.textContent = 'STAND GUARD... WATCH OPPONENT RECOVERY...';
  }

  // Random delay between 1500ms and 3500ms
  const delayMs = Math.floor(Math.random() * 2000) + 1500;

  state.punishment.drillTimer = setTimeout(() => {
    state.punishment.drillStartTime = performance.now();
    state.punishment.drillWaitingForInput = true;

    if (stage) stage.className = 'trainer-display-stage punish-now';
    if (prompt) prompt.textContent = '⚡ OPPONENT IN BLOCK STUN! EXECUTE PUNISH INPUT NOW!';
    if (punishBtn) punishBtn.disabled = false;
    if (status) {
      status.className = 'trainer-status active';
      status.textContent = 'PUNISH WINDOW ACTIVE!';
    }
  }, delayMs);
}

function handlePunishExecution() {
  if (!state.punishment.drillWaitingForInput) return;

  const elapsed = Math.round(performance.now() - state.punishment.drillStartTime);
  state.punishment.drillWaitingForInput = false;

  const stage = document.getElementById('trainerStage');
  const prompt = document.getElementById('trainerPrompt');
  const timer = document.getElementById('trainerTimer');
  const status = document.getElementById('trainerStatusIndicator');
  const punishBtn = document.getElementById('btnExecutePunish');

  if (punishBtn) punishBtn.disabled = true;
  if (timer) {
    timer.style.display = 'block';
    timer.textContent = `${elapsed} ms reaction`;
  }

  // Human reaction threshold: under 450ms is successful punish confirmation
  const isSuccess = elapsed <= 450;

  if (isSuccess) {
    if (stage) stage.className = 'trainer-display-stage';
    if (prompt) {
      prompt.innerHTML = `<span style="color:#00e676; font-weight:900;">PERFECT TIMING! Punish Confirmed (${elapsed}ms)!</span>`;
    }
    if (status) {
      status.className = 'trainer-status success';
      status.textContent = 'EXECUTION SUCCESS (+1)';
    }
    recordPracticeTrial('SUCCESS');
  } else {
    if (stage) stage.className = 'trainer-display-stage';
    if (prompt) {
      prompt.innerHTML = `<span style="color:var(--accent-red); font-weight:900;">TOO SLOW (${elapsed}ms)! Opponent guarded.</span>`;
    }
    if (status) {
      status.className = 'trainer-status failed';
      status.textContent = 'ATTEMPT FAILED';
    }
    recordPracticeTrial('FAIL');
  }
}

async function recordPracticeTrial(result) {
  const opt = state.punishment.currentPracticeMove;
  if (!opt) return;

  const pSelect = document.getElementById('playerSelect');
  const oSelect = document.getElementById('opponentSelect');
  if (!pSelect || !oSelect) return;

  const playerId = parseInt(pSelect.value);
  const opponentId = parseInt(oSelect.value);

  const payload = {
    session_token: state.sessionToken,
    player_character_id: playerId,
    opponent_character_id: opponentId,
    opponent_move_id: opt.opponent_move_id,
    opponent_move_name: opt.opponent_move_name,
    opponent_move_input: opt.opponent_move_input,
    punish_move_input: opt.recommended_punish_input || '1,2',
    result: result
  };

  try {
    const res = await fetch(`${API_BASE}/punishment/practice/record`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const record = await res.json();
      updateModalMasteryUI(record);
      await loadGlobalPracticeProgress();
    }
  } catch (err) {
    console.error('Failed to record practice trial:', err);
  }
}

function updateModalMasteryUI(record) {
  const pctEl = document.getElementById('modalMasteryPct');
  const sCountEl = document.getElementById('modalSuccessCount');
  const fCountEl = document.getElementById('modalFailCount');
  const totEl = document.getElementById('modalTotalAttempts');
  const barEl = document.getElementById('modalMasteryBar');

  if (pctEl) pctEl.textContent = `${record.mastery_score}% Mastery`;
  if (sCountEl) sCountEl.textContent = record.success_count;
  if (fCountEl) fCountEl.textContent = record.fail_count;
  if (totEl) totEl.textContent = record.attempts;
  if (barEl) barEl.style.width = `${record.mastery_score}%`;
}

async function loadMovePracticeProgress(moveName) {
  try {
    const res = await fetch(`${API_BASE}/punishment/practice/progress?session_token=${state.sessionToken}`);
    if (res.ok) {
      const data = await res.json();
      const rec = (data.records || []).find(r => r.opponent_move_name === moveName);
      if (rec) {
        updateModalMasteryUI(rec);
      } else {
        updateModalMasteryUI({
          mastery_score: 0,
          success_count: 0,
          fail_count: 0,
          attempts: 0
        });
      }
    }
  } catch (err) {
    console.error('Failed to load move practice progress:', err);
  }
}

async function loadGlobalPracticeProgress() {
  try {
    const res = await fetch(`${API_BASE}/punishment/practice/progress?session_token=${state.sessionToken}`);
    if (res.ok) {
      const data = await res.json();
      const accEl = document.getElementById('pmAccuracy');
      const attEl = document.getElementById('pmAttempts');
      if (accEl) accEl.textContent = `${data.overall_accuracy_pct}%`;
      if (attEl) attEl.textContent = data.total_attempts;
    }
  } catch (err) {
    console.error('Failed to load global practice progress:', err);
  }
}

async function resetSessionPracticeProgress() {
  if (!confirm('Are you sure you want to reset all training progress for this session?')) return;
  try {
    const res = await fetch(`${API_BASE}/punishment/practice/reset?session_token=${state.sessionToken}`, {
      method: 'POST'
    });
    if (res.ok) {
      updateModalMasteryUI({
        mastery_score: 0,
        success_count: 0,
        fail_count: 0,
        attempts: 0
      });
      await loadGlobalPracticeProgress();
    }
  } catch (err) {
    console.error('Failed to reset practice progress:', err);
  }
}

// ==========================================================================
// Phase 7: Matchup Data Management, Import Studio & Quality Hub
// ==========================================================================

function toggleAdminHub() {
  const content = document.getElementById('adminHubContent');
  const icon = document.getElementById('adminToggleIcon');
  const text = document.getElementById('adminToggleText');
  if (!content) return;
  const isHidden = content.style.display === 'none';
  if (isHidden) {
    content.style.display = 'block';
    if (icon) icon.textContent = '▼';
    if (text) text.textContent = 'Collapse Admin / Evaluator Studio';
    refreshAdminDashboard();
  } else {
    content.style.display = 'none';
    if (icon) icon.textContent = '▶';
    if (text) text.textContent = 'Expand Admin / Evaluator Studio';
  }
}
window.toggleAdminHub = toggleAdminHub;

function initAdminHub() {
  const keyInput = document.getElementById('adminSecretKeyInput');
  const userInput = document.getElementById('adminUsernameInput');
  if (keyInput) keyInput.value = state.admin.key;
  if (userInput) userInput.value = state.admin.user;

  populateAdminCharacterSelect();
  refreshAdminDashboard();
  loadAdminSources();
}

async function refreshAdminDashboard() {
  const keyInput = document.getElementById('adminSecretKeyInput');
  const userInput = document.getElementById('adminUsernameInput');
  if (keyInput) state.admin.key = keyInput.value.trim();
  if (userInput) state.admin.user = userInput.value.trim();

  const badge = document.getElementById('adminAuthBadge');

  try {
    const res = await fetch(`${API_BASE}/admin/dashboard`, {
      headers: {
        'X-Admin-Key': state.admin.key,
        'X-Admin-User': state.admin.user
      }
    });

    if (!res.ok) {
      if (badge) {
        badge.className = 'admin-auth-badge unauthorized';
        badge.innerHTML = '<span>✕</span> <span>INVALID ADMIN KEY</span>';
      }
      return;
    }

    if (badge) {
      badge.className = 'admin-auth-badge authorized';
      badge.innerHTML = '<span>●</span> <span>ADMIN SESSION ACTIVE</span>';
    }

    const data = await res.json();
    state.admin.dashboardData = data;

    // Populate KPI cards
    const setVal = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    setVal('adminMissingFramesVal', data.missing_frame_data_count);
    setVal('adminMissingStagesVal', data.missing_stage_mechanics_count);
    setVal('adminCombosNoCompatVal', data.combos_without_opponent_compatibility_count);
    setVal('adminUnverifiedPunishesVal', data.unverified_punish_options_count);
    setVal('adminConflictsVal', data.conflicting_records_count);
    setVal('adminOutdatedPatchVal', data.outdated_patch_records_count);
    setVal('adminIncompleteSourcesVal', data.incomplete_source_metadata_count);
    setVal('adminAwaitingReviewVal', data.records_awaiting_review_count);

    // Populate data states chips
    const dist = data.status_distribution || {};
    const setChip = (id, label, count) => {
      const el = document.getElementById(id);
      if (el) el.textContent = `${label} (${count || 0})`;
    };
    setChip('chipVerified', 'VERIFIED', dist.VERIFIED);
    setChip('chipUnverified', 'UNVERIFIED', dist.UNVERIFIED);
    setChip('chipConflicting', 'CONFLICTING', dist.CONFLICTING);
    setChip('chipUnavailable', 'UNAVAILABLE', dist.UNAVAILABLE);
    setChip('chipConfirmedAbsent', 'CONFIRMED ABSENT', dist.CONFIRMED_ABSENT);
    setChip('chipUnknown', 'UNKNOWN', dist.UNKNOWN);
    setChip('chipNotProvided', 'NOT PROVIDED', dist.NOT_PROVIDED);

    // Render issues table
    renderAdminIssues(data.audit_issues || []);

  } catch (err) {
    console.warn('Failed to load admin quality dashboard:', err);
    if (badge) {
      badge.className = 'admin-auth-badge unauthorized';
      badge.innerHTML = '<span>✕</span> <span>CONNECTION ERROR</span>';
    }
  }
}

function renderAdminIssues(issues) {
  const tbody = document.getElementById('adminIssuesTableBody');
  const countTab = document.getElementById('adminIssuesCountTab');
  if (countTab) countTab.textContent = issues.length;
  if (!tbody) return;

  if (issues.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" style="text-align:center; padding:1.5rem; color:#00e676;">
          ✓ All data records are verified with complete telemetry and zero active discrepancies!
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = issues.map(iss => {
    let sevClass = 'badge-pending';
    if (iss.severity === 'CRITICAL' || iss.severity === 'HIGH') sevClass = 'badge-unverified';
    else if (iss.severity === 'MEDIUM') sevClass = 'badge-review';
    else sevClass = 'badge-approved';

    return `
      <tr>
        <td><span class="feat-badge ${sevClass}">${iss.severity}</span></td>
        <td><strong style="color:var(--accent-cyan); font-size:0.7rem;">${iss.entity_type}</strong></td>
        <td><div style="font-weight:700; color:#fff;">${iss.title}</div></td>
        <td><span style="color:#fbbf24; font-weight:700;">${iss.issue_type}</span></td>
        <td><span class="state-chip ${iss.status.toLowerCase().replace(/_/g, '-')}">${iss.status}</span></td>
        <td style="color:var(--text-muted);">${iss.details}</td>
        <td>
          <button type="button" class="btn-tb-reset" style="font-size:0.68rem; padding:0.2rem 0.5rem;" onclick="quickUpdateStatus('${iss.entity_type}', ${iss.entity_id}, 'VERIFIED')">
            Mark Verified
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function switchAdminTab(tabId) {
  state.admin.currentTab = tabId;
  document.querySelectorAll('.admin-tab-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.tab === tabId);
  });
  document.querySelectorAll('.admin-tab-pane').forEach(p => {
    p.classList.toggle('active', p.id === tabId);
  });

  if (tabId === 'tabHistory') loadVerificationHistory();
  if (tabId === 'tabAttribution') loadAdminSources();
}

async function loadVerificationHistory() {
  const tbody = document.getElementById('adminHistoryTableBody');
  if (!tbody) return;

  try {
    const res = await fetch(`${API_BASE}/admin/history?limit=50`, {
      headers: {
        'X-Admin-Key': state.admin.key,
        'X-Admin-User': state.admin.user
      }
    });
    if (!res.ok) return;

    const records = await res.json();
    if (records.length === 0) {
      tbody.innerHTML = '<tr><td colspan="10" style="text-align:center; padding:1.5rem; color:var(--text-dim);">No verification audit records found yet.</td></tr>';
      return;
    }

    tbody.innerHTML = records.map(r => {
      const dt = new Date(r.verified_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      return `
        <tr>
          <td style="color:var(--text-dim);">${dt}</td>
          <td><strong style="color:var(--accent-cyan);">${r.entity_type}</strong></td>
          <td>${r.field_name || '—'}</td>
          <td style="color:#ff4d6d; font-family:monospace;">${r.old_value !== null ? r.old_value : '—'}</td>
          <td style="color:#00e676; font-family:monospace;">${r.new_value !== null ? r.new_value : '—'}</td>
          <td>${r.verified_by}</td>
          <td><span style="font-size:0.65rem; color:#cbd5e1;">${r.method}</span></td>
          <td><span class="feat-badge ${r.result === 'VERIFIED' ? 'badge-approved' : 'badge-unverified'}">${r.result}</span></td>
          <td>${r.patch_version}</td>
          <td style="color:var(--text-muted); font-size:0.7rem;">${r.evidence_notes || '—'}</td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    console.warn('Failed to load history:', err);
  }
}

async function loadAdminSources() {
  const container = document.getElementById('adminSourcesList');
  if (!container) return;

  try {
    const res = await fetch(`${API_BASE}/admin/sources`, {
      headers: {
        'X-Admin-Key': state.admin.key,
        'X-Admin-User': state.admin.user
      }
    });
    if (!res.ok) return;
    const sources = await res.json();

    container.innerHTML = sources.map(s => `
      <div style="background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.08); border-radius:6px; padding:0.85rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
          <strong style="color:#fff; font-size:0.85rem;">${s.name}</strong>
          <span class="feat-badge badge-approved">${s.approval_status}</span>
        </div>
        <div style="font-size:0.72rem; color:var(--accent-gold); margin-bottom:0.25rem;">
          License: <strong>${s.license_type}</strong>
        </div>
        <div style="font-size:0.7rem; color:var(--text-muted); margin-bottom:0.4rem;">
          ${s.attribution_text || 'Attribution statement pending compliance review.'}
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.68rem; color:var(--text-dim);">
          <span>Rate: ${s.rate_limit_policy}</span>
          <a href="${s.base_url}" target="_blank" style="color:var(--accent-cyan); text-decoration:none;">Visit Source &rarr;</a>
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.warn('Failed to load sources:', err);
  }
}

function populateAdminCharacterSelect() {
  const sel = document.getElementById('editMoveCharSelect');
  if (!sel || !state.characters) return;

  sel.innerHTML = state.characters.map(c => `
    <option value="${c.id}">${c.name} (${c.slug})</option>
  `).join('');
}

async function quickUpdateStatus(entityType, entityId, newStatus) {
  const reason = prompt(`Enter justification / lab evidence notes to update ${entityType} #${entityId} to ${newStatus}:`, 'Verified in Practice Mode with 60fps frame counter');
  if (!reason) return;

  try {
    const res = await fetch(`${API_BASE}/admin/verification-status`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Admin-Key': state.admin.key,
        'X-Admin-User': state.admin.user
      },
      body: JSON.stringify({
        entity_type: entityType,
        entity_id: entityId,
        new_status: newStatus,
        evidence_notes: reason
      })
    });

    if (res.ok) {
      alert(`Status successfully updated to ${newStatus} and recorded in audit trail.`);
      refreshAdminDashboard();
    } else {
      const err = await res.json();
      alert(`Error updating status: ${err.detail || 'Request failed'}`);
    }
  } catch (err) {
    alert(`Failed to update status: ${err.message}`);
  }
}

async function handleAdminSaveMove(e) {
  e.preventDefault();
  const feedback = document.getElementById('adminEditorFeedback');

  const charId = parseInt(document.getElementById('editMoveCharSelect').value);
  const name = document.getElementById('editMoveName').value.trim();
  const notation = document.getElementById('editMoveNotation').value.trim();
  const startup = document.getElementById('editMoveStartup').value ? parseInt(document.getElementById('editMoveStartup').value) : null;
  const block = document.getElementById('editMoveBlock').value ? parseInt(document.getElementById('editMoveBlock').value) : null;
  const damage = document.getElementById('editMoveDamage').value ? parseInt(document.getElementById('editMoveDamage').value) : null;
  const hitLevel = document.getElementById('editMoveHitLevel').value.trim() || null;
  const statusVal = document.getElementById('editMoveStatus').value;
  const reason = document.getElementById('editMoveReason').value.trim();

  const payload = {
    character_id: charId,
    name: name,
    normalized_notation: notation,
    original_notation: notation,
    startup_frames: startup,
    block_advantage: block,
    damage: damage,
    hit_level: hitLevel,
    verification_status: statusVal,
    reason_for_change: reason
  };

  try {
    const res = await fetch(`${API_BASE}/admin/moves`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Admin-Key': state.admin.key,
        'X-Admin-User': state.admin.user
      },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      if (feedback) {
        feedback.style.color = '#00e676';
        feedback.textContent = `✓ Move '${notation}' saved with audit trail!`;
      }
      refreshAdminDashboard();
    } else {
      const err = await res.json();
      if (feedback) {
        feedback.style.color = '#ff4d6d';
        feedback.textContent = `Error: ${err.detail || 'Failed to save move'}`;
      }
    }
  } catch (err) {
    if (feedback) {
      feedback.style.color = '#ff4d6d';
      feedback.textContent = `Error: ${err.message}`;
    }
  }
}

function loadSampleImportJson() {
  const textarea = document.getElementById('importPayloadTextarea');
  const entitySel = document.getElementById('importEntityTypeSelect');
  const formatSel = document.getElementById('importFormatSelect');

  if (entitySel) entitySel.value = 'MOVES';
  if (formatSel) formatSel.value = 'JSON';

  const sample = [
    {
      "character_slug": "jin",
      "name": "Demon Scissors Extension",
      "normalized_notation": "4~3",
      "startup_frames": 23,
      "block_advantage": -13,
      "damage": 25,
      "hit_level": "m",
      "verification_status": "VERIFIED"
    },
    {
      "character_slug": "kazuya",
      "name": "Abolishing Fist",
      "normalized_notation": "df+1,2",
      "startup_frames": 15,
      "block_advantage": -14,
      "damage": 32,
      "hit_level": "m,m",
      "verification_status": "UNVERIFIED"
    }
  ];

  if (textarea) textarea.value = JSON.stringify(sample, null, 2);
}

function handleImportFileSelect(e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (event) => {
    const text = event.target.result;
    const textarea = document.getElementById('importPayloadTextarea');
    if (textarea) textarea.value = text;

    const formatSel = document.getElementById('importFormatSelect');
    if (formatSel) {
      formatSel.value = file.name.endsWith('.csv') ? 'CSV' : 'JSON';
    }
  };
  reader.readAsText(file);
}

async function previewImportPayload() {
  const textarea = document.getElementById('importPayloadTextarea');
  const entityType = document.getElementById('importEntityTypeSelect').value;
  const formatType = document.getElementById('importFormatSelect').value;
  const pill = document.getElementById('importPreviewStatusPill');
  const issuesList = document.getElementById('importIssuesList');
  const commitBtn = document.getElementById('btnCommitImport');

  if (!textarea || !textarea.value.trim()) {
    alert('Please enter or load a CSV/JSON payload first.');
    return;
  }

  const payload = {
    entity_type: entityType,
    format: formatType,
    raw_content: textarea.value.trim(),
    source_name: 'Admin Workbench Import'
  };

  try {
    const res = await fetch(`${API_BASE}/admin/import/preview`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Admin-Key': state.admin.key,
        'X-Admin-User': state.admin.user
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      alert(`Preview failed: ${err.detail || 'Invalid payload'}`);
      return;
    }

    const preview = await res.json();
    state.admin.previewResponse = preview;

    // Metrics
    document.getElementById('ipmValid').textContent = preview.valid_rows_count;
    document.getElementById('ipmErrors').textContent = preview.error_rows_count;
    document.getElementById('ipmDuplicates').textContent = preview.duplicate_count;
    document.getElementById('ipmProtected').textContent = preview.verified_protection_count;

    if (pill) {
      if (preview.is_importable) {
        pill.className = 'feat-badge badge-approved';
        pill.textContent = 'VALIDATION PASSED';
      } else {
        pill.className = 'feat-badge badge-unverified';
        pill.textContent = `${preview.error_rows_count} ERRORS DETECTED`;
      }
    }

    // Issues list
    if (issuesList) {
      if (preview.issues.length === 0) {
        issuesList.innerHTML = '<div style="color:#00e676; padding:0.5rem;">✓ Zero validation errors or conflict blocks detected. Ready to commit.</div>';
      } else {
        issuesList.innerHTML = preview.issues.map(iss => {
          let color = '#ff4d6d';
          if (iss.issue_type === 'DUPLICATE') color = '#fbbf24';
          if (iss.issue_type === 'UNVERIFIED_OVERWRITE_PROTECTED') color = '#c084fc';
          return `
            <div style="border-bottom:1px solid rgba(255,255,255,0.05); padding:0.25rem 0;">
              <span style="color:${color}; font-weight:800;">[Row ${iss.row_index}] ${iss.issue_type}:</span>
              <span style="color:#e2e8f0;">${iss.message}</span>
            </div>
          `;
        }).join('');
      }
    }

    if (commitBtn) {
      commitBtn.disabled = !preview.is_importable || preview.valid_rows_count === 0;
    }

  } catch (err) {
    alert(`Error during preview: ${err.message}`);
  }
}

async function executeCommittedImport() {
  const preview = state.admin.previewResponse;
  if (!preview || !preview.preview_rows) return;

  const allowOverride = document.getElementById('checkAllowVerifiedOverride').checked;
  const feedback = document.getElementById('importResultFeedback');
  const commitBtn = document.getElementById('btnCommitImport');

  if (commitBtn) commitBtn.disabled = true;
  if (feedback) {
    feedback.style.color = '#38bdf8';
    feedback.textContent = 'Executing transaction-safe import...';
  }

  const payload = {
    entity_type: preview.entity_type,
    rows: preview.preview_rows,
    source_name: 'Admin Workbench Import',
    allow_override_verified: allowOverride
  };

  try {
    const res = await fetch(`${API_BASE}/admin/import/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Admin-Key': state.admin.key,
        'X-Admin-User': state.admin.user
      },
      body: JSON.stringify(payload)
    });

    const summary = await res.json();
    if (summary.success) {
      if (feedback) {
        feedback.style.color = '#00e676';
        feedback.textContent = `✓ ${summary.message}`;
      }
      refreshAdminDashboard();
    } else {
      if (feedback) {
        feedback.style.color = '#ff4d6d';
        feedback.textContent = `✕ Import rolled back: ${summary.message}`;
      }
    }
  } catch (err) {
    if (feedback) {
      feedback.style.color = '#ff4d6d';
      feedback.textContent = `Error: ${err.message}`;
    }
  }
}

// ==========================================================================
// 1. Audio Synthesis Sound FX Engine (Web Audio API)
// ==========================================================================
let audioCtx = null;
function getAudioContext() {
  if (!audioCtx && (window.AudioContext || window.webkitAudioContext)) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx && audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
  return audioCtx;
}

function playSfx(type = 'click') {
  const enabled = localStorage.getItem('tekken8_sound_fx') !== 'false';
  if (!enabled) return;
  try {
    const ctx = getAudioContext();
    if (!ctx) return;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    const now = ctx.currentTime;

    if (type === 'click') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(800, now);
      osc.frequency.exponentialRampToValueAtTime(300, now + 0.04);
      gain.gain.setValueAtTime(0.06, now);
      gain.gain.linearRampToValueAtTime(0.001, now + 0.04);
      osc.start(now);
      osc.stop(now + 0.04);
    } else if (type === 'correct') {
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(523.25, now);
      osc.frequency.setValueAtTime(659.25, now + 0.06);
      osc.frequency.setValueAtTime(783.99, now + 0.12);
      gain.gain.setValueAtTime(0.1, now);
      gain.gain.linearRampToValueAtTime(0.001, now + 0.25);
      osc.start(now);
      osc.stop(now + 0.25);
    } else if (type === 'wrong') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(180, now);
      osc.frequency.linearRampToValueAtTime(110, now + 0.18);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.linearRampToValueAtTime(0.001, now + 0.18);
      osc.start(now);
      osc.stop(now + 0.18);
    } else if (type === 'launch') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.15);
      gain.gain.setValueAtTime(0.1, now);
      gain.gain.linearRampToValueAtTime(0.001, now + 0.18);
      osc.start(now);
      osc.stop(now + 0.18);
    }
  } catch (e) {}
}

// ==========================================================================
// 2. Toast Notification System
// ==========================================================================
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast-item toast-${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${type === 'success' ? '✓' : type === 'fav' ? '⭐' : 'ℹ️'}</span>
    <span class="toast-msg">${message}</span>
  `;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('fade-out');
    setTimeout(() => toast.remove(), 350);
  }, 2600);
}

// ==========================================================================
// 3. Persistent Favorites System (localStorage)
// ==========================================================================
function getFavorites() {
  try {
    const raw = localStorage.getItem('tekken8_favorites');
    if (raw) return JSON.parse(raw);
  } catch (e) {}
  return { fighters: [], moves: [], combos: [] };
}

function saveFavorites(favs) {
  localStorage.setItem('tekken8_favorites', JSON.stringify(favs));
  updateFavoritesBadges();
}

function updateFavoritesBadges() {
  const favs = getFavorites();
  const total = (favs.fighters?.length || 0) + (favs.moves?.length || 0) + (favs.combos?.length || 0);
  const badge1 = document.getElementById('navFavBadge');
  const badge2 = document.getElementById('favCountPill');
  if (badge1) badge1.textContent = total;
  if (badge2) badge2.textContent = total;
  const countF = document.getElementById('favCountFighters');
  const countM = document.getElementById('favCountMoves');
  const countC = document.getElementById('favCountCombos');
  if (countF) countF.textContent = favs.fighters?.length || 0;
  if (countM) countM.textContent = favs.moves?.length || 0;
  if (countC) countC.textContent = favs.combos?.length || 0;
}

function toggleCharacterFavorite(slug) {
  if (!slug) return;
  const favs = getFavorites();
  const idx = favs.fighters.indexOf(slug);
  const char = state.characters.find(c => c.slug === slug);
  const name = char ? char.name : slug;
  if (idx > -1) {
    favs.fighters.splice(idx, 1);
    showToast(`Removed ${name} from favorites`, 'info');
  } else {
    favs.fighters.push(slug);
    showToast(`Added ${name} to favorites!`, 'fav');
    playSfx('correct');
  }
  saveFavorites(favs);
  renderRosterGrid();
  renderCarousel();
  updateProfileFavState(slug);
}

function toggleMoveFavorite(moveCommand, moveName) {
  const favs = getFavorites();
  const key = `${state.selectedCharacter?.slug || 'unknown'}__${moveCommand}`;
  const existing = favs.moves.findIndex(m => m.key === key);
  if (existing > -1) {
    favs.moves.splice(existing, 1);
    showToast(`Removed move from favorites`, 'info');
  } else {
    favs.moves.push({
      key,
      charSlug: state.selectedCharacter?.slug || 'jin',
      charName: state.selectedCharacter?.name || 'Jin',
      command: moveCommand,
      name: moveName || moveCommand
    });
    showToast(`Starred move ${moveCommand}!`, 'fav');
    playSfx('correct');
  }
  saveFavorites(favs);
}

function toggleComboFavorite(comboId, comboTitle, notation) {
  const favs = getFavorites();
  const existing = favs.combos.findIndex(c => c.id === comboId);
  if (existing > -1) {
    favs.combos.splice(existing, 1);
    showToast(`Removed combo from favorites`, 'info');
  } else {
    favs.combos.push({
      id: comboId,
      charSlug: state.selectedCharacter?.slug || 'jin',
      charName: state.selectedCharacter?.name || 'Jin',
      title: comboTitle || 'Combo Route',
      notation: notation || ''
    });
    showToast(`Starred combo!`, 'fav');
    playSfx('correct');
  }
  saveFavorites(favs);
  renderComboLab();
}

function openFavoritesModal() {
  playSfx('click');
  const modal = document.getElementById('favoritesModal');
  if (!modal) return;
  renderFavoritesModal();
  modal.style.display = 'flex';
}

function closeFavoritesModal() {
  playSfx('click');
  const modal = document.getElementById('favoritesModal');
  if (modal) modal.style.display = 'none';
}

function renderFavoritesModal() {
  const favs = getFavorites();
  updateFavoritesBadges();

  document.querySelectorAll('.fav-tab-btn').forEach(btn => {
    btn.onclick = (e) => {
      document.querySelectorAll('.fav-tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.fav-tab-panel').forEach(p => p.classList.remove('active'));
      e.target.classList.add('active');
      const target = document.getElementById(e.target.dataset.favtab);
      if (target) target.classList.add('active');
      playSfx('click');
    };
  });

  const fList = document.getElementById('favFightersList');
  const fEmpty = document.getElementById('favFightersEmpty');
  if (fList && fEmpty) {
    if (favs.fighters.length === 0) {
      fList.innerHTML = '';
      fEmpty.style.display = 'block';
    } else {
      fEmpty.style.display = 'none';
      fList.innerHTML = favs.fighters.map(slug => {
        const char = state.characters.find(c => c.slug === slug);
        const name = char ? char.name : slug;
        const avatar = char ? char.avatar_url : '/assets/avatars/jin-brand-256-C1-oe_x3.webp';
        return `
          <div class="fav-item-chip fighter" onclick="selectCharacter('${slug}'); closeFavoritesModal();">
            <img src="${avatar}" alt="${name}" class="fav-avatar-mini">
            <span class="fav-name">${name}</span>
            <button type="button" class="btn-fav-remove" onclick="event.stopPropagation(); toggleCharacterFavorite('${slug}'); renderFavoritesModal();">&times;</button>
          </div>
        `;
      }).join('');
    }
  }

  const mList = document.getElementById('favMovesList');
  const mEmpty = document.getElementById('favMovesEmpty');
  if (mList && mEmpty) {
    if (favs.moves.length === 0) {
      mList.innerHTML = '';
      mEmpty.style.display = 'block';
    } else {
      mEmpty.style.display = 'none';
      mList.innerHTML = favs.moves.map(m => `
        <div class="fav-item-chip move">
          <div class="fav-move-meta">
            <span class="fav-char-tag">${m.charName}</span>
            <span class="fav-cmd">${m.command}</span>
            <span class="fav-title">${m.name}</span>
          </div>
          <button type="button" class="btn-fav-remove" onclick="toggleMoveFavorite('${m.command}', '${m.name}'); renderFavoritesModal();">&times;</button>
        </div>
      `).join('');
    }
  }

  const cList = document.getElementById('favCombosList');
  const cEmpty = document.getElementById('favCombosEmpty');
  if (cList && cEmpty) {
    if (favs.combos.length === 0) {
      cList.innerHTML = '';
      cEmpty.style.display = 'block';
    } else {
      cEmpty.style.display = 'none';
      cList.innerHTML = favs.combos.map(c => `
        <div class="fav-item-chip combo">
          <div class="fav-combo-meta">
            <span class="fav-char-tag">${c.charName}</span>
            <span class="fav-title">${c.title}</span>
            <div class="fav-notation">${formatTekkenNotation(c.notation)}</div>
          </div>
          <button type="button" class="btn-fav-remove" onclick="toggleComboFavorite('${c.id}'); renderFavoritesModal();">&times;</button>
        </div>
      `).join('');
    }
  }
}

function clearAllFavorites() {
  playSfx('click');
  saveFavorites({ fighters: [], moves: [], combos: [] });
  renderFavoritesModal();
  renderRosterGrid();
  renderCarousel();
  showToast('All saved favorites cleared', 'info');
}

// ==========================================================================
// 4. Hero Combat Triad Launchpad (Phase 12)
// ==========================================================================
function populateHeroCombatTriad() {
  const pSelect = document.getElementById('heroPlayerSelect');
  const oSelect = document.getElementById('heroOpponentSelect');
  const sSelect = document.getElementById('heroStageSelect');
  if (!pSelect || !oSelect || !state.characters || state.characters.length === 0) return;

  const chars = [...state.characters].sort((a,b) => a.name.localeCompare(b.name));
  const charOpts = chars.map(c => `<option value="${c.slug}">${c.name}</option>`).join('');
  pSelect.innerHTML = charOpts;
  oSelect.innerHTML = charOpts;

  pSelect.value = state.characters.find(c => c.slug === 'jin') ? 'jin' : chars[0].slug;
  oSelect.value = state.characters.find(c => c.slug === 'kazuya') ? 'kazuya' : (chars[1] ? chars[1].slug : chars[0].slug);

  if (sSelect && state.stages && state.stages.length > 0) {
    sSelect.innerHTML = state.stages.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
    sSelect.value = state.stages[0].id;
  }

  pSelect.addEventListener('change', () => {
    const c = state.characters.find(x => x.slug === pSelect.value);
    const img = document.getElementById('heroPlayerAvatar');
    if (img && c) img.src = c.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp';
    playSfx('click');
  });

  oSelect.addEventListener('change', () => {
    const c = state.characters.find(x => x.slug === oSelect.value);
    const img = document.getElementById('heroOpponentAvatar');
    if (img && c) img.src = c.avatar_url || '/assets/avatars/kazuya-brand-256-BInk9tTm.webp';
    playSfx('click');
  });

  if (sSelect) {
    sSelect.addEventListener('change', () => {
      const stg = state.stages.find(x => String(x.id) === String(sSelect.value));
      const thumb = document.getElementById('heroStageThumb');
      if (thumb && stg) thumb.src = stg.image_url || stg.image || '/assets/img/stages/arena.jpg';
      playSfx('click');
      setGlobalStage(sSelect.value);
    });
  }
}

function launchFromHero(targetSection) {
  playSfx('launch');
  const pSelect = document.getElementById('heroPlayerSelect');
  const oSelect = document.getElementById('heroOpponentSelect');
  const sSelect = document.getElementById('heroStageSelect');
  if (!pSelect || !oSelect) return;

  const pSlug = pSelect.value;
  const oSlug = oSelect.value;
  const sId = sSelect ? parseInt(sSelect.value) : 1;

  const pMain = document.getElementById('playerSelect');
  const oMain = document.getElementById('opponentSelect');
  const sMain = document.getElementById('stageSelect');
  if (pMain) pMain.value = pSlug;
  if (oMain) oMain.value = oSlug;
  if (sMain) sMain.value = sId;

  const pChar = state.characters.find(c => c.slug === pSlug);
  const oChar = state.characters.find(c => c.slug === oSlug);
  if (pChar) {
    state.matchup.player = pChar;
    selectCharacter(pChar.slug);
  }
  if (oChar) state.matchup.opponent = oChar;
  state.matchup.stage = state.stages.find(s => s.id === sId) || state.stages[0];

  if (targetSection === 'analyzer') {
    const el = document.getElementById('analyzer');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
    runMatchupAnalysis();
    showToast(`Launching Matchup Lab: ${pChar?.name} vs ${oChar?.name}`, 'info');
  } else if (targetSection === 'combo-lab') {
    const el = document.getElementById('combo-lab');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
    loadComboLabForFighter(pSlug);
    showToast(`Combo Lab: Loaded routes for ${pChar?.name}`, 'info');
  } else if (targetSection === 'punish-assistant') {
    const el = document.getElementById('punish-assistant');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
    loadPunishmentMatrix(pChar?.id || 1, oChar?.id || 2);
    showToast(`Punish Trainer: Ready to punish ${oChar?.name}`, 'info');
  }
}

// ==========================================================================
// 5. Dedicated Ultimate Combo Lab & Advanced P1/P2 Combo Finder (Phase 3)
// ==========================================================================

function initComboLab() {
  const fSelect = document.getElementById('comboLabFighterSelect');
  const oSelect = document.getElementById('comboLabOpponentSelect');
  const sSelect = document.getElementById('comboLabStageSelect');
  if (!fSelect || !state.characters || state.characters.length === 0) return;

  const chars = [...state.characters].sort((a,b) => a.name.localeCompare(b.name));
  fSelect.innerHTML = chars.map(c => `<option value="${c.slug}">${c.name}</option>`).join('');
  if (oSelect) oSelect.innerHTML = chars.map(c => `<option value="${c.slug}">${c.name}</option>`).join('');
  if (sSelect && state.stages && state.stages.length > 0) {
    sSelect.innerHTML = state.stages.map(s => {
      const shape = s.boundary_shape || (s.has_walls ? 'Walled' : 'Infinite');
      return `<option value="${s.id}">${s.name} (${shape})</option>`;
    }).join('');
  }

  // Setup category pills listener
  document.querySelectorAll('#comboLabCategoryPills .combo-cat-pill').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('#comboLabCategoryPills .combo-cat-pill').forEach(b => b.classList.remove('active'));
      const target = e.currentTarget || e.target;
      target.classList.add('active');
      state.comboFinder.category = target.dataset.cat || 'ALL';
      playSfx('click');
      renderComboLab();
    });
  });

  // Resolve initial fighters
  const p1Initial = state.selectedCharacter?.slug || state.matchup?.player?.slug || (chars[0] ? chars[0].slug : 'jin');
  let p2Initial = state.matchup?.opponent?.slug || 'kazuya';
  if (p1Initial === p2Initial) {
    const altChar = chars.find(c => c.slug !== p1Initial);
    p2Initial = altChar ? altChar.slug : 'kazuya';
  }

  state.comboFinder.p1Slug = p1Initial;
  state.comboFinder.p2Slug = p2Initial;
  fSelect.value = p1Initial;
  if (oSelect) oSelect.value = p2Initial;

  const initialStage = state.stages && state.stages.length > 0 ? state.stages[0].id : 1;
  state.comboFinder.stageId = initialStage;
  if (sSelect) sSelect.value = initialStage;

  // Update initial stage hazard thumbnail
  onComboLabStageChange(initialStage);

  // Load both fighters independently
  Promise.all([
    loadComboFinderFighter('p1'),
    loadComboFinderFighter('p2')
  ]).then(() => {
    renderComboLab();
  });
}

async function loadComboFinderFighter(playerKey) {
  const isP1 = playerKey === 'p1';
  const slug = isP1 ? (state.comboFinder.p1Slug || 'jin') : (state.comboFinder.p2Slug || 'kazuya');
  const rivalSlug = isP1 ? (state.comboFinder.p2Slug || 'kazuya') : (state.comboFinder.p1Slug || 'jin');
  const char = state.characters?.find(c => c.slug === slug);
  if (!char) return;

  const avatarEl = document.getElementById(isP1 ? 'comboLabFighterAvatar' : 'comboLabOpponentAvatar');
  if (avatarEl) {
    avatarEl.src = char.avatar_url || (isP1 ? '/assets/avatars/jin-brand-256-C1-oe_x3.webp' : '/assets/avatars/kazuya-brand-256-BInk9tTm.webp');
  }

  const badgeEl = document.getElementById(isP1 ? 'comboLabP1HurtboxBadge' : 'comboLabHurtboxBadge');
  if (badgeEl) {
    const hb = getCharacterHurtboxProfile(slug);
    badgeEl.textContent = hb.label;
    badgeEl.className = `cl-hurtbox-badge ${hb.type.toLowerCase()}`;
  }

  const nameEl = document.getElementById(isP1 ? 'comboPerspP1Name' : 'comboPerspP2Name');
  if (nameEl) nameEl.textContent = char.name;

  const selectEl = document.getElementById(isP1 ? 'comboLabFighterSelect' : 'comboLabOpponentSelect');
  if (selectEl) selectEl.value = slug;

  const stageId = state.comboFinder.stageId || 1;
  let rawCombos = [];
  let recReport = null;

  try {
    const [combosRes, reportRes] = await Promise.all([
      fetchAPI(`/combos?character_slug=${encodeURIComponent(slug)}`),
      fetchAPI(`/combos/recommendations?player_slug=${encodeURIComponent(slug)}&opponent_slug=${encodeURIComponent(rivalSlug)}&stage_id=${stageId}`)
    ]);
    if (Array.isArray(combosRes)) rawCombos = combosRes;
    if (reportRes && typeof reportRes === 'object') recReport = reportRes;
  } catch (err) {
    console.warn(`Error loading combos for ${playerKey} (${slug}):`, err);
  }

  if (isP1) {
    state.comboFinder.p1Report = recReport;
    state.combosPhase5.recommendations = recReport;
  } else {
    state.comboFinder.p2Report = recReport;
  }

  const comboMap = new Map();
  const categories = [
    'beginner_friendly', 'standard_launch', 'high_damage_optimal',
    'wall_carry', 'wall_combo', 'heat_dependent', 'counter_hit',
    'character_specific', 'stage_break', 'alternative_routes'
  ];

  if (recReport) {
    categories.forEach(cat => {
      (recReport[cat] || []).forEach(c => {
        if (!comboMap.has(c.id)) {
          comboMap.set(c.id, {
            ...c,
            character_name: char.name,
            character_slug: slug,
            player_key: isP1 ? 'p1' : 'p2',
            category: cat,
            damage: c.total_damage || c.damage || 65,
            raw_damage_sum: c.raw_damage_sum || c.damage || 65,
            hits: c.hit_count || c.hits || 7,
            notation_sequence: c.notation_sequence || c.notation || '',
            starter_move: c.starter_move_input || c.starter_move || 'df+2',
            launcher_type: c.launcher_type || (c.requires_counter_hit ? 'COUNTER_HIT' : 'NORMAL_HIT'),
            requires_ch: Boolean(c.requires_counter_hit || c.requires_ch),
            requires_heat: Boolean(c.uses_heat || c.requires_heat),
            uses_wall: Boolean(c.uses_wall),
            uses_tornado: Boolean(c.uses_tornado),
            is_stage_dependent: Boolean(c.is_stage_dependent),
            difficulty: c.difficulty || 3,
            verification_status: c.verification_status || 'VERIFIED',
            patch_version: c.patch_version || '3.00.02',
            source: c.source || 'Tekken 8 Practice Lab / wavu.wiki',
            scaling_breakdown: c.scaling_breakdown || [],
            is_stage_compatible: c.is_stage_compatible !== undefined ? c.is_stage_compatible : true,
            stage_compatibility_status: c.stage_compatibility_status || 'SUPPORTED',
            stage_incompatibility_reason: c.stage_incompatibility_reason || null,
            alternative_route_id: c.alternative_route_id || null,
            alternative_route_title: c.alternative_route_title || null,
            alternative_route_notation: c.alternative_route_notation || null,
            alternative_route_damage: c.alternative_route_damage || null
          });
        }
      });
    });
  }

  const currentStageObj = state.stages?.find(s => String(s.id) === String(stageId));

  rawCombos.forEach(c => {
    if (!comboMap.has(c.id)) {
      let autoCat = 'standard_launch';
      if (c.difficulty === 1 || c.difficulty === 'EASY' || c.difficulty <= 2) autoCat = 'beginner_friendly';
      else if (c.difficulty === 5 || c.difficulty === 'OPTIMAL' || c.damage >= 70) autoCat = 'high_damage_optimal';
      else if (c.uses_wall || c.combo_type === 'WALL_CARRY') autoCat = 'wall_carry';
      else if (c.combo_type === 'WALL_COMBO') autoCat = 'wall_combo';
      else if (c.requires_heat) autoCat = 'heat_dependent';
      else if (c.requires_ch) autoCat = 'counter_hit';
      else if (c.is_stage_dependent || ['WALL_BREAK','FLOOR_BREAK','BALCONY_BREAK'].includes(c.combo_type)) autoCat = 'stage_break';

      let isStageComp = true;
      let stageStatus = 'SUPPORTED';
      let stageReason = null;
      let altRouteId = null;
      let altRouteTitle = null;
      let altRouteNotation = null;
      let altRouteDamage = null;

      if (currentStageObj) {
        const ctype = (c.combo_type || '').toUpperCase();
        const cnotes = (c.conditions_notes || '').toLowerCase();
        const reasons = [];

        if (!currentStageObj.has_walls && (c.uses_wall || ctype === 'WALL_COMBO' || ctype === 'WALL_CARRY')) {
          reasons.push(`Perimeter walls are absent on '${currentStageObj.name}' (Infinite Arena). Wall splats and enders cannot be executed.`);
        }
        if ((ctype === 'WALL_BREAK' || cnotes.includes('wall-break')) && !currentStageObj.wall_break && !currentStageObj.wall_blast) {
          reasons.push(`Wall Break hazard is unavailable on '${currentStageObj.name}'.`);
        }
        if ((ctype === 'FLOOR_BREAK' || cnotes.includes('floor-break')) && !currentStageObj.floor_break && !currentStageObj.floor_blast) {
          reasons.push(`Floor Break hazard is unavailable on '${currentStageObj.name}'.`);
        }
        if ((ctype === 'BALCONY_BREAK' || cnotes.includes('balcony-break')) && !currentStageObj.balcony_break) {
          reasons.push(`Balcony Break hazard is unavailable on '${currentStageObj.name}'.`);
        }
        if (c.is_stage_dependent && c.stage_id && c.stage_id !== currentStageObj.id) {
          reasons.push(`Route is calibrated for a specific arena (Stage ID ${c.stage_id}) and cannot connect on '${currentStageObj.name}'.`);
        }

        if (reasons.length > 0) {
          isStageComp = false;
          stageStatus = 'UNAVAILABLE_ON_STAGE';
          stageReason = reasons.join(' | ');

          const alt = rawCombos.find(ac => {
            if (ac.id === c.id) return false;
            if (!currentStageObj.has_walls && (ac.uses_wall || ac.combo_type === 'WALL_COMBO' || ac.combo_type === 'WALL_CARRY')) return false;
            if (ac.is_stage_dependent && ac.stage_id && ac.stage_id !== currentStageObj.id) return false;
            return ac.combo_type === 'MIDSCREEN' || !ac.uses_wall;
          });
          if (alt) {
            stageStatus = 'ALTERNATIVE_AVAILABLE';
            altRouteId = alt.id;
            altRouteTitle = alt.title || 'Midscreen Route';
            altRouteNotation = alt.notation_sequence || alt.notation || '';
            altRouteDamage = alt.damage || 65;
          }
        }
      }

      comboMap.set(c.id, {
        ...c,
        character_name: char.name,
        character_slug: slug,
        player_key: isP1 ? 'p1' : 'p2',
        category: autoCat,
        damage: c.damage || 65,
        raw_damage_sum: c.raw_damage_sum || c.damage || 65,
        hits: c.hits || 7,
        notation_sequence: c.notation_sequence || c.notation || '',
        starter_move: c.starter_move || 'df+2',
        launcher_type: c.launcher_type || (c.requires_ch ? 'COUNTER_HIT' : 'NORMAL_HIT'),
        requires_ch: Boolean(c.requires_ch),
        requires_heat: Boolean(c.requires_heat),
        uses_wall: Boolean(c.uses_wall),
        uses_tornado: Boolean(c.uses_tornado),
        is_stage_dependent: Boolean(c.is_stage_dependent),
        difficulty: c.difficulty || 3,
        verification_status: c.verification_status || 'VERIFIED',
        patch_version: c.patch_version || '3.00.02',
        source: c.source || 'Tekken 8 Practice Lab / wavu.wiki',
        scaling_breakdown: c.scaling_breakdown || [],
        is_stage_compatible: isStageComp,
        stage_compatibility_status: stageStatus,
        stage_incompatibility_reason: stageReason,
        alternative_route_id: altRouteId,
        alternative_route_title: altRouteTitle,
        alternative_route_notation: altRouteNotation,
        alternative_route_damage: altRouteDamage
      });
    }
  });

  const list = Array.from(comboMap.values());
  if (isP1) {
    state.comboFinder.p1Combos = list;
    const countEl = document.getElementById('comboPerspP1Count');
    if (countEl) countEl.textContent = list.length;
  } else {
    state.comboFinder.p2Combos = list;
    const countEl = document.getElementById('comboPerspP2Count');
    if (countEl) countEl.textContent = list.length;
  }
}

// Backward-compatible loader for external callers
async function loadComboLabForFighter(slug) {
  if (state.comboFinder) {
    state.comboFinder.p1Slug = slug;
    const fSelect = document.getElementById('comboLabFighterSelect');
    if (fSelect) fSelect.value = slug;
    await loadComboFinderFighter('p1');
    renderComboLab();
  }
}

function setComboPerspective(persp) {
  playSfx('click');
  state.comboFinder.perspective = persp;

  const btnP1 = document.getElementById('btnComboPerspP1');
  const btnP2 = document.getElementById('btnComboPerspP2');
  const btnDual = document.getElementById('btnComboPerspDual');

  if (btnP1) {
    btnP1.classList.toggle('active', persp === 'P1');
    btnP1.classList.toggle('p1-active', persp === 'P1');
  }
  if (btnP2) {
    btnP2.classList.toggle('active', persp === 'P2');
    btnP2.classList.toggle('p2-active', persp === 'P2');
  }
  if (btnDual) {
    btnDual.classList.toggle('active', persp === 'DUAL');
  }

  renderComboLab();
}

function swapComboLabFighters() {
  playSfx('click');
  const oldP1Slug = state.comboFinder.p1Slug;
  const oldP2Slug = state.comboFinder.p2Slug;

  state.comboFinder.p1Slug = oldP2Slug;
  state.comboFinder.p2Slug = oldP1Slug;

  const tmpCombos = state.comboFinder.p1Combos;
  state.comboFinder.p1Combos = state.comboFinder.p2Combos.map(c => ({ ...c, player_key: 'p1' }));
  state.comboFinder.p2Combos = tmpCombos.map(c => ({ ...c, player_key: 'p2' }));

  const tmpReport = state.comboFinder.p1Report;
  state.comboFinder.p1Report = state.comboFinder.p2Report;
  state.comboFinder.p2Report = tmpReport;

  const p1Char = state.characters?.find(c => c.slug === state.comboFinder.p1Slug);
  const p2Char = state.characters?.find(c => c.slug === state.comboFinder.p2Slug);

  const fSelect = document.getElementById('comboLabFighterSelect');
  const oSelect = document.getElementById('comboLabOpponentSelect');
  if (fSelect) fSelect.value = state.comboFinder.p1Slug;
  if (oSelect) oSelect.value = state.comboFinder.p2Slug;

  const p1Avatar = document.getElementById('comboLabFighterAvatar');
  const p2Avatar = document.getElementById('comboLabOpponentAvatar');
  if (p1Avatar && p1Char) p1Avatar.src = p1Char.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp';
  if (p2Avatar && p2Char) p2Avatar.src = p2Char.avatar_url || '/assets/avatars/kazuya-brand-256-BInk9tTm.webp';

  const p1Badge = document.getElementById('comboLabP1HurtboxBadge');
  const p2Badge = document.getElementById('comboLabHurtboxBadge');
  if (p1Badge) {
    const hb = getCharacterHurtboxProfile(state.comboFinder.p1Slug);
    p1Badge.textContent = hb.label;
    p1Badge.className = `cl-hurtbox-badge ${hb.type.toLowerCase()}`;
  }
  if (p2Badge) {
    const hb = getCharacterHurtboxProfile(state.comboFinder.p2Slug);
    p2Badge.textContent = hb.label;
    p2Badge.className = `cl-hurtbox-badge ${hb.type.toLowerCase()}`;
  }

  const p1NameSpan = document.getElementById('comboPerspP1Name');
  const p2NameSpan = document.getElementById('comboPerspP2Name');
  if (p1NameSpan && p1Char) p1NameSpan.textContent = p1Char.name;
  if (p2NameSpan && p2Char) p2NameSpan.textContent = p2Char.name;

  const p1Count = document.getElementById('comboPerspP1Count');
  const p2Count = document.getElementById('comboPerspP2Count');
  if (p1Count) p1Count.textContent = state.comboFinder.p1Combos.length;
  if (p2Count) p2Count.textContent = state.comboFinder.p2Combos.length;

  // Cross-synchronize with Matchup Lab
  const pSelect = document.getElementById('playerSelect');
  const labOpponentSelect = document.getElementById('opponentSelect');
  if (pSelect && p1Char && String(pSelect.value) !== String(p1Char.id)) pSelect.value = p1Char.id;
  if (labOpponentSelect && p2Char && String(labOpponentSelect.value) !== String(p2Char.id)) labOpponentSelect.value = p2Char.id;
  if (typeof updatePlayerPreview === 'function') updatePlayerPreview();
  if (typeof updateOpponentPreview === 'function') updateOpponentPreview();
  if (typeof runMatchupAnalysis === 'function') runMatchupAnalysis();

  showToast(`⇄ Fighters Swapped: P1 is now ${p1Char?.name || 'P1'}, P2 is now ${p2Char?.name || 'P2'}`, 'info');
  renderComboLab();
}

function onComboLabFighterChange(slug) {
  playSfx('click');
  state.comboFinder.p1Slug = slug;
  const char = state.characters?.find(c => c.slug === slug);
  const pSelect = document.getElementById('playerSelect');
  if (pSelect && char && String(pSelect.value) !== String(char.id)) {
    pSelect.value = char.id;
    if (typeof updatePlayerPreview === 'function') updatePlayerPreview();
    if (typeof runMatchupAnalysis === 'function') runMatchupAnalysis();
  }
  loadComboFinderFighter('p1').then(() => {
    renderComboLab();
  });
}

function onComboLabOpponentChange(slug) {
  playSfx('click');
  state.comboFinder.p2Slug = slug;
  const char = state.characters?.find(c => c.slug === slug);
  const oSelect = document.getElementById('opponentSelect');
  if (oSelect && char && String(oSelect.value) !== String(char.id)) {
    oSelect.value = char.id;
    if (typeof updateOpponentPreview === 'function') updateOpponentPreview();
    if (typeof runMatchupAnalysis === 'function') runMatchupAnalysis();
  }
  loadComboFinderFighter('p2').then(() => {
    renderComboLab();
  });
}


function onComboLabStageChange(stageId) {
  playSfx('click');
  setGlobalStage(stageId);
}

function filterCombos(list) {
  if (!Array.isArray(list)) return [];
  const activeCat = state.comboFinder.category || 'ALL';
  const starterFilter = document.getElementById('comboLabStarterTypeFilter')?.value || 'ALL';
  const diffFilter = document.getElementById('comboLabDifficultyFilter')?.value || 'ALL';
  const wallFilter = document.getElementById('comboLabWallFilter')?.value || 'ALL';
  const stanceFilter = document.getElementById('comboLabStanceFilter')?.value || 'ALL';
  const minDmg = parseInt(document.getElementById('comboLabMinDamage')?.value) || null;
  const maxDmg = parseInt(document.getElementById('comboLabMaxDamage')?.value) || null;
  const searchQ = (document.getElementById('comboLabSearchInput')?.value || '').toLowerCase().trim();

  return list.filter(c => {
    // 1. Category Filter
    if (activeCat !== 'ALL') {
      if (activeCat === 'beginner_friendly') {
        const isEasy = c.difficulty === 1 || c.difficulty === 2 || String(c.difficulty).toUpperCase() === 'EASY' || c.category === 'beginner_friendly';
        if (!isEasy) return false;
      } else if (activeCat === 'standard_launch') {
        const isStandard = c.category === 'standard_launch' || c.launcher_type === 'LAUNCHER' || c.combo_type === 'MIDSCREEN' || (c.title && c.title.toLowerCase().includes('standard'));
        if (!isStandard) return false;
      } else if (activeCat === 'high_damage_optimal') {
        const isOpt = c.category === 'high_damage_optimal' || c.difficulty === 5 || c.difficulty === 4 || String(c.difficulty).toUpperCase() === 'OPTIMAL' || (c.damage >= 70);
        if (!isOpt) return false;
      } else if (activeCat === 'wall_carry') {
        const isCarry = c.category === 'wall_carry' || c.uses_wall || c.combo_type === 'WALL_CARRY';
        if (!isCarry) return false;
      } else if (activeCat === 'wall_combo') {
        const isWall = c.category === 'wall_combo' || c.combo_type === 'WALL_COMBO' || (c.uses_wall && (c.title && c.title.toLowerCase().includes('wall')));
        if (!isWall) return false;
      } else if (activeCat === 'heat_dependent') {
        if (!c.requires_heat && c.category !== 'heat_dependent') return false;
      } else if (activeCat === 'counter_hit') {
        if (!c.requires_ch && c.launcher_type !== 'COUNTER_HIT' && c.category !== 'counter_hit') return false;
      } else if (activeCat === 'stage_break') {
        const isBreak = c.category === 'stage_break' || ['WALL_BREAK','FLOOR_BREAK','BALCONY_BREAK'].includes(c.combo_type) || c.is_stage_dependent;
        if (!isBreak) return false;
      } else if (activeCat === 'character_specific') {
        const isCharSpec = c.category === 'character_specific' || (c.target_hurtbox_class && c.target_hurtbox_class !== 'UNIVERSAL');
        if (!isCharSpec) return false;
      } else if (activeCat === 'alternative_routes') {
        const isAlt = c.category === 'alternative_routes' || Boolean(c.easier_alternative_notes || c.easier_alternative_id);
        if (!isAlt) return false;
      } else if (c.category !== activeCat) {
        return false;
      }
    }

    // 2. Starter Type Filter
    if (starterFilter === 'NORMAL_HIT') {
      if (c.requires_ch || c.launcher_type === 'COUNTER_HIT') return false;
    } else if (starterFilter === 'COUNTER_HIT') {
      if (!c.requires_ch && c.launcher_type !== 'COUNTER_HIT') return false;
    } else if (starterFilter === 'LAUNCHER') {
      const isL = c.launcher_type === 'LAUNCHER' || c.combo_type === 'MIDSCREEN' || (c.starter_move && (c.starter_move.includes('df+2') || c.starter_move.includes('EWGF') || c.starter_move.includes('uf+4')));
      if (!isL) return false;
    } else if (starterFilter === 'PUNISH') {
      const isP = c.launcher_type === 'PUNISH' || (c.title && c.title.toLowerCase().includes('punish'));
      if (!isP) return false;
    }

    // 3. Difficulty Filter
    if (diffFilter !== 'ALL') {
      const d = String(c.difficulty).toUpperCase();
      if (diffFilter === 'EASY' && !(d === '1' || d === '2' || d === 'EASY')) return false;
      if (diffFilter === 'MEDIUM' && !(d === '3' || d === 'MEDIUM')) return false;
      if (diffFilter === 'HARD' && !(d === '4' || d === 'HARD')) return false;
      if (diffFilter === 'OPTIMAL' && !(d === '5' || d === 'OPTIMAL')) return false;
    }

    // 4. Wall / Environment Filter
    if (wallFilter === 'WALL_CARRY') {
      if (!c.uses_wall && c.combo_type !== 'WALL_CARRY') return false;
    } else if (wallFilter === 'WALL_COMBO') {
      if (c.combo_type !== 'WALL_COMBO' && !(c.uses_wall && c.title && c.title.toLowerCase().includes('wall'))) return false;
    } else if (wallFilter === 'STAGE_BREAK') {
      if (!['WALL_BREAK','FLOOR_BREAK','BALCONY_BREAK'].includes(c.combo_type) && !c.is_stage_dependent) return false;
    }

    // 5. Stance Filter
    if (stanceFilter === 'STANCE_REQUIRED') {
      if (!c.required_stance || c.required_stance === 'NONE' || c.required_stance === '') return false;
    } else if (stanceFilter === 'NONE') {
      if (c.required_stance && c.required_stance !== 'NONE' && c.required_stance !== '') return false;
    }

    // 6. Damage Range Filter
    if (minDmg !== null && c.damage < minDmg) return false;
    if (maxDmg !== null && c.damage > maxDmg) return false;

    // 7. Search Filter
    if (searchQ) {
      const matchTitle = (c.title || '').toLowerCase().includes(searchQ);
      const matchNotation = (c.notation_sequence || c.notation || '').toLowerCase().includes(searchQ);
      const matchStarter = (c.starter_move || '').toLowerCase().includes(searchQ);
      const matchStance = (c.required_stance || '').toLowerCase().includes(searchQ);
      const matchChar = (c.character_name || '').toLowerCase().includes(searchQ);
      if (!matchTitle && !matchNotation && !matchStarter && !matchStance && !matchChar) return false;
    }

    return true;
  });
}

function renderComboCard(c, playerKey) {
  const isP1 = playerKey === 'p1';
  const favs = getFavorites();
  const isFav = favs.combos.some(x => String(x.id) === String(c.id));
  const isComparing = comboCompareList.some(x => String(x.id) === String(c.id));
  const isExpanded = state.comboFinder.expandedSteps.has(c.id);

  const diffOrder = { 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 'EASY': 1, 'MEDIUM': 3, 'HARD': 4, 'OPTIMAL': 5 };
  const numDiff = diffOrder[c.difficulty] || 3;
  const diffStars = '★'.repeat(numDiff) + '☆'.repeat(5 - numDiff);
  const catLabel = (c.category || 'JUGGLE ROUTE').toUpperCase().replace('_', ' ');
  const formattedNotation = formatTekkenNotation(c.notation_sequence || c.starter_move || 'df+2');
  const stage = state.stages?.find(s => String(s.id) === String(state.comboFinder.stageId));

  // Stage hazard mismatch warning & alternative route recommendation
  let stageWarningHtml = '';
  const isStageIncompatible = c.is_stage_compatible === false;
  const stageReason = c.stage_incompatibility_reason || (
    stage && ((c.uses_wall || c.combo_type === 'WALL_COMBO') && (stage.has_walls === false || stage.boundary_shape === 'Infinite'))
      ? `Perimeter walls are absent on ${stage.name} (Infinite Stage). Wall splats and enders cannot be executed.`
      : (c.combo_type === 'WALL_BREAK' && stage && !stage.wall_break && !stage.wall_blast)
        ? `Requires Wall Break hazard, unavailable on ${stage.name}.`
        : (c.combo_type === 'FLOOR_BREAK' && stage && !stage.floor_break && !stage.floor_blast)
          ? `Requires Floor Break hazard, unavailable on ${stage.name}.`
          : (c.combo_type === 'BALCONY_BREAK' && stage && !stage.balcony_break)
            ? `Requires Balcony Break hazard, unavailable on ${stage.name}.`
            : null
  );

  if (isStageIncompatible || stageReason) {
    const hasAlt = Boolean(c.alternative_route_title || c.alternative_route_notation);
    stageWarningHtml = `
      <div class="combo-stage-warning ${hasAlt ? 'has-alt' : ''}">
        <div class="stage-warn-header">
          <span class="stage-warn-icon">⚠️</span>
          <span class="stage-warn-title">Stage Incompatible (${stage ? stage.name : 'Selected Stage'})</span>
        </div>
        <div class="stage-warn-detail">${escapeHtml(stageReason || 'This route cannot connect on the active stage.')}</div>
        ${hasAlt ? `
          <div class="stage-warn-alt">
            <span class="stage-alt-label">Suggested Stage Alternative:</span>
            <div class="stage-alt-card">
              <div class="stage-alt-card-top">
                <span class="stage-alt-title">${escapeHtml(c.alternative_route_title || 'Midscreen Route')}</span>
                ${c.alternative_route_damage ? `<span class="stage-alt-dmg">${c.alternative_route_damage} DMG</span>` : ''}
              </div>
              ${c.alternative_route_notation ? `<code class="stage-alt-not">${formatTekkenNotation(c.alternative_route_notation)}</code>` : ''}
            </div>
          </div>
        ` : ''}
      </div>
    `;
  } else if (stage && (c.combo_type === 'WALL_BREAK' || c.combo_type === 'FLOOR_BREAK' || c.combo_type === 'BALCONY_BREAK')) {
    stageWarningHtml = `
      <div style="margin-bottom:0.4rem;">
        <span class="stage-compat-pill supported">✓ Hazard Available on ${stage.name}</span>
      </div>
    `;
  }

  // Parse combo steps for expandable breakdown
  const rawSeq = c.notation_sequence || '';
  const steps = rawSeq.split(/\s*(?:>|->|=>)\s*/).filter(s => s && s.trim());
  let stepsMarkup = '';
  if (isExpanded && steps.length > 0) {
    stepsMarkup = `
      <div class="combo-steps-wrapper">
        <div style="font-size:0.7rem; font-weight:800; color:var(--text-muted); text-transform:uppercase; margin-bottom:0.25rem;">
          Ordered Combo Route Steps (${steps.length} Steps)
        </div>
        ${steps.map((st, idx) => {
          let role = 'Float / Link';
          if (idx === 0) role = 'Starter / Launcher';
          else if (idx === steps.length - 1) role = 'Combo Ender';
          else if (st.includes('T!') || st.includes('TORNADO') || idx === steps.length - 2) role = 'Tornado Spin';
          return `
            <div class="combo-step-row">
              <span class="combo-step-num">STEP ${idx + 1}</span>
              <span class="combo-step-notation">${formatTekkenNotation(st)}</span>
              <span class="combo-step-role" style="margin-left:auto; font-size:0.65rem; color:var(--accent-gold);">${role}</span>
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  const starterProperty = c.requires_ch ? 'Counter-Hit (CH)' : (c.launcher_type === 'PUNISH' ? 'Punish Starter' : 'Normal Hit');

  return `
    <div class="combo-route-card ${isP1 ? 'p1-card' : 'p2-card'} ${isComparing ? 'comparing' : ''}" id="cl_combo_${c.id}">
      <div class="crc-top-row">
        <div style="display:flex; align-items:center; gap:0.4rem; flex-wrap:wrap;">
          <span class="fighter-meta-chip" style="font-size:0.68rem; font-weight:800; border-color:${isP1 ? 'var(--btn-lp-cyan)' : 'var(--btn-rk-pink)'}; color:${isP1 ? 'var(--btn-lp-cyan)' : 'var(--btn-rk-pink)'};">
            ${isP1 ? '● P1' : '● P2'}: ${c.character_name}
          </span>
          <span class="crc-cat-badge ${c.category || ''}">${catLabel}</span>
          <span class="starter-chip" style="font-size:0.65rem;">${starterProperty}</span>
        </div>
        <div class="crc-top-actions">
          <button type="button" class="btn-combo-action-mini ${isFav ? 'active' : ''}" onclick="toggleComboFavorite('${c.id}', '${(c.title || '').replace(/'/g, "\\'")}', '${(c.notation_sequence || '').replace(/'/g, "\\'")}')" title="Bookmark Combo">
            ${isFav ? '★' : '☆'}
          </button>
          <button type="button" class="btn-combo-action-mini ${isComparing ? 'active' : ''}" onclick="toggleComboCompare('${c.id}')" title="Compare Side-by-Side">
            ⚖️
          </button>
        </div>
      </div>

      <h4 class="crc-title">${c.title || 'Standard Route'}</h4>
      <div class="crc-starter-tag">
        Starter: <strong>${c.starter_move || 'df+2'}</strong>
        ${c.required_stance ? `<span class="starter-chip stance" style="margin-left:0.5rem; font-size:0.65rem; color:#38bdf8;">Stance: ${c.required_stance}</span>` : ''}
      </div>

      <div class="crc-notation-sequence">
        ${formattedNotation}
      </div>

      ${stageWarningHtml}

      ${c.easier_alternative_notes ? `
        <div class="combo-alt-badge">
          💡 <strong>Practical Alternative:</strong> ${c.easier_alternative_notes}
        </div>
      ` : ''}

      ${c.execution_notes ? `
        <div style="font-size:0.75rem; color:#9ca3af; margin-top:0.4rem;">
          ⚙️ <strong>Execution Tip:</strong> ${c.execution_notes}
        </div>
      ` : ''}

      ${stepsMarkup}

      <div class="crc-stats-row">
        <div class="crc-stat-chip damage">
          <span class="crc-stat-val">${c.damage || 65} DMG</span>
          <span class="crc-stat-lbl">VERIFIED SCALED</span>
        </div>
        <div class="crc-stat-chip hits">
          <span class="crc-stat-val">${c.hits || 7}</span>
          <span class="crc-stat-lbl">HITS</span>
        </div>
        <div class="crc-stat-chip difficulty">
          <span class="crc-stat-val stars">${diffStars}</span>
          <span class="crc-stat-lbl">${String(c.difficulty).toUpperCase()}</span>
        </div>
        <div class="crc-stat-chip" style="border: 1px solid rgba(255,255,255,0.1);">
          <span class="crc-stat-val" style="font-size:0.75rem; color:#00e676;">${c.verification_status || 'VERIFIED'}</span>
          <span class="crc-stat-lbl">v${c.patch_version || '3.00.02'}</span>
        </div>
      </div>

      <div class="crc-card-footer">
        <button type="button" class="btn-crc-footer copy" onclick="copyComboToClipboard('${(c.notation_sequence || c.notation || '').replace(/'/g, "\\'")}', this)">
          📋 Copy
        </button>
        <button type="button" class="btn-crc-footer steps-btn" onclick="toggleComboSteps('${c.id}')">
          📑 ${isExpanded ? 'Hide Steps' : 'Steps'}
        </button>
        <button type="button" class="btn-crc-footer breakdown" onclick="openDamageScalingModal('${c.id}')">
          🧪 Scaling
        </button>
        <button type="button" class="btn-crc-footer compare-btn" onclick="toggleComboCompare('${c.id}')">
          ⚖️ Compare
        </button>
      </div>
    </div>
  `;
}

function renderComboLab() {
  const container = document.getElementById('comboLabGrid');
  const dualContainer = document.getElementById('comboLabDualGrid');
  const countPill = document.getElementById('comboLabCountPill');
  const emptyState = document.getElementById('comboLabEmpty');
  if (!container || !dualContainer) return;

  const persp = state.comboFinder.perspective || 'P1';

  // Update Perspective Button Counts
  const p1Filtered = filterCombos(state.comboFinder.p1Combos || []);
  const p2Filtered = filterCombos(state.comboFinder.p2Combos || []);

  const p1CountEl = document.getElementById('comboPerspP1Count');
  const p2CountEl = document.getElementById('comboPerspP2Count');
  if (p1CountEl) p1CountEl.textContent = p1Filtered.length;
  if (p2CountEl) p2CountEl.textContent = p2Filtered.length;

  if (persp === 'DUAL') {
    container.style.display = 'none';
    dualContainer.style.display = 'grid';
    renderComboDualGrid(p1Filtered, p2Filtered);
    if (countPill) countPill.textContent = `${p1Filtered.length + p2Filtered.length} Combos (Dual)`;
    if (emptyState) emptyState.style.display = (p1Filtered.length === 0 && p2Filtered.length === 0) ? 'block' : 'none';
  } else {
    dualContainer.style.display = 'none';
    container.style.display = 'grid';

    const activeList = persp === 'P1' ? p1Filtered : p2Filtered;
    const playerKey = persp.toLowerCase();

    if (countPill) countPill.textContent = `${activeList.length} Combos`;

    if (activeList.length === 0) {
      container.innerHTML = '';
      if (emptyState) emptyState.style.display = 'block';
    } else {
      if (emptyState) emptyState.style.display = 'none';
      container.innerHTML = activeList.map(c => renderComboCard(c, playerKey)).join('');
    }
  }

  renderComboCompareDock();
}

function renderComboDualGrid(p1Filtered, p2Filtered) {
  const dualContainer = document.getElementById('comboLabDualGrid');
  if (!dualContainer) return;

  const p1Char = state.characters?.find(c => c.slug === state.comboFinder.p1Slug);
  const p2Char = state.characters?.find(c => c.slug === state.comboFinder.p2Slug);
  const p1Name = p1Char?.name || 'Player 1';
  const p2Name = p2Char?.name || 'Player 2';

  dualContainer.innerHTML = `
    <div class="combo-dual-column p1-column">
      <div class="combo-dual-col-header p1">
        <div>
          <span style="font-weight:900; color:var(--btn-lp-cyan);">● P1: ${p1Name}</span>
          <span style="font-size:0.75rem; color:var(--text-muted); margin-left:0.5rem;">Verified Juggles</span>
        </div>
        <span class="badge" style="background:rgba(0,229,255,0.15); color:var(--btn-lp-cyan); font-weight:800; font-size:0.75rem; padding:2px 8px; border-radius:4px;">${p1Filtered.length} Routes</span>
      </div>
      <div class="combo-dual-card-list" style="display:flex; flex-direction:column; gap:1rem;">
        ${p1Filtered.length === 0 ? '<div style="color:var(--text-muted); padding:1.5rem; text-align:center; background:rgba(0,0,0,0.3); border-radius:8px;">No matching P1 combo routes for active filters.</div>' : p1Filtered.map(c => renderComboCard(c, 'p1')).join('')}
      </div>
    </div>

    <div class="combo-dual-column p2-column">
      <div class="combo-dual-col-header p2">
        <div>
          <span style="font-weight:900; color:var(--btn-rk-pink);">● P2: ${p2Name}</span>
          <span style="font-size:0.75rem; color:var(--text-muted); margin-left:0.5rem;">Verified Juggles</span>
        </div>
        <span class="badge" style="background:rgba(255,30,56,0.15); color:var(--btn-rk-pink); font-weight:800; font-size:0.75rem; padding:2px 8px; border-radius:4px;">${p2Filtered.length} Routes</span>
      </div>
      <div class="combo-dual-card-list" style="display:flex; flex-direction:column; gap:1rem;">
        ${p2Filtered.length === 0 ? '<div style="color:var(--text-muted); padding:1.5rem; text-align:center; background:rgba(0,0,0,0.3); border-radius:8px;">No matching P2 combo routes for active filters.</div>' : p2Filtered.map(c => renderComboCard(c, 'p2')).join('')}
      </div>
    </div>
  `;
}

function filterComboLabGrid() {
  renderComboLab();
}

function toggleComboSteps(comboId) {
  playSfx('click');
  const idNum = parseInt(comboId) || comboId;
  if (state.comboFinder.expandedSteps.has(idNum)) {
    state.comboFinder.expandedSteps.delete(idNum);
  } else {
    state.comboFinder.expandedSteps.add(idNum);
  }
  renderComboLab();
}

let comboCompareList = [];

function toggleComboCompare(comboId) {
  playSfx('click');
  const idStr = String(comboId);

  // Find combo across P1 and P2 lists
  const allCombos = [...(state.comboFinder.p1Combos || []), ...(state.comboFinder.p2Combos || [])];
  const found = allCombos.find(c => String(c.id) === idStr);
  if (!found) return;

  const idx = comboCompareList.findIndex(c => String(c.id) === idStr);
  if (idx > -1) {
    comboCompareList.splice(idx, 1);
    showToast(`Removed from comparison dock`, 'info');
  } else {
    if (comboCompareList.length >= 2) {
      comboCompareList.shift();
    }
    comboCompareList.push(found);
    showToast(`Added ${found.character_name} combo to benchmark comparison dock!`, 'info');
  }
  renderComboCompareDock();
  renderComboLab();
}

function clearComboComparison() {
  playSfx('click');
  comboCompareList = [];
  renderComboCompareDock();
  renderComboLab();
}

function renderComboCompareDock() {
  const dock = document.getElementById('comboLabCompareDock');
  const body = document.getElementById('comboCompareBody');
  if (!dock || !body) return;

  if (comboCompareList.length === 0) {
    dock.style.display = 'none';
    return;
  }

  dock.style.display = 'block';

  let benchmarkHeader = '';
  if (comboCompareList.length === 2) {
    const c1 = comboCompareList[0];
    const c2 = comboCompareList[1];
    const dmg1 = c1.damage || 65;
    const dmg2 = c2.damage || 65;
    const hits1 = c1.hits || 7;
    const hits2 = c2.hits || 7;
    const dmgDiff = dmg1 - dmg2;
    const hitDiff = hits1 - hits2;
    const dph1 = (dmg1 / Math.max(1, hits1)).toFixed(1);
    const dph2 = (dmg2 / Math.max(1, hits2)).toFixed(1);

    const sameCH = Boolean(c1.requires_ch) === Boolean(c2.requires_ch);
    const sameWall = Boolean(c1.uses_wall) === Boolean(c2.uses_wall);
    const isComparable = sameCH && sameWall;

    benchmarkHeader = `
      <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); border-radius:8px; padding:0.75rem 1rem; margin-bottom:1rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem; flex-wrap:wrap; gap:0.5rem;">
          <span style="font-weight:900; color:var(--accent-gold); font-size:0.85rem; letter-spacing:0.05em; text-transform:uppercase;">
            ⚔️ Analytical Benchmark: ${isComparable ? 'Directly Comparable' : 'Conditional Divergence'}
          </span>
          <span style="font-size:0.75rem; color:var(--text-muted);">
            ${isComparable ? 'Both routes share starter properties and neutral conditions.' : 'Routes differ in starter properties (CH vs NH) or wall reliance.'}
          </span>
        </div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:0.6rem; font-size:0.75rem;">
          <div style="background:rgba(0,0,0,0.3); padding:0.4rem 0.6rem; border-radius:4px;">
            <div style="color:var(--text-muted); font-size:0.65rem;">DAMAGE DELTA</div>
            <div style="font-weight:800; color:${dmgDiff > 0 ? 'var(--btn-lp-cyan)' : (dmgDiff < 0 ? 'var(--btn-rk-pink)' : '#fff')};">
              ${dmgDiff > 0 ? `+${dmgDiff} DMG (${c1.character_name})` : (dmgDiff < 0 ? `+${Math.abs(dmgDiff)} DMG (${c2.character_name})` : 'Equal Damage')}
            </div>
          </div>
          <div style="background:rgba(0,0,0,0.3); padding:0.4rem 0.6rem; border-radius:4px;">
            <div style="color:var(--text-muted); font-size:0.65rem;">HIT DELTA</div>
            <div style="font-weight:800; color:#fff;">
              ${hitDiff > 0 ? `+${hitDiff} Hits (${c1.character_name})` : (hitDiff < 0 ? `+${Math.abs(hitDiff)} Hits (${c2.character_name})` : 'Equal Hit Count')}
            </div>
          </div>
          <div style="background:rgba(0,0,0,0.3); padding:0.4rem 0.6rem; border-radius:4px;">
            <div style="color:var(--text-muted); font-size:0.65rem;">DAMAGE EFFICIENCY</div>
            <div style="font-weight:800; color:#38bdf8;">
              ${c1.character_name}: ${dph1} D/H vs ${c2.character_name}: ${dph2} D/H
            </div>
          </div>
        </div>
      </div>
    `;
  }

  body.innerHTML = `
    ${benchmarkHeader}
    <div class="compare-cards-grid">
      ${comboCompareList.map((c, i) => {
        const dmg = c.damage || 65;
        const hits = c.hits || 7;
        const eff = (dmg / Math.max(1, hits)).toFixed(1);
        const isP1 = c.player_key === 'p1';
        return `
          <div class="compare-card card-${i + 1}" style="border-top:3px solid ${isP1 ? 'var(--btn-lp-cyan)' : 'var(--btn-rk-pink)'};">
            <div class="cc-badge" style="color:${isP1 ? 'var(--btn-lp-cyan)' : 'var(--btn-rk-pink)'};">
              ${isP1 ? '● P1' : '● P2'}: ${c.character_name} — ${c.category ? c.category.toUpperCase().replace('_',' ') : 'JUGGLE'}
            </div>
            <h4 class="cc-title">${c.title || 'Standard Route'}</h4>
            <div class="cc-notation">${formatTekkenNotation(c.notation_sequence || c.notation || c.starter_move || 'df+2')}</div>
            <div class="cc-metrics-grid">
              <div class="cc-metric">
                <span class="cc-val">${dmg} DMG</span>
                <span class="cc-lbl">Verified Scaled</span>
              </div>
              <div class="cc-metric">
                <span class="cc-val">${hits} Hits</span>
                <span class="cc-lbl">Hit Count</span>
              </div>
              <div class="cc-metric">
                <span class="cc-val">${eff} D/H</span>
                <span class="cc-lbl">Damage Efficiency</span>
              </div>
              <div class="cc-metric">
                <span class="cc-val">${'★'.repeat(c.difficulty || 3)}</span>
                <span class="cc-lbl">Difficulty</span>
              </div>
            </div>
            <div class="cc-actions">
              <button type="button" class="btn-tb-reset" onclick="openDamageScalingModal('${c.id}')">Breakdown</button>
              <button type="button" class="btn-tb-reset" onclick="toggleComboCompare('${c.id}')">Remove</button>
            </div>
          </div>
        `;
      }).join('')}
      ${comboCompareList.length === 1 ? `
        <div class="compare-card placeholder">
          <div class="cc-placeholder-content">
            <span style="font-size:1.8rem;">⚖️</span>
            <div style="font-weight:700; color:#fff; margin-top:0.5rem;">Select a Second Combo</div>
            <div style="font-size:0.8rem; color:var(--text-muted);">Click "⚖️ Compare" on any combo card (P1 or P2) to benchmark damage efficiency side-by-side.</div>
          </div>
        </div>
      ` : ''}
    </div>
  `;
}

function copyComboToClipboard(notation, btn) {
  playSfx('click');
  navigator.clipboard.writeText(notation).then(() => {
    showToast(`Combo notation copied to clipboard!`, 'success');
    if (btn) {
      const orig = btn.innerHTML;
      btn.innerHTML = '✓ Copied!';
      setTimeout(() => btn.innerHTML = orig, 1800);
    }
  }).catch(() => {
    showToast(`Copied: ${notation}`, 'info');
  });
}

// Window global exports for HTML inline handlers
window.initComboLab = initComboLab;
window.renderComboLab = renderComboLab;
window.loadComboLabForFighter = loadComboLabForFighter;
window.setComboPerspective = setComboPerspective;
window.swapComboLabFighters = swapComboLabFighters;
window.onComboLabFighterChange = onComboLabFighterChange;
window.onComboLabOpponentChange = onComboLabOpponentChange;
window.onComboLabStageChange = onComboLabStageChange;
window.filterComboLabGrid = filterComboLabGrid;
window.resetComboFilters = resetComboFilters;
window.toggleComboSteps = toggleComboSteps;
window.toggleComboCompare = toggleComboCompare;
window.clearComboComparison = clearComboComparison;
window.copyComboToClipboard = copyComboToClipboard;

// ==========================================================================
// 6. Interactive Punishment Reaction Drill Quiz (Phase 7)
// ==========================================================================
const quizState = {
  currentQuestion: null,
  streak: 0,
  score: 0,
  totalAttempts: 0,
  correctAttempts: 0
};

function setPunishViewMode(mode) {
  playSfx('click');
  const btnMatrix = document.getElementById('btnPunishModeMatrix');
  const btnQuiz = document.getElementById('btnPunishModeQuiz');
  const quizCard = document.getElementById('punishQuizContainer');
  const toolbarCard = document.getElementById('punishToolbarCard');
  const tableCard = document.querySelector('.punish-results-card');

  if (btnMatrix && btnQuiz) {
    btnMatrix.classList.toggle('active', mode === 'matrix');
    btnQuiz.classList.toggle('active', mode === 'quiz');
  }

  if (quizCard) quizCard.style.display = mode === 'quiz' ? 'block' : 'none';
  if (toolbarCard) toolbarCard.style.display = mode === 'matrix' ? 'block' : 'none';
  if (tableCard) tableCard.style.display = mode === 'matrix' ? 'block' : 'none';

  if (mode === 'quiz' && !quizState.currentQuestion) {
    generateNextQuizQuestion();
  }
}

function initPunishQuiz() {
  try {
    const saved = localStorage.getItem('tekken8_punish_quiz');
    if (saved) {
      const parsed = JSON.parse(saved);
      quizState.streak = parsed.streak || 0;
      quizState.score = parsed.score || 0;
      quizState.totalAttempts = parsed.totalAttempts || 0;
      quizState.correctAttempts = parsed.correctAttempts || 0;
      updateQuizScoreDisplay();
    }
  } catch (e) {}
}

function updateQuizScoreDisplay() {
  const streakEl = document.getElementById('quizStreakVal');
  const accEl = document.getElementById('quizAccuracyVal');
  const scoreEl = document.getElementById('quizScoreVal');
  if (streakEl) streakEl.textContent = quizState.streak;
  if (scoreEl) scoreEl.textContent = quizState.score;
  if (accEl) {
    const acc = quizState.totalAttempts > 0 ? Math.round((quizState.correctAttempts / quizState.totalAttempts) * 100) : 100;
    accEl.textContent = `${acc}%`;
  }
  try {
    localStorage.setItem('tekken8_punish_quiz', JSON.stringify(quizState));
  } catch (e) {}
}

function resetQuizStats() {
  playSfx('click');
  quizState.streak = 0;
  quizState.score = 0;
  quizState.totalAttempts = 0;
  quizState.correctAttempts = 0;
  updateQuizScoreDisplay();
  showToast('Reaction quiz score reset', 'info');
  generateNextQuizQuestion();
}

function generateNextQuizQuestion() {
  playSfx('click');
  const feedback = document.getElementById('quizFeedbackBanner');
  if (feedback) feedback.style.display = 'none';

  const defender = state.matchup.player || (state.characters && state.characters[0]);
  const attacker = state.matchup.opponent || (state.characters && state.characters[1]) || defender;

  const situations = [
    {
      moveName: "Demon Scissors (df+2)",
      notation: "df+2",
      blockAdv: -12,
      recovery: "STANDING",
      hitLevel: "Mid",
      optimal: { move: "2,4", startup: 12, dmg: 24, reason: "12f punisher deals guaranteed knockdown" },
      distractor1: { move: "df+2", startup: 15, dmg: 18, reason: "Too slow (15f)! Opponent will block and punish you." },
      distractor2: { move: "1", startup: 10, dmg: 7, reason: "Suboptimal (10f)! Leaves 17 points of free damage on the table." }
    },
    {
      moveName: "Hellsweep / Spinning Demon (cd+4)",
      notation: "f,n,d,df+4",
      blockAdv: -23,
      recovery: "CROUCHING",
      hitLevel: "Low",
      optimal: { move: "WS+2 (Full Hopkick Launch)", startup: 15, dmg: 68, reason: "At -23 OB, full While Standing launch is 100% guaranteed!" },
      distractor1: { move: "WS+4 (Toe Kick)", startup: 11, dmg: 16, reason: "Massive under-punish! Gave up a 70+ damage launch juggle." },
      distractor2: { move: "df+1 (Standing Poke)", startup: 13, dmg: 11, reason: "Invalid state! Defender is in crouch guard, standing move will not come out in time." }
    },
    {
      moveName: "Wind God Fist (Blocked f,n,d,df+2)",
      notation: "f,n,d,df+2",
      blockAdv: -10,
      recovery: "STANDING",
      hitLevel: "High",
      optimal: { move: "1,1,2 (i10 Flash Jab)", startup: 10, dmg: 25, reason: "Exact i10 punisher knocks down and provides oki pressure." },
      distractor1: { move: "b+1,2", startup: 14, dmg: 28, reason: "Too slow (14f)! Opponent recovers and blocks cleanly." },
      distractor2: { move: "d+4 (Low Kick)", startup: 16, dmg: 10, reason: "Far too slow (16f) and -15 on block yourself!" }
    },
    {
      moveName: "Stature Smash (db+4)",
      notation: "db+4",
      blockAdv: -14,
      recovery: "CROUCHING",
      hitLevel: "Low",
      optimal: { move: "WS+1,2 or WS+1,4", startup: 13, dmg: 32, reason: "Optimal i13 While Standing punisher maximizes standing frame advantage." },
      distractor1: { move: "WS+2 (Full Launcher)", startup: 15, dmg: 65, reason: "1 frame too slow (15f vs -14). Opponent blocks and you get launched." },
      distractor2: { move: "Dick Jab (d+1)", startup: 10, dmg: 5, reason: "Under-punish! Deals only 5 damage without knockdown." }
    },
    {
      moveName: "Dragon Uppercut (f,n,d,df+1)",
      notation: "f,n,d,df+1",
      blockAdv: -16,
      recovery: "STANDING",
      hitLevel: "Mid",
      optimal: { move: "df+2 or Can-Can Kicks (Full Launch)", startup: 15, dmg: 72, reason: "Opponent is -16, comfortably within your 15f launcher window!" },
      distractor1: { move: "1,2", startup: 10, dmg: 17, reason: "Suboptimal jab string on a -16 launch-punishable blunder." },
      distractor2: { move: "f,f,f+3 (Slash Kick)", startup: 20, dmg: 30, reason: "Way too slow (20f)! Opponent will block or sidestep." }
    }
  ];

  const q = situations[Math.floor(Math.random() * situations.length)];
  quizState.currentQuestion = q;

  const nameEl = document.getElementById('quizAttackerName');
  const avatarEl = document.getElementById('quizAttackerAvatar');
  const moveEl = document.getElementById('quizMoveName');
  const notEl = document.getElementById('quizMoveNotation');
  const badgeEl = document.getElementById('quizRecoveryStateBadge');
  const disadvVal = document.querySelector('#quizDisadvBadge .pq-disadv-val');

  if (nameEl) nameEl.textContent = attacker ? attacker.name : 'Opponent';
  if (avatarEl && attacker) avatarEl.src = attacker.avatar_url || '/assets/avatars/kazuya-brand-256-BInk9tTm.webp';
  if (moveEl) moveEl.textContent = q.moveName;
  if (notEl) notEl.textContent = q.notation;
  if (badgeEl) badgeEl.textContent = `${q.recovery} RECOVERY`;
  if (disadvVal) disadvVal.textContent = `${q.blockAdv} OB`;

  const rawOptions = [
    { type: 'optimal', title: q.optimal.move, startup: q.optimal.startup, dmg: q.optimal.dmg, reason: q.optimal.reason, correct: true },
    { type: 'slow', title: q.distractor1.move, startup: q.distractor1.startup, dmg: q.distractor1.dmg, reason: q.distractor1.reason, correct: false },
    { type: 'suboptimal', title: q.distractor2.move, startup: q.distractor2.startup, dmg: q.distractor2.dmg, reason: q.distractor2.reason, correct: false }
  ].sort(() => Math.random() - 0.5);

  const container = document.getElementById('quizOptionsGrid');
  if (!container) return;

  container.innerHTML = rawOptions.map((opt, idx) => `
    <button type="button" class="pq-option-btn" id="quiz_opt_${idx}" onclick="selectQuizOption(${idx}, ${opt.correct}, '${opt.reason.replace(/'/g, "\\'")}', '${opt.title.replace(/'/g, "\\'")}')">
      <div class="pqo-head">
        <span class="pqo-letter">${String.fromCharCode(65 + idx)}</span>
        <span class="pqo-move-name">${opt.title}</span>
      </div>
      <div class="pqo-specs">
        <span class="pqo-spec-chip">Startup: i${opt.startup}</span>
        <span class="pqo-spec-chip dmg">${opt.dmg} DMG</span>
      </div>
    </button>
  `).join('');
}

function selectQuizOption(index, isCorrect, reason, moveTitle) {
  document.querySelectorAll('.pq-option-btn').forEach(btn => btn.disabled = true);
  const selectedBtn = document.getElementById(`quiz_opt_${index}`);
  const feedback = document.getElementById('quizFeedbackBanner');

  quizState.totalAttempts++;

  if (isCorrect) {
    playSfx('correct');
    quizState.streak++;
    quizState.score += (100 + (quizState.streak * 20));
    quizState.correctAttempts++;
    if (selectedBtn) selectedBtn.classList.add('correct');
    if (feedback) {
      feedback.className = 'pq-feedback-banner correct';
      feedback.style.display = 'block';
      feedback.innerHTML = `
        <div class="pq-fb-title">✓ PERFECT EXECUTION!</div>
        <div class="pq-fb-desc"><strong>${moveTitle}</strong> is optimal: ${reason}</div>
      `;
    }
  } else {
    playSfx('wrong');
    quizState.streak = 0;
    if (selectedBtn) selectedBtn.classList.add('wrong');
    if (feedback) {
      feedback.className = 'pq-feedback-banner wrong';
      feedback.style.display = 'block';
      feedback.innerHTML = `
        <div class="pq-fb-title">✕ INCORRECT RESPONSE</div>
        <div class="pq-fb-desc"><strong>${moveTitle}</strong> failed: ${reason}</div>
      `;
    }
  }

  updateQuizScoreDisplay();
}

// ==========================================================================
// 7. Stage Showcase Filters & Deep Dive Modal (Phase 9)
// ==========================================================================
function setupStageFilters() {
  document.querySelectorAll('#stageFilterPills .stage-f-pill').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('#stageFilterPills .stage-f-pill').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      const filter = e.target.dataset.stageFilter;
      playSfx('click');
      filterStagesGrid(filter);
    });
  });
}

function filterStagesGrid(filter = 'ALL') {
  const container = document.getElementById('stagesGrid');
  if (!container || !state.stages) return;

  let list = [...state.stages];
  if (filter === 'WALL') {
    list = list.filter(s => s.has_walls !== false);
  } else if (filter === 'WALL_BREAK') {
    list = list.filter(s => s.wall_break || (s.hazards && s.hazards.some(h => h.toLowerCase().includes('wall'))));
  } else if (filter === 'FLOOR_BREAK') {
    list = list.filter(s => s.floor_break || (s.hazards && s.hazards.some(h => h.toLowerCase().includes('floor break'))));
  } else if (filter === 'BALCONY_BREAK') {
    list = list.filter(s => s.balcony_break || (s.hazards && s.hazards.some(h => h.toLowerCase().includes('balcony'))));
  } else if (filter === 'FLOOR_BLAST') {
    list = list.filter(s => s.floor_blast || (s.hazards && s.hazards.some(h => h.toLowerCase().includes('blast'))));
  } else if (filter === 'INFINITE') {
    list = list.filter(s => s.has_walls === false || (s.hazards && s.hazards.length === 0));
  }

  container.innerHTML = list.map(s => {
    const hazardsList = s.hazards || [];
    const imgSrc = s.image_url || s.image || '/assets/img/stages/arena.jpg';
    const locationStr = s.location || 'Official Arena';
    const gimmickStr = s.notes || s.special_mechanics || s.gimmick || (s.has_walls ? 'Walled tournament battleground' : 'Infinite arena');

    return `
      <div class="stage-card" id="stage_card_${s.id}" onclick="openStageDetailModal('${s.id}')">
        <div class="stage-img-wrap">
          <img class="stage-img" src="${imgSrc}" alt="${s.name}" loading="lazy"/>
          <div class="stage-overlay"></div>
          <div class="stage-hazard-badges">
            ${hazardsList.map(h => `<span class="hazard-badge">${h}</span>`).join('')}
            ${s.has_walls === false ? '<span class="hazard-badge" style="background:#3b82f6;">INFINITE</span>' : ''}
          </div>
        </div>
        <div class="stage-info">
          <h3 class="stage-name">${s.name}</h3>
          <p class="stage-location">${locationStr}</p>
          <p class="stage-gimmick">${gimmickStr}</p>
          <button type="button" class="btn-stage-inspect" onclick="event.stopPropagation(); openStageDetailModal('${s.id}')">
            <span>Inspect Arena Dynamics</span> &rarr;
          </button>
        </div>
      </div>
    `;
  }).join('');
}

let activeDetailStageId = null;

function openStageDetailModal(stageId) {
  playSfx('click');
  const stage = state.stages.find(s => String(s.id) === String(stageId)) || state.stages[0];
  if (!stage) return;

  activeDetailStageId = stage.id;

  const modal = document.getElementById('stageDetailModal');
  const heroImg = document.getElementById('sdHeroImg');
  const title = document.getElementById('sdTitle');
  const loc = document.getElementById('sdLocation');
  const catPill = document.getElementById('sdCategoryPill');
  const gimmickText = document.getElementById('sdGimmickText');
  const hazardsList = document.getElementById('sdHazardsList');
  const tacticsText = document.getElementById('sdTacticsText');

  if (heroImg) heroImg.src = stage.image_url || stage.image || '/assets/img/stages/arena.jpg';
  if (title) title.textContent = stage.name;
  if (loc) loc.textContent = stage.location || 'Tournament Arena';
  if (catPill) catPill.textContent = stage.has_walls === false ? 'INFINITE ARENA' : 'OCTAGONAL WALL ARENA';
  if (gimmickText) gimmickText.textContent = stage.notes || stage.gimmick || 'Standard Tekken 8 competitive stage featuring dynamic destructible boundaries.';

  if (hazardsList) {
    const list = stage.hazards || (stage.wall_break ? ['Wall Break'] : ['Wall Bound']);
    hazardsList.innerHTML = list.map(h => `
      <div class="sd-hazard-chip">
        <span class="sdh-icon">💥</span>
        <div class="sdh-meta">
          <div class="sdh-title">${h}</div>
          <div class="sdh-desc">Expands combo potential with additional scaling floor bounce or wall collapse.</div>
        </div>
      </div>
    `).join('');
  }

  if (tacticsText) {
    tacticsText.textContent = stage.has_walls === false
      ? 'Infinite arena eliminates corner carry danger. Focus on infinite backdashing, keepout pokes, and long-range whiff punishment.'
      : 'Maintain center stage dominance. Wall carry routes should be prioritized over raw damage, routing into wall splat for guaranteed 20+ additional wall combo damage.';
  }

  if (modal) modal.style.display = 'flex';
}

function closeStageDetailModal() {
  playSfx('click');
  const modal = document.getElementById('stageDetailModal');
  if (modal) modal.style.display = 'none';
}

function selectStageAsBattleground() {
  if (!activeDetailStageId) return;
  playSfx('launch');
  selectStage(activeDetailStageId);
  closeStageDetailModal();
  showToast(`Selected stage as battleground!`, 'success');
}

// ==========================================================================
// 8. Tactical Attribute Bars & Move Comparison Tool (Phase 8)
// ==========================================================================
function renderMatchupStatBars(player, opponent) {
  const container = document.getElementById('statsBarsGrid');
  if (!container || !player) return;

  const opp = opponent || player;

  function getAttr(char, attr) {
    const slug = (char.slug || '').toLowerCase();
    const arch = (char.archetype || '').toLowerCase();
    const isMishima = arch.includes('mishima') || slug === 'jin' || slug === 'kazuya' || slug === 'reina';
    const isGrappler = arch.includes('grappler') || slug === 'king';
    const isRushdown = arch.includes('rushdown') || slug === 'hwoarang' || slug === 'nina' || slug === 'law';

    if (attr === 'Range') return isMishima ? 88 : (slug === 'claudio' || slug === 'bryan' ? 92 : 78);
    if (attr === 'Punishment') return isMishima ? 94 : (slug === 'lee' || slug === 'paul' ? 90 : 82);
    if (attr === 'Pressure') return isRushdown ? 94 : (isMishima ? 86 : 80);
    if (attr === 'Mobility') return isMishima ? 88 : (slug === 'alisa' || slug === 'lili' ? 95 : 76);
    if (attr === 'Counter-Hit') return slug === 'bryan' || slug === 'steve' ? 96 : (slug === 'jin' ? 88 : 78);
    if (attr === 'Wall Carry') return isGrappler ? 86 : (slug === 'leo' || slug === 'lars' || slug === 'dragunov' ? 94 : 84);
    return 80;
  }

  const attributes = ['Range', 'Punishment', 'Pressure', 'Mobility', 'Counter-Hit', 'Wall Carry'];

  container.innerHTML = attributes.map(attr => {
    const valP1 = getAttr(player, attr);
    const valP2 = getAttr(opp, attr);
    const p1Adv = valP1 >= valP2;

    return `
      <div class="stat-compare-row">
        <div class="scr-label-col">
          <span class="scr-attr-name">${attr}</span>
          <span class="scr-adv-tag ${p1Adv ? 'p1' : 'p2'}">${p1Adv ? '+Advantage' : 'Threat'}</span>
        </div>
        <div class="scr-bars-col">
          <div class="scr-bar-wrap p1">
            <span class="scr-val p1">${valP1}</span>
            <div class="scr-bar-track">
              <div class="scr-bar-fill p1" style="width: ${valP1}%;"></div>
            </div>
          </div>
          <div class="scr-bar-wrap p2">
            <div class="scr-bar-track">
              <div class="scr-bar-fill p2" style="width: ${valP2}%;"></div>
            </div>
            <span class="scr-val p2">${valP2}</span>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

let cachedP1Moves = [];
let cachedP2Moves = [];

function setupMoveComparison(p1Moves = [], p2Moves = []) {
  cachedP1Moves = p1Moves;
  cachedP2Moves = p2Moves;

  const s1 = document.getElementById('mcSelectP1');
  const s2 = document.getElementById('mcSelectP2');
  if (!s1 || !s2) return;

  const h1 = document.getElementById('mcHeaderP1');
  const h2 = document.getElementById('mcHeaderP2');
  if (h1 && state.matchup.player) h1.textContent = `${state.matchup.player.name} Move`;
  if (h2 && state.matchup.opponent) h2.textContent = `${state.matchup.opponent.name} Move`;

  const defaultP1 = p1Moves.length > 0 ? p1Moves : [
    { command: '1', name: 'Flash Jab', hit_level: 'h', startup_frames: 10, block_advantage: 1, hit_advantage: 8, damage: 5 },
    { command: 'df+1', name: 'Belly Poke', hit_level: 'm', startup_frames: 13, block_advantage: -3, hit_advantage: 5, damage: 11 },
    { command: 'f+4', name: 'Demon Keepout Kick', hit_level: 'm', startup_frames: 16, block_advantage: -7, hit_advantage: 4, damage: 21 },
    { command: 'd+2', name: 'Demon Low Punch', hit_level: 'l', startup_frames: 22, block_advantage: -14, hit_advantage: 4, damage: 17 }
  ];

  const defaultP2 = p2Moves.length > 0 ? p2Moves : [
    { command: '1', name: 'Flash Jab', hit_level: 'h', startup_frames: 10, block_advantage: 1, hit_advantage: 8, damage: 5 },
    { command: 'df+1', name: 'Twin Piston Starter', hit_level: 'm', startup_frames: 15, block_advantage: -7, hit_advantage: 4, damage: 12 },
    { command: 'f,n,d,df+2', name: 'Electric Wind God Fist', hit_level: 'h', startup_frames: 11, block_advantage: 5, hit_advantage: 'Launch', damage: 23 },
    { command: 'f,n,d,df+4,1', name: 'Spinning Demon (Hellsweep)', hit_level: 'l,m', startup_frames: 16, block_advantage: -23, hit_advantage: 'Knockdown', damage: 25 }
  ];

  s1.innerHTML = defaultP1.map((m, i) => `<option value="${i}">${m.command} (${m.name || 'Move'})</option>`).join('');
  s2.innerHTML = defaultP2.map((m, i) => `<option value="${i}">${m.command} (${m.name || 'Move'})</option>`).join('');

  updateMoveComparison();
}

function updateMoveComparison() {
  const s1 = document.getElementById('mcSelectP1');
  const s2 = document.getElementById('mcSelectP2');
  const tbody = document.getElementById('mcTableBody');
  if (!s1 || !s2 || !tbody) return;

  const p1List = cachedP1Moves.length > 0 ? cachedP1Moves : [
    { command: '1', name: 'Flash Jab', hit_level: 'h', startup_frames: 10, block_advantage: 1, hit_advantage: 8, damage: 5 },
    { command: 'df+1', name: 'Belly Poke', hit_level: 'm', startup_frames: 13, block_advantage: -3, hit_advantage: 5, damage: 11 },
    { command: 'f+4', name: 'Demon Keepout Kick', hit_level: 'm', startup_frames: 16, block_advantage: -7, hit_advantage: 4, damage: 21 },
    { command: 'd+2', name: 'Demon Low Punch', hit_level: 'l', startup_frames: 22, block_advantage: -14, hit_advantage: 4, damage: 17 }
  ];

  const p2List = cachedP2Moves.length > 0 ? cachedP2Moves : [
    { command: '1', name: 'Flash Jab', hit_level: 'h', startup_frames: 10, block_advantage: 1, hit_advantage: 8, damage: 5 },
    { command: 'df+1', name: 'Twin Piston Starter', hit_level: 'm', startup_frames: 15, block_advantage: -7, hit_advantage: 4, damage: 12 },
    { command: 'f,n,d,df+2', name: 'Electric Wind God Fist', hit_level: 'h', startup_frames: 11, block_advantage: 5, hit_advantage: 'Launch', damage: 23 },
    { command: 'f,n,d,df+4,1', name: 'Spinning Demon (Hellsweep)', hit_level: 'l,m', startup_frames: 16, block_advantage: -23, hit_advantage: 'Knockdown', damage: 25 }
  ];

  const m1 = p1List[parseInt(s1.value)] || p1List[0];
  const m2 = p2List[parseInt(s2.value)] || p2List[0];

  const s1Val = parseInt(m1.startup_frames) || 12;
  const s2Val = parseInt(m2.startup_frames) || 12;
  const speedAdv = s1Val < s2Val ? `P1 is ${s2Val - s1Val}f faster` : (s1Val > s2Val ? `P2 is ${s1Val - s2Val}f faster` : 'Equal startup speed');

  const b1Val = parseInt(m1.block_advantage) || 0;
  const b2Val = parseInt(m2.block_advantage) || 0;
  const safetyAdv = b1Val > b2Val ? `P1 safer on block (+${b1Val - b2Val})` : (b1Val < b2Val ? `P2 safer on block (+${b2Val - b1Val})` : 'Equal block safety');

  tbody.innerHTML = `
    <tr>
      <td><strong>Command &amp; Name</strong></td>
      <td><strong>${m1.command}</strong> (${m1.name || 'Move'})</td>
      <td><strong>${m2.command}</strong> (${m2.name || 'Move'})</td>
      <td><span class="badge badge-frame">1v1 Comparison</span></td>
    </tr>
    <tr>
      <td><strong>Startup Speed</strong></td>
      <td>i${m1.startup_frames || '12'}</td>
      <td>i${m2.startup_frames || '12'}</td>
      <td><span class="mc-adv-tag ${s1Val <= s2Val ? 'green' : 'red'}">${speedAdv}</span></td>
    </tr>
    <tr>
      <td><strong>On Block Advantage</strong></td>
      <td>${m1.block_advantage > 0 ? '+' : ''}${m1.block_advantage || 0}</td>
      <td>${m2.block_advantage > 0 ? '+' : ''}${m2.block_advantage || 0}</td>
      <td><span class="mc-adv-tag ${b1Val >= b2Val ? 'green' : 'gold'}">${safetyAdv}</span></td>
    </tr>
    <tr>
      <td><strong>Hit Level</strong></td>
      <td>${(m1.hit_level || 'm').toUpperCase()}</td>
      <td>${(m2.hit_level || 'm').toUpperCase()}</td>
      <td>${m1.hit_level === m2.hit_level ? 'Same level' : 'Different height'}</td>
    </tr>
    <tr>
      <td><strong>Damage Output</strong></td>
      <td>${m1.damage || 15} DMG</td>
      <td>${m2.damage || 15} DMG</td>
      <td>${(m1.damage || 0) >= (m2.damage || 0) ? 'P1 deals higher dmg' : 'P2 deals higher dmg'}</td>
    </tr>
  `;
}

// ==========================================================================
// 9. Character Profile Dashboard Modal (Phase 4 - 17 Sections)
// ==========================================================================
function openCharacterProfile(slugOrObj) {
  playSfx('click');
  const slug = typeof slugOrObj === 'string' ? slugOrObj : (slugOrObj?.slug || 'jin');
  const char = state.characters.find(c => c.slug === slug) || state.characters[0];
  if (!char) return;

  const modal = document.getElementById('characterProfileModal');
  if (!modal) return;

  const avatar = document.getElementById('cpAvatarImg');
  const name = document.getElementById('cpCharName');
  const arch = document.getElementById('cpArchetypeBadge');
  const country = document.getElementById('cpCountryBadge');
  const diff = document.getElementById('cpDifficultyBadge');
  const hurtbox = document.getElementById('cpHurtboxBadge');
  const style = document.getElementById('cpStyleName');

  const hb = getCharacterHurtboxProfile(char.slug);
  const fStyle = FIGHTING_STYLES[char.slug] || char.archetype || 'Traditional Martial Arts';

  if (avatar) avatar.src = char.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp';
  if (name) name.textContent = char.name;
  if (arch) arch.textContent = `${char.archetype || 'Fighter'}${char.is_dlc ? ' • DLC' : ''}`;
  if (country) country.textContent = char.slug === 'jin' || char.slug === 'kazuya' ? '🇯🇵 Japan' : (char.slug === 'king' ? '🇲🇽 Mexico' : (char.slug === 'nina' ? '🇮🇪 Ireland' : '🌍 World'));
  if (diff) diff.textContent = char.slug === 'kazuya' ? '★★★★★ Master Execution' : (char.slug === 'jin' ? '★★★★☆ Advanced Execution' : '★★★☆☆ Intermediate Execution');
  if (hurtbox) hurtbox.textContent = hb.label;
  if (style) style.textContent = fStyle;

  updateProfileFavState(char.slug);

  document.querySelectorAll('#cpTabsBar .cp-tab-btn').forEach(btn => {
    btn.onclick = (e) => {
      document.querySelectorAll('#cpTabsBar .cp-tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.cp-tab-panel').forEach(p => p.classList.remove('active'));
      e.target.classList.add('active');
      const targetPanel = document.getElementById(e.target.dataset.cptab);
      if (targetPanel) targetPanel.classList.add('active');
      playSfx('click');
    };
  });

  populateProfileSections(char);
  modal.style.display = 'flex';
}

function closeCharacterProfile() {
  playSfx('click');
  const modal = document.getElementById('characterProfileModal');
  if (modal) modal.style.display = 'none';
}

function updateProfileFavState(slug) {
  const favs = getFavorites();
  const isFav = favs.fighters.includes(slug);
  const icon = document.getElementById('cpFavIcon');
  const text = document.getElementById('cpFavText');
  if (icon) icon.textContent = isFav ? '★' : '☆';
  if (text) text.textContent = isFav ? 'Favorited' : 'Favorite Fighter';
}

function setFighterFromProfile(role) {
  playSfx('launch');
  if (!state.selectedCharacter) return;
  if (role === 'P1') {
    state.matchup.player = state.selectedCharacter;
    const sel = document.getElementById('playerSelect');
    if (sel) sel.value = state.selectedCharacter.slug;
    showToast(`Set ${state.selectedCharacter.name} as Player 1`, 'success');
  } else {
    state.matchup.opponent = state.selectedCharacter;
    const sel = document.getElementById('opponentSelect');
    if (sel) sel.value = state.selectedCharacter.slug;
    showToast(`Set ${state.selectedCharacter.name} as Opponent`, 'info');
  }
  closeCharacterProfile();
  const an = document.getElementById('analyzer');
  if (an) an.scrollIntoView({ behavior: 'smooth' });
}

function openComboLabFromProfile() {
  playSfx('click');
  const slug = state.selectedCharacter?.slug || 'jin';
  closeCharacterProfile();
  const lab = document.getElementById('combo-lab');
  if (lab) lab.scrollIntoView({ behavior: 'smooth' });
  loadComboLabForFighter(slug);
}

function populateProfileSections(char) {
  const bio = document.getElementById('cpBioText');
  if (bio) {
    bio.textContent = `${char.name} is a premier ${char.archetype || 'Tekken 8'} combatant characterized by formidable neutral control, oppressive block advantage frames, and devastating wall conversions under the Tekken 8 Heat Engine. Built for tournament pressure, this fighter excels when dictating combat pace at Range 2.`;
  }

  const top5List = document.getElementById('cpTop5MovesList');
  if (top5List) {
    top5List.innerHTML = `
      <div class="cp-move-chip"><strong>1</strong> — 10f Standard Flash Poke (+1 OB)</div>
      <div class="cp-move-chip"><strong>df+1</strong> — 13f Mid Check Poke (-3 OB, safe check)</div>
      <div class="cp-move-chip"><strong>f+4</strong> — Long-range mid keepout & counter-hit starter</div>
      <div class="cp-move-chip"><strong>df+2</strong> — 15f Normal Hit Mid Launcher</div>
      <div class="cp-move-chip"><strong>db+4</strong> — High-crushing low poke with frame advantage</div>
    `;
  }

  const gameplan = document.getElementById('cpCoreGameplan');
  if (gameplan) {
    gameplan.textContent = `Control mid-range with df+1 and f+4. When opponent hesitates, enforce low pokes. Bait whiffs with fluid backdashing and retaliate instantly with your 15f launcher into full air juggle.`;
  }

  const basicLauncher = document.getElementById('cpBasicLauncherBox');
  if (basicLauncher) {
    basicLauncher.innerHTML = `<strong>df+2 (Mid Launcher)</strong> ➔ Startup: i15 ➔ Launches on Normal Hit ➔ Follow up with standard juggle route for 65+ DMG`;
  }

  const statsGrid = document.getElementById('cpStatsRadarGrid');
  if (statsGrid) {
    const stats = [
      { name: 'Offensive Pressure', val: 90 },
      { name: 'Defensive Punishment', val: 88 },
      { name: 'Neutral Range', val: 85 },
      { name: 'Execution Demand', val: 82 },
      { name: 'Mixup Potential', val: 86 },
      { name: 'Wall Carry Efficiency', val: 92 }
    ];
    statsGrid.innerHTML = stats.map(s => `
      <div class="cp-stat-row">
        <span class="cp-stat-lbl">${s.name}</span>
        <div class="cp-stat-bar-track">
          <div class="cp-stat-bar-fill" style="width:${s.val}%;"></div>
        </div>
        <span class="cp-stat-num">${s.val}/100</span>
      </div>
    `).join('');
  }

  const neutralBody = document.getElementById('cpNeutralMovesBody');
  if (neutralBody) {
    neutralBody.innerHTML = `
      <tr><td>Fast Poke</td><td><strong>1, 2</strong></td><td>h, h</td><td>i10</td><td>-1</td><td>17</td><td>Universal safe interrupt and turn-stealer</td></tr>
      <tr><td>Mid Check</td><td><strong>df+1</strong></td><td>m</td><td>i13</td><td>-3</td><td>11</td><td>Dominant mid check; beats ducking attempts</td></tr>
      <tr><td>Keepout</td><td><strong>f+4</strong></td><td>m</td><td>i16</td><td>-7</td><td>21</td><td>Longest range neutral poke; counter-hit launcher</td></tr>
      <tr><td>Gap Closer</td><td><strong>f,f+2</strong></td><td>m</td><td>i15</td><td>-9</td><td>24</td><td>Demon paw; massive pushback makes it safe</td></tr>
      <tr><td>Low Harass</td><td><strong>db+4</strong></td><td>l</td><td>i20</td><td>-13</td><td>18</td><td>High crushes; +3 on hit to enforce mixup</td></tr>
    `;
  }

  const launchersBody = document.getElementById('cpLaunchersBody');
  if (launchersBody) {
    launchersBody.innerHTML = `
      <tr><td>Normal Hit</td><td><strong>df+2</strong></td><td>i15</td><td>-12</td><td>Standard Juggle</td><td>Primary standing whiff and block punisher</td></tr>
      <tr><td>Hopkick</td><td><strong>uf+4</strong></td><td>i15</td><td>-13</td><td>Full Aerial Launch</td><td>Low crushes on frame 9; great panic launcher</td></tr>
      <tr><td>Counter Hit</td><td><strong>4 (Magic 4)</strong></td><td>i11</td><td>-9</td><td>CH Screw / Tornado</td><td>Fastest CH launcher in the game</td></tr>
      <tr><td>While Standing</td><td><strong>WS+2</strong></td><td>i15</td><td>-12</td><td>Full Juggle</td><td>Crouching block punish against heavy lows</td></tr>
    `;
  }

  const throwsBody = document.getElementById('cpThrowsBody');
  if (throwsBody) {
    throwsBody.innerHTML = `
      <tr><td><strong>1+3 or f+1+3</strong></td><td>Shoulder Throw</td><td>1 or 2</td><td>35</td><td>Side-swaps opponent towards your back</td></tr>
      <tr><td><strong>2+4 or f+2+4</strong></td><td>Leg Sweep Takedown</td><td>1 or 2</td><td>35</td><td>Pushes opponent away towards wall</td></tr>
      <tr><td><strong>uf+1+2</strong></td><td>Command Overhead Slam</td><td>1+2 Break</td><td>40</td><td>Leaves opponent face-up grounded for oki mixup</td></tr>
    `;
  }

  const standingBody = document.getElementById('cpStandingPunishBody');
  if (standingBody) {
    standingBody.innerHTML = `
      <tr><td>i10 (-10 OB)</td><td><strong>1, 1, 2</strong> or <strong>2, 4</strong></td><td>25</td><td>Knockdown</td><td>Guaranteed knockdown and wall travel</td></tr>
      <tr><td>i12 (-12 OB)</td><td><strong>2, 4</strong> or <strong>f+1+2</strong></td><td>28</td><td>+4 OB / Splat</td><td>Wall splats if opponent backs to corner</td></tr>
      <tr><td>i14 (-14 OB)</td><td><strong>f+2, 4</strong> or <strong>b+1, 2</strong></td><td>34</td><td>Knockdown</td><td>Heavy damage punish on staggering mids</td></tr>
      <tr><td>i15+ (-15 OB)</td><td><strong>df+2</strong> or <strong>uf+4</strong></td><td>68+</td><td>Launch</td><td>FULL LAUNCH! Execute BnB combo for 68+ DMG</td></tr>
    `;
  }

  const crouchBody = document.getElementById('cpCrouchingPunishBody');
  if (crouchBody) {
    crouchBody.innerHTML = `
      <tr><td>i11 (-11 OB)</td><td><strong>WS+4</strong></td><td>16</td><td>+5 On Hit</td><td>Universal toe kick; maintains turn</td></tr>
      <tr><td>i13 (-13 OB)</td><td><strong>WS+1, 2</strong></td><td>28</td><td>Knockdown</td><td>Strong punish on intermediate blocked lows</td></tr>
      <tr><td>i15+ (-15 OB)</td><td><strong>WS+2</strong></td><td>70+</td><td>Full Launch</td><td>Full standing juggle on blocked hellsweeps / stagger lows</td></tr>
    `;
  }

  const whiffBody = document.getElementById('cpWhiffPunishBody');
  if (whiffBody) {
    whiffBody.innerHTML = `
      <tr><td><strong>df+2</strong></td><td>i15</td><td>Range 1.5</td><td>68 DMG (Launch)</td><td>Close to mid-range whiffs</td></tr>
      <tr><td><strong>f,f+2 (Demon Paw)</strong></td><td>i15</td><td>Range 2.8</td><td>24 DMG (Knockdown)</td><td>Long-range whiff retaliation across the screen</td></tr>
      <tr><td><strong>b+2, 1</strong></td><td>i14</td><td>Range 2.0</td><td>32 DMG</td><td>Consistent hit-confirm whiff punisher</td></tr>
    `;
  }

  const bnbCombos = document.getElementById('cpBnbCombosList');
  if (bnbCombos) {
    bnbCombos.innerHTML = `
      <div class="cp-combo-row">
        <div class="cpr-header"><strong>Hopkick Bread &amp; Butter (68 DMG • 7 Hits)</strong></div>
        <div class="cpr-notation">${formatTekkenNotation('df+2 > f+1 > b+3~f > 1 > b+3~f > 2 > f,f,f+3')}</div>
      </div>
      <div class="cp-combo-row">
        <div class="cpr-header"><strong>Counter-Hit Magic 4 Route (62 DMG • 6 Hits)</strong></div>
        <div class="cpr-notation">${formatTekkenNotation('4 (CH) > dash > b+3~f > 1 > b+3~f > 2 > f,f+2')}</div>
      </div>
    `;
  }

  const optimalCombos = document.getElementById('cpOptimalCombosList');
  if (optimalCombos) {
    optimalCombos.innerHTML = `
      <div class="cp-combo-row">
        <div class="cpr-header"><strong>Max Damage Micro-Dash Route (76 DMG • 9 Hits)</strong></div>
        <div class="cpr-notation">${formatTekkenNotation('df+2 > micro-dash > 1+2 > b+3~f > 1 > dash > b+3~f > 2 > Heat Burst > Heat Dash f,f+2')}</div>
      </div>
    `;
  }

  const wallCombos = document.getElementById('cpWallCombosList');
  if (wallCombos) {
    wallCombos.innerHTML = `
      <div class="cp-combo-row">
        <div class="cpr-header"><strong>Standard Wall Splat Ender (+26 DMG)</strong></div>
        <div class="cpr-notation">${formatTekkenNotation('Wall Splat > df+1 > 4 > db+2,2,3')}</div>
      </div>
      <div class="cp-combo-row">
        <div class="cpr-header"><strong>Tornado at Wall + Floor Blast Extension (+34 DMG)</strong></div>
        <div class="cpr-notation">${formatTekkenNotation('Wall Splat > b+1+2 (Tornado) > Floor Blast > uf+2,2')}</div>
      </div>
    `;
  }

  const heatGrid = document.getElementById('cpHeatBreakdownGrid');
  if (heatGrid) {
    heatGrid.innerHTML = `
      <div class="cp-heat-box">
        <div class="cph-title">HEAT ENGAGERS (5 TOOLS)</div>
        <p class="cph-desc">f,f+2, 1+2, cd+1, df+1+2, and ws+1+2 instantly ignite Heat with +17 frame advantage on hit.</p>
      </div>
      <div class="cp-heat-box">
        <div class="cph-title">HEAT SMASH</div>
        <p class="cph-desc">Input: 2+3 during Heat. Deals 52 raw damage with immense chip damage and +8 on block.</p>
      </div>
      <div class="cp-heat-box">
        <div class="cph-title">HEAT DASH</div>
        <p class="cph-desc">Cancel Heat Engager into forward sprint. Grants +5 on block for free mixup or full combo extension.</p>
      </div>
    `;
  }

  const rageBox = document.getElementById('cpRageBox');
  if (rageBox) {
    rageBox.innerHTML = `
      <div class="cpr-title">RAGE ART (df+1+2) • 55 DAMAGE</div>
      <p class="cpr-desc">Armored on frame 8. Absorbs highs, mids, and lows while below 25% health. Safe against hasty enemy offense.</p>
    `;
  }

  const stancesGrid = document.getElementById('cpStancesGrid');
  if (stancesGrid) {
    stancesGrid.innerHTML = `
      <div class="cp-stance-card">
        <div class="cps-title">ZEN / Crouching Demon Stance (CDS)</div>
        <p class="cps-desc">Input: d+1+2 or transition from b+3~f. High crushes with unblockable sweeps (ZEN 3) or mid launch (ZEN 1+2).</p>
      </div>
    `;
  }

  const strengthsList = document.getElementById('cpKeyStrengthsList');
  if (strengthsList) {
    strengthsList.innerHTML = `
      <li>Dominant range 2 keepout with f+4 and Demon Paw</li>
      <li>One of the best i10 block punishers in the game</li>
      <li>Strong safe mid checks prevent ducking</li>
    `;
  }

  const weaknessesList = document.getElementById('cpKeyWeaknessesList');
  if (weaknessesList) {
    weaknessesList.innerHTML = `
      <li>Weak to linear sidestepping towards opponent's left</li>
      <li>High execution required for optimal electric inputs</li>
      <li>Stance transitions can be interrupted by fast jabs</li>
    `;
  }

  const counterplayList = document.getElementById('cpCounterplayList');
  if (counterplayList) {
    counterplayList.innerHTML = `
      <li>Sidestep Walk Left (SSL) at medium distance to avoid f+4 and f,f+2</li>
      <li>Duck the second hit of strings that end in high</li>
      <li>Block low and punish with your 15f While Standing launcher</li>
    `;
  }

  const drillsList = document.getElementById('cpDrillsList');
  if (drillsList) {
    drillsList.innerHTML = `
      <div class="cp-drill-item"><strong>Drill 1: 10f Block Punishment</strong> — Set training dummy to perform -10 moves and punish 20 times consecutively with 1,1,2.</div>
      <div class="cp-drill-item"><strong>Drill 2: Whiff Baiting & Launch</strong> — Backdash out of enemy jab range, then immediately execute df+2 into full juggle.</div>
      <div class="cp-drill-item"><strong>Drill 3: Wall Splat Conversion</strong> — Carry dummy from center stage to wall and perform wall combo without dropping.</div>
    `;
  }

  const stageSyn = document.getElementById('cpStageSynergyText');
  if (stageSyn) {
    stageSyn.textContent = `Thrives on medium walled stages such as The Arena and Urban Square where wall carry enders convert into additional 25+ damage splat setups. On hazard stages like Sanctum and Rebel Hangar, floor blasts grant supplementary extensions.`;
  }
}

// ==========================================================================
// 10. Platform Settings & Preferences Modal (Phase 11)
// ==========================================================================
function openSettingsModal() {
  playSfx('click');
  const modal = document.getElementById('settingsModal');
  if (!modal) return;
  const soundCheck = document.getElementById('checkSoundEffects');
  if (soundCheck) soundCheck.checked = localStorage.getItem('tekken8_sound_fx') !== 'false';
  modal.style.display = 'flex';
}

function closeSettingsModal() {
  playSfx('click');
  const modal = document.getElementById('settingsModal');
  if (modal) modal.style.display = 'none';
}

function setDamageMode(mode) {
  playSfx('click');
  const b1 = document.getElementById('btnDmgScaled');
  const b2 = document.getElementById('btnDmgRaw');
  if (b1 && b2) {
    b1.classList.toggle('active', mode === 'scaled');
    b2.classList.toggle('active', mode === 'raw');
  }
  localStorage.setItem('tekken8_damage_mode', mode);
  showToast(`Damage display set to: ${mode === 'scaled' ? 'Verified Scaled (Official)' : 'Raw Unscaled Sum'}`, 'info');
}

function toggleSoundEffects(enabled) {
  localStorage.setItem('tekken8_sound_fx', enabled ? 'true' : 'false');
  if (enabled) playSfx('click');
}

function resetAllLocalData() {
  if (confirm('Are you sure you want to clear all stored preferences, favorites, and drill statistics?')) {
    localStorage.clear();
    location.reload();
  }
}

// Window Exports for Phase 4 Move Explorer
window.initMoveExplorer = initMoveExplorer;
window.onMoveExplorerFighterChange = onMoveExplorerFighterChange;
window.filterMovesTable = filterMovesTable;
window.resetMovesFilter = resetMovesFilter;
window.openMoveDetailModal = openMoveDetailModal;
window.closeMoveDetailModal = closeMoveDetailModal;
window.changeMovesPage = changeMovesPage;

// ==========================================================================
// Phase 6: Global Search & Command Palette (Ctrl+K)
// ==========================================================================
let globalSearchDebounceTimer = null;
let globalSearchActiveIndex = -1;
let globalSearchCategory = 'ALL';
let globalSearchResultsData = [];

function initGlobalSearch() {
  const input = document.getElementById('globalSearchInput');
  if (input) {
    input.addEventListener('input', (e) => {
      clearTimeout(globalSearchDebounceTimer);
      globalSearchDebounceTimer = setTimeout(() => {
        performGlobalSearch(e.target.value);
      }, 180);
    });

    input.addEventListener('keydown', handleGlobalSearchKeydown);
  }

  // Global keyboard shortcuts: Ctrl+K, Cmd+K, or "/"
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      openGlobalSearch();
    } else if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {
      e.preventDefault();
      openGlobalSearch();
    } else if (e.key === 'Escape') {
      const gsModal = document.getElementById('globalSearchModal');
      if (gsModal && gsModal.style.display !== 'none') {
        closeGlobalSearch();
      }
      const ngModal = document.getElementById('notationGuideModal');
      if (ngModal && ngModal.style.display !== 'none') {
        closeNotationGuideModal();
      }
      const pnModal = document.getElementById('practiceNotesModal');
      if (pnModal && pnModal.style.display !== 'none') {
        closePracticeNotesModal();
      }
      const pneModal = document.getElementById('practiceNoteEditModal');
      if (pneModal && pneModal.style.display !== 'none') {
        closePracticeNoteEditModal();
      }
    }
  });
}

function openGlobalSearch() {
  playSfx('click');
  const modal = document.getElementById('globalSearchModal');
  const input = document.getElementById('globalSearchInput');
  if (!modal) return;
  modal.style.display = 'flex';
  if (input) {
    input.value = '';
    setTimeout(() => input.focus(), 60);
  }
  globalSearchActiveIndex = -1;
  renderGlobalSearchResults([]);
}

function closeGlobalSearch() {
  playSfx('click');
  const modal = document.getElementById('globalSearchModal');
  if (modal) modal.style.display = 'none';
}

function setGlobalSearchCategory(cat) {
  playSfx('click');
  globalSearchCategory = cat;
  document.querySelectorAll('.gs-cat-pill').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.cat === cat);
  });
  const input = document.getElementById('globalSearchInput');
  if (input && input.value.trim()) {
    performGlobalSearch(input.value.trim());
  }
}

async function performGlobalSearch(query) {
  const q = (query || '').trim();
  const listEl = document.getElementById('globalSearchResultsList');
  if (!listEl) return;

  if (!q) {
    listEl.innerHTML = `
      <div class="gs-empty-state">
        <div class="gs-empty-icon">🔍</div>
        <div class="gs-empty-text">Type to search characters, frame data queries (e.g. <code>i10</code>, <code>-14</code>), combos, and arenas</div>
      </div>
    `;
    globalSearchResultsData = [];
    globalSearchActiveIndex = -1;
    return;
  }

  try {
    const data = await fetchAPI(`/search?q=${encodeURIComponent(q)}&category=${encodeURIComponent(globalSearchCategory)}&limit=10`);
    if (data && data.results) {
      globalSearchResultsData = data.results;
      globalSearchActiveIndex = -1;
      renderGlobalSearchResults(data.results);
    }
  } catch (err) {
    console.error('Global search error:', err);
  }
}

function renderGlobalSearchResults(items) {
  const listEl = document.getElementById('globalSearchResultsList');
  if (!listEl) return;

  if (!items || items.length === 0) {
    listEl.innerHTML = `
      <div class="gs-empty-state">
        <div class="gs-empty-icon">🥊</div>
        <div class="gs-empty-text">No results found for current query and category filter.</div>
      </div>
    `;
    return;
  }

  listEl.innerHTML = items.map((item, idx) => {
    let catClass = 'cat-fighter';
    let catIcon = '🥋';
    if (item.category === 'MOVE') { catClass = 'cat-move'; catIcon = '⚡'; }
    else if (item.category === 'COMBO') { catClass = 'cat-combo'; catIcon = '🥊'; }
    else if (item.category === 'STAGE') { catClass = 'cat-stage'; catIcon = '🏛️'; }

    return `
      <div class="gs-result-item ${idx === globalSearchActiveIndex ? 'selected' : ''}" 
           id="gs_res_${idx}" 
           onclick="selectGlobalSearchResult(${idx})" 
           role="option" 
           aria-selected="${idx === globalSearchActiveIndex}">
        <span class="gs-item-cat ${catClass}">${catIcon} ${item.category}</span>
        <div class="gs-item-content">
          <div class="gs-item-title">${escapeHtml(item.title)}</div>
          <div class="gs-item-sub">${escapeHtml(item.subtitle)}</div>
        </div>
        ${item.badge ? `<span class="gs-item-badge">${escapeHtml(item.badge)}</span>` : ''}
      </div>
    `;
  }).join('');
}

function handleGlobalSearchKeydown(e) {
  const items = globalSearchResultsData;
  if (!items || items.length === 0) return;

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    globalSearchActiveIndex = (globalSearchActiveIndex + 1) % items.length;
    updateGlobalSearchSelection();
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    globalSearchActiveIndex = (globalSearchActiveIndex - 1 + items.length) % items.length;
    updateGlobalSearchSelection();
  } else if (e.key === 'Enter') {
    e.preventDefault();
    if (globalSearchActiveIndex >= 0 && globalSearchActiveIndex < items.length) {
      selectGlobalSearchResult(globalSearchActiveIndex);
    }
  }
}

function updateGlobalSearchSelection() {
  document.querySelectorAll('.gs-result-item').forEach((el, idx) => {
    const isSelected = idx === globalSearchActiveIndex;
    el.classList.toggle('selected', isSelected);
    el.setAttribute('aria-selected', isSelected ? 'true' : 'false');
    if (isSelected) {
      el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  });
}

function selectGlobalSearchResult(index) {
  const item = globalSearchResultsData[index];
  if (!item) return;

  playSfx('launch');
  closeGlobalSearch();

  if (item.category === 'CHARACTER' && item.deep_link_params?.character_slug) {
    selectCharacter(item.deep_link_params.character_slug);
    const el = document.getElementById('fighters');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
    showToast(`Selected fighter: ${item.character_name}`, 'info');
  } else if (item.category === 'MOVE') {
    if (item.deep_link_params?.character_slug) {
      selectCharacter(item.deep_link_params.character_slug);
    }
    const movesEl = document.getElementById('moves');
    if (movesEl) movesEl.scrollIntoView({ behavior: 'smooth' });
    if (item.deep_link_params?.move_id) {
      setTimeout(() => openMoveDetailModal(item.deep_link_params.move_id), 400);
    }
    showToast(`Loaded move: ${item.title}`, 'info');
  } else if (item.category === 'COMBO') {
    if (item.deep_link_params?.character_slug) {
      state.comboFinder.p1Slug = item.deep_link_params.character_slug;
      const fSel = document.getElementById('comboLabFighterSelect');
      if (fSel) fSel.value = item.deep_link_params.character_slug;
      loadComboFinderFighter('p1').then(() => renderComboLab());
    }
    const comboEl = document.getElementById('combo-lab');
    if (comboEl) comboEl.scrollIntoView({ behavior: 'smooth' });
    showToast(`Navigated to combo: ${item.title}`, 'info');
  } else if (item.category === 'STAGE' && item.deep_link_params?.stage_id) {
    selectStage(item.deep_link_params.stage_id);
    const stEl = document.getElementById('stages');
    if (stEl) stEl.scrollIntoView({ behavior: 'smooth' });
    showToast(`Selected stage: ${item.title}`, 'info');
  }
}

// ==========================================================================
// Phase 6: User Practice Notes (CRUD & Manager)
// ==========================================================================
function getPracticeNotes() {
  try {
    const raw = localStorage.getItem('tekken8_practice_notes');
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (e) {
    console.warn('Failed to read practice notes from localStorage:', e);
    return [];
  }
}

function savePracticeNotesArray(notes) {
  try {
    localStorage.setItem('tekken8_practice_notes', JSON.stringify(notes));
    updateNotesCountBadge();
    return true;
  } catch (e) {
    console.error('Failed to save practice notes to localStorage:', e);
    showToast('Storage quota exceeded or storage blocked', 'error');
    return false;
  }
}

function updateNotesCountBadge() {
  const notes = getPracticeNotes();
  const pills = document.querySelectorAll('#notesCountPill');
  pills.forEach(p => {
    p.textContent = notes.length;
    p.style.display = notes.length > 0 ? 'inline-block' : 'none';
  });
}

function openPracticeNotesModal() {
  playSfx('click');
  const modal = document.getElementById('practiceNotesModal');
  if (!modal) return;

  const charSelect = document.getElementById('notesCharacterFilter');
  if (charSelect && state.characters) {
    const curVal = charSelect.value || 'ALL';
    charSelect.innerHTML = `<option value="ALL">All Fighters</option>` +
      state.characters.map(c => `<option value="${c.slug}">${c.name}</option>`).join('');
    charSelect.value = curVal;
  }

  renderPracticeNotesList();
  modal.style.display = 'flex';
}

function closePracticeNotesModal() {
  playSfx('click');
  const modal = document.getElementById('practiceNotesModal');
  if (modal) modal.style.display = 'none';
}

function renderPracticeNotesList() {
  const container = document.getElementById('practiceNotesListContainer');
  if (!container) return;

  const notes = getPracticeNotes();
  const searchQ = (document.getElementById('notesSearchInput')?.value || '').toLowerCase().trim();
  const charFilter = document.getElementById('notesCharacterFilter')?.value || 'ALL';
  const catFilter = document.getElementById('notesCategoryFilter')?.value || 'ALL';

  const filtered = notes.filter(n => {
    if (charFilter !== 'ALL' && n.characterSlug !== charFilter) return false;
    if (catFilter !== 'ALL' && n.category !== catFilter) return false;
    if (searchQ) {
      const matchLabel = (n.targetLabel || '').toLowerCase().includes(searchQ);
      const matchContent = (n.content || '').toLowerCase().includes(searchQ);
      const matchCat = (n.category || '').toLowerCase().includes(searchQ);
      if (!matchLabel && !matchContent && !matchCat) return false;
    }
    return true;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="empty-state-card" style="padding:2.5rem 1rem;">
        <div class="empty-icon">📝</div>
        <h4 class="empty-title">No Practice Notes Found</h4>
        <p class="empty-desc">Create personal matchup cues, timing reminders, and execution notes across moves and combos.</p>
        <button type="button" class="btn btn-primary" onclick="openPracticeNoteEditModal(null)">+ Create First Note</button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(n => {
    const formattedDate = n.updatedAt ? new Date(n.updatedAt).toLocaleDateString() : 'Recent';
    return `
      <div class="practice-note-card" id="note_card_${n.id}">
        <div class="pnc-header">
          <div class="pnc-meta">
            <span class="user-practice-note-badge" title="User-created personal practice note. Not verified official frame data.">📝 USER PRACTICE NOTE</span>
            <span class="pnc-category">${escapeHtml(n.category || 'General')}</span>
            <span class="pnc-fighter">${escapeHtml(n.characterName || 'Tekken Warrior')}</span>
          </div>
          <div class="pnc-actions">
            <button type="button" class="btn-tb-reset" onclick="openPracticeNoteEditModal('${n.id}')">Edit</button>
            <button type="button" class="btn-tb-reset danger" onclick="deletePracticeNote('${n.id}')">Delete</button>
          </div>
        </div>
        <div class="pnc-target">${escapeHtml(n.targetLabel || 'General Practice Note')}</div>
        <div class="pnc-content">${escapeHtml(n.content || '')}</div>
        <div class="pnc-footer">
          <span>Saved locally: ${formattedDate}</span>
          ${n.targetType === 'MOVE' ? `<button type="button" class="btn-pnc-link" onclick="goToMoveFromNote('${n.characterSlug}', '${n.targetKey}')">View Move &rarr;</button>` : ''}
        </div>
      </div>
    `;
  }).join('');
}

function openPracticeNoteEditModal(noteId = null, defaultTarget = null) {
  playSfx('click');
  const modal = document.getElementById('practiceNoteEditModal');
  if (!modal) return;

  const idInput = document.getElementById('noteEditId');
  const targetKeyInput = document.getElementById('noteEditTargetKey');
  const targetTypeInput = document.getElementById('noteEditTargetType');
  const labelInput = document.getElementById('noteEditTargetLabel');
  const charSelect = document.getElementById('noteEditCharacterSlug');
  const catSelect = document.getElementById('noteEditCategory');
  const contentInput = document.getElementById('noteEditContent');
  const titleEl = document.getElementById('noteEditModalTitle');

  if (charSelect && state.characters) {
    charSelect.innerHTML = state.characters.map(c => `<option value="${c.slug}">${c.name}</option>`).join('');
  }

  if (noteId) {
    const notes = getPracticeNotes();
    const note = notes.find(n => n.id === noteId);
    if (note) {
      if (titleEl) titleEl.textContent = 'EDIT PRACTICE NOTE';
      if (idInput) idInput.value = note.id;
      if (targetKeyInput) targetKeyInput.value = note.targetKey || '';
      if (targetTypeInput) targetTypeInput.value = note.targetType || 'MOVE';
      if (labelInput) labelInput.value = note.targetLabel || '';
      if (charSelect) charSelect.value = note.characterSlug || 'jin';
      if (catSelect) catSelect.value = note.category || 'Execution Tip';
      if (contentInput) contentInput.value = note.content || '';
    }
  } else {
    if (titleEl) titleEl.textContent = 'NEW PRACTICE NOTE';
    if (idInput) idInput.value = '';
    if (targetKeyInput) targetKeyInput.value = defaultTarget?.key || '';
    if (targetTypeInput) targetTypeInput.value = defaultTarget?.type || 'MOVE';
    if (labelInput) labelInput.value = defaultTarget?.label || '';
    if (charSelect) charSelect.value = defaultTarget?.characterSlug || state.selectedCharacter?.slug || 'jin';
    if (catSelect) catSelect.value = defaultTarget?.category || 'Execution Tip';
    if (contentInput) contentInput.value = defaultTarget?.content || '';
  }

  modal.style.display = 'flex';
  if (contentInput) setTimeout(() => contentInput.focus(), 80);
}

function closePracticeNoteEditModal() {
  playSfx('click');
  const modal = document.getElementById('practiceNoteEditModal');
  if (modal) modal.style.display = 'none';
}

function savePracticeNoteFromModal() {
  playSfx('click');
  const idInput = document.getElementById('noteEditId');
  const targetKeyInput = document.getElementById('noteEditTargetKey');
  const targetTypeInput = document.getElementById('noteEditTargetType');
  const labelInput = document.getElementById('noteEditTargetLabel');
  const charSelect = document.getElementById('noteEditCharacterSlug');
  const catSelect = document.getElementById('noteEditCategory');
  const contentInput = document.getElementById('noteEditContent');

  const content = (contentInput?.value || '').trim();
  if (!content) {
    showToast('Please enter note content', 'warning');
    return;
  }

  const notes = getPracticeNotes();
  const noteId = idInput?.value || ('note_' + Date.now() + '_' + Math.random().toString(36).substring(2, 6));
  const charSlug = charSelect?.value || 'jin';
  const charObj = state.characters?.find(c => c.slug === charSlug);

  const existingIdx = notes.findIndex(n => n.id === noteId);
  const noteObj = {
    id: noteId,
    targetKey: targetKeyInput?.value || `general_${Date.now()}`,
    targetType: targetTypeInput?.value || 'GENERAL',
    targetLabel: labelInput?.value || 'General Practice Note',
    characterSlug: charSlug,
    characterName: charObj ? charObj.name : 'Tekken Warrior',
    category: catSelect?.value || 'General',
    content: content,
    updatedAt: new Date().toISOString()
  };

  if (existingIdx >= 0) {
    notes[existingIdx] = { ...notes[existingIdx], ...noteObj };
  } else {
    noteObj.createdAt = new Date().toISOString();
    notes.unshift(noteObj);
  }

  if (savePracticeNotesArray(notes)) {
    closePracticeNoteEditModal();
    renderPracticeNotesList();
    showToast('Practice note saved successfully!', 'success');
  }
}

function deletePracticeNote(noteId) {
  playSfx('click');
  if (!confirm('Are you sure you want to delete this practice note?')) return;
  const notes = getPracticeNotes().filter(n => n.id !== noteId);
  savePracticeNotesArray(notes);
  renderPracticeNotesList();
  showToast('Practice note removed', 'info');
}

function goToMoveFromNote(charSlug, moveKey) {
  closePracticeNotesModal();
  selectCharacter(charSlug);
  const el = document.getElementById('moves');
  if (el) el.scrollIntoView({ behavior: 'smooth' });
}

// ==========================================================================
// Phase 6: Notation Reference Guide Modal
// ==========================================================================
function openNotationGuideModal() {
  playSfx('click');
  const modal = document.getElementById('notationGuideModal');
  if (modal) modal.style.display = 'flex';
}

function closeNotationGuideModal() {
  playSfx('click');
  const modal = document.getElementById('notationGuideModal');
  if (modal) modal.style.display = 'none';
}

// ==========================================================================
// Phase 6: Shareable URLs & State Restoration
// ==========================================================================
function generateShareableUrl() {
  const url = new URL(window.location.origin + window.location.pathname);
  const p1Slug = state.matchup?.player?.slug || state.comboFinder?.p1Slug || state.selectedCharacter?.slug || 'jin';
  const p2Slug = state.matchup?.opponent?.slug || state.comboFinder?.p2Slug || 'kazuya';
  const stageSlug = state.matchup?.stage?.slug || (state.stages && state.stages[0]?.slug) || 'the-arena';

  url.searchParams.set('p1', p1Slug);
  url.searchParams.set('p2', p2Slug);
  url.searchParams.set('stage', stageSlug);
  if (state.controllerLayout) {
    url.searchParams.set('layout', state.controllerLayout);
  }
  return url.toString();
}

function copyShareableUrl() {
  playSfx('click');
  const shareUrl = generateShareableUrl();
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(shareUrl).then(() => {
      showToast('Matchup & State URL copied to clipboard!', 'success');
    }).catch(() => {
      fallbackCopyText(shareUrl);
    });
  } else {
    fallbackCopyText(shareUrl);
  }
}

function fallbackCopyText(text) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.select();
  try {
    document.execCommand('copy');
    showToast('Matchup & State URL copied to clipboard!', 'success');
  } catch (e) {
    prompt('Copy your shareable URL:', text);
  }
  document.body.removeChild(ta);
}

function restoreStateFromUrl() {
  try {
    const params = new URLSearchParams(window.location.search);
    const p1Param = params.get('p1');
    const p2Param = params.get('p2');
    const stageParam = params.get('stage');
    const layoutParam = params.get('layout');

    if (layoutParam && ['ARCADE', 'PLAYSTATION', 'XBOX'].includes(layoutParam.toUpperCase())) {
      setControllerLayout(layoutParam.toUpperCase());
    }

    if (p1Param && state.characters) {
      const p1Char = state.characters.find(c => c.slug.toLowerCase() === p1Param.toLowerCase());
      if (p1Char) {
        selectCharacter(p1Char.slug);
        if (state.comboFinder) state.comboFinder.p1Slug = p1Char.slug;
      }
    }

    if (p2Param && state.characters) {
      const p2Char = state.characters.find(c => c.slug.toLowerCase() === p2Param.toLowerCase());
      if (p2Char && state.comboFinder) {
        state.comboFinder.p2Slug = p2Char.slug;
        const oSelect = document.getElementById('comboLabOpponentSelect');
        if (oSelect) oSelect.value = p2Char.slug;
      }
    }

    if (stageParam && state.stages) {
      const st = state.stages.find(s => s.slug.toLowerCase() === stageParam.toLowerCase());
      if (st) {
        selectStage(st.id);
      }
    }
  } catch (err) {
    console.warn('URL state restoration skipped:', err);
  }
}

// Window global exports for Phase 6 features
window.initGlobalSearch = initGlobalSearch;
window.openGlobalSearch = openGlobalSearch;
window.closeGlobalSearch = closeGlobalSearch;
window.setGlobalSearchCategory = setGlobalSearchCategory;
window.selectGlobalSearchResult = selectGlobalSearchResult;
window.openPracticeNotesModal = openPracticeNotesModal;
window.closePracticeNotesModal = closePracticeNotesModal;
window.renderPracticeNotesList = renderPracticeNotesList;
window.openPracticeNoteEditModal = openPracticeNoteEditModal;
window.closePracticeNoteEditModal = closePracticeNoteEditModal;
window.savePracticeNoteFromModal = savePracticeNoteFromModal;
window.deletePracticeNote = deletePracticeNote;
window.goToMoveFromNote = goToMoveFromNote;
window.openNotationGuideModal = openNotationGuideModal;
window.closeNotationGuideModal = closeNotationGuideModal;
window.generateShareableUrl = generateShareableUrl;
window.copyShareableUrl = copyShareableUrl;

// ==========================================================================
// Master Compendium & Pro Tactics Hub Module (Parts 1 to 26)
// ==========================================================================

function renderProTacticsRelativityCard(data) {
  const card = document.getElementById('proTacticsRelativityCard');
  if (!card) return;

  const p1 = data.player_character;
  const p2 = data.opponent_character;

  // 1. Weak Sidestep (Part 5)
  const ss = data.opponent_sidestep_guide;
  const ssBadge = document.getElementById('proOpponentWeakSideBadge');
  const ssHead = document.getElementById('ptOpponentSidestepHeading');
  const ssDesc = document.getElementById('ptOpponentSidestepDesc');
  const ssTag = document.getElementById('ptOpponentWhiffTag');
  if (ss) {
    const side = ss.weak_side || 'SSL';
    if (ssBadge) ssBadge.textContent = side;
    if (ssHead) ssHead.textContent = `Weak Side: ${side}`;
    if (ssDesc) ssDesc.textContent = ss.details || ss.whiff_notes || `Step towards ${side} outside close jab range.`;
    if (ssTag) ssTag.textContent = `Whiffs on step: ${ss.whiffs_on_step || ss.whiff_notes || 'Linear approach attacks'}`;
  } else {
    if (ssBadge) ssBadge.textContent = 'NEUTRAL';
    if (ssHead) ssHead.textContent = `Weak Side: Adaptive Neutral`;
    if (ssDesc) ssDesc.textContent = `Observe ${p2.name}'s tendencies. Avoid sidewalking into homing moves.`;
    if (ssTag) ssTag.textContent = `Whiffs on step: Linear strings`;
  }

  // 2. Command Throw Break (Part 8)
  const tb = data.opponent_throw_break_guide;
  const tbHead = document.getElementById('ptOpponentThrowHeading');
  const tbDesc = document.getElementById('ptOpponentThrowDesc');
  const tbTag = document.getElementById('ptOpponentThrowBreakTag');
  if (tb) {
    if (tbHead) tbHead.textContent = `${p2.name}: ${tb.throw_name} (${tb.input_notation || 'Command Grab'})`;
    if (tbDesc) tbDesc.textContent = tb.break_guide;
    if (tbTag) {
      const match = tb.break_guide ? tb.break_guide.match(/Break\s+([0-9\+]+)/i) : null;
      tbTag.textContent = match ? `Guaranteed Break: ${match[1]}` : tb.break_guide;
    }
  } else {
    if (tbHead) tbHead.textContent = `${p2.name}: Generic Throws (1+3 / 2+4)`;
    if (tbDesc) tbDesc.textContent = `Generic throws are breakable with either 1 or 2. Watch for 1+2 break on command grabs.`;
    if (tbTag) tbTag.textContent = `Standard Break: 1 or 2`;
  }

  // 3. Anti-Cheese & Scrub String (Part 14)
  const ac = data.opponent_anti_cheese_guide;
  const acHead = document.getElementById('ptOpponentCheeseHeading');
  const acDesc = document.getElementById('ptOpponentCheeseDesc');
  const acTag = document.getElementById('ptOpponentCheeseCounterTag');
  if (ac) {
    if (acHead) acHead.textContent = `Spammed Trap: ${ac.cheese_move}`;
    if (acDesc) acDesc.textContent = ac.pro_counter;
    if (acTag) acTag.textContent = `Trap Reason: ${ac.why_players_lose}`;
  } else {
    if (acHead) acHead.textContent = `Patience vs ${p2.name} Strings`;
    if (acDesc) acDesc.textContent = `Do not challenge safe mid pokes. Use i10 jab to check slow extensions.`;
    if (acTag) acTag.textContent = `Counter: Patient Guard`;
  }

  // 4. Character Install & Meter (Part 23)
  const inst = data.opponent_install_guide;
  const instHead = document.getElementById('ptOpponentInstallHeading');
  const instDesc = document.getElementById('ptOpponentInstallDesc');
  const instTag = document.getElementById('ptOpponentInstallTag');
  if (inst) {
    if (instHead) instHead.textContent = `${inst.install_name}`;
    if (instDesc) instDesc.textContent = `Activation: ${inst.activation} — Threat: ${inst.unlocks_danger}`;
    if (instTag) instTag.textContent = `Status: Active Buff Hazard`;
  } else {
    if (instHead) instHead.textContent = `Heat System Standard`;
    if (instDesc) instDesc.textContent = `${p2.name} relies on standard Heat Dash, Heat Burst (+2 on hit), and Heat Smash mixups.`;
    if (instTag) instTag.textContent = `Status: Standard Engine`;
  }

  // 5. 10-Hit Combo Counter (Part 19)
  const th = data.opponent_ten_hit_guide;
  const thHead = document.getElementById('ptOpponentTenHitHeading');
  const thDesc = document.getElementById('ptOpponentTenHitDesc');
  const thTag = document.getElementById('ptOpponentTenHitTag');
  if (th) {
    if (thHead) thHead.textContent = `${th.ten_hit_name}`;
    if (thDesc) thDesc.textContent = th.how_to_counter;
    if (thTag) thTag.textContent = `Interrupt Point: Verified`;
  } else {
    if (thHead) thHead.textContent = `String Interrupts`;
    if (thDesc) thDesc.textContent = `Look for duckable high hits or low-parryable sweep hits inside multi-hit strings.`;
    if (thTag) thTag.textContent = `Interrupt: Standard Duck/Parry`;
  }

  // 6. Player Wall Combo Ender (Part 22)
  const we = data.player_wall_combo_guide;
  const weHead = document.getElementById('ptPlayerWallEnderHeading');
  const weDesc = document.getElementById('ptPlayerWallEnderDesc');
  const weTag = document.getElementById('ptPlayerWallEnderTag');
  if (we) {
    if (weHead) weHead.textContent = `${p1.name} Optimal: ${we.wall_ender_optimal}`;
    if (weDesc) weDesc.textContent = we.damage_utility;
    if (weTag) weTag.textContent = `Optimal Wall Splat Route`;
  } else {
    if (weHead) weHead.textContent = `${p1.name} Wall Ender`;
    if (weDesc) weDesc.textContent = `Use high-damage 3-hit string or ground-pound stomp for guaranteed oki on wall splat.`;
    if (weTag) weTag.textContent = `Standard Wall Ender`;
  }
}

// Tactics Compendium Cache & State
if (!window.tacticsState) {
  window.tacticsState = {
    currentTab: 'sidesteps',
    cache: {},
    searchTerm: ''
  };
}

async function openTacticsHubModal(defaultTab = 'sidesteps') {
  playSfx('click');
  const modal = document.getElementById('tacticsHubModal');
  if (modal) modal.style.display = 'flex';
  await switchTacticsTab(defaultTab);
}

function closeTacticsHubModal() {
  playSfx('click');
  const modal = document.getElementById('tacticsHubModal');
  if (modal) modal.style.display = 'none';
}

async function switchTacticsTab(tabName) {
  window.tacticsState.currentTab = tabName;

  // Update tab buttons
  const tabs = document.querySelectorAll('.tactics-tab-btn');
  tabs.forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-tab') === tabName);
  });

  const searchInput = document.getElementById('tacticsCompendiumSearch');
  const query = searchInput ? searchInput.value.trim() : '';

  await loadAndRenderTacticsData(tabName, query);
}

async function loadAndRenderTacticsData(tabName, query = '') {
  const container = document.getElementById('tacticsCompendiumContent');
  const countLabel = document.getElementById('tacticsEntryCountLabel');
  if (!container) return;

  container.innerHTML = '<div style="padding:2rem; text-align:center; color:var(--text-muted);"><div class="spinner-neon" style="margin:0 auto 1rem;"></div>Loading verified compendium records...</div>';

  let endpoint = '';
  switch(tabName) {
    case 'sidesteps': endpoint = '/guides/sidesteps'; break;
    case 'throw-breaks': endpoint = '/guides/throw-breaks'; break;
    case 'anti-cheese': endpoint = '/guides/anti-cheese'; break;
    case 'installs': endpoint = '/guides/installs'; break;
    case 'wall-combos': endpoint = '/guides/wall-combos'; break;
    case 'ten-hit': endpoint = '/guides/ten-hit-combos'; break;
    case 'heat-smashes': endpoint = '/guides/heat-smashes'; break;
    case 'movement': endpoint = '/guides/movement-bible'; break;
    case 'hardware': endpoint = '/guides/hardware-settings'; break;
    case 'emergency': endpoint = '/guides/emergency-protocol'; break;
    default: endpoint = '/guides/sidesteps';
  }

  try {
    const data = await fetchAPI(endpoint, true);
    window.tacticsState.cache[tabName] = data;
    renderTacticsUI(tabName, data, query);
  } catch(err) {
    container.innerHTML = `<div style="padding:2rem; text-align:center; color:var(--accent-red);">Failed to load guide records: ${err.message}</div>`;
  }
}

function renderTacticsUI(tabName, rawData, query = '') {
  const container = document.getElementById('tacticsCompendiumContent');
  const countLabel = document.getElementById('tacticsEntryCountLabel');
  if (!container) return;

  const q = query.toLowerCase().trim();

  if (tabName === 'hardware') {
    renderHardwareGuide(container, rawData);
    if (countLabel) countLabel.textContent = 'Hardware zero-lag latency optimization & controller specs';
    return;
  }

  if (!Array.isArray(rawData)) {
    container.innerHTML = '<div style="padding:2rem; text-align:center; color:var(--text-muted);">No records found.</div>';
    return;
  }

  // Filter
  const filtered = q ? rawData.filter(item => {
    return Object.values(item).some(val => typeof val === 'string' && val.toLowerCase().includes(q));
  }) : rawData;

  if (countLabel) {
    countLabel.textContent = `Showing ${filtered.length} of ${rawData.length} entries`;
  }

  if (filtered.length === 0) {
    container.innerHTML = `<div class="empty-state-card" style="margin:2rem auto;"><div class="empty-icon">🔍</div><h4 class="empty-title">No matching entries found</h4><p class="empty-desc">No entries match your search query "${query}".</p></div>`;
    return;
  }

  if (tabName === 'sidesteps') {
    container.innerHTML = `
      <table class="analyzer-table tactics-table">
        <thead>
          <tr>
            <th>Character</th>
            <th>Weak Side</th>
            <th>Whiff Exploit &amp; Linear Moves</th>
          </tr>
        </thead>
        <tbody>
          ${filtered.map(row => {
            const side = row.weak_side || '';
            const isLeft = side.includes('SSL');
            const isRight = side.includes('SSR');
            const badgeCls = isLeft ? 'ssl' : (isRight ? 'ssr' : 'neutral');
            return `
              <tr>
                <td><strong>${row.character}</strong></td>
                <td><span class="sidestep-badge-pill ${badgeCls}">${side}</span></td>
                <td>${row.whiff_notes || row.details || '—'}</td>
              </tr>
            `;
          }).join('')}
        </tbody>
      </table>
    `;
  } else if (tabName === 'throw-breaks') {
    container.innerHTML = `
      <table class="analyzer-table tactics-table">
        <thead>
          <tr>
            <th>Character</th>
            <th>Throw Name</th>
            <th>Input</th>
            <th>Visual Hand Cue &amp; Guaranteed Break</th>
          </tr>
        </thead>
        <tbody>
          ${filtered.map(row => `
            <tr>
              <td><strong>${row.character}</strong></td>
              <td><span style="color:var(--accent-gold); font-weight:700;">${row.throw_name}</span></td>
              <td><code>${formatTekkenNotation(row.input_notation || '')}</code></td>
              <td><span class="break-subtag">${row.break_guide}</span></td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  } else if (tabName === 'anti-cheese') {
    container.innerHTML = `
      <div class="compendium-cards-grid">
        ${filtered.map(row => `
          <div class="compendium-tactic-card">
            <div class="ctc-header">
              <span class="ctc-char">${row.character}</span>
              <span class="ctc-move">${row.cheese_move}</span>
            </div>
            <div class="ctc-problem"><strong>Why Players Lose:</strong> ${row.why_players_lose}</div>
            <div class="ctc-solution"><strong>Pro Counter:</strong> ${row.pro_counter}</div>
          </div>
        `).join('')}
      </div>
    `;
  } else if (tabName === 'installs') {
    container.innerHTML = `
      <div class="compendium-cards-grid">
        ${filtered.map(row => `
          <div class="compendium-tactic-card install-card">
            <div class="ctc-header">
              <span class="ctc-char">${row.character}</span>
              <span class="ctc-move" style="color:var(--accent-cyan);">${row.install_name}</span>
            </div>
            <div class="ctc-problem"><strong>Activation:</strong> ${row.activation}</div>
            <div class="ctc-solution" style="color:var(--accent-pink);"><strong>Danger / Unlocks:</strong> ${row.unlocks_danger}</div>
          </div>
        `).join('')}
      </div>
    `;
  } else if (tabName === 'wall-combos') {
    container.innerHTML = `
      <table class="analyzer-table tactics-table">
        <thead>
          <tr>
            <th>Character</th>
            <th>Optimal Wall Ender</th>
            <th>Damage &amp; Utility Notes</th>
          </tr>
        </thead>
        <tbody>
          ${filtered.map(row => `
            <tr>
              <td><strong>${row.character}</strong></td>
              <td><span style="color:var(--accent-cyan); font-weight:700;">${row.wall_ender_optimal}</span></td>
              <td>${row.damage_utility}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  } else if (tabName === 'ten-hit') {
    container.innerHTML = `
      <table class="analyzer-table tactics-table">
        <thead>
          <tr>
            <th>Character</th>
            <th>10-Hit Combo Name</th>
            <th>Counter / Low Parry / Duck Window</th>
          </tr>
        </thead>
        <tbody>
          ${filtered.map(row => `
            <tr>
              <td><strong>${row.character}</strong></td>
              <td><span style="color:var(--accent-gold);">${row.ten_hit_name}</span></td>
              <td><span class="counter-subtag">${row.how_to_counter}</span></td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  } else if (tabName === 'heat-smashes') {
    container.innerHTML = `
      <div class="compendium-cards-grid">
        ${filtered.map(row => `
          <div class="compendium-tactic-card">
            <div class="ctc-header">
              <span class="ctc-char">${row.category || 'Heat Smash'}</span>
              <span class="ctc-move" style="color:var(--accent-gold);">${row.advantage_on_block || ''}</span>
            </div>
            <div class="ctc-problem"><strong>Properties:</strong> ${row.properties || ''}</div>
            <div class="ctc-solution"><strong>Tactical Counter:</strong> ${row.counter_strategy || row.description || ''}</div>
          </div>
        `).join('')}
      </div>
    `;
  } else if (tabName === 'movement') {
    container.innerHTML = `
      <div class="compendium-cards-grid">
        ${filtered.map(row => `
          <div class="compendium-tactic-card">
            <div class="ctc-header">
              <span class="ctc-char" style="color:var(--accent-cyan);">${row.technique}</span>
              <span class="ctc-move">${row.input_execution || ''}</span>
            </div>
            <div class="ctc-problem"><strong>Execution Detail:</strong> ${row.details || row.execution || ''}</div>
            <div class="ctc-solution"><strong>Tactical Application:</strong> ${row.tactical_use || row.application || ''}</div>
          </div>
        `).join('')}
      </div>
    `;
  } else if (tabName === 'emergency') {
    container.innerHTML = `
      <div class="compendium-cards-grid">
        ${filtered.map(row => `
          <div class="compendium-tactic-card emergency-card">
            <div class="ctc-header">
              <span class="ctc-char" style="color:var(--accent-red);">${row.scenario || 'Blender Scenario'}</span>
              <span class="ctc-move">${row.urgency || 'HIGH'}</span>
            </div>
            <div class="ctc-problem"><strong>Panic Trigger:</strong> ${row.situation || ''}</div>
            <div class="ctc-solution" style="color:var(--accent-gold);"><strong>Safe Response:</strong> ${row.action || row.solution || ''}</div>
          </div>
        `).join('')}
      </div>
    `;
  }
}

function renderHardwareGuide(container, data) {
  if (!data) return;
  const cfg = data.pc_zero_lag_config || {};
  const ctl = data.controllers || [];

  container.innerHTML = `
    <div class="hardware-guide-layout">
      <div class="dash-card">
        <h4 style="color:var(--accent-cyan); margin-bottom:0.75rem;">⚡ Zero-Lag PC &amp; Tournament Display Configuration</h4>
        <div class="hardware-specs-grid">
          <div class="hw-spec-item"><strong>V-Sync:</strong> ${cfg.vsync || 'OFF (Enables lowest frame delivery latency)'}</div>
          <div class="hw-spec-item"><strong>NVIDIA Reflex:</strong> ${cfg.nvidia_reflex || 'ON + BOOST (GPU latency reduction)'}</div>
          <div class="hw-spec-item"><strong>Frame Rate:</strong> ${cfg.framerate_cap || 'Locked 60 FPS (Tekken 8 physics engine lock)'}</div>
          <div class="hw-spec-item"><strong>Display Mode:</strong> ${cfg.display_mode || 'Exclusive Fullscreen (Bypasses DWM compositor)'}</div>
          <div class="hw-spec-item"><strong>USB Polling:</strong> ${cfg.usb_polling || '1000 Hz / 1ms (Overclocked Controller)'}</div>
          <div class="hw-spec-item"><strong>SOCD Rule:</strong> ${cfg.socd_cleaner || 'Neutral SOCD (Left+Right=N, Up+Down=N) - Tournament Legal'}</div>
        </div>
      </div>
      <div class="dash-card" style="margin-top:1rem;">
        <h4 style="color:var(--accent-gold); margin-bottom:0.75rem;">🕹️ Controller Latency &amp; Input Comparison</h4>
        <div class="compendium-cards-grid">
          ${ctl.map(c => `
            <div class="compendium-tactic-card">
              <div class="ctc-header">
                <span class="ctc-char">${c.type}</span>
                <span class="ctc-move" style="color:var(--accent-cyan);">${c.input_latency || ''}</span>
              </div>
              <div class="ctc-problem"><strong>Pros:</strong> ${c.pros || ''}</div>
              <div class="ctc-solution"><strong>Cons &amp; Notes:</strong> ${c.cons || ''}</div>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
}

function filterTacticsCompendium() {
  const searchInput = document.getElementById('tacticsCompendiumSearch');
  const query = searchInput ? searchInput.value : '';
  const tabName = window.tacticsState.currentTab || 'sidesteps';
  const cachedData = window.tacticsState.cache[tabName];
  if (cachedData) {
    renderTacticsUI(tabName, cachedData, query);
  } else {
    loadAndRenderTacticsData(tabName, query);
  }
}

function clearTacticsSearch() {
  const searchInput = document.getElementById('tacticsCompendiumSearch');
  if (searchInput) {
    searchInput.value = '';
    filterTacticsCompendium();
    searchInput.focus();
  }
}

// Window global exports for Compendium
window.openTacticsHubModal = openTacticsHubModal;
window.closeTacticsHubModal = closeTacticsHubModal;
window.switchTacticsTab = switchTacticsTab;
window.filterTacticsCompendium = filterTacticsCompendium;
window.clearTacticsSearch = clearTacticsSearch;
window.renderProTacticsRelativityCard = renderProTacticsRelativityCard;




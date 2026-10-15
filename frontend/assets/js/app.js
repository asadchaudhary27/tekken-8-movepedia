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
    }
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
      const res = await fetch(`/api/v1${endpoint}`);
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
  if (trimmed.includes('>') || trimmed.includes('→')) {
    const steps = trimmed.split(/\s*(?:>|->|=>|→)\s*/);
    return `<div class="tk-combo-sequence">${steps.map(s => formatSingleStep(s)).join('<span class="tk-next-arrow">›</span>')}</div>`;
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
      bodyHtml += '<span class="tk-sep-chip">,</span>';
    } else if (t === '~') {
      bodyHtml += '<span class="tk-sep-chip">~</span>';
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
  if (norm === '1') return '<span class="tk-btn-chip tk-btn-1" title="Left Punch (1)">1</span>';
  if (norm === '2') return '<span class="tk-btn-chip tk-btn-2" title="Right Punch (2)">2</span>';
  if (norm === '3') return '<span class="tk-btn-chip tk-btn-3" title="Left Kick (3)">3</span>';
  if (norm === '4') return '<span class="tk-btn-chip tk-btn-4" title="Right Kick (4)">4</span>';
  if (norm === '1+2') return '<span class="tk-btn-chip tk-btn-1-2" title="1+2 (LP+RP)">1+2</span>';
  if (norm === '3+4') return '<span class="tk-btn-chip tk-btn-3-4" title="3+4 (LK+RK)">3+4</span>';
  if (norm === '1+4') return '<span class="tk-btn-chip tk-btn-multi" title="1+4 (LP+RK)">1+4</span>';
  if (norm === '2+3') return '<span class="tk-btn-chip tk-btn-multi" title="2+3 (RP+LK)">2+3</span>';
  if (norm === '1+3') return '<span class="tk-btn-chip tk-btn-1-2" title="1+3 (Throw)">1+3</span>';
  if (norm === '2+4') return '<span class="tk-btn-chip tk-btn-3-4" title="2+4 (Throw)">2+4</span>';
  if (/^[1-4\+]+$/.test(norm)) return `<span class="tk-btn-chip tk-btn-multi">${norm}</span>`;
  return null;
}

// 1. Initial Load
document.addEventListener('DOMContentLoaded', async () => {
  setupEventListeners();
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
});

// Event Listeners Setup
function setupEventListeners() {
  // Notation Input
  const notInput = document.getElementById('notationInput');
  if (notInput) {
    notInput.addEventListener('input', debounce(updateNotationDisplay, 150));
  }

  // Controller Toggles
  document.querySelectorAll('.ctl-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.ctl-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      state.controllerLayout = e.target.dataset.layout;
      updateNotationDisplay();
    });
  });

  // Carousel Filters
  document.querySelectorAll('#carouselFilterPills .filter-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('#carouselFilterPills .filter-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      state.activeFilter = e.target.dataset.filter;
      renderCarousel();
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

  // Carousel Navigation Buttons (< and >) & Side-Scroll Mousewheel
  const prevBtn = document.getElementById('carouselPrevBtn');
  const nextBtn = document.getElementById('carouselNextBtn');
  const track = document.getElementById('carouselTrack');
  if (prevBtn && track) {
    prevBtn.addEventListener('click', () => {
      track.scrollBy({ left: -260, behavior: 'smooth' });
    });
  }
  if (nextBtn && track) {
    nextBtn.addEventListener('click', () => {
      track.scrollBy({ left: 260, behavior: 'smooth' });
    });
  }
  if (track) {
    // Enable effortless horizontal side-scrolling via mouse wheel
    track.addEventListener('wheel', (e) => {
      if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
        e.preventDefault();
        track.scrollBy({ left: e.deltaY * 1.6, behavior: 'auto' });
      }
    }, { passive: false });
  }

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
}

// 2. Load & Render Characters
async function loadCharacters() {
  const data = await fetchAPI('/characters', true);
  if (data && Array.isArray(data)) {
    state.characters = data;
    renderCarousel();
    renderSidebarQuickFighters('ALL');
    
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

  const filtered = state.characters.filter(c => {
    if (state.activeFilter === 'ALL') return true;
    if (state.activeFilter === 'NEWCOMERS') return c.archetype && c.archetype.includes('Newcomers');
    if (state.activeFilter === 'MISHIMA') return c.archetype && c.archetype.includes('Mishima');
    if (state.activeFilter === 'ALLIES') return c.archetype && c.archetype.includes('Allies');
    if (state.activeFilter === 'REBELS') return c.archetype && c.archetype.includes('Rebels');
    return true;
  });

  if (filtered.length === 0) {
    track.innerHTML = '<div style="color:var(--text-muted); padding:1rem;">No fighters in this category.</div>';
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
               onerror="this.src='/assets/avatars/jin-brand-256-C1-oe_x3.webp'"/>
        </div>
        <div class="carousel-name">${c.name}</div>
      </div>
    `;
  }).join('');
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

  // Fetch moves for this fighter
  await loadMovesForCharacter(char.id);
}

// 3. Load & Render Moves Table
async function loadMovesForCharacter(characterId) {
  const data = await fetchAPI(`/moves?character_id=${characterId}`, true);
  state.moves = data || [];
  renderMovesTable(state.moves, true);
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

  tbody.innerHTML = pagedMoves.map(m => {
    const startupStr = m.startup_raw ? m.startup_raw : (m.startup_frames !== null ? `i${m.startup_frames}` : 'N/A');
    
    // Block Advantage styling
    let blockStr = 'N/A';
    let blockClass = 'frame-null';
    if (m.block_advantage_raw) {
      blockStr = m.block_advantage_raw;
      if (m.block_advantage !== null) {
        blockClass = m.block_advantage > 0 ? 'frame-plus' : (m.block_advantage < 0 ? 'frame-minus' : '');
      }
    } else if (m.block_advantage !== null) {
      blockStr = m.block_advantage > 0 ? `+${m.block_advantage}` : `${m.block_advantage}`;
      blockClass = m.block_advantage > 0 ? 'frame-plus' : (m.block_advantage < 0 ? 'frame-minus' : '');
    }

    // Hit Advantage styling
    let hitStr = 'N/A';
    let hitClass = 'frame-null';
    if (m.hit_advantage_raw) {
      hitStr = m.hit_advantage_raw;
      if (m.hit_advantage !== null) {
        hitClass = m.hit_advantage > 0 ? 'frame-plus' : (m.hit_advantage < 0 ? 'frame-minus' : '');
      }
    } else if (m.hit_advantage !== null) {
      hitStr = m.hit_advantage > 0 ? `+${m.hit_advantage}` : `${m.hit_advantage}`;
      hitClass = m.hit_advantage > 0 ? 'frame-plus' : (m.hit_advantage < 0 ? 'frame-minus' : '');
    }

    const dmgStr = m.damage !== null ? m.damage : '—';
    const hitLevel = m.hit_level ? m.hit_level.toUpperCase() : '—';

    // Move Property Badges
    const props = m.properties || [];
    const propBadges = props.map(p => {
      const pName = typeof p === 'string' ? p : p.property_name;
      if (pName.includes('heat')) return `<span class="feat-badge badge-launcher" style="padding:0.15rem 0.4rem; font-size:0.65rem;">HEAT</span>`;
      if (pName.includes('rage')) return `<span class="feat-badge badge-crush" style="padding:0.15rem 0.4rem; font-size:0.65rem;">RAGE</span>`;
      if (pName.includes('crush')) return `<span class="feat-badge badge-crush" style="padding:0.15rem 0.4rem; font-size:0.65rem;">CRUSH</span>`;
      if (pName.includes('launcher')) return `<span class="feat-badge badge-launcher" style="padding:0.15rem 0.4rem; font-size:0.65rem;">LAUNCH</span>`;
      if (pName.includes('tornado')) return `<span class="feat-badge badge-block" style="padding:0.15rem 0.4rem; font-size:0.65rem;">TORNADO</span>`;
      return `<span class="hazard-pill">${pName}</span>`;
    }).join(' ');

    return `
      <tr onclick="testNotationString('${m.original_notation}')" style="cursor:pointer;" title="Click to test in Notation Engine">
        <td style="font-weight:700; color:#fff;">${m.name}</td>
        <td>${formatTekkenNotation(m.original_notation)}</td>
        <td><span style="font-weight:800; color:var(--text-muted);">${hitLevel}</span></td>
        <td><span style="font-weight:700;">${startupStr}</span></td>
        <td><span class="${blockClass}">${blockStr}</span></td>
        <td><span class="${hitClass}">${hitStr}</span></td>
        <td><span style="font-weight:800; color:var(--accent-gold);">${dmgStr}</span></td>
        <td><div style="display:flex; gap:0.25rem; flex-wrap:wrap;">${propBadges || '—'}</div></td>
      </tr>
    `;
  }).join('');
}

function filterMovesTable(query) {
  if (!query) {
    renderMovesTable(state.moves, true);
    return;
  }
  const filtered = state.moves.filter(m => 
    m.name.toLowerCase().includes(query) ||
    m.original_notation.toLowerCase().includes(query) ||
    (m.hit_level && m.hit_level.toLowerCase().includes(query)) ||
    (m.properties && m.properties.some(p => (typeof p === 'string' ? p : p.property_name).toLowerCase().includes(query)))
  );
  renderMovesTable(filtered, true);
}

// 4. Render Stages Showcase
async function loadStages() {
  const data = await fetchAPI('/stages', true);
  if (data && Array.isArray(data) && data.length > 0) {
    state.stages = data;
  }
  renderStages();
}

function renderStages() {
  const container = document.getElementById('stagesGrid');
  if (!container) return;

  container.innerHTML = state.stages.map(s => {
    const hazardsList = s.hazards || [];
    const imgSrc = s.image_url || s.image || '/assets/img/stages/arena.jpg';
    const locationStr = s.location || 'Official Arena';
    const gimmickStr = s.notes || s.special_mechanics || s.gimmick || (s.has_walls ? 'Walled tournament battleground' : 'Infinite arena');

    return `
      <div class="stage-card" title="${gimmickStr}">
        <div class="stage-img-wrap">
          <img class="stage-img" src="${imgSrc}" alt="${s.name}" onerror="this.src='/assets/img/stages/arena.jpg'">
        </div>
        <div class="stage-meta">
          <div class="stage-name">${s.name}</div>
          <div class="stage-location">${locationStr}</div>
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
    const res = await fetch('/api/v1/notation/convert', {
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
    });
  }

  if (oSelect) {
    oSelect.addEventListener('change', () => {
      updateOpponentPreview();
      runMatchupAnalysis();
    });
  }

  if (sSelect) {
    sSelect.addEventListener('change', () => {
      updateStagePreview();
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

function updatePlayerPreview() {
  const pSelect = document.getElementById('playerSelect');
  const avatarImg = document.getElementById('playerAvatarPreview');
  const badge = document.getElementById('playerArchetypeBadge');
  if (!pSelect) return;

  const selectedOpt = pSelect.selectedOptions[0];
  if (selectedOpt) {
    const avatar = selectedOpt.dataset.avatar || '/assets/avatars/jin-brand-256-C1-oe_x3.webp';
    if (avatarImg) {
      avatarImg.src = avatar;
      avatarImg.onerror = () => { avatarImg.src = '/assets/avatars/jin-brand-256-C1-oe_x3.webp'; };
    }
    if (badge) badge.textContent = selectedOpt.dataset.archetype || 'Fighter';
  }
}

function updateOpponentPreview() {
  const oSelect = document.getElementById('opponentSelect');
  const avatarImg = document.getElementById('opponentAvatarPreview');
  const badge = document.getElementById('opponentArchetypeBadge');
  if (!oSelect) return;

  const selectedOpt = oSelect.selectedOptions[0];
  if (selectedOpt) {
    const avatar = selectedOpt.dataset.avatar || '/assets/avatars/kazuya-brand-256-BInk9tTm.webp';
    if (avatarImg) {
      avatarImg.src = avatar;
      avatarImg.onerror = () => { avatarImg.src = '/assets/avatars/kazuya-brand-256-BInk9tTm.webp'; };
    }
    if (badge) badge.textContent = selectedOpt.dataset.archetype || 'Fighter';
  }
}

function updateStagePreview() {
  const sSelect = document.getElementById('stageSelect');
  const thumb = document.getElementById('selectedStageThumb');
  const hazardsBox = document.getElementById('stageHazardsMini');
  if (!sSelect) return;

  const stageId = parseInt(sSelect.value);
  const stage = state.stages.find(s => s.id === stageId);
  if (stage) {
    if (thumb) {
      thumb.src = stage.image_url || stage.image || '/assets/img/stages/arena.jpg';
      thumb.onerror = () => { thumb.src = '/assets/img/stages/arena.jpg'; };
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
    const response = await fetch('/api/v1/matchup/analyze', {
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

  // 1. Face-off Hero Banner
  const p1 = data.player_character;
  const p2 = data.opponent_character;
  const st = data.stage;

  document.getElementById('dashP1Img').src = p1.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp';
  document.getElementById('dashP1Name').textContent = p1.name;
  document.getElementById('dashP1Archetype').textContent = p1.archetype || 'Fighter';

  document.getElementById('dashP2Img').src = p2.avatar_url || '/assets/avatars/kazuya-brand-256-BInk9tTm.webp';
  document.getElementById('dashP2Name').textContent = p2.name;
  document.getElementById('dashP2Archetype').textContent = p2.archetype || 'Fighter';

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

  // 3. SECTION 7: Guaranteed Punish Matrix Table & Defensive Tactics
  const punishPill = document.getElementById('punishCountPill');
  const punishTbody = document.getElementById('punishMatrixBody');
  const punishEmpty = document.getElementById('punishEmptyState');

  if (punishPill) punishPill.textContent = `${data.punish_matrix.length} Verified Punishes`;

  if (!data.punish_matrix || data.punish_matrix.length === 0) {
    if (punishTbody) punishTbody.innerHTML = '';
    if (punishEmpty) punishEmpty.style.display = 'block';
  } else {
    if (punishEmpty) punishEmpty.style.display = 'none';
    if (punishTbody) {
      punishTbody.innerHTML = data.punish_matrix.map(p => {
        let tierClass = 'jab';
        if (p.punish_tier.includes('Launch')) tierClass = 'launch';
        else if (p.punish_tier.includes('Intermediate') || p.punish_tier.includes('i14')) tierClass = 'intermediate';

        return `
          <tr>
            <td>
              <div style="font-weight:700; color:#fff;">${p.opponent_move_name}</div>
              <div style="font-family:monospace; font-size:0.75rem; color:var(--text-muted);">${p.opponent_move_input}</div>
            </td>
            <td>
              <span class="frame-disadvantage-badge">${p.opponent_block_advantage}</span>
            </td>
            <td>
              <div style="font-weight:700; color:#fff;">${p.recommended_punish_name}</div>
              <span class="km-input-badge">${p.recommended_punish_input}</span>
            </td>
            <td>
              <span class="punish-startup-badge">i${p.punish_startup}</span>
            </td>
            <td>
              <span style="font-weight:800; color:var(--accent-gold);">${p.damage !== null ? p.damage : '—'}</span>
            </td>
            <td>
              <span class="punish-tier-badge ${tierClass}">${p.punish_type}</span>
            </td>
          </tr>
        `;
      }).join('');
    }
  }

  // Defensive Tactics (Fuzzy Guard, Interrupts, Low Defense)
  const dt = data.defensive_tactics;
  const fuzzyEl = document.getElementById('fuzzyGuardText');
  const interruptEl = document.getElementById('interruptText');
  const lowDefEl = document.getElementById('lowDefenseText');
  if (fuzzyEl) fuzzyEl.textContent = dt.fuzzy_guard_notes || 'Fuzzy guard against strings with high extensions.';
  if (interruptEl) interruptEl.textContent = dt.interrupt_opportunities || 'Use fastest jab check to break stance transitions.';
  if (lowDefEl) lowDefEl.textContent = dt.low_defense_priority || 'Stay standing by default; react to launch-punishable sweeps.';

  // 4. SECTION 4: Player's Useful Moves (vs this Rival)
  const usefulGrid = document.getElementById('usefulMovesGrid');
  const usefulPill = document.getElementById('usefulMovesCountPill');
  if (usefulPill) usefulPill.textContent = `${data.useful_moves.length} Recommended Tools`;

  if (usefulGrid) {
    if (!data.useful_moves || data.useful_moves.length === 0) {
      usefulGrid.innerHTML = '<div style="color:var(--text-muted); padding:1rem;">No specific moves cataloged yet.</div>';
    } else {
      usefulGrid.innerHTML = data.useful_moves.map(m => {
        const stp = m.startup_frames ? `i${m.startup_frames}` : '—';
        const blk = m.block_advantage !== null ? (m.block_advantage > 0 ? `+${m.block_advantage}` : `${m.block_advantage}`) : '—';
        const blkCls = m.block_advantage !== null ? (m.block_advantage >= 0 ? 'frame-plus' : 'frame-minus') : '';
        const dmg = m.damage ? `${m.damage} DMG` : '—';

        return `
          <div class="useful-move-card" onclick="testNotationString('${m.input}')" title="Click to test in Notation Engine">
            <div class="um-header">
              <div>
                <span class="um-name">${m.move_name}</span>
                <div style="margin-top:0.2rem;">${formatTekkenNotation(m.input)}</div>
              </div>
              <span class="um-role-tag">${m.role}</span>
            </div>
            <div class="um-stats-row">
              <span>Startup: <strong>${stp}</strong></span>
              <span class="${blkCls}">Block: <strong>${blk}</strong></span>
              <span style="color:var(--accent-gold);"><strong>${dmg}</strong></span>
            </div>
            <div class="um-purpose">${m.tactical_purpose}</div>
          </div>
        `;
      }).join('');
    }
  }

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
  if (stageAdvantageBox) {
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
    applyStageComboFilter();
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

  // Dimensions & Description
  if (dimPill) dimPill.textContent = report.wall_distance || 'Standard (24m)';
  if (boundaryDesc) boundaryDesc.textContent = report.layout_description;

  // Danger Badge
  if (dangerBadge) {
    if (!report.stage.has_walls) {
      dangerBadge.textContent = 'SAFE (INFINITE)';
      dangerBadge.className = 'danger-level-badge safe';
    } else if (report.stage.wall_blast || (report.stage.wall_break && report.stage.balcony_break)) {
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
          ${report.stage.wall_break ? '<div class="stage-legend-item"><span class="stage-legend-dot" style="background:#ef4444;"></span> Wall Break</div>' : ''}
          ${report.stage.floor_break ? '<div class="stage-legend-item"><span class="stage-legend-dot" style="background:#f97316;"></span> Floor Break</div>' : ''}
          ${report.stage.balcony_break ? '<div class="stage-legend-item"><span class="stage-legend-dot" style="background:#f59e0b;"></span> Balcony Rail</div>' : ''}
        </div>
      `;
      blueprintContainer.innerHTML = svgMarkup;
    } else {
      // Unmapped / Infinite Stage panel (Zero Fabricated Geometry)
      blueprintContainer.innerHTML = `
        <div class="stage-unmapped-panel">
          <div class="stage-unmapped-header">
            <svg viewBox="0 0 24 24" width="16" height="16" stroke="#f59e0b" stroke-width="2.5" fill="none"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <span>${report.stage.name} • UNBOUNDED / INFINITE BATTLEGROUND</span>
          </div>
          <p class="stage-unmapped-text">
            ⚠️ <strong>Zero Fabricated Geometry Rule:</strong> ${report.stage.name} features unbounded open terrain with no perimeter wall bounds. Movement is unrestricted; no artificial polygonal boundary mesh is displayed.
          </p>
          <div class="stage-unmapped-metrics-grid">
            <div class="stage-unmapped-metric-cell">
              <div class="label">Boundary Shape</div>
              <div class="value">${report.stage.boundary_shape || 'Infinite'}</div>
            </div>
            <div class="stage-unmapped-metric-cell">
              <div class="label">Wall Distance</div>
              <div class="value">${report.wall_distance}</div>
            </div>
            <div class="stage-unmapped-metric-cell">
              <div class="label">Wall Splat Status</div>
              <div class="value" style="color:#ef4444;">${report.wall_availability_status}</div>
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

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:2.5rem; color:var(--text-muted); font-size:0.85rem;">
        No combo routes match the active criteria for this target profile and filter combination.
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
  const report = state.combosPhase5.recommendations;
  if (!report) return;

  let combo = null;
  const categories = [
    'beginner_friendly', 'standard_launch', 'high_damage_optimal',
    'wall_carry', 'wall_combo', 'heat_dependent', 'counter_hit',
    'character_specific', 'stage_break', 'alternative_routes'
  ];
  for (const cat of categories) {
    const found = (report[cat] || []).find(c => c.id === comboId);
    if (found) {
      combo = found;
      break;
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

  if (titleEl) titleEl.textContent = `${combo.title} (${combo.total_damage} DMG)`;
  if (explEl) explEl.textContent = report.damage_scaling_rules_explanation;

  const hits = combo.scaling_breakdown || [];
  const rawSum = combo.raw_damage_sum || hits.reduce((acc, h) => acc + (h.raw_damage || 0), 0);
  const scaledTotal = hits.reduce((acc, h) => acc + (h.scaled_damage || 0), 0) || combo.total_damage;
  const avoidedOverest = Math.max(0, rawSum - scaledTotal);

  if (rawSumEl) rawSumEl.textContent = `${rawSum} DMG`;
  if (scaledValEl) scaledValEl.textContent = `${scaledTotal} DMG`;
  if (testedValEl) testedValEl.textContent = `${combo.total_damage} DMG`;
  if (dmgTypeBadge) dmgTypeBadge.textContent = combo.damage_type === 'TESTED' ? 'TESTED IN PRACTICE LAB' : 'SCALED ESTIMATE';
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
    const res = await fetch('/api/v1/punishment/practice/record', {
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
    const res = await fetch(`/api/v1/punishment/practice/progress?session_token=${state.sessionToken}`);
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
    const res = await fetch(`/api/v1/punishment/practice/progress?session_token=${state.sessionToken}`);
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
    const res = await fetch(`/api/v1/punishment/practice/reset?session_token=${state.sessionToken}`, {
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
    const res = await fetch('/api/v1/admin/dashboard', {
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
    const res = await fetch('/api/v1/admin/history?limit=50', {
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
    const res = await fetch('/api/v1/admin/sources', {
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
    const res = await fetch('/api/v1/admin/verification-status', {
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
    const res = await fetch('/api/v1/admin/moves', {
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
    const res = await fetch('/api/v1/admin/import/preview', {
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
    const res = await fetch('/api/v1/admin/import/execute', {
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


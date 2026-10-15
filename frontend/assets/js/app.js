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
      image: "/assets/img/stages/urban-square.svg",
      hazards: ["Wall Break", "Balcony Break"],
      gimmick: "Rain-slicked neon metropolitan streets with breakable glass barriers"
    },
    {
      id: "yakushima",
      name: "Yakushima",
      location: "Sacred Misty Forest, Japan",
      image: "/assets/img/stages/yakushima.svg",
      hazards: ["Hard Wall Break"],
      gimmick: "Ancient mystical mossy cedar forest with morning fog and sacred shrines"
    },
    {
      id: "rebel-hangar",
      name: "Rebel Hangar",
      location: "Yggdrasil Military Base",
      image: "/assets/img/stages/rebel-hangar.svg",
      hazards: ["Wall Blast", "Floor Break"],
      gimmick: "High-tech military fortress with combat mechs and attack jets"
    },
    {
      id: "sanctum",
      name: "Sanctum",
      location: "Subterranean Magma Ruins",
      image: "/assets/img/stages/sanctum.svg",
      hazards: ["Floor Break", "Hard Wall Break"],
      gimmick: "Ancient volcanic sacrificial temple with cascading lava pools"
    },
    {
      id: "stratosphere",
      name: "Into the Stratosphere",
      location: "Outer Atmosphere Orbit",
      image: "/assets/img/stages/stratosphere.svg",
      hazards: ["Wall Blast", "Floor Blast"],
      gimmick: "Zero-gravity cataclysmic battle atop orbital meteor debris"
    },
    {
      id: "ortiz-farm",
      name: "Ortiz Farm",
      location: "Andes Coffee Valley, Peru",
      image: "/assets/img/stages/ortiz-farm.svg",
      hazards: ["Balcony Break", "Floor Break"],
      gimmick: "Sunlit Peruvian mountain terrace coffee plantation"
    },
    {
      id: "coliseum",
      name: "Colosseum",
      location: "Ancient Imperial Arena, Italy",
      image: "/assets/img/stages/coliseum.svg",
      hazards: ["Wall Break"],
      gimmick: "Timeless Roman amphitheater bathed in golden sunset glow"
    },
    {
      id: "celebration-on-the-seine",
      name: "Celebration on the Seine",
      location: "River Seine Cruise, France",
      image: "/assets/img/stages/celebration-on-the-seine.svg",
      hazards: ["Balcony Break"],
      gimmick: "Parisian festival riverboat with Eiffel Tower fireworks in the night sky"
    },
    {
      id: "midnight-siege",
      name: "Midnight Siege",
      location: "G Corp Skyscraper Rooftop",
      image: "/assets/img/stages/midnight-siege.svg",
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

// API Helper
async function fetchAPI(endpoint) {
  try {
    const res = await fetch(`/api/v1${endpoint}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn(`API call failed for ${endpoint}:`, err);
    return null;
  }
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

  // Carousel Navigation Buttons (< and >)
  const prevBtn = document.getElementById('carouselPrevBtn');
  const nextBtn = document.getElementById('carouselNextBtn');
  const track = document.getElementById('carouselTrack');
  if (prevBtn && track) {
    prevBtn.addEventListener('click', () => {
      track.scrollBy({ left: -320, behavior: 'smooth' });
    });
  }
  if (nextBtn && track) {
    nextBtn.addEventListener('click', () => {
      track.scrollBy({ left: 320, behavior: 'smooth' });
    });
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
}

// 2. Load & Render Characters
async function loadCharacters() {
  const data = await fetchAPI('/characters');
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
    const styleName = FIGHTING_STYLES[c.slug] || (c.archetype ? c.archetype.split('/')[0].trim() : 'Tekken Fighter');
    return `
      <div class="carousel-fighter-card ${isSelected ? 'active' : ''}" 
           id="card_${c.slug}"
           onclick="selectCharacter('${c.slug}')">
        <div class="carousel-avatar-wrap">
          <img class="carousel-avatar" 
               src="${c.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp'}" 
               alt="${c.name}"
               onerror="this.src='/assets/avatars/jin-brand-256-C1-oe_x3.webp'"/>
        </div>
        <div class="carousel-name" title="${c.name}">${c.name}</div>
        <div class="carousel-style" title="${styleName}">${styleName}</div>
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
  const data = await fetchAPI(`/moves?character_id=${characterId}`);
  state.moves = data || [];
  renderMovesTable(state.moves);
}

function renderMovesTable(movesList) {
  const tbody = document.getElementById('movesTableBody');
  const emptyState = document.getElementById('movesEmptyState');
  if (!tbody) return;

  if (!movesList || movesList.length === 0) {
    tbody.innerHTML = '';
    if (emptyState) emptyState.style.display = 'block';
    return;
  }

  if (emptyState) emptyState.style.display = 'none';

  tbody.innerHTML = movesList.map(m => {
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
        <td><span class="cmd-badge">${m.original_notation}</span></td>
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
    renderMovesTable(state.moves);
    return;
  }
  const filtered = state.moves.filter(m => 
    m.name.toLowerCase().includes(query) ||
    m.original_notation.toLowerCase().includes(query) ||
    (m.hit_level && m.hit_level.toLowerCase().includes(query)) ||
    (m.properties && m.properties.some(p => (typeof p === 'string' ? p : p.property_name).toLowerCase().includes(query)))
  );
  renderMovesTable(filtered);
}

// 4. Render Stages Showcase
async function loadStages() {
  const data = await fetchAPI('/stages');
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
          <img class="stage-img" src="${imgSrc}" alt="${s.name}" onerror="this.src='/assets/img/stages/arena.svg'">
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
  const data = await fetchAPI('/coverage/summary');
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
  const data = await fetchAPI('/sources');
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
      thumb.onerror = () => { thumb.src = '/assets/img/stages/arena.svg'; };
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
                <span class="km-input-badge">${m.input}</span>
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
                <span class="km-input-badge">${dm.input}</span>
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

  // 9. SECTION 10: Stage Hazards & Suitable Combos
  const sms = data.stage_matchup_synergy;
  const dangerBadge = document.getElementById('wallDangerBadge');
  const boundaryDesc = document.getElementById('stageBoundaryDescription');
  const mechanicsRow = document.getElementById('synergyMechanicsRow');
  const tacticalAdvice = document.getElementById('stageTacticalAdvice');
  const stageAdvantageBox = document.getElementById('characterStageAdvantage');

  if (dangerBadge) {
    dangerBadge.textContent = sms.wall_danger_level;
    dangerBadge.className = 'danger-level-badge ' + (sms.wall_danger_level.toLowerCase().includes('extreme') ? 'extreme' : (sms.wall_danger_level.toLowerCase().includes('safe') ? 'safe' : 'moderate'));
  }
  if (boundaryDesc) {
    boundaryDesc.textContent = st.notes || `Boundary shape: ${st.boundary_shape || 'Enclosed'}. ${st.special_mechanics || ''}`;
  }
  if (mechanicsRow) {
    const allMechs = [...sms.wall_mechanics, ...sms.floor_mechanics];
    if (allMechs.length === 0) {
      mechanicsRow.innerHTML = '<span class="mini-hazard-pill safe">No Destructibles</span>';
    } else {
      mechanicsRow.innerHTML = allMechs.map(m => `<span class="mini-hazard-pill">${m}</span>`).join('');
    }
  }
  if (tacticalAdvice) tacticalAdvice.textContent = sms.tactical_advice;
  if (stageAdvantageBox) {
    stageAdvantageBox.innerHTML = `<strong>Stage Win-Condition:</strong> ${sms.character_stage_advantage}`;
  }

  // Suitable Combos
  const combosContainer = document.getElementById('suitableCombosContainer');
  if (combosContainer) {
    if (!data.suitable_combos || data.suitable_combos.length === 0) {
      combosContainer.innerHTML = '<div style="color:var(--text-muted); font-size:0.8rem; padding:1rem;">No specific combo route matched for current stage hazards. Standard staple juggles apply.</div>';
    } else {
      combosContainer.innerHTML = data.suitable_combos.map(c => `
        <div class="combo-card">
          <div class="combo-card-header">
            <span class="combo-title">${c.title}</span>
            <span class="combo-dmg-badge">${c.damage} DMG (${c.hits} Hits) • ${c.difficulty}</span>
          </div>
          <div class="combo-notation-box">${c.notation}</div>
          <div class="combo-synergy-note">🎯 ${c.synergy_reason}</div>
        </div>
      `).join('');
    }
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
    const res = await fetch(`/api/v1/punishment/options?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
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
    const punInput = opt.recommended_punish_input ? `<span class="km-input-badge">${opt.recommended_punish_input}</span>` : '—';
    const punStp = opt.punish_startup ? `i${opt.punish_startup}` : '—';
    const punDmg = opt.punish_damage ? `<span style="color:var(--accent-gold); font-weight:800;">${opt.punish_damage} DMG</span>` : '—';
    const punTier = opt.punish_tier ? `<span class="punish-tier-badge ${opt.punish_tier.toLowerCase().includes('launch') ? 'launch' : (opt.punish_tier.toLowerCase().includes('ws') ? 'intermediate' : 'jab')}">${opt.punish_tier}</span>` : '';

    return `
      <tr>
        <td>
          <div style="font-weight:700; color:#fff;">${opt.opponent_move_name}</div>
          <div style="display:flex; align-items:center; gap:0.4rem; margin-top:0.25rem;">
            <span class="km-input-badge" style="font-size:0.75rem;">${opt.opponent_move_input}</span>
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

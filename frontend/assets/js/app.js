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
  stages: [
    {
      id: "arena",
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
  renderStages();
  await loadCoverageData();
  await loadSourcesData();
  updateNotationDisplay();
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
function renderStages() {
  const container = document.getElementById('stagesGrid');
  if (!container) return;

  container.innerHTML = state.stages.map(s => `
    <div class="stage-card" title="${s.gimmick}">
      <div class="stage-img-wrap">
        <img class="stage-img" src="${s.image}" alt="${s.name}" onerror="this.src='/assets/img/stages/arena.svg'">
      </div>
      <div class="stage-meta">
        <div class="stage-name">${s.name}</div>
        <div class="stage-location">${s.location}</div>
        <div class="stage-hazards">
          ${s.hazards.map(h => `<span class="hazard-pill">${h}</span>`).join('')}
        </div>
      </div>
    </div>
  `).join('');
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

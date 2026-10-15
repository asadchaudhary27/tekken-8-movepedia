/**
 * Tekken 8 Movepedia - Interactive Vanilla JavaScript Application.
 * Handles character roster filtering, dynamic move tables, real-time notation translation,
 * and coverage reporting integrations.
 */

// Global State
const state = {
  characters: [],
  selectedCharacter: null,
  activeFilter: 'ALL',
  controllerLayout: 'PLAYSTATION',
  currentNotation: 'df+2',
  sources: [],
  coverage: null
};

// Client-side quick notation mappings for zero-latency typing
const CLIENT_DIRECTIONS = {
  'u': { arrow: '↑', english: 'Up', numpad: '8' },
  'ub': { arrow: '↖', english: 'Up Back', numpad: '7' },
  'uf': { arrow: '↗', english: 'Up Forward', numpad: '9' },
  'b': { arrow: '←', english: 'Back', numpad: '4' },
  'n': { arrow: '•', english: 'Neutral', numpad: '5' },
  'f': { arrow: '→', english: 'Forward', numpad: '6' },
  'db': { arrow: '↙', english: 'Down Back', numpad: '1' },
  'd': { arrow: '↓', english: 'Down', numpad: '2' },
  'df': { arrow: '↘', english: 'Down Forward', numpad: '3' }
};

const CLIENT_BUTTONS = {
  '1': { english: 'Left Punch', ps: '□', xbox: 'X', arcade: '1' },
  '2': { english: 'Right Punch', ps: '△', xbox: 'Y', arcade: '2' },
  '3': { english: 'Left Kick', ps: '✕', xbox: 'A', arcade: '3' },
  '4': { english: 'Right Kick', ps: '○', xbox: 'B', arcade: '4' }
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

// Notation Converter
async function updateNotationDisplay() {
  const inputVal = document.getElementById('notationInput').value.trim() || 'df+2';
  state.currentNotation = inputVal;

  // Attempt server-side full conversion
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
    // Fall back to client parser
  }

  // Client-side fallback
  renderClientNotation(inputVal);
}

function renderNotationCards(data) {
  document.getElementById('modeArrow').textContent = data.arrow_display || '—';
  document.getElementById('modeEnglish').textContent = data.english_display || '—';
  document.getElementById('modeNumpad').textContent = data.numpad_display || '—';
  document.getElementById('modeController').textContent = data.controller_display || '—';

  const unsAlert = document.getElementById('unsupportedAlert');
  if (data.has_unsupported_syntax) {
    unsAlert.style.display = 'block';
    unsAlert.textContent = `Unsupported syntax flagged for review: ${data.unsupported_tokens.join(', ')}`;
  } else {
    unsAlert.style.display = 'none';
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

// Roster Rendering
function renderRoster() {
  const container = document.getElementById('rosterGrid');
  if (!container) return;

  const filtered = state.characters.filter(c => {
    if (state.activeFilter === 'ALL') return true;
    if (state.activeFilter === 'NEWCOMERS') return c.archetype && c.archetype.includes('Newcomers');
    if (state.activeFilter === 'MISHIMA') return c.archetype && c.archetype.includes('Mishima');
    if (state.activeFilter === 'ALLIES') return c.archetype && c.archetype.includes('Allies');
    if (state.activeFilter === 'REBELS') return c.archetype && c.archetype.includes('Rebels');
    return true;
  });

  if (filtered.length === 0) {
    container.innerHTML = '<div style="color:var(--text-muted); grid-column:1/-1; padding:2rem; text-align:center;">No characters found matching category.</div>';
    return;
  }

  container.innerHTML = filtered.map(c => `
    <div class="fighter-card ${state.selectedCharacter && state.selectedCharacter.slug === c.slug ? 'active' : ''}" 
         onclick="selectCharacter('${c.slug}')">
      <div class="fighter-avatar-wrap">
        <img class="fighter-avatar" src="${c.avatar_url || '/assets/avatars/jin-brand-256-C1-oe_x3.webp'}" 
             alt="${c.name}" onerror="this.src='/assets/avatars/jin-brand-256-C1-oe_x3.webp'"/>
      </div>
      <div class="fighter-info">
        <div class="fighter-name">${c.name}</div>
        <div class="fighter-archetype">${c.archetype || 'Fighter'}</div>
      </div>
    </div>
  `).join('');
}

// Select Fighter & Load Frame Data
async function selectCharacter(slug) {
  const char = state.characters.find(c => c.slug === slug);
  if (!char) return;
  state.selectedCharacter = char;
  renderRoster();

  document.getElementById('currentFighterTitle').textContent = `${char.name} Frame Data & Moves`;

  const moves = await fetchAPI(`/moves?character_slug=${slug}`);
  renderMovesTable(moves || []);
}

function renderMovesTable(moves) {
  const tbody = document.getElementById('movesTableBody');
  const emptyState = document.getElementById('movesEmptyState');

  if (!moves || moves.length === 0) {
    tbody.innerHTML = '';
    emptyState.style.display = 'block';
    return;
  }

  emptyState.style.display = 'none';
  tbody.innerHTML = moves.map(m => {
    let blockCls = 'fa-neutral';
    if (m.block_advantage !== null) {
      if (m.block_advantage > 0) blockCls = 'fa-plus';
      else if (m.block_advantage < 0) blockCls = 'fa-minus';
    }

    const blockStr = m.block_advantage !== null ? (m.block_advantage > 0 ? `+${m.block_advantage}` : m.block_advantage) : (m.block_advantage_raw || '—');
    const hitStr = m.hit_advantage !== null ? (m.hit_advantage > 0 ? `+${m.hit_advantage}` : m.hit_advantage) : (m.hit_advantage_raw || '—');
    const startupStr = m.startup_frames !== null ? `i${m.startup_frames}` : (m.startup_raw || '—');

    const propBadges = (m.properties || []).map(p => `<span class="badge badge-heat">${p.property_type || p}</span>`).join(' ');

    return `
      <tr>
        <td style="font-weight:700; color:#fff;">${m.name || '—'}</td>
        <td style="font-family:monospace; color:var(--accent-cyan); font-weight:700;">${m.original_notation}</td>
        <td><span class="badge badge-damage">${(m.hit_level || 'm').toUpperCase()}</span></td>
        <td style="font-family:monospace;">${startupStr}</td>
        <td class="${blockCls}">${blockStr}</td>
        <td style="font-weight:600;">${hitStr}</td>
        <td style="font-weight:700; color:#fff;">${m.damage || m.damage_raw || '—'}</td>
        <td>${propBadges}</td>
      </tr>
    `;
  }).join('');
}

// Data Sources Status
async function loadSources() {
  const sources = await fetchAPI('/sources');
  const container = document.getElementById('sourcesGrid');
  if (!sources || !container) return;

  container.innerHTML = sources.map(s => {
    let cls = 'source-status-approved';
    if (s.approval_status.includes('RESTRICTIONS')) cls = 'source-status-restricted';
    else if (s.approval_status.includes('BLOCKED') || s.approval_status.includes('RESEARCH')) cls = 'source-status-blocked';

    return `
      <div class="source-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <strong style="color:#fff;">${s.name}</strong>
          <span class="badge ${cls}">${s.approval_status.replace(/_/g, ' ')}</span>
        </div>
        <div style="font-size:0.75rem; color:var(--text-muted); word-break:break-all;">${s.base_url}</div>
        <div style="font-size:0.7rem; color:var(--text-dim); margin-top:0.25rem;">License: ${s.license_type} | Policy: ${s.rate_limit_policy}</div>
      </div>
    `;
  }).join('');
}

// Coverage Metrics
async function loadCoverage() {
  const coverage = await fetchAPI('/coverage/summary');
  if (!coverage) return;
  state.coverage = coverage;

  document.getElementById('covRosterCount').textContent = `${coverage.roster_summary.ingested_character_count} / ${coverage.roster_summary.expected_roster_count}`;
  document.getElementById('covRosterPct').textContent = `${coverage.roster_summary.roster_coverage_percentage}%`;
  document.getElementById('covTotalMoves').textContent = coverage.move_summary.total_moves_ingested;
  document.getElementById('covOverallPct').textContent = `${coverage.field_coverage.overall_field_coverage_percentage}%`;
  document.getElementById('covDuplicates').textContent = coverage.move_summary.duplicate_records_detected;
  document.getElementById('covUnverified').textContent = coverage.move_summary.unverified_records;
}

// Initializer
document.addEventListener('DOMContentLoaded', async () => {
  // Setup notation input listener
  const notInput = document.getElementById('notationInput');
  if (notInput) {
    notInput.addEventListener('input', () => updateNotationDisplay());
  }

  // Setup controller layout toggles
  document.querySelectorAll('.ctl-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.ctl-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      state.controllerLayout = e.target.getAttribute('data-layout');
      updateNotationDisplay();
    });
  });

  // Setup roster filter buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      state.activeFilter = e.target.getAttribute('data-filter');
      renderRoster();
    });
  });

  // Load initial data
  const chars = await fetchAPI('/characters');
  if (chars && chars.length > 0) {
    state.characters = chars;
    renderRoster();
    selectCharacter(chars[0].slug);
  }

  updateNotationDisplay();
  loadSources();
  loadCoverage();
});

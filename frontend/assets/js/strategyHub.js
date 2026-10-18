/**
 * TEKKEN 8 ROSTER & ANTI-CHARACTER STRATEGY HUB UI CONTROLLER
 * Pure Vanilla ES6 Modular Drop-in Component.
 * Integrates 100% of canonical competitive data for all 44 Fighters & Universal Combat Mechanics.
 * Version: Tekken 8 Patch v3.00.02
 */

(function () {
  'use strict';

  const state = {
    activeUniversalTab: 'controls-frame',
    activeModalTab: 'tab-anti', // Default to the critical Anti-Character Guide tab on open!
    currentModalFighter: null,
    searchQuery: '',
    selectedSeason: 'ALL',
    selectedFaction: 'ALL',
    selectedWeakSide: 'ALL',
    isInitialized: false
  };

  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function getMasterData() {
    return window.TEKKEN8_MASTER_DATA || null;
  }

  // =========================================================================
  // StrategyHub Main Controller
  // =========================================================================
  const StrategyHub = {
    init: function () {
      const container = document.getElementById('strategyHubContainer');
      if (!container) return;

      const data = getMasterData();
      if (!data) {
        console.warn('StrategyHub: TEKKEN8_MASTER_DATA not yet loaded.');
        return;
      }

      if (!state.isInitialized) {
        container.innerHTML = this.renderHubLayout(data);
        this.attachEventListeners();
        state.isInitialized = true;
      }

      this.renderUniversalMechanics();
      this.filterRosterGrid();
    },

    renderHubLayout: function (data) {
      return `
        <div class="strat-hub-container">
          <!-- Hub Hero Banner -->
          <div class="strat-hub-hero">
            <div class="strat-hub-hero-badge">
              <span class="pulse-dot"></span>
              <span>TEKKEN 8 TOURNAMENT STRATEGY HUB • 44 WARRIORS &amp; MASTER MECHANICS</span>
            </div>
            <h1 class="strat-hub-title">ROSTER &amp; ANTI-CHARACTER GUIDE</h1>
            <p class="strat-hub-subtitle">
              مکمل 44 فائٹرز کی پروفائلز، پریشر سسٹمز، مکس اپ بلینڈرز اور حریف کو چکمہ دے کر ہرانے کی مکمل گائیڈ (سائیڈ سٹیپ، پنشرز، ڈک اینڈ لانچ، اور پیری رولز)۔
            </p>
          </div>

          <!-- Component 3: Universal Mechanics Section -->
          <div class="strat-hub-mechanics-wrapper" id="stratHubMechanicsSection">
            <div class="strat-hub-card strat-hub-mechanics-card">
              <div class="strat-hub-mech-header">
                <div class="strat-hub-mech-title-group">
                  <span class="mech-badge">GLOBAL COMBAT ENGINE</span>
                  <h2 class="strat-hub-section-title">Universal Mechanics &amp; Tournament Science</h2>
                </div>

                <!-- Universal Mechanics Sub-Tabs -->
                <div class="strat-hub-tab-bar" role="tablist">
                  <button type="button" class="strat-hub-tab-btn ${state.activeUniversalTab === 'controls-frame' ? 'active' : ''}" 
                          data-mech-tab="controls-frame" onclick="StrategyHub.switchUniversalTab('controls-frame')">
                    🎮 Controls &amp; Frame Data
                  </button>
                  <button type="button" class="strat-hub-tab-btn ${state.activeUniversalTab === 'parry-matrix' ? 'active' : ''}" 
                          data-mech-tab="parry-matrix" onclick="StrategyHub.switchUniversalTab('parry-matrix')">
                    🛡️ Parry &amp; Duck vs. Block
                  </button>
                  <button type="button" class="strat-hub-tab-btn ${state.activeUniversalTab === 'wall-bible' ? 'active' : ''}" 
                          data-mech-tab="wall-bible" onclick="StrategyHub.switchUniversalTab('wall-bible')">
                    🧱 Wall Traps &amp; Escape Bible
                  </button>
                </div>
              </div>

              <!-- Universal Content Container -->
              <div class="strat-hub-mech-body" id="stratHubUniversalContent">
                <!-- Injected via renderUniversalMechanics() -->
              </div>
            </div>
          </div>

          <!-- Component 1: Filterable Character Roster Grid -->
          <div class="strat-hub-roster-section" id="stratHubRosterSection">
            <div class="strat-hub-roster-header">
              <div class="strat-hub-roster-title-wrap">
                <h2 class="strat-hub-section-title">44-FIGHTER STRATEGY COMPENDIUM</h2>
                <span class="strat-hub-counter-badge" id="stratHubRosterCount">Showing 44 of 44 Warriors</span>
              </div>
              <p class="strat-hub-roster-sub">
                کسی بھی فائٹر کے کارڈ پر کلک کریں تاکہ اس کی مکمل پروفائل، آفینس، مکس اپ بلینڈر اور اینٹی گائیڈ کھل جائے۔
              </p>
            </div>

            <!-- Filters & Search Toolbar -->
            <div class="strat-hub-filters-bar">
              <!-- Search Bar -->
              <div class="strat-hub-search-wrap">
                <svg class="strat-hub-search-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2.5" fill="none">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <input type="text" id="stratHubSearchInput" class="strat-hub-search-input" 
                       placeholder="Search fighter name, country, fighting style, or title..." 
                       value="${escapeHtml(state.searchQuery)}" oninput="StrategyHub.onSearchInput(this.value)">
                ${state.searchQuery ? `<button type="button" class="strat-hub-search-clear" onclick="StrategyHub.clearSearch()">&times;</button>` : ''}
              </div>

              <!-- Filter Pills Toolbar -->
              <div class="strat-hub-pill-groups">
                <!-- Season Filter -->
                <div class="strat-hub-pill-group">
                  <span class="strat-hub-pill-label">Season:</span>
                  <div class="strat-hub-pill-list" id="stratHubSeasonPills">
                    <button type="button" class="strat-hub-pill ${state.selectedSeason === 'ALL' ? 'active' : ''}" onclick="StrategyHub.setSeasonFilter('ALL')">All (44)</button>
                    <button type="button" class="strat-hub-pill ${state.selectedSeason === 'Base' ? 'active' : ''}" onclick="StrategyHub.setSeasonFilter('Base')">Base (32)</button>
                    <button type="button" class="strat-hub-pill ${state.selectedSeason === 'Season 1' ? 'active' : ''}" onclick="StrategyHub.setSeasonFilter('Season 1')">Season 1 (4)</button>
                    <button type="button" class="strat-hub-pill ${state.selectedSeason === 'Season 2' ? 'active' : ''}" onclick="StrategyHub.setSeasonFilter('Season 2')">Season 2 (4)</button>
                    <button type="button" class="strat-hub-pill ${state.selectedSeason === 'Season 3' ? 'active' : ''}" onclick="StrategyHub.setSeasonFilter('Season 3')">Season 3 (4)</button>
                  </div>
                </div>

                <!-- Weak Side Filter -->
                <div class="strat-hub-pill-group">
                  <span class="strat-hub-pill-label">Step Weakness:</span>
                  <div class="strat-hub-pill-list" id="stratHubWeakSidePills">
                    <button type="button" class="strat-hub-pill ${state.selectedWeakSide === 'ALL' ? 'active' : ''}" onclick="StrategyHub.setWeakSideFilter('ALL')">All Sides</button>
                    <button type="button" class="strat-hub-pill ssl-pill ${state.selectedWeakSide === 'SSL' ? 'active' : ''}" onclick="StrategyHub.setWeakSideFilter('SSL')">⟵ SSL (Weak to Left)</button>
                    <button type="button" class="strat-hub-pill ssr-pill ${state.selectedWeakSide === 'SSR' ? 'active' : ''}" onclick="StrategyHub.setWeakSideFilter('SSR')">SSR (Weak to Right) ⟶</button>
                  </div>
                </div>

                <!-- Faction Filter -->
                <div class="strat-hub-pill-group">
                  <span class="strat-hub-pill-label">Faction / Alliance:</span>
                  <div class="strat-hub-pill-list" id="stratHubFactionPills">
                    <button type="button" class="strat-hub-pill ${state.selectedFaction === 'ALL' ? 'active' : ''}" onclick="StrategyHub.setFactionFilter('ALL')">All Factions</button>
                    <button type="button" class="strat-hub-pill ${state.selectedFaction === 'Yggdrasil & Jin\'s Allies' ? 'active' : ''}" onclick="StrategyHub.setFactionFilter('Yggdrasil & Jin\'s Allies')">Yggdrasil / Jin</button>
                    <button type="button" class="strat-hub-pill ${state.selectedFaction === 'G-Corporation & Kazuya\'s Allies' ? 'active' : ''}" onclick="StrategyHub.setFactionFilter('G-Corporation & Kazuya\'s Allies')">G-Corp / Kazuya</button>
                    <button type="button" class="strat-hub-pill ${state.selectedFaction === 'Mishima Bloodline & Enforcers' ? 'active' : ''}" onclick="StrategyHub.setFactionFilter('Mishima Bloodline & Enforcers')">Mishima Clan</button>
                    <button type="button" class="strat-hub-pill ${state.selectedFaction === 'Tekken Monks & Traditional Purifiers' ? 'active' : ''}" onclick="StrategyHub.setFactionFilter('Tekken Monks & Traditional Purifiers')">Tekken Monks</button>
                    <button type="button" class="strat-hub-pill ${state.selectedFaction === 'Tournament Veterans & Wildcards' ? 'active' : ''}" onclick="StrategyHub.setFactionFilter('Tournament Veterans & Wildcards')">Veterans / Neutral</button>
                    <button type="button" class="strat-hub-pill ${state.selectedFaction === 'Guest Legends' ? 'active' : ''}" onclick="StrategyHub.setFactionFilter('Guest Legends')">Guest Fighters</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Cards Grid -->
            <div class="strat-hub-grid" id="stratHubGrid">
              <!-- Rendered via filterRosterGrid() -->
            </div>
          </div>
        </div>
      `;
    },

    attachEventListeners: function () {
      // Global Escape key handler for closing modal
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          this.closeStrategyModal();
        }
      });
    },

    // =========================================================================
    // Universal Mechanics Sub-Tab Rendering
    // =========================================================================
    switchUniversalTab: function (tabKey) {
      state.activeUniversalTab = tabKey;
      document.querySelectorAll('.strat-hub-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-mech-tab') === tabKey);
      });
      this.renderUniversalMechanics();
    },

    renderUniversalMechanics: function () {
      const container = document.getElementById('stratHubUniversalContent');
      if (!container) return;

      const data = getMasterData();
      if (!data || !data.universal) return;

      const u = data.universal;

      if (state.activeUniversalTab === 'controls-frame') {
        container.innerHTML = `
          <div class="strat-hub-mech-pane">
            <!-- Buttons & Notation Row -->
            <div class="strat-hub-subgrid">
              <div class="strat-hub-box">
                <h3 class="strat-hub-box-title">🕹️ Standard Attack Buttons (بٹنوں کی پہچان)</h3>
                <p class="strat-hub-box-desc">${escapeHtml(u.controls_notation.desc_ur)}</p>
                <div class="strat-hub-btn-grid">
                  ${u.controls_notation.buttons.map(b => `
                    <div class="strat-hub-btn-card">
                      <div class="btn-badge">${escapeHtml(b.btn)}</div>
                      <div class="btn-info">
                        <div class="btn-name">${escapeHtml(b.name)}</div>
                        <div class="btn-platform">PS: ${escapeHtml(b.ps)} | XB: ${escapeHtml(b.xb)}</div>
                        <div class="btn-desc-ur">${escapeHtml(b.desc_ur)}</div>
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>

              <!-- Directions & States -->
              <div class="strat-hub-box">
                <h3 class="strat-hub-box-title">🧭 Directions &amp; States (ڈائریکشنز اور اسٹیٹس)</h3>
                <div class="strat-hub-dir-list">
                  ${u.controls_notation.directions.map(d => `
                    <div class="strat-hub-dir-item">
                      <span class="dir-code">${escapeHtml(d.dir)}</span>
                      <span class="dir-name">${escapeHtml(d.name)}</span>
                      <span class="dir-ur">${escapeHtml(d.ur)}</span>
                    </div>
                  `).join('')}
                </div>
              </div>
            </div>

            <!-- Frame Data Priority Science -->
            <div class="strat-hub-box mt-4">
              <div class="box-head-split">
                <h3 class="strat-hub-box-title">⏱️ Frame Data Science: باری کس کی ہے؟</h3>
                <span class="box-head-pill">${escapeHtml(u.frame_data_science.fps_rule)}</span>
              </div>
              <div class="strat-hub-frame-tiers-grid">
                ${u.frame_data_science.rules.map(r => `
                  <div class="strat-hub-tier-card tier-${escapeHtml(r.color)}">
                    <div class="tier-badge">${escapeHtml(r.badge)}</div>
                    <h4 class="tier-title">${escapeHtml(r.tier)}</h4>
                    <p class="tier-desc-ur">${escapeHtml(r.ur)}</p>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- High Mid Low Triangle & 4-Step Frame Trap -->
            <div class="strat-hub-subgrid mt-4">
              <div class="strat-hub-box">
                <h3 class="strat-hub-box-title">🔺 High, Mid, Low Triangle (اپر، مڈل، لوئر کا کھیل)</h3>
                <div class="strat-hub-triangle-list">
                  <div class="triangle-item item-high">
                    <span class="tri-tag tag-high">HIGH (Upper)</span>
                    <p class="tri-text">${escapeHtml(u.frame_data_science.triangle.high_ur)}</p>
                  </div>
                  <div class="triangle-item item-mid">
                    <span class="tri-tag tag-mid">MID (Middle)</span>
                    <p class="tri-text">${escapeHtml(u.frame_data_science.triangle.mid_ur)}</p>
                  </div>
                  <div class="triangle-item item-low">
                    <span class="tri-tag tag-low">LOW (Lower)</span>
                    <p class="tri-text">${escapeHtml(u.frame_data_science.triangle.low_ur)}</p>
                  </div>
                </div>
              </div>

              <div class="strat-hub-box">
                <h3 class="strat-hub-box-title">🕸️ The 4-Step Frame Trap (حریف کو جال میں پھنسانا)</h3>
                <div class="strat-hub-stepper">
                  ${u.frame_data_science.frame_trap_4step.map(s => `
                    <div class="strat-hub-step-item">
                      <div class="step-num">${escapeHtml(s.step.split('.')[0])}</div>
                      <div class="step-content">
                        <div class="step-title-row">
                          <span class="step-name">${escapeHtml(s.step)}</span>
                          <span class="step-cmd">${escapeHtml(s.cmd)}</span>
                        </div>
                        <p class="step-desc-ur">${escapeHtml(s.desc_ur)}</p>
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>
            </div>

            <!-- Spacing, Gap & Settings -->
            <div class="strat-hub-box mt-4">
              <h3 class="strat-hub-box-title">📐 Spacing (فاصلہ) &amp; Optimal Tournament Settings</h3>
              <div class="strat-hub-spacing-grid">
                <div class="spacing-col">
                  <span class="spacing-tag range-0">Range 0 (Kissing Distance)</span>
                  <p class="spacing-desc">${escapeHtml(u.frame_data_science.spacing_settings.range_0_ur)}</p>
                </div>
                <div class="spacing-col">
                  <span class="spacing-tag range-mid">Range 1.5 - 2 (Mid-Range)</span>
                  <p class="spacing-desc">${escapeHtml(u.frame_data_science.spacing_settings.range_mid_ur)}</p>
                </div>
                <div class="spacing-col">
                  <span class="spacing-tag range-long">Range 3+ (Long Range)</span>
                  <p class="spacing-desc">${escapeHtml(u.frame_data_science.spacing_settings.range_long_ur)}</p>
                </div>
              </div>
              <div class="strat-hub-settings-bar">
                <strong>⚙️ Recommended Pro Settings:</strong> ${escapeHtml(u.frame_data_science.spacing_settings.settings_ur)}
              </div>
            </div>

            <!-- 5 Golden Escape Rules -->
            <div class="strat-hub-box mt-4">
              <h3 class="strat-hub-box-title">🛡️ 5 Golden Escape Rules (دباؤ توڑنے کے پانچ اصول)</h3>
              <div class="strat-hub-defense-grid">
                ${u.defense_escape_5rules.map((rule, idx) => `
                  <div class="defense-rule-card">
                    <span class="def-num">#${idx + 1}</span>
                    <h4 class="def-title">${escapeHtml(rule.name)}</h4>
                    <p class="def-desc">${escapeHtml(rule.desc_ur)}</p>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
        `;
      } else if (state.activeUniversalTab === 'parry-matrix') {
        const pm = u.parry_reversal_matrix;
        container.innerHTML = `
          <div class="strat-hub-mech-pane">
            <!-- Low Parry Universal Guide -->
            <div class="strat-hub-box">
              <div class="box-head-split">
                <h3 class="strat-hub-box-title">🦶 1. Universal Low Parry (ہر کریکٹر کی لو پیری)</h3>
                <span class="box-head-pill gold">Command: ${escapeHtml(pm.low_parry_guide.cmd)}</span>
              </div>
              <p class="strat-hub-box-desc">${escapeHtml(pm.low_parry_guide.how_ur)}</p>
              
              <div class="strat-hub-callout-row">
                <div class="callout-card callout-punish">
                  <span class="callout-label">⚡ Guaranteed Combo Punish Flow</span>
                  <div class="callout-code">${escapeHtml(pm.low_parry_guide.punish_flow_ur)}</div>
                </div>
                <div class="callout-card callout-warning">
                  <span class="callout-label">🚫 What CANNOT be Low Parried?</span>
                  <div class="callout-text">${escapeHtml(pm.low_parry_guide.unparryable_ur)}</div>
                </div>
              </div>
            </div>

            <!-- Master Table: When to Low Parry vs Duck vs Block -->
            <div class="strat-hub-box mt-4">
              <h3 class="strat-hub-box-title">📊 2. Master Decision Matrix: Low Parry vs. Duck vs. Block</h3>
              <p class="strat-hub-box-desc">
                ہر لو اٹیک کو لو پیری نہیں کیا جاتا! نیچے دیئے گئے تقابلی جدول سے سمجھیں کہ کب لو پیری کرنی ہے اور کب بلاک کر کے لانچ کرنا ہے۔
              </p>
              <div class="strat-hub-table-wrapper">
                <table class="strat-hub-table">
                  <thead>
                    <tr>
                      <th style="width:30%;">حالت / موو کی قسم (Situation / Move)</th>
                      <th style="width:25%;">کیا کرنا چاہیے؟ (Action Required)</th>
                      <th style="width:45%;">وجہ اور حکمت عملی (Strategic Reason)</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${pm.decision_matrix.map(row => `
                      <tr class="action-row-${escapeHtml(row.action_type)}">
                        <td><strong>${escapeHtml(row.situation)}</strong></td>
                        <td>
                          <span class="action-badge badge-${escapeHtml(row.action_type)}">
                            ${escapeHtml(row.action)}
                          </span>
                        </td>
                        <td class="cell-ur">${escapeHtml(row.reason_ur)}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Unparryable Attacks vs Normal Reversals -->
            <div class="strat-hub-box mt-4">
              <h3 class="strat-hub-box-title">🚫 3. Unparryable Attacks (ریورسل کو چیرنے والے حملے)</h3>
              <p class="strat-hub-box-desc">
                اگر کوئی کریکٹر (جیسے آسوکا، نینا، پال، یا کنگ) نارمل b+1+3 ریورسل لگائے، تو ان حملوں سے ان کی پیری توڑیں:
              </p>
              <div class="strat-hub-unparry-grid">
                ${pm.unparryable_reversals.map(up => `
                  <div class="unparry-card">
                    <div class="unparry-type">${escapeHtml(up.type)}</div>
                    <div class="unparry-examples">Examples: <code>${escapeHtml(up.examples)}</code></div>
                    <div class="unparry-rule">${escapeHtml(up.rule)}</div>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- Character Specific Parries Table -->
            <div class="strat-hub-box mt-4">
              <h3 class="strat-hub-box-title">🥋 4. Character-Specific Special Parries (خاص کریکٹرز کی پیریز)</h3>
              <div class="strat-hub-table-wrapper">
                <table class="strat-hub-table">
                  <thead>
                    <tr>
                      <th style="width:20%;">کریکٹر (Character)</th>
                      <th style="width:18%;">کمانڈ (Command)</th>
                      <th style="width:32%;">کیا پکڑتی ہے؟ (Catches)</th>
                      <th style="width:30%;">پیری کے بعد پنشر (Follow-up Punish)</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${pm.character_parries_table.map(cp => `
                      <tr>
                        <td><strong>${escapeHtml(cp.char)}</strong></td>
                        <td><code class="cmd-pill">${escapeHtml(cp.cmd)}</code></td>
                        <td>${escapeHtml(cp.catches)}</td>
                        <td class="cell-ur">${escapeHtml(cp.followup_ur)}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Charge Guard Breaks & Parries -->
            <div class="strat-hub-box mt-4">
              <h3 class="strat-hub-box-title">⚡ 5. How to "Charge" Guard-Breaks &amp; Defensive Parries</h3>
              <div class="strat-hub-subgrid">
                <div class="charge-card charge-defensive">
                  <span class="charge-label">🛡️ Defensive Parry Extension</span>
                  <p class="charge-desc">${escapeHtml(pm.charge_guard_break_guide.defensive_ur)}</p>
                </div>
                <div class="charge-card charge-offensive">
                  <span class="charge-label">💥 Offensive Guard-Break Holds (*)</span>
                  <p class="charge-desc">${escapeHtml(pm.charge_guard_break_guide.offensive_ur)}</p>
                </div>
              </div>
            </div>
          </div>
        `;
      } else if (state.activeUniversalTab === 'wall-bible') {
        const wb = u.wall_traps_escape;
        container.innerHTML = `
          <div class="strat-hub-mech-pane">
            <!-- Wall Combo Science -->
            <div class="strat-hub-box">
              <div class="box-head-split">
                <h3 class="strat-hub-box-title">🧱 1. The Wall Combo &amp; Wall Crush Science</h3>
                <span class="box-head-pill gold">+5 to +9 Wall Crush</span>
              </div>
              <p class="strat-hub-box-desc">${escapeHtml(wb.wall_combo_science_ur)}</p>
              <div class="strat-hub-wall-crush-callout">
                <strong>Universal Wall Crush Mechanics:</strong> ${escapeHtml(wb.universal_wall_crush_ur)}
              </div>
            </div>

            <!-- 8 Character Specific Wall Traps -->
            <div class="strat-hub-box mt-4">
              <h3 class="strat-hub-box-title">🩸 2. 8 Character-Specific Deadly Wall Traps (دیوار کے جان لیوا جال)</h3>
              <div class="strat-hub-wall-traps-grid">
                ${wb.character_wall_traps.map((wt, idx) => `
                  <div class="wall-trap-card">
                    <div class="wt-head">
                      <span class="wt-num">#${idx + 1}</span>
                      <div class="wt-char-info">
                        <span class="wt-char">${escapeHtml(wt.char)}</span>
                        <h4 class="wt-name">${escapeHtml(wt.name)}</h4>
                      </div>
                    </div>
                    <p class="wt-desc-ur">${escapeHtml(wt.desc_ur)}</p>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- Wall Escape 3 Golden Rules -->
            <div class="strat-hub-box mt-4">
              <h3 class="strat-hub-box-title">🏃 3. Wall Escape Bible: دیوار کے جال سے خود کیسے نکلیں؟</h3>
              <p class="strat-hub-box-desc">
                اگر آپ خود دیوار کے ساتھ پھنس جائیں تو گھبرا کر سست لانچرز مت دبائیں! یہ 3 سنہری طریقے آپ کی جان بچائیں گے:
              </p>
              <div class="strat-hub-escape-grid">
                ${wb.escape_rules.map(er => `
                  <div class="escape-rule-card">
                    <div class="esc-badge">${escapeHtml(er.badge)}</div>
                    <h4 class="esc-title">${escapeHtml(er.rule)}</h4>
                    <p class="esc-desc-ur">${escapeHtml(er.desc_ur)}</p>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
        `;
      }
    },

    // =========================================================================
    // Filterable Character Roster Grid
    // =========================================================================
    onSearchInput: function (val) {
      state.searchQuery = val || '';
      this.filterRosterGrid();
    },

    clearSearch: function () {
      state.searchQuery = '';
      const input = document.getElementById('stratHubSearchInput');
      if (input) input.value = '';
      this.filterRosterGrid();
    },

    setSeasonFilter: function (season) {
      state.selectedSeason = season;
      document.querySelectorAll('#stratHubSeasonPills .strat-hub-pill').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.includes(season) || (season === 'ALL' && btn.textContent.includes('All')));
      });
      this.filterRosterGrid();
    },

    setWeakSideFilter: function (ws) {
      state.selectedWeakSide = ws;
      document.querySelectorAll('#stratHubWeakSidePills .strat-hub-pill').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.includes(ws) || (ws === 'ALL' && btn.textContent.includes('All')));
      });
      this.filterRosterGrid();
    },

    setFactionFilter: function (fac) {
      state.selectedFaction = fac;
      document.querySelectorAll('#stratHubFactionPills .strat-hub-pill').forEach(btn => {
        const text = btn.textContent;
        const isMatch = (fac === 'ALL' && text.includes('All')) ||
                        (fac.includes('Yggdrasil') && text.includes('Yggdrasil')) ||
                        (fac.includes('G-Corp') && text.includes('G-Corp')) ||
                        (fac.includes('Mishima') && text.includes('Mishima')) ||
                        (fac.includes('Monks') && text.includes('Monks')) ||
                        (fac.includes('Veterans') && text.includes('Veterans')) ||
                        (fac.includes('Guest') && text.includes('Guest'));
        btn.classList.toggle('active', isMatch);
      });
      this.filterRosterGrid();
    },

    filterRosterGrid: function () {
      const data = getMasterData();
      if (!data || !data.roster) return;

      const grid = document.getElementById('stratHubGrid');
      const counter = document.getElementById('stratHubRosterCount');
      if (!grid) return;

      const filtered = data.filterRoster({
        season: state.selectedSeason,
        faction: state.selectedFaction,
        weak_side: state.selectedWeakSide,
        search: state.searchQuery
      });

      if (counter) {
        counter.textContent = `Showing ${filtered.length} of ${data.roster.length} Warriors`;
      }

      if (filtered.length === 0) {
        grid.innerHTML = `
          <div class="strat-hub-empty">
            <div class="empty-icon">🔍</div>
            <h3>No Warriors Matched Your Filters</h3>
            <p>Try clearing your search query or switching season/faction pills.</p>
            <button type="button" class="btn btn-secondary mt-2" onclick="StrategyHub.resetAllFilters()">Reset All Filters</button>
          </div>
        `;
        return;
      }

      grid.innerHTML = filtered.map(f => `
        <div class="strat-hub-card fighter-card" onclick="StrategyHub.openStrategyModal('${f.slug}')" role="button" tabindex="0">
          <!-- Card Header Avatar & Flags -->
          <div class="f-card-banner">
            <img src="${escapeHtml(f.avatar)}" alt="${escapeHtml(f.name)}" class="f-card-avatar" onerror="this.src='/assets/avatars/heihachi.jpg'">
            <div class="f-card-tags">
              <span class="f-tag-season">${escapeHtml(f.season)}</span>
              <span class="f-tag-weak ${f.weak_side.toLowerCase()}">${escapeHtml(f.weak_side)}</span>
            </div>
          </div>

          <!-- Card Body -->
          <div class="f-card-body">
            <div class="f-card-title-row">
              <h3 class="f-card-name">${escapeHtml(f.name)}</h3>
              <span class="f-card-flag" title="${escapeHtml(f.country)}">${escapeHtml(f.country_flag)}</span>
            </div>
            <div class="f-card-title-alias">${escapeHtml(f.title)}</div>

            <div class="f-card-faction">
              <span class="faction-dot"></span>
              <span class="faction-text">${escapeHtml(f.faction_badge)}</span>
            </div>

            <div class="f-card-style">
              <span class="style-icon">🥋</span>
              <span class="style-text">${escapeHtml(f.style)}</span>
            </div>
          </div>

          <!-- Card Footer CTA -->
          <div class="f-card-footer">
            <span class="f-cta-label">Open Strategy Dossier</span>
            <span class="f-cta-arrow">⟶</span>
          </div>
        </div>
      `).join('');
    },

    resetAllFilters: function () {
      state.searchQuery = '';
      state.selectedSeason = 'ALL';
      state.selectedFaction = 'ALL';
      state.selectedWeakSide = 'ALL';
      const searchInput = document.getElementById('stratHubSearchInput');
      if (searchInput) searchInput.value = '';
      this.filterRosterGrid();
    },

    // =========================================================================
    // Component 2: Interactive Character Profile Modal (3 Tabs)
    // =========================================================================
    openStrategyModal: function (slug) {
      const data = getMasterData();
      if (!data) return;

      const fighter = data.getFighter(slug);
      if (!fighter) {
        console.error('StrategyHub: Fighter not found with slug:', slug);
        return;
      }

      state.currentModalFighter = fighter;
      const modal = document.getElementById('strategyDossierModal');
      if (!modal) return;

      modal.innerHTML = this.renderModalContent(fighter);
      modal.style.display = 'flex';
      document.body.classList.add('sh-modal-open');

      // Default active tab: Tab 3 (Anti-Character Guide) or previous selection
      this.switchModalTab(state.activeModalTab);
    },

    closeStrategyModal: function () {
      const modal = document.getElementById('strategyDossierModal');
      if (modal) {
        modal.style.display = 'none';
        modal.innerHTML = '';
      }
      document.body.classList.remove('sh-modal-open');
      state.currentModalFighter = null;
    },

    switchModalTab: function (tabKey) {
      state.activeModalTab = tabKey;
      document.querySelectorAll('.sh-modal-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-tab') === tabKey);
      });
      document.querySelectorAll('.sh-modal-tab-content').forEach(pane => {
        pane.classList.toggle('active', pane.getAttribute('data-tab') === tabKey);
      });
    },

    renderModalContent: function (f) {
      return `
        <div class="sh-modal-card" onclick="event.stopPropagation()">
          <!-- Modal Top Header -->
          <div class="sh-modal-header">
            <div class="sh-modal-hero-left">
              <img src="${escapeHtml(f.avatar)}" alt="${escapeHtml(f.name)}" class="sh-modal-avatar" onerror="this.src='/assets/avatars/heihachi.jpg'">
              <div class="sh-modal-identity">
                <div class="sh-modal-badge-row">
                  <span class="sh-badge-season">${escapeHtml(f.season)}</span>
                  <span class="sh-badge-faction">${escapeHtml(f.faction_badge)}</span>
                  <span class="sh-badge-weak ${f.weak_side.toLowerCase()}">Step Weakness: ${escapeHtml(f.weak_side)}</span>
                </div>
                <h2 class="sh-modal-title">${escapeHtml(f.name)}</h2>
                <div class="sh-modal-alias">
                  <span>${escapeHtml(f.country_flag)} ${escapeHtml(f.country)}</span> • 
                  <span>${escapeHtml(f.title)}</span> • 
                  <span>${escapeHtml(f.style)}</span>
                </div>
              </div>
            </div>

            <button type="button" class="sh-modal-close-btn" onclick="StrategyHub.closeStrategyModal()" title="Close Dossier (Esc)">&times;</button>
          </div>

          <!-- Modal Navigation 3 Tabs -->
          <div class="sh-modal-nav-bar" role="tablist">
            <button type="button" class="sh-modal-tab-btn ${state.activeModalTab === 'tab-profile' ? 'active' : ''}" 
                    data-tab="tab-profile" onclick="StrategyHub.switchModalTab('tab-profile')">
              📖 Tab 1: Profile &amp; Lore (پروفائل اور کہانی)
            </button>
            <button type="button" class="sh-modal-tab-btn ${state.activeModalTab === 'tab-offense' ? 'active' : ''}" 
                    data-tab="tab-offense" onclick="StrategyHub.switchModalTab('tab-offense')">
              ⚔️ Tab 2: Offense &amp; Traps (پریشر اور جال)
            </button>
            <button type="button" class="sh-modal-tab-btn ${state.activeModalTab === 'tab-anti' ? 'active' : ''}" 
                    data-tab="tab-anti" onclick="StrategyHub.switchModalTab('tab-anti')">
              🎯 Tab 3: Anti-Character Guide (چکمہ اور کمزوریاں)
            </button>
          </div>

          <!-- Modal Tab Panes -->
          <div class="sh-modal-body">
            
            <!-- Tab 1: Profile & Lore -->
            <div class="sh-modal-tab-content ${state.activeModalTab === 'tab-profile' ? 'active' : ''}" data-tab="tab-profile">
              <div class="sh-tab-grid">
                <!-- Physical Attributes Box -->
                <div class="sh-card-section">
                  <h4 class="sh-section-head">📊 Physical Stats &amp; Identity Metrics</h4>
                  <div class="sh-stats-grid">
                    <div class="sh-stat-item">
                      <span class="sh-stat-lbl">Height (قد):</span>
                      <span class="sh-stat-val">${escapeHtml(f.height || 'Standard')}</span>
                    </div>
                    <div class="sh-stat-item">
                      <span class="sh-stat-lbl">Weight (وزن):</span>
                      <span class="sh-stat-val">${escapeHtml(f.weight || 'Standard')}</span>
                    </div>
                    <div class="sh-stat-item">
                      <span class="sh-stat-lbl">Origin Country (ملک):</span>
                      <span class="sh-stat-val">${escapeHtml(f.country_flag)} ${escapeHtml(f.country)}</span>
                    </div>
                    <div class="sh-stat-item">
                      <span class="sh-stat-lbl">Fighting Style:</span>
                      <span class="sh-stat-val">${escapeHtml(f.style)}</span>
                    </div>
                    <div class="sh-stat-item">
                      <span class="sh-stat-lbl">Faction Alliance:</span>
                      <span class="sh-stat-val">${escapeHtml(f.faction)}</span>
                    </div>
                    <div class="sh-stat-item">
                      <span class="sh-stat-lbl">Sidestep Vulnerability:</span>
                      <span class="sh-stat-val highlight-${f.weak_side.toLowerCase()}">${escapeHtml(f.weak_side)}</span>
                    </div>
                  </div>
                </div>

                <!-- Story & Lore Box -->
                <div class="sh-card-section">
                  <h4 class="sh-section-head">📜 Background History &amp; Tekken 8 Role (کہانی اور کردار)</h4>
                  <div class="sh-lore-box">
                    <p class="sh-lore-text">${escapeHtml(f.job_lore_ur)}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Tab 2: Offense, Pressure & Trap Setup -->
            <div class="sh-modal-tab-content ${state.activeModalTab === 'tab-offense' ? 'active' : ''}" data-tab="tab-offense">
              <div class="sh-offense-flow">
                <!-- Poking Buttons -->
                <div class="sh-card-section">
                  <div class="sh-sec-badge-row">
                    <span class="sh-sec-badge poke">POKING ARSENAL</span>
                    <h4 class="sh-section-head">Key Poking Buttons (تیز رفتار مکے اور ککس)</h4>
                  </div>
                  <div class="sh-code-box">
                    <pre>${escapeHtml(f.poking_buttons_ur)}</pre>
                  </div>
                </div>

                <!-- Plus-Frame Pressure Moves -->
                <div class="sh-card-section">
                  <div class="sh-sec-badge-row">
                    <span class="sh-sec-badge plus">PLUS FRAME PRESSURE</span>
                    <h4 class="sh-section-head">Relentless Pressure Moves (پلس فریم اور اپنی باری قائم رکھنا)</h4>
                  </div>
                  <div class="sh-code-box">
                    <pre>${escapeHtml(f.pressure_moves_ur)}</pre>
                  </div>
                </div>

                <!-- Upper / Mid / Low Mix-up Blender -->
                <div class="sh-card-section">
                  <div class="sh-sec-badge-row">
                    <span class="sh-sec-badge blender">3-WAY MIX-UP BLENDER</span>
                    <h4 class="sh-section-head">High / Mid / Low Stance &amp; 50/50 Mix-up Blender</h4>
                  </div>
                  <div class="sh-code-box">
                    <pre>${escapeHtml(f.mixup_blender_ur)}</pre>
                  </div>
                </div>

                <!-- The Trap ("Jaal") & Wall Setup -->
                <div class="sh-card-section">
                  <div class="sh-sec-badge-row">
                    <span class="sh-sec-badge trap">SIGNATURE TRAP ("JAAL")</span>
                    <h4 class="sh-section-head">Frame Trap Sequence &amp; Deadly Wall Oki Setup</h4>
                  </div>
                  <div class="sh-code-box">
                    <pre>${escapeHtml(f.trap_setup_ur)}</pre>
                  </div>
                </div>
              </div>
            </div>

            <!-- Tab 3: Anti-Character Guide (CRITICAL) -->
            <div class="sh-modal-tab-content ${state.activeModalTab === 'tab-anti' ? 'active' : ''}" data-tab="tab-anti">
              <div class="sh-anti-flow">
                <!-- 1. Which Side to Step -->
                <div class="sh-anti-card step-card">
                  <div class="anti-card-head">
                    <span class="anti-step-badge ${f.weak_side.toLowerCase()}">
                      ${f.weak_side === 'SSL' ? '⟵ SIDESTEP LEFT (SSL)' : 'SIDESTEP RIGHT (SSR) ⟶'}
                    </span>
                    <h4 class="anti-card-title">1. Which Side to Step (کس سائیڈ سے پکڑنا ہے؟)</h4>
                  </div>
                  <p class="anti-card-desc-ur">${escapeHtml(f.anti_guide.weak_side_detail_ur)}</p>
                </div>

                <!-- 2. Minus & Launch Punishable Moves -->
                <div class="sh-anti-card punish-card">
                  <div class="anti-card-head">
                    <span class="anti-step-badge minus">-10 to -14 &amp; -15+ LAUNCH</span>
                    <h4 class="anti-card-title">2. Minus Frame &amp; Launch Punishable Moves (غیر محفوظ مووز)</h4>
                  </div>
                  <p class="anti-card-desc-ur">${escapeHtml(f.anti_guide.minus_punishable_moves_ur)}</p>
                </div>

                <!-- 3. Bait, Duck & Interrupt -->
                <div class="sh-anti-card duck-card">
                  <div class="anti-card-head">
                    <span class="anti-step-badge duck">DUCK &amp; LAUNCH / DICKJAB</span>
                    <h4 class="anti-card-title">3. How to Bait, Duck &amp; Interrupt (چکمہ کیسے دیں؟)</h4>
                  </div>
                  <p class="anti-card-desc-ur">${escapeHtml(f.anti_guide.bait_duck_interrupt_ur)}</p>
                </div>

                <!-- 4. Parry Vulnerabilities -->
                <div class="sh-anti-card parry-card">
                  <div class="anti-card-head">
                    <span class="anti-step-badge parry">PARRY &amp; REVERSAL COUNTERS</span>
                    <h4 class="anti-card-title">4. Parry Vulnerabilities &amp; Unparryable Moves</h4>
                  </div>
                  <p class="anti-card-desc-ur">${escapeHtml(f.anti_guide.parry_vulnerabilities_ur)}</p>
                </div>
              </div>
            </div>

          </div>

          <!-- Modal Footer with Quick Links -->
          <div class="sh-modal-footer">
            <div class="sh-footer-links">
              <button type="button" class="btn btn-secondary btn-sm" onclick="StrategyHub.launchInMatchup('${f.slug}')">
                ⚔️ Load in Matchup Lab
              </button>
              <button type="button" class="btn btn-secondary btn-sm" onclick="StrategyHub.launchInComboLab('${f.slug}')">
                🥋 Open in Combo Lab
              </button>
            </div>
            <button type="button" class="btn btn-primary btn-sm" onclick="StrategyHub.closeStrategyModal()">
              Close Dossier
            </button>
          </div>
        </div>
      `;
    },

    launchInMatchup: function (slug) {
      this.closeStrategyModal();
      if (typeof window.switchAppView === 'function') {
        window.switchAppView('matchup', 'analyzer');
      }
      if (typeof window.compareInMatchup === 'function') {
        window.compareInMatchup(slug);
      }
    },

    launchInComboLab: function (slug) {
      this.closeStrategyModal();
      if (typeof window.switchAppView === 'function') {
        window.switchAppView('fighters', 'combo-lab');
      }
      if (typeof window.loadInComboLab === 'function') {
        window.loadInComboLab(slug);
      }
    }
  };

  // Expose globally
  window.StrategyHub = StrategyHub;

  console.log('✅ StrategyHub Controller Loaded.');
})();

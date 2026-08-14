/**
 * RegexForge - Complete Frontend Application Logic & Compiler Integration
 * Course: CSE314 — Compiler Design Lab (Project 24 | Uronto Helicopter)
 */

document.addEventListener('DOMContentLoaded', () => {
  console.log('⚡ RegexForge Engine Initialized');
  setupThemeToggle();
  highlightActiveNav();
  setupExampleModal();
  setupWorkspacePage();
  setupAnalyzerPage();
  setupNFAPage();
  setupDFAPage();
  setupTestingPage();
});

/**
 * Handles Dark/Light Mode toggle and persistence.
 */
function setupThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle-btn');
  const toggleIcon = document.getElementById('theme-toggle-icon');
  
  const updateIcon = () => {
    const isDark = document.documentElement.classList.contains('dark');
    if (toggleIcon) {
      toggleIcon.textContent = isDark ? 'light_mode' : 'dark_mode';
    }
  };

  updateIcon();

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      document.documentElement.classList.toggle('dark');
      const isDark = document.documentElement.classList.contains('dark');
      localStorage.setItem('regexforge-theme', isDark ? 'dark' : 'light');
      updateIcon();
      showToast(`Switched to ${isDark ? 'Dark' : 'Light'} Mode`, 'info');
      
      if (window.nfaVis) window.nfaVis.updateThemeColors(isDark);
      if (window.dfaVis) window.dfaVis.updateThemeColors(isDark);
    });
  }
}

const REGEX_STORAGE_KEY = 'regexforge_active_regex';
const REGEX_DEFAULT = '(a|b)*abb';

/**
 * Returns currently active regex from URL query, localStorage, or fallback default.
 */
function getActiveRegex() {
  const urlParams = new URLSearchParams(window.location.search);
  const queryRegex = urlParams.get('regex');
  if (queryRegex && queryRegex.trim() !== '') {
    const val = queryRegex.trim();
    localStorage.setItem(REGEX_STORAGE_KEY, val);
    return val;
  }
  const saved = localStorage.getItem(REGEX_STORAGE_KEY);
  if (saved && saved.trim() !== '') {
    return saved.trim();
  }
  return REGEX_DEFAULT;
}

/**
 * Persists newly specified regex and updates top navbar links.
 */
function setActiveRegex(val) {
  if (val === undefined || val === null || val.trim() === '') return;
  const cleaned = val.trim();
  localStorage.setItem(REGEX_STORAGE_KEY, cleaned);
  highlightActiveNav();
}

/**
 * Highlights current active menu item based on window location.
 */
function highlightActiveNav() {
  const currentPath = window.location.pathname;
  const activeRegex = getActiveRegex();
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    const origHref = link.getAttribute('href') || '';
    const basePath = origHref.split('?')[0];

    if (activeRegex && (basePath === '/workspace' || basePath === '/analyzer' || basePath === '/nfa' || basePath === '/dfa' || basePath === '/testing')) {
      link.setAttribute('href', `${basePath}?regex=${encodeURIComponent(activeRegex)}`);
    } else if (basePath === '/') {
      link.setAttribute('href', '/');
    }

    if (basePath === currentPath) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

/**
 * Show toast notification message.
 */
function showToast(message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${message}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

/**
 * Modal logic for loading regex examples.
 */
function setupExampleModal() {
  const modal = document.getElementById('examples-modal');
  const openBtn = document.getElementById('btn-load-examples');
  const closeBtn = document.getElementById('btn-close-modal');

  if (openBtn && modal) {
    openBtn.addEventListener('click', async () => {
      modal.classList.add('active');
      loadExamplesList();
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => {
      modal.classList.remove('active');
    });
  }
}

async function loadExamplesList() {
  const container = document.getElementById('examples-list');
  if (!container) return;

  try {
    const res = await fetch('/api/examples');
    const examples = await res.json();

    container.innerHTML = examples.map(ex => `
      <div class="glass-panel" style="padding: 1rem; margin-bottom: 0.75rem; cursor: pointer;" onclick="selectExample('${ex.regex}')">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <h4 style="color: var(--accent-cyan); font-family: var(--font-mono);">${ex.regex}</h4>
          <span class="badge badge-info">${ex.name}</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">${ex.description}</p>
      </div>
    `).join('');
  } catch (err) {
    container.innerHTML = `<p style="color: var(--accent-rose);">Failed to load examples.</p>`;
  }
}

function selectExample(regex) {
  setActiveRegex(regex);
  const input = document.getElementById('regex-input') || document.getElementById('test-regex-input');
  if (input) {
    input.value = regex;
    showToast(`Loaded pattern: ${regex}`, 'info');
    const modal = document.getElementById('examples-modal');
    if (modal) modal.classList.remove('active');
  }
}

/**
 * 1. Workspace Homepage Integration
 */
function setupWorkspacePage() {
  const form = document.getElementById('regex-form');
  const regexInput = document.getElementById('regex-input');
  if (!form || !regexInput) return;

  const activeRegex = getActiveRegex();
  regexInput.value = activeRegex;

  const updateMetrics = async (regex) => {
    try {
      const res = await fetch(`/api/analyze?regex=${encodeURIComponent(regex)}`);
      const data = await res.json();
      if (data.success && data.stats) {
        document.getElementById('stat-tokens').textContent = data.stats.tokens;
        document.getElementById('stat-nodes').textContent = data.stats.ast_nodes;
        document.getElementById('stat-nfa-states').textContent = data.stats.nfa_states;
        document.getElementById('stat-nfa-trans').textContent = data.stats.nfa_transitions;
        document.getElementById('stat-dfa-states').textContent = data.stats.dfa_states;
        document.getElementById('stat-dfa-trans').textContent = data.stats.dfa_transitions;
      }
    } catch (err) {
      console.error(err);
    }
  };

  updateMetrics(activeRegex);

  regexInput.addEventListener('input', (e) => {
    const val = e.target.value.trim();
    if (val) {
      setActiveRegex(val);
      updateMetrics(val);
    }
  });

  form.addEventListener('submit', (e) => {
    const val = regexInput.value.trim();
    if (val) {
      setActiveRegex(val);
      animateCompilerPipeline();
    }
  });
}

function animateCompilerPipeline() {
  const cards = document.querySelectorAll('.pipeline-stage-card');
  if (!cards || cards.length === 0) return;

  cards.forEach(c => c.classList.remove('active-stage', 'completed-stage'));

  let stage = 0;
  const interval = setInterval(() => {
    if (stage < cards.length) {
      if (stage > 0) {
        cards[stage - 1].classList.remove('active-stage');
        cards[stage - 1].classList.add('completed-stage');
      }
      cards[stage].classList.add('active-stage');
      stage++;
    } else {
      clearInterval(interval);
      if (cards.length > 0) {
        cards[cards.length - 1].classList.remove('active-stage');
        cards[cards.length - 1].classList.add('completed-stage');
      }
    }
  }, 250);
}

/**
 * 2. Analyzer Page Integration
 */
function setupAnalyzerPage() {
  const tableBody = document.getElementById('token-table-body');
  if (!tableBody) return;

  const regex = getActiveRegex();

  const badge = document.getElementById('current-regex-badge');
  if (badge) {
    badge.textContent = `Expression: /${regex}/`;
  }

  fetchAnalysisData(regex);
}

async function fetchAnalysisData(regex) {
  const tableBody = document.getElementById('token-table-body');
  if (!tableBody) return;

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ regex: regex })
    });

    const data = await response.json();

    if (data.success) {
      renderTokenTable(data.tokens);
      if (data.ast && typeof ASTVisualizer !== 'undefined') {
        ASTVisualizer.renderTree('ast-tree-container', data.ast);
      }
    } else {
      renderAnalysisError(data.error);
    }
  } catch (err) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="4" style="color: var(--accent-rose); text-align: center;">
          Network/Server error while analyzing expression.
        </td>
      </tr>
    `;
  }
}

function getTokenBadgeClass(type) {
  switch (type) {
    case 'SYMBOL': return 'badge-success';
    case 'CONCAT': return 'badge-warning';
    case 'UNION': return 'badge-warning';
    case 'KLEENE_STAR': return 'badge-warning';
    case 'PLUS': return 'badge-warning';
    case 'OPTIONAL': return 'badge-warning';
    case 'LPAREN': return 'badge-info';
    case 'RPAREN': return 'badge-info';
    case 'WILDCARD': return 'badge-info';
    case 'EOF': return 'badge-secondary';
    default: return 'badge-info';
  }
}

function getTokenMeaning(token) {
  switch (token.type) {
    case 'SYMBOL': return `Literal Symbol '${token.value}'`;
    case 'CONCAT': return 'Explicit Concatenation Operator (•)';
    case 'UNION': return 'Union / Alternation Operator (|)';
    case 'KLEENE_STAR': return 'Zero-or-more Repetition (*)';
    case 'PLUS': return 'One-or-more Repetition (+)';
    case 'OPTIONAL': return 'Zero-or-one Optional (?)';
    case 'LPAREN': return "Left Group Parenthesis '('";
    case 'RPAREN': return "Right Group Parenthesis ')'";
    case 'WILDCARD': return 'Wildcard Any-Character Symbol (.)';
    case 'EOF': return 'End of Expression';
    default: return token.type;
  }
}

function renderTokenTable(tokens) {
  const tableBody = document.getElementById('token-table-body');
  if (!tableBody) return;

  tableBody.innerHTML = tokens.map(t => {
    const badgeClass = getTokenBadgeClass(t.type);
    const meaning = getTokenMeaning(t);
    const displayVal = t.value === "" ? "EOF" : t.value;

    return `
      <tr>
        <td><code>${t.position}</code></td>
        <td><code>${displayVal}</code></td>
        <td><span class="badge ${badgeClass}">${t.type}</span></td>
        <td>${meaning}</td>
      </tr>
    `;
  }).join('');
}

function renderAnalysisError(error) {
  const tableBody = document.getElementById('token-table-body');
  const astContainer = document.getElementById('ast-tree-container');

  if (tableBody) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="4" style="padding: 1rem; background: rgba(244, 63, 94, 0.1); border: 1px solid var(--accent-rose); border-radius: 8px;">
          <div style="color: var(--accent-rose); font-weight: bold; margin-bottom: 0.25rem;">
            ❌ ${error.error_type || 'Syntax Error'} (Position ${error.position})
          </div>
          <div style="color: var(--text-primary); font-size: 0.9rem;">
            ${error.message}
          </div>
        </td>
      </tr>
    `;
  }

  if (astContainer) {
    astContainer.innerHTML = `
      <div style="padding: 1.5rem; color: var(--accent-rose); font-family: var(--font-mono);">
        ❌ Syntax Error at position ${error.position}:<br>
        ${error.message}
      </div>
    `;
  }
}

/**
 * 3. NFA Page Integration
 */
function setupNFAPage() {
  const container = document.getElementById('nfa-cy-container');
  if (!container) return;

  const regex = getActiveRegex();

  const badge = document.getElementById('nfa-regex-badge');
  if (badge) badge.textContent = `Expression: /${regex}/`;

  window.nfaVis = new GraphVisualizer('nfa-cy-container');
  window.thompsonAnimator = new ThompsonConstructionAnimator(window.nfaVis);

  const playBtn = document.getElementById('btn-play-nfa');
  const prevBtn = document.getElementById('btn-prev-nfa');
  const stepBtn = document.getElementById('btn-step-nfa');
  const resetBtn = document.getElementById('btn-reset-nfa');

  fetch(`/api/analyze?regex=${encodeURIComponent(regex)}`)
    .then(res => res.json())
    .then(data => {
      if (data.success && data.nfa) {
        document.getElementById('nfa-start-badge').textContent = `Start: ${data.nfa.start_state}`;
        document.getElementById('nfa-accept-badge').textContent = `Accepting: ${data.nfa.accept_states.join(', ')}`;
        document.getElementById('nfa-count-badge').textContent = `${data.nfa.transitions.length} Transitions`;

        window.nfaVis.renderGraph(data.nfa_elements);
        renderNFATable(data.nfa.transitions);

        if (window.thompsonAnimator) {
          window.thompsonAnimator.setData(data.nfa_elements);
        }
      }
    })
    .catch(err => console.error(err));

  if (playBtn) playBtn.onclick = () => window.thompsonAnimator && window.thompsonAnimator.play();
  if (prevBtn) prevBtn.onclick = () => window.thompsonAnimator && window.thompsonAnimator.prev();
  if (stepBtn) stepBtn.onclick = () => window.thompsonAnimator && window.thompsonAnimator.next();
  if (resetBtn) resetBtn.onclick = () => window.thompsonAnimator && window.thompsonAnimator.reset();
}

function renderNFATable(transitions) {
  const body = document.getElementById('nfa-table-body');
  if (!body) return;

  body.innerHTML = transitions.map(t => {
    const isEpsilon = t.symbol === 'ε';
    const badgeClass = isEpsilon ? 'badge-warning' : 'badge-success';
    const typeLabel = isEpsilon ? 'Epsilon Transition' : 'Symbol Transition';

    return `
      <tr>
        <td><code>${t.from}</code></td>
        <td><code>${t.symbol}</code></td>
        <td><code>${t.to}</code></td>
        <td><span class="badge ${badgeClass}">${typeLabel}</span></td>
      </tr>
    `;
  }).join('');
}

/**
 * 4. DFA Page Integration
 */
function setupDFAPage() {
  const container = document.getElementById('dfa-cy-container');
  if (!container) return;

  const regex = getActiveRegex();

  const badge = document.getElementById('dfa-regex-badge');
  if (badge) badge.textContent = `Expression: /${regex}/`;

  window.dfaVis = new GraphVisualizer('dfa-cy-container');
  window.subsetAnimator = new SubsetConstructionAnimator(window.dfaVis);

  const playBtn = document.getElementById('btn-play-subset');
  const prevBtn = document.getElementById('btn-prev-subset');
  const stepBtn = document.getElementById('btn-step-subset');
  const resetBtn = document.getElementById('btn-reset-subset');

  fetch(`/api/analyze?regex=${encodeURIComponent(regex)}`)
    .then(res => res.json())
    .then(data => {
      if (data.success && data.dfa) {
        document.getElementById('dfa-start-badge').textContent = `Start State: ${data.dfa.start_state}`;
        document.getElementById('dfa-accept-badge').textContent = `Accepting: ${data.dfa.accept_states.join(', ')}`;

        window.dfaVis.renderGraph(data.dfa_elements);
        renderDFATable(data.dfa);

        if (window.subsetAnimator) {
          window.subsetAnimator.setData(data.dfa, data.dfa_elements);
        }
      }
    })
    .catch(err => console.error(err));

  if (playBtn) playBtn.onclick = () => window.subsetAnimator && window.subsetAnimator.play();
  if (prevBtn) prevBtn.onclick = () => window.subsetAnimator && window.subsetAnimator.prev();
  if (stepBtn) stepBtn.onclick = () => window.subsetAnimator && window.subsetAnimator.next();
  if (resetBtn) resetBtn.onclick = () => window.subsetAnimator && window.subsetAnimator.reset();
}

function renderDFATable(dfa) {
  const body = document.getElementById('dfa-table-body');
  if (!body) return;

  body.innerHTML = dfa.states.map(state => {
    const nfaSet = dfa.state_sets[state] || [];
    const isAccepting = dfa.accept_states.includes(state);
    const isStart = state === dfa.start_state;

    let statusBadge = `<span class="badge badge-info">Intermediate</span>`;
    if (isAccepting) statusBadge = `<span class="badge badge-success">✓ Accepting</span>`;
    if (isStart) statusBadge += ` <span class="badge badge-info">Start State</span>`;

    const outTransitions = dfa.transitions.filter(t => t.from === state);
    const transStr = outTransitions.map(t => `${t.symbol} ➔ ${t.to}`).join(', ') || 'None';

    return `
      <tr>
        <td><code style="color: var(--accent-cyan); font-weight: bold;">${state}</code></td>
        <td><code>{${nfaSet.join(', ')}}</code></td>
        <td><code>${transStr}</code></td>
        <td>${statusBadge}</td>
      </tr>
    `;
  }).join('');
}

/**
 * 5. String Matcher & Testing Page Integration
 */
function setupTestingPage() {
  const runBtn = document.getElementById('btn-run-match');
  if (!runBtn) return;

  const regexInput = document.getElementById('test-regex-input');
  const activeRegex = getActiveRegex();
  if (regexInput) {
    regexInput.value = activeRegex;
  }

  const animateBtn = document.getElementById('btn-animate-trace');
  if (animateBtn) {
    animateBtn.onclick = () => {
      if (window.lastMatchResults && window.lastMatchResults.length > 0) {
        const activeItem = window.activeTraceResult || window.lastMatchResults[0];
        if (typeof TraceAnimator !== 'undefined') {
          TraceAnimator.animateStringTrace(activeItem);
        }
      }
    };
  }

  const executeBatch = async () => {
    const regexInput = document.getElementById('test-regex-input');
    const stringsInput = document.getElementById('test-strings-input');
    if (!regexInput || !stringsInput) return;

    const regex = regexInput.value.trim() || activeRegex;
    setActiveRegex(regex);

    const testStrings = stringsInput.value.split('\n').map(s => s.trim()).filter(s => s !== null);

    const badge = document.getElementById('testing-regex-badge');
    if (badge) badge.textContent = `Regex: /${regex}/`;

    try {
      const res = await fetch('/api/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ regex: regex, test_strings: testStrings })
      });

      const data = await res.json();
      if (data.success) {
        window.lastMatchResults = data.results;
        renderTestResultsTable(data.results);
        if (data.results.length > 0) {
          renderTraceTimeline(data.results[0]);
        }
      } else {
        renderMatcherError(data.error);
      }
    } catch (err) {
      console.error(err);
    }
  };

  runBtn.addEventListener('click', executeBatch);
  if (regexInput) {
    regexInput.addEventListener('input', (e) => {
      const val = e.target.value.trim();
      if (val) {
        setActiveRegex(val);
      }
    });
  }
  executeBatch();
}

function renderTestResultsTable(results) {
  const body = document.getElementById('test-results-body');
  if (!body) return;

  body.innerHTML = results.map((r, idx) => {
    const badgeClass = r.is_match ? 'badge-success' : 'badge-error';
    const resultLabel = r.is_match ? '✓ MATCH' : '✕ NO MATCH';
    const displayString = r.string === "" ? 'ε (empty)' : r.string;

    return `
      <tr>
        <td><code>${displayString}</code></td>
        <td><code>${r.final_state}</code></td>
        <td><span class="badge ${badgeClass}">${resultLabel}</span></td>
        <td><button class="btn btn-secondary btn-sm" onclick="selectTrace(${idx})">🔍 Trace</button></td>
      </tr>
    `;
  }).join('');
}

function selectTrace(index) {
  if (window.lastMatchResults && window.lastMatchResults[index]) {
    renderTraceTimeline(window.lastMatchResults[index]);
  }
}

function renderTraceTimeline(result) {
  window.activeTraceResult = result;
  const container = document.getElementById('trace-steps-container');
  const badge = document.getElementById('trace-string-badge');
  if (!container) return;

  if (badge) {
    const displayStr = result.string === "" ? "ε (empty)" : `"${result.string}"`;
    badge.textContent = `String: ${displayStr}`;
  }

  if (!result.trace || result.trace.length === 0) {
    const initialStatus = result.is_match ? "✓ MATCH (Start state is Accepting)" : "✕ NO MATCH";
    container.innerHTML = `
      <div class="stat-card" style="border-left: 3px solid var(--accent-indigo);">
        <span class="stat-label">Empty String Evaluation</span>
        <div style="font-family: var(--font-mono); font-size: 1rem; color: var(--text-primary); margin-top: 0.25rem;">
          Final State: <strong>${result.final_state}</strong> (${initialStatus})
        </div>
      </div>
    `;
    return;
  }

  container.innerHTML = result.trace.map(step => {
    const isEnd = step.step === result.trace.length;
    let border = 'var(--accent-indigo)';
    let badgeHtml = `<span class="badge badge-info">Step ${step.step}</span>`;

    if (step.next_state === 'DEAD') {
      border = 'var(--accent-rose)';
      badgeHtml = `<span class="badge badge-error">✕ Dead State</span>`;
    } else if (step.is_accepting && isEnd) {
      border = 'var(--accent-emerald)';
      badgeHtml = `<span class="badge badge-success">✓ Accept State</span>`;
    }

    return `
      <div class="stat-card" style="border-left: 3px solid ${border}; margin-bottom: 0.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span class="stat-label">Step ${step.step} • Read '${step.character}'</span>
          ${badgeHtml}
        </div>
        <div style="font-family: var(--font-mono); font-size: 1rem; color: var(--text-primary); margin-top: 0.25rem;">
          State <strong>${step.current_state}</strong> ➔ State <strong>${step.next_state}</strong>
        </div>
      </div>
    `;
  }).join('');

  if (typeof TraceAnimator !== 'undefined') {
    TraceAnimator.animateStringTrace({
      input_string: result.string,
      trace: result.trace,
      is_match: result.is_match
    });
  }
}

function renderMatcherError(error) {
  const body = document.getElementById('test-results-body');
  if (body) {
    body.innerHTML = `
      <tr>
        <td colspan="4" style="color: var(--accent-rose); padding: 1rem;">
          ❌ ${error.error_type || 'Syntax Error'}: ${error.message}
        </td>
      </tr>
    `;
  }
}

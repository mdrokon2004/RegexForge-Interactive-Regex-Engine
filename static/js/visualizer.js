/**
 * RegexForge - AST Tree, Subset Construction & Execution Trace Visualizer Engine
 * Course: CSE314 — Compiler Design Lab (Uronto Helicopter)
 */

class ASTVisualizer {
  /**
   * Renders Abstract Syntax Tree into container element with staggered entrance.
   */
  static renderTree(containerId, astData) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!astData || Object.keys(astData).length === 0) {
      container.innerHTML = `<div style="color: var(--text-muted); padding: 1rem;">No AST generated.</div>`;
      return;
    }

    const treeText = ASTVisualizer.formatNode(astData, "", true);
    container.innerHTML = `
      <pre class="font-mono ast-node-appear" style="color: var(--accent-cyan); font-size: 0.95rem; line-height: 1.5; margin: 0;">${treeText}</pre>
    `;
  }

  /**
   * Formats AST dict into clean ASCII tree representation.
   */
  static formatNode(node, prefix = "", isLast = true) {
    if (!node) return "";

    const connector = isLast ? "└── " : "├── ";
    let label = node.label || node.type || "NODE";
    if (node.type === "SYMBOL") {
      label = `'${node.value}'`;
    } else if (node.type === "WILDCARD") {
      label = "WILDCARD (.)";
    }

    let result = prefix + connector + label + "\n";

    const children = node.children || [];
    const childPrefix = prefix + (isLast ? "    " : "│   ");

    for (let i = 0; i < children.length; i++) {
      const isLastChild = (i === children.length - 1);
      result += ASTVisualizer.formatNode(children[i], childPrefix, isLastChild);
    }

    return result;
  }
}

class TraceVisualizer {
  static renderTrace(containerId, traceSteps) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = traceSteps.map(step => `
      <div class="stat-card" style="margin-bottom: 0.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span class="stat-label">Step ${step.step}: Read Symbol '${step.character}'</span>
          <span class="badge badge-info font-mono">${step.current_state} ➔ ${step.next_state}</span>
        </div>
        <span class="text-xs text-on-surface-variant font-mono mt-1">${step.action}</span>
      </div>
    `).join('');
  }
}

class ThompsonConstructionAnimator {
  constructor(nfaVis) {
    this.nfaVis = nfaVis;
    this.nfaElements = null;
    this.currentStep = 0;
    this.timer = null;
    this.isPlaying = false;
  }

  setData(nfaElements) {
    this.nfaElements = nfaElements;
    this.currentStep = 0;
    this.stop();
  }

  getStepsCount() {
    return 5;
  }

  renderCurrentStep() {
    if (!this.nfaVis || !this.nfaVis.cy) return;

    const cy = this.nfaVis.cy;

    cy.batch(() => {
      cy.elements().removeClass('highlighted completed dimmed');

      if (this.currentStep >= 4) {
        const explainText = document.getElementById('nfa-explain-text');
        if (explainText) {
          explainText.innerHTML = `<strong>Step 5 / 5 — Thompson NFA Complete:</strong> Full Non-Deterministic Finite Automaton with all ε-transitions established.`;
        }
        return;
      }

      cy.elements().addClass('dimmed');

      let stepTitle = "";
      let stepDescription = "";

      switch (this.currentStep) {
        case 0:
          const symbolEdges = cy.edges().filter(e => e.data('label') !== 'ε');
          const symbolNodes = symbolEdges.connectedNodes();
          symbolEdges.removeClass('dimmed').addClass('highlighted');
          symbolNodes.removeClass('dimmed').addClass('highlighted');
          stepTitle = "Step 1 / 5 — Base Literal Symbols";
          stepDescription = "Constructing NFA state pairs for literal character transitions (e.g. 'a', 'b').";
          break;
        case 1:
          const epsEdges = cy.edges().filter(e => e.data('label') === 'ε');
          const epsNodes = epsEdges.connectedNodes();
          cy.edges().filter(e => e.data('label') !== 'ε').removeClass('dimmed').addClass('completed');
          epsEdges.removeClass('dimmed').addClass('highlighted');
          epsNodes.removeClass('dimmed').addClass('highlighted');
          stepTitle = "Step 2 / 5 — Linking Epsilon (ε) Transitions";
          stepDescription = "Injecting non-deterministic ε-transitions for operators (|), (+), (*), and grouping.";
          break;
        case 2:
          cy.edges().removeClass('dimmed').addClass('completed');
          cy.nodes().removeClass('dimmed').addClass('completed');
          stepTitle = "Step 3 / 5 — Alternation & Kleene Star Loops";
          stepDescription = "Evaluating branch splits and feedback loops across Thompson fragment sub-graphs.";
          break;
        case 3:
          cy.elements().removeClass('dimmed').addClass('completed');
          const startNode = cy.nodes('.start-node');
          const acceptNodes = cy.nodes('.accept-node');
          if (startNode) startNode.removeClass('dimmed completed').addClass('highlighted');
          if (acceptNodes) acceptNodes.removeClass('dimmed completed').addClass('highlighted');
          stepTitle = "Step 4 / 5 — Binding Start & Accept States";
          stepDescription = "Designating single entry start state (q0) and accepting exit state(s).";
          break;
      }

      const explainText = document.getElementById('nfa-explain-text');
      if (explainText) {
        explainText.innerHTML = `<strong>${stepTitle}:</strong> ${stepDescription}`;
      }
    });
  }

  next() {
    if (this.currentStep < 4) {
      this.currentStep++;
      this.renderCurrentStep();
    } else {
      this.stop();
    }
  }

  prev() {
    if (this.currentStep > 0) {
      this.currentStep--;
      this.renderCurrentStep();
    }
  }

  play() {
    if (this.isPlaying) return;
    this.isPlaying = true;
    if (this.currentStep >= 4) {
      this.currentStep = 0;
    }
    this.renderCurrentStep();
    this.timer = setInterval(() => {
      if (this.currentStep < 4) {
        this.next();
      } else {
        this.stop();
      }
    }, 1200);
  }

  stop() {
    this.isPlaying = false;
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  reset() {
    this.stop();
    this.currentStep = 4;
    if (this.nfaVis && this.nfaVis.cy) {
      this.nfaVis.cy.elements().removeClass('highlighted completed dimmed');
    }
    const explainText = document.getElementById('nfa-explain-text');
    if (explainText) {
      explainText.textContent = 'Click "▶ Visualize Thompson Construction" to step through the inductive composition of literal fragment NFAs, union (|), Kleene star (*), and concatenation.';
    }
  }
}

class SubsetConstructionAnimator {
  constructor(dfaVis) {
    this.dfaVis = dfaVis;
    this.dfaData = null;
    this.dfaElements = null;
    this.currentStep = 0;
    this.timer = null;
    this.isPlaying = false;
  }

  setData(dfaData, dfaElements) {
    this.dfaData = dfaData;
    this.dfaElements = dfaElements;
    this.currentStep = 0;
    this.stop();
  }

  getStepsCount() {
    if (!this.dfaData || !this.dfaData.states) return 0;
    return this.dfaData.states.length;
  }

  renderCurrentStep() {
    if (!this.dfaVis || !this.dfaVis.cy || !this.dfaData) return;

    const cy = this.dfaVis.cy;
    const states = this.dfaData.states || [];
    const total = states.length;
    if (total === 0) return;

    cy.batch(() => {
      cy.elements().removeClass('highlighted completed dimmed');

      if (this.currentStep >= total) {
        const explainText = document.getElementById('subset-explain-text');
        if (explainText) {
          explainText.innerHTML = `<strong>Step ${total} / ${total} — Subset Construction Complete:</strong> All ${total} DFA states and deterministic transitions fully mapped.`;
        }
        return;
      }

      cy.elements().addClass('dimmed');

      const completedStateIds = states.slice(0, this.currentStep);
      completedStateIds.forEach(id => {
        const node = cy.nodes(`#${id}`);
        if (node) node.removeClass('dimmed').addClass('completed');
      });

      const currentStateId = states[this.currentStep];
      const activeNode = cy.nodes(`#${currentStateId}`);
      if (activeNode) {
        activeNode.removeClass('dimmed completed').addClass('highlighted');
      }

      if (this.currentStep > 0) {
        const inEdges = cy.edges(`[target = "${currentStateId}"]`);
        if (inEdges) inEdges.removeClass('dimmed').addClass('highlighted');
      }

      const nfaSet = (this.dfaData.state_sets && this.dfaData.state_sets[currentStateId]) || [];
      const isStart = currentStateId === this.dfaData.start_state;
      const isAccept = this.dfaData.accept_states.includes(currentStateId);

      let statusBadge = isStart ? ' [Start State]' : (isAccept ? ' [Accepting State]' : '');
      const explainText = document.getElementById('subset-explain-text');

      if (explainText) {
        if (this.currentStep === 0) {
          explainText.innerHTML = `<strong>Step 1 / ${total} — Start State ε-closure:</strong> Computed ε-closure(q0) ➔ Formed start DFA state <code style="color: var(--accent-cyan); font-weight: bold;">${currentStateId}</code> = <code style="font-family: var(--font-mono);">{${nfaSet.join(', ')}}</code>${statusBadge}.`;
        } else {
          explainText.innerHTML = `<strong>Step ${this.currentStep + 1} / ${total} — Subset Transition:</strong> Computed move &amp; ε-closure operations ➔ Formed DFA state <code style="color: var(--accent-cyan); font-weight: bold;">${currentStateId}</code> = <code style="font-family: var(--font-mono);">{${nfaSet.join(', ')}}</code>${statusBadge}.`;
        }
      }
    });
  }

  next() {
    const total = this.getStepsCount();
    if (this.currentStep < total - 1) {
      this.currentStep++;
      this.renderCurrentStep();
    } else {
      this.stop();
    }
  }

  prev() {
    if (this.currentStep > 0) {
      this.currentStep--;
      this.renderCurrentStep();
    }
  }

  play() {
    if (this.isPlaying) return;
    this.isPlaying = true;
    if (this.currentStep >= this.getStepsCount() - 1) {
      this.currentStep = 0;
    }
    this.renderCurrentStep();
    this.timer = setInterval(() => {
      if (this.currentStep < this.getStepsCount() - 1) {
        this.next();
      } else {
        this.stop();
      }
    }, 1200);
  }

  stop() {
    this.isPlaying = false;
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  reset() {
    this.stop();
    const total = this.getStepsCount();
    this.currentStep = total > 0 ? total : 0;
    if (this.dfaVis && this.dfaVis.cy) {
      this.dfaVis.cy.elements().removeClass('highlighted completed dimmed');
    }
    const explainText = document.getElementById('subset-explain-text');
    if (explainText) {
      explainText.textContent = 'Click "▶ Visualize Subset Construction" to step through the ε-closure and symbol transition set mapping algorithm from Thompson NFA to Subset DFA.';
    }
  }
}

class TraceAnimator {
  static animateStringTrace(resultObj) {
    if (!resultObj) return;

    const ribbon = document.getElementById('char-ribbon-container');
    const banner = document.getElementById('trace-status-banner');
    if (!ribbon) return;

    const inputString = resultObj.input_string;
    const trace = resultObj.trace || [];
    const isMatch = resultObj.is_match;

    const chars = inputString === '' ? ['ε'] : inputString.split('');
    ribbon.innerHTML = chars.map((ch, idx) => `
      <span class="char-track-item" id="char-track-${idx}">${ch}</span>
    `).join('<span class="text-on-surface-variant text-xs">➔</span>');

    if (banner) {
      banner.textContent = 'Animating Transition Trace...';
      banner.className = 'text-primary font-bold';
    }

    let stepIndex = 0;
    const interval = setInterval(() => {
      if (stepIndex < trace.length) {
        const item = document.getElementById(`char-track-${stepIndex}`);
        if (item) {
          document.querySelectorAll('.char-track-item').forEach(el => el.classList.remove('active'));
          item.classList.add('active');
        }
        stepIndex++;
      } else {
        clearInterval(interval);
        document.querySelectorAll('.char-track-item').forEach(el => {
          el.classList.remove('active');
          if (isMatch) el.classList.add('matched');
        });

        if (banner) {
          if (isMatch) {
            banner.textContent = '✓ ACCEPTED BY DFA';
            banner.className = 'text-emerald-600 dark:text-emerald-400 font-bold';
          } else {
            banner.textContent = '✕ REJECTED BY DFA';
            banner.className = 'text-rose-500 font-bold';
          }
        }
      }
    }, 450);
  }
}

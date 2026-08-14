/**
 * RegexForge - Cytoscape.js Automata Visualizer Adapter
 * Course: CSE314 — Compiler Design Lab (Uronto Helicopter)
 */

class GraphVisualizer {
  constructor(containerId) {
    this.containerId = containerId;
    this.container = document.getElementById(containerId);
    this.cy = null;
  }

  renderGraph(elements) {
    if (!this.container) return;

    if (!elements || elements.length === 0) {
      this.container.innerHTML = `
        <div style="display: flex; height: 100%; align-items: center; justify-content: center; color: var(--text-muted);">
          No graph data available.
        </div>
      `;
      return;
    }

    // Clean container HTML
    this.container.innerHTML = '';

    try {
      this.cy = cytoscape({
        container: this.container,
        elements: elements,
        style: [
          {
            selector: 'node',
            style: {
              'background-color': '#0d1c2d',
              'border-color': '#c0c1ff',
              'border-width': 2,
              'color': '#d4e4fa',
              'label': 'data(label)',
              'font-family': 'JetBrains Mono, monospace',
              'font-size': '12px',
              'font-weight': '600',
              'text-valign': 'center',
              'text-halign': 'center',
              'width': '48px',
              'height': '48px',
              'text-wrap': 'wrap'
            }
          },
          {
            selector: 'node.start-node',
            style: {
              'border-color': '#6366f1',
              'border-width': 3,
              'background-color': 'rgba(99, 102, 241, 0.25)'
            }
          },
          {
            selector: 'node.accept-node',
            style: {
              'border-color': '#10b981',
              'border-width': 4,
              'background-color': 'rgba(16, 185, 129, 0.25)'
            }
          },
          {
            selector: 'edge',
            style: {
              'width': 2,
              'line-color': '#464554',
              'target-arrow-color': '#22d3ee',
              'target-arrow-shape': 'triangle',
              'curve-style': 'bezier',
              'label': 'data(label)',
              'color': '#22d3ee',
              'font-family': 'JetBrains Mono, monospace',
              'font-size': '12px',
              'font-weight': '600',
              'text-background-color': '#051424',
              'text-background-opacity': 0.95,
              'text-background-padding': '4px',
              'text-background-shape': 'roundrectangle'
            }
          },
          {
            selector: 'node.highlighted',
            style: {
              'border-color': '#a855f7',
              'border-width': 5,
              'background-color': 'rgba(168, 85, 247, 0.45)',
              'color': '#ffffff',
              'width': '54px',
              'height': '54px',
              'font-size': '13px',
              'font-weight': 'bold',
              'z-index': 999,
              'opacity': 1
            }
          },
          {
            selector: 'edge.highlighted',
            style: {
              'width': 5,
              'line-color': '#a855f7',
              'target-arrow-color': '#a855f7',
              'color': '#a855f7',
              'font-weight': 'bold',
              'z-index': 999,
              'opacity': 1
            }
          },
          {
            selector: 'node.completed',
            style: {
              'border-color': '#22d3ee',
              'border-width': 3,
              'opacity': 0.9
            }
          },
          {
            selector: 'edge.completed',
            style: {
              'width': 3,
              'line-color': '#22d3ee',
              'target-arrow-color': '#22d3ee',
              'opacity': 0.85
            }
          },
          {
            selector: 'node.dimmed',
            style: {
              'opacity': 0.2
            }
          },
          {
            selector: 'edge.dimmed',
            style: {
              'opacity': 0.15
            }
          }
        ],
        layout: {
          name: 'breadthfirst',
          directed: true,
          padding: 30,
          spacingFactor: 1.25
        }
      });
    } catch (e) {
      console.error('Cytoscape render error:', e);
      this.container.innerHTML = `<div style="color: var(--accent-rose); padding: 1rem;">Failed to render graph visualization.</div>`;
    }
  }

  zoomIn() {
    if (this.cy) this.cy.zoom(this.cy.zoom() * 1.2);
  }

  zoomOut() {
    if (this.cy) this.cy.zoom(this.cy.zoom() * 0.8);
  }

  fitGraph() {
    if (this.cy) this.cy.fit();
  }

  resetLayout() {
    if (this.cy) {
      this.cy.layout({ name: 'breadthfirst', directed: true, padding: 30 }).run();
      this.cy.fit();
    }
  }

  updateThemeColors(isDark) {
    if (!this.cy) return;
    const nodeBg = isDark ? '#0d1c2d' : '#ffffff';
    const nodeText = isDark ? '#d4e4fa' : '#0f172a';
    const nodeBorder = isDark ? '#c0c1ff' : '#4f46e5';
    const edgeBg = isDark ? '#051424' : '#f4f6fb';
    const edgeText = isDark ? '#22d3ee' : '#0284c7';

    this.cy.style()
      .selector('node')
      .style({
        'background-color': nodeBg,
        'border-color': nodeBorder,
        'color': nodeText
      })
      .selector('edge')
      .style({
        'color': edgeText,
        'target-arrow-color': edgeText,
        'text-background-color': edgeBg
      })
      .update();
  }
}

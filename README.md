# RegexForge ⚡

> **Build Regex. Generate Automata. Test Strings.**

A modern, interactive Regular Expression Engine developed for **CSE314 — Compiler Design Lab**.

---

## 📌 Project Information

- **Course:** CSE314 — Compiler Design Lab
- **Project Number:** 24
- **Project Topic:** Regular Expression Engine
- **Group:** 9
- **Team Name:** Uronto Helicopter

### 👥 Team Members

1. **MD Rokonuzzaman** — ID: `242-15-550` *(Lead)*
2. **Abdullah Hell Kafi** — ID: `242-15-387`

---

## 🔬 Custom Regex Compilation & Execution Pipeline

RegexForge features a ground-up implementation of a custom Regular Expression Engine without using standard library regex modules (`re`).

```
Regular Expression
        ↓
      Lexer
        ↓
     Tokens
        ↓
     Parser
        ↓
  Parse Tree / AST
        ↓
Thompson's Construction
        ↓
       NFA
        ↓
Subset Construction
        ↓
       DFA
        ↓
  String Matcher
        ↓
  MATCH / NO MATCH
```

---

## 🌟 Supported Features & Operators

- **Literal Symbols:** `a`, `b`, `c`, `0`, `1`, etc.
- **Concatenation:** `ab` (Explicit `CONCAT` token insertion)
- **Union / Alternation:** `a|b`
- **Kleene Star:** `a*`
- **Plus Operator:** `a+` (Transformed to `aa*`)
- **Optional Operator:** `a?` (Transformed to `(a|ε)`)
- **Grouping:** `(a|b)`
- **Wildcard:** `.` (Matches any symbol in the alphabet)

---

## 🛠️ Project Structure

```
RegexForge/
│
├── app.py              # Flask server and route endpoints
├── errors.py           # Custom exception definitions
├── models.py           # Data structures and schemas
│
├── lexer.py            # Tokenizer and scanner
├── ast.py              # Abstract Syntax Tree nodes
├── parser.py           # Recursive descent parser
├── nfa.py              # NFA representation & graph data
├── thompson.py         # Thompson's NFA construction
├── dfa.py              # DFA representation & graph data
├── subset.py           # Subset construction algorithm (NFA -> DFA)
├── matcher.py          # DFA string execution & trace generator
├── utils.py            # General utilities & graph formatters
│
├── templates/          # Jinja2 HTML5 templates
│   ├── base.html
│   ├── index.html       # Main Workspace
│   ├── analyzer.html    # Lexer & AST breakdown
│   ├── nfa.html         # Interactive Thompson NFA view
│   ├── dfa.html         # Interactive Subset DFA view
│   ├── testing.html     # Batch testing & trace visualizer
│   ├── how_it_works.html# Pipeline explanation
│   └── about.html       # Course & team metadata
│
├── static/
│   ├── css/
│   │   └── style.css    # Dark glassmorphic design system
│   └── js/
│       ├── app.js       # Core frontend logic & toast notifications
│       ├── graph.js     # Cytoscape.js visual graph adapter
│       └── visualizer.js# AST tree & execution trace renderer
│
├── examples/
│   └── examples.json    # Standard regex test cases
│
├── tests/              # Unit test suite
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_nfa.py
│   ├── test_dfa.py
│   └── test_matcher.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Quick Start (Local Setup)

1. **Clone & Navigate:**
   ```bash
   cd RegexForge
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application:**
   ```bash
   python app.py
   ```

4. **Access Web Application:**
   Open your browser at `http://127.0.0.1:5000`

---

## 🧪 Running Automated Tests

Run the test suite using `pytest`:

```bash
pytest
```

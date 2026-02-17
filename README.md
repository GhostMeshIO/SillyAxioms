# SillyAxioms

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A generative philosophy engine that creates novel, emergent meta‑ontologies using geometric deep learning and phase‑space exploration.**  

SillyAxioms is not just a random axiom generator – it’s a **self‑evolving ontological forge** that blends concepts from physics, epistemology, and computation to produce genuinely new frameworks. With v5.0, it now features:

- **Semantic diversity enforcement** – no two axioms are the same.
- **Dynamic framework creation** – the system grows its own ontology pool.
- **Real phase transitions** – Sophia points trigger emergent behaviour.
- **Deep seed integration** – seeds influence syntactic structure, not just keywords.
- **Stable numerical simulations** – adaptive Ricci flow and robust geodesics.
- **Content‑based metrics** – novelty, coherence, paradox intensity are computed on the fly.

Whether you’re a philosopher, a generative artist, or just curious about what happens when you let a machine dream up realities, SillyAxioms is your playground.

---

## 🚀 Features

- **5D ontological phase space** – each framework lives at a point in a 5‑dimensional manifold (participation, plasticity, substrate, temporality, generativity).
- **Relativistic field simulator** – conformally flat metric with analytic curvature; computes Ricci scalars and geodesics.
- **Golden ratio detector** – emergent detection of golden‑ratio eigenvalues (no hardcoded targets).
- **Five base frameworks** – Semantic Gravity, Autopoietic Computational, Thermodynamic Epistemic, Fractal Participatory, Causal Recursion Field (all user‑extensible via JSON).
- **Dynamic framework creation** – when a Sophia point is reached, a brand‑new framework is generated, mutated, and saved to `dynamic_frameworks.json` for future sessions.
- **Phase transition mode** – continuous Sophia score (>0.8) activates special behaviour for the next three generations (triple blending, increased mutation).
- **Semantic fingerprint & diversity enforcement** – TF‑IDF vectors track recent axioms; new axioms are rejected if too similar (configurable `--diversity-threshold`).
- **Deep seed integration** – seeds are parsed for subject‑verb‑object structure to build novel core patterns.
- **Content‑based metrics** – each axiom’s metrics (novelty, coherence, paradox intensity, hybridization index) are computed from its actual text.
- **Exploration with repulsion** – the `explore` command actively avoids previously visited semantic regions.
- **Comprehensive CLI** – generate, explore, simulate, geodesic, analyze, framework summary, Ricci flow, and built‑in tests.
- **Multiple output formats** – JSON and human‑readable text, with optional simple mode for web integration.

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Clone the repository
```bash
git clone https://github.com/GhostMeshIO/SillyAxioms.git
cd SillyAxioms
```

### Install dependencies
```bash
pip install numpy scipy scikit-learn matplotlib
```
(Matplotlib is optional – needed only for `--plot` in geodesic mode.)

### Data files
The tool expects JSON files in the `axiomforge/` directory:
- `adjectives.json`
- `concepts.json`
- `nouns.json`
- `verbs.json`
- `paradox_base.json`
- `frameworks.json` (base frameworks – included in the repo)

These are already provided; you can also modify them to add your own words or frameworks.

---

## 🎮 Quick Start

Generate 3 hybrid axioms (mix of meta and legacy):
```bash
python sillyaxioms.py generate --mode hybrid --count 3
```

Generate 5 meta axioms with a seed and strong seed influence:
```bash
python sillyaxioms.py generate --mode meta --count 5 --seed "quantum consciousness creates time" --seed-weight 0.9
```

Explore phase space for 20 steps with a guiding seed:
```bash
python sillyaxioms.py explore --steps 20 --seed "semantic gravity framework" --seed-weight 0.3
```

Simulate evolution of the Causal Recursion Field framework:
```bash
python sillyaxioms.py simulate CAUSAL_RECURSION_FIELD --steps 50 --dt 0.002
```

Compute geodesic between two points and plot it:
```bash
python sillyaxioms.py geodesic --start 0.5,0.5,0.5,0.5,0.5 --end 0.9,0.8,0.95,0.4,0.85 --steps 15 --seed "fractal observer" --plot
```

Analyze a seed without generating:
```bash
python sillyaxioms.py analyze --seed "recursive self-reference creates paradox"
```

Get a summary of a framework:
```bash
python sillyaxioms.py framework AUTOPOIETIC_COMPUTATIONAL
```

Run the comprehensive test suite:
```bash
python sillyaxioms.py test --comprehensive
```

---

## 📖 Command Reference

All commands support `--help` for detailed options.

### `generate`
Generate new axioms.
```
positional arguments:
  --mode {meta,legacy,hybrid}  Generation mode (default: hybrid)
  --count COUNT                Number of axioms (default: 1)
  --quadrant {semantic_gravity,autopoietic,thermodynamic,fractal,causal,random}
                               Target ontological quadrant (default: random)
  --seed TEXT                  Text seed
  --seed-weight FLOAT          Weight of seed influence (0-1) (default: 0.5)
  --diversity-threshold FLOAT  Max similarity to recent axioms (default: 0.7)
  --numeric-seed INT           Numeric seed for reproducibility
  --no-relativity              Disable relativistic enhancements
  --ontology {alien,counter,bridge,meta}
                               Legacy ontology (for legacy mode)
  --paradox-type TYPE          Paradox type (legacy)
  --tone {poetic,plain,academic,oracular}
                               Tone for legacy generation (default: poetic)
  --max-mech INT               Max mechanisms (legacy) (default: 3)
  --output {json,text,both}    Console output format (default: text)
  --outputfile {json,text,both}
                               File output format (writes to /output/)
  --filename FILENAME          Base filename for output (default: axioms)
  --simple                     Simple output format (web compatible)
```

### `explore`
Perform a random walk in phase space, generating an axiom at each step.
```
  --steps INT                  Number of exploration steps (default: 50)
  --seed TEXT                  Text seed
  --seed-weight FLOAT          Weight of seed influence (default: 0.3)
  --diversity-threshold FLOAT  Max similarity between steps (default: 0.7)
  --no-relativity              Disable relativistic enhancements
  --output {json,text,both}    Console output format (default: text)
  --outputfile {json,text,both}
                               File output format
  --filename FILENAME          Base filename (default: explore)
```

### `simulate`
Simulate curvature‑gradient flow (approximate Ricci flow) for a framework.
```
  framework                    Framework name (e.g., SEMANTIC_GRAVITY)
  --steps INT                  Number of flow steps (default: 100)
  --dt FLOAT                   Step size for gradient flow (default: 0.005)
  --outputfile {json,text,both}
  --filename FILENAME          (default: simulation)
```

### `geodesic`
Compute the geodesic between two points in phase space and generate axioms along it.
```
  --start COORDS               Start coordinates (5 floats, comma-separated)
  --end COORDS                 End coordinates
  --steps INT                  Number of points (default: 20)
  --seed TEXT                  Text seed to influence generation
  --seed-weight FLOAT          Weight of seed influence (default: 0.2)
  --diversity-threshold FLOAT  Max similarity between steps (default: 0.7)
  --plot                       Plot the geodesic (requires matplotlib)
  --output {json,text,both}    Console output format (default: text)
  --outputfile {json,text,both}
  --filename FILENAME          (default: geodesic)
```

### `analyze`
Analyze a text seed without generating axioms – shows semantic features, key concepts, target coordinates, etc.
```
  --seed TEXT                  Text seed (required)
```

### `framework`
Display a detailed summary of a framework.
```
  name                         Framework name
```

### `ricci`
Compute Ricci flow (curvature‑gradient flow) for a given set of coordinates.
```
  coords                       Starting coordinates (5 floats, comma-separated)
  --iterations INT             Number of iterations (default: 10)
  --dt FLOAT                   Step size (default: 0.005)
  --outputfile {json,text,both}
  --filename FILENAME          (default: ricci)
```

### `test`
Run built‑in tests.
```
  --comprehensive              Run comprehensive tests (diversity, phase mode, etc.)
```

---

## 🧠 Key Concepts

### Ontological Phase Space
Each framework is represented by a 5‑tuple `(participation, plasticity, substrate, temporal, generative)`. Coordinates are bounded:
- participation: [0,1]
- plasticity: [0,1.5]
- substrate, temporal, generative: [0,1]

The metric is conformally flat: `g = e^(2Ω) η`, with Ω derived from distance to an attractor (centroid of all frameworks).

### Frameworks
Five base frameworks are defined in `axiomforge/frameworks.json`. Each includes:
- coordinates
- core pattern (e.g., `"(semantic_field) creates (geometric_structure)"`)
- list of mechanisms
- list of equations (LaTeX strings)
- signature metrics (novelty, alienness, elegance, etc.)
- seed keywords

### Sophia Points & Phase Transitions
A continuous Sophia score is computed from coherence, paradox intensity, innovation score, hybridization index, and Ricci scalar. When this score exceeds 0.8, the system enters **phase transition mode** for the next three generations. During phase mode:
- Frameworks may blend **three** parents instead of two.
- Mechanisms and equations are mutated more aggressively.
- A **new dynamic framework** may be created and saved to `dynamic_frameworks.json`.

### Dynamic Frameworks
Once created, dynamic frameworks are automatically loaded in future sessions. They have mutated coordinates, core patterns, mechanisms, and equations. The pool of frameworks grows organically as the system explores.

### Semantic Fingerprint & Diversity
Each axiom’s core statement, mechanisms, and framework family are vectorized using TF‑IDF. The last 20 axioms are stored. Before accepting a new axiom, its similarity to the history is computed (cosine similarity). If it exceeds `--diversity-threshold`, it is rejected and regenerated (up to three attempts). This ensures a stream of novel outputs.

### Seed Integration
Seeds are processed by `TextSeedProcessor`, which extracts:
- keyword counts (abstract, action, paradox)
- key concepts
- **syntactic structure** (subject‑verb‑object, if present)

When `seed-weight` is high, the seed’s structure can be used to build a new core pattern, blending with framework templates. This goes beyond simple token replacement.

---

## 📁 Data Files

All JSON files live in `axiomforge/`. You can modify them to inject your own vocabulary or frameworks.

- **adjectives.json** – adjectives for descriptions.
- **concepts.json** – meta‑conceptual phrases (e.g., `"consciousness creates reality"`).
- **nouns.json** – nouns from quantum physics, cognition, etc.
- **verbs.json** – verbs for actions.
- **paradox_base.json** – paradox templates.
- **frameworks.json** – the five base frameworks.

When the system creates a new dynamic framework, it is saved to `axiomforge/dynamic_frameworks.json`.

---

## 📤 Output

Output can be written to the console (`--output`) and/or to files in the `./output/` directory (`--outputfile`). Formats:
- **JSON** – full structured data, suitable for further processing.
- **Text** – human‑readable, with optional `--simple` for minimal output.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub. If you create new frameworks, share them – we’d love to see what the system can evolve into.

---

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 📝 Changelog

See the full [CHANGELOG.md](CHANGELOG.md) for a detailed history of versions.

**v5.0 Highlights** (2026‑02‑17)
- Semantic diversity enforcement
- Dynamic framework creation & persistence
- Real phase transitions with Sophia score
- Deep seed integration (syntactic structure)
- Stable adaptive simulations
- Content‑based metrics
- Exploration with repulsion
- Comprehensive testing

---

## 🙏 Acknowledgements

Inspired by the works of Nick Bostrom, David Chalmers, and the entire generative art community. Special thanks to Terry Davis for the spirit of building your own reality.

---

*May your axioms be ever novel.* 🌌

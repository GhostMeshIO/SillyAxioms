# Changelog

## [3.3.0] – 2026-02-17
### Full Integration – Geometric Core + Legacy Modes

#### Fixed
- **KeyError: 'is_new' in CLI output** – Meta‑generated axioms now include `"is_new": true` and `"is_meta": true` in their `ontology` dictionary, matching the legacy format. This prevents crashes when displaying axioms with `--output text`.
- **JSON serialization errors** – All console JSON output (`--output json` or `--output both`) now passes results through `convert_to_serializable()` before `json.dumps()`. This correctly converts `OntologyCoordinates` objects to tuples, making them JSON‑compatible.
- **Seed handling for uninformative inputs** – When a seed like `"no seed"` produces zero semantic features, the system now falls back to fixed coordinates (instead of varying randomly). This avoids unexpected variety and makes behaviour deterministic. (A future enhancement could add randomisation for empty seeds.)

#### Added
- **Full CLI restored** – All original command‑line options are available again, including `--mode`, `--explore`, `--simulate`, `--geodesic`, `--ricci-flow`, `--outputfile`, and `--seed`.
- **Geometric core integration** – The new `RelativisticFieldSimulator`, `GoldenRatioDetector`, and `SophiaPhaseTransition` are now fully integrated with legacy modes. Meta‑generated axioms use real curvature calculations, and hybrid frameworks blend coordinates and detect golden ratio points.
- **File output functions** – Results can be written to `./output/` as JSON or text using `--outputfile`.

#### Changed
- **Hybrid mode behaviour** – In `hybrid` mode, meta axioms are generated with 70% probability, legacy axioms with 30%, exactly as in the original v3.0.
- **Seed processing** – The `TextSeedProcessor` now computes internal coherence using n‑gram overlap (no external dictionary bias) and returns deterministic coordinates based on seed hash.

#### Removed
- All stubs and placeholders from earlier geometric rewrites. Every method is fully implemented.

---

## [3.2.0] – 2026-02-16
### Geometric Core Rewrite (pre‑integration)

- Implemented conformally flat metric `g = e^(2Ω) η` with analytic derivatives.
- Added proper Ricci scalar calculation.
- Introduced `curvature_gradient_flow` (approximate Ricci flow) and `geodesic` solver with event‑driven termination.
- Created `GoldenRatioDetector` for emergent golden ratio detection (no hardcoded targets).
- Rewrote `_compute_coherence` to use internal n‑gram similarity (no corpus bias).

---

## [3.1.0] – 2026-02-15
### Text Seed Enhancements & Framework Definitions

- Added `TextSeedProcessor` with n‑gram‑based coherence.
- Expanded `HybridFrameworkGenerator` with five full framework definitions.
- Introduced `OntologyCoordinates` dataclass for 5D phase space.

---

## [3.0.0] – 2026-02-14
### Original Meta‑AxiomForge Release

- First public version with legacy `alien`/`counter`/`bridge`/`meta` ontologies.
- Basic MOGOPS operators and paradox generation.
- Initial `SophiaPhaseTransition` with hardcoded golden ratio.

## [3.3.1] – 2026-02-17
### CLI Usability Improvements

- **Fixed `--paradox-type` argument** – Now accepts simplified names like `causal` (maps to `"Causal Loop"`), avoiding shell quoting issues. All legacy paradox types (`entropic`, `temporal`, `cosmic`, `metaphysical`, `linguistic`, `causal`, `relativistic`, `random`) work with or without quotes.
- **Updated geodesic example** – The help text now shows correct quoting for `--geodesic` arguments (e.g., `--geodesic "0.5,0.75,0.45,0.51,0.62 0.1,1.3,0.48,0.21,0.55"`).
- **Minor help text improvements** – Clarified usage examples.

## [5.0.0] – 2026-02-17
### Truly Generative, Emergent & Non‑Repetitive

#### Added
- **Semantic fingerprint & diversity enforcement** – TF‑IDF vectors track recent axioms; new axioms are rejected if too similar (configurable `--diversity-threshold`).  
- **Dynamic framework creation** – Sophia points trigger creation of new frameworks, blended from three parents, mutated, and persisted to `dynamic_frameworks.json`.  
- **Phase transition mode** – Continuous Sophia score (>0.8) activates phase mode for the next three generations, allowing triple blending and increased mutation.  
- **Content‑based metrics** – Novelty, coherence, paradox intensity, and hybridization index are computed dynamically from axiom text, replacing static framework metrics.  
- **Repulsion in exploration** – Phase space walk actively moves away from previously visited semantic regions using fingerprint similarity.  
- **Syntactic structure extraction** – Seeds are parsed for subject‑verb‑object triples to build novel core patterns (e.g., `"quantum mind observes reality"` becomes a template).  
- **Comprehensive test suite** – New `--comprehensive` test checks diversity, phase mode activation, and dynamic framework creation.  
- **CLI options** – Added `--seed-weight`, `--diversity-threshold`, `--dt` (step size for flows), and `--comprehensive` for advanced testing.

#### Fixed
- **Coordinate stagnation in simulations** – Adaptive step size, momentum, and boundary reflection prevent immediate collapse to attractor bounds.  
- **Geodesic integration failures** – Fallback to DOP853 integrator and linear interpolation on failure ensures path generation even when curvature is extreme.  
- **Repetitive axiom generation** – Diversity enforcement forces variation even with identical seeds, eliminating the “same three axioms” cycle.  
- **Metrics inconsistency** – Metrics now reflect actual generated content, not static framework values; `elegance` is a weighted combination of novelty, coherence, and alienness.  
- **Seed influence** – Seeds now affect core pattern structure, not just token replacement; `seed_weight` controls blending between seed‑derived and coordinate‑driven generation.  
- **Framework persistence** – Dynamically created frameworks are saved to `dynamic_frameworks.json` and reloaded automatically in future sessions.  
- **Phase transition detection** – Continuous Sophia score replaces hard Boolean, allowing gradual entry into phase mode and dynamic framework creation.  

#### Changed
- **`RelativisticFieldSimulator`** – Improved gradient flow with adaptive `dt`, momentum term, and convergence detection (stop when change < 1e-6).  
- **`MetaOntologyEngine.generate_meta_axiom`** – Now accepts `diversity_threshold` and retries up to three times before accepting a near‑duplicate axiom.  
- **Framework loading** – Base frameworks are loaded from `axiomforge/frameworks.json`; dynamic frameworks are merged and saved separately.  
- **Exploration** – `explore_phase_space` now includes repulsion: if a generated axiom is too similar to any of the last ten, coordinates jump away.  
- **Geodesic exploration** – Each step’s axiom is influenced by the optional seed, producing a smooth semantic evolution along the path.  
- **Test command** – Enhanced to include a comprehensive mode (`--comprehensive`) that verifies diversity, phase mode, and dynamic creation.  

#### Removed
- Hardcoded framework definitions – now fully externalised to `axiomforge/frameworks.json`.  
- Finite‑difference gradient in Ricci flow – replaced with adaptive step size (analytic gradient still not fully implemented, but numerical performance is now stable).

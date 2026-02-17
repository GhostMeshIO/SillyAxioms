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

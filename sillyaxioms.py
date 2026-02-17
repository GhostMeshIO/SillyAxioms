#!/usr/bin/env python3
"""
META-AXIOMFORGE v3.3 - Full Integration
Beyond-God Tier Meta-Ontology Generator with Geometric Core
"""

import numpy as np
import json
import random
import math
import argparse
import sys
import re
import os
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
from scipy.integrate import solve_ivp

# ============================================================================
# TEXT SEED PROCESSOR & SEMANTIC ENHANCER (with n-gram coherence)
# ============================================================================

class TextSeedProcessor:
    """Process text seed using n-gram coherence and semantic mapping."""

    _word_corpus = None

    @classmethod
    def _load_corpus(cls, data_root: Path):
        """Load all words from JSON files into a single corpus string."""
        if cls._word_corpus is not None:
            return
        words = []
        json_files = ["adjectives.json", "concepts.json", "nouns.json", "verbs.json", "paradox_base.json"]
        for fname in json_files:
            path = data_root / fname
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Recursively extract all strings
                        def extract(obj):
                            if isinstance(obj, str):
                                words.append(obj.lower())
                            elif isinstance(obj, list):
                                for item in obj:
                                    extract(item)
                            elif isinstance(obj, dict):
                                for val in obj.values():
                                    extract(val)
                        extract(data)
                except Exception:
                    pass
        cls._word_corpus = " ".join(words)

    def __init__(self, data_root: str = "."):
        self.data_root = Path(data_root)
        self._load_corpus(self.data_root)

    def process_text_seed(self, seed_text: str) -> Dict[str, Any]:
        """Extract semantic features and generate control parameters."""
        seed_text = seed_text.strip().lower()
        words = re.findall(r'\b[a-z]+\b', seed_text)
        unique_words = set(words)

        # Character n-grams (size 3) for coherence
        def ngram_set(text, n=3):
            text = re.sub(r'\s+', ' ', text)
            return {text[i:i+n] for i in range(len(text)-n+1)}
        seed_ngrams = ngram_set(seed_text)

        semantic_features = {
            "abstract_count": sum(1 for w in words if w in [
                "reality", "consciousness", "existence", "being", "universe",
                "quantum", "entropy", "information", "time", "space"
            ]),
            "action_count": sum(1 for w in words if w in [
                "creates", "generates", "forms", "builds", "makes",
                "entails", "implies", "requires", "necessitates"
            ]),
            "paradox_count": sum(1 for w in words if w in [
                "paradox", "contradiction", "impossible", "contradictory",
                "both", "neither", "simultaneously", "recursive", "self"
            ]),
            "complexity": len(words) / max(1, len(unique_words)),
            "coherence_score": self._compute_coherence(seed_text, seed_ngrams),
            "semantic_density": len([w for w in words if len(w) > 6]) / max(1, len(words))
        }

        seed_hash = int(hashlib.sha256(seed_text.encode()).hexdigest()[:8], 16)

        # Extract key concepts
        key_concepts = [w for w in unique_words if len(w) > 5 and w not in
                        ["through", "between", "without", "within"]][:5]

        coordinates = self._map_to_coordinates(semantic_features, seed_hash)
        framework = self._determine_framework(seed_text, semantic_features)

        return {
            "seed_text": seed_text,
            "seed_hash": seed_hash,
            "semantic_features": semantic_features,
            "key_concepts": key_concepts,
            "target_coordinates": coordinates,
            "preferred_framework": framework,
            "is_complex": semantic_features["abstract_count"] > 2 or semantic_features["paradox_count"] > 0,
            "suggested_tone": self._suggest_tone(semantic_features)
        }

    def _compute_coherence(self, text: str, seed_ngrams: set) -> float:
        """
        Internal coherence of the seed text using n-gram overlap between sentences.
        If multiple sentences, average pairwise Jaccard of their n-gram sets.
        If single sentence, split into halves or use random chunks.
        """
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        if len(sentences) < 2:
            # Fallback: split into two halves by word count
            words = text.split()
            mid = len(words) // 2
            if mid == 0:
                return 0.5
            part1 = " ".join(words[:mid])
            part2 = " ".join(words[mid:])
            sentences = [part1, part2]

        ngram_sets = []
        for sent in sentences:
            sent = sent.strip()
            if sent:
                ngram_sets.append({sent[i:i+3] for i in range(len(sent)-2)})

        if len(ngram_sets) < 2:
            return 0.5

        # Average pairwise Jaccard
        scores = []
        for i in range(len(ngram_sets)):
            for j in range(i+1, len(ngram_sets)):
                inter = len(ngram_sets[i] & ngram_sets[j])
                union = len(ngram_sets[i] | ngram_sets[j])
                if union > 0:
                    scores.append(inter / union)
        return np.mean(scores) if scores else 0.5

    def _map_to_coordinates(self, features: Dict[str, float], seed_hash: int) -> 'OntologyCoordinates':
        """Map semantic features to ontological coordinates."""
        random.seed(seed_hash)
        participation = 0.5 + (features["abstract_count"] * 0.1) - (features["action_count"] * 0.05)
        plasticity = 0.5 + (features["paradox_count"] * 0.15) + (features["complexity"] * 0.1)
        substrate = 0.5 + (features["semantic_density"] * 0.3) - (features["coherence_score"] * 0.1)
        temporal = 0.5 + (features["action_count"] * 0.1) + (random.random() * 0.2 - 0.1)
        generative = 0.5 + (features["abstract_count"] * 0.08) + (features["paradox_count"] * 0.12)

        participation = max(0.0, min(1.0, participation))
        plasticity = max(0.0, min(1.5, plasticity))
        substrate = max(0.0, min(1.0, substrate))
        temporal = max(0.0, min(1.0, temporal))
        generative = max(0.0, min(1.0, generative))

        return OntologyCoordinates(participation, plasticity, substrate, temporal, generative)

    def _determine_framework(self, text: str, features: Dict[str, float]) -> str:
        """Determine which ontology framework best matches the seed text."""
        text_lower = text.lower()
        framework_scores = {
            "SEMANTIC_GRAVITY": 0,
            "AUTOPOIETIC_COMPUTATIONAL": 0,
            "THERMODYNAMIC_EPISTEMIC": 0,
            "FRACTAL_PARTICIPATORY": 0,
            "CAUSAL_RECURSION_FIELD": 0
        }
        keywords = {
            "SEMANTIC_GRAVITY": ["meaning", "language", "semantic", "word", "grammar", "linguistic", "gravity"],
            "AUTOPOIETIC_COMPUTATIONAL": ["self", "recursive", "comput", "program", "algorithm", "code", "autopoietic", "gödel"],
            "THERMODYNAMIC_EPISTEMIC": ["knowledge", "entropy", "heat", "temperature", "belief", "information", "epistemic", "thermo"],
            "FRACTAL_PARTICIPATORY": ["observer", "scale", "fractal", "hierarchical", "measurement", "participation", "holographic"],
            "CAUSAL_RECURSION_FIELD": ["time", "causal", "temporal", "future", "past", "present", "loop", "recursion", "chronon"]
        }
        for fw, kwlist in keywords.items():
            for kw in kwlist:
                if kw in text_lower:
                    framework_scores[fw] += 2
        if features["semantic_density"] > 0.3:
            framework_scores["SEMANTIC_GRAVITY"] += 1
        if features["paradox_count"] > 0:
            framework_scores["AUTOPOIETIC_COMPUTATIONAL"] += 2
        if features["abstract_count"] > features["action_count"]:
            framework_scores["THERMODYNAMIC_EPISTEMIC"] += 1
        if features["coherence_score"] > 0.6:
            framework_scores["FRACTAL_PARTICIPATORY"] += 1
        return max(framework_scores.items(), key=lambda x: x[1])[0]

    def _suggest_tone(self, features: Dict[str, float]) -> str:
        if features["paradox_count"] > 1:
            return "oracular"
        elif features["abstract_count"] > 2:
            return "poetic"
        elif features["action_count"] > features["abstract_count"]:
            return "academic"
        else:
            return "poetic"

# ============================================================================
# 5D ONTOLOGICAL PHASE SPACE
# ============================================================================

@dataclass
class OntologyCoordinates:
    participation: float
    plasticity: float
    substrate: float
    temporal: float
    generative: float

    def __post_init__(self):
        self.participation = max(0.0, min(1.0, self.participation))
        self.plasticity = max(0.0, min(1.5, self.plasticity))
        self.substrate = max(0.0, min(1.0, self.substrate))
        self.temporal = max(0.0, min(1.0, self.temporal))
        self.generative = max(0.0, min(1.0, self.generative))

    def to_tuple(self) -> Tuple[float, ...]:
        return (self.participation, self.plasticity, self.substrate,
                self.temporal, self.generative)

    def distance_to(self, other: 'OntologyCoordinates') -> float:
        return math.sqrt(sum((a-b)**2 for a,b in zip(self.to_tuple(), other.to_tuple())))

# ============================================================================
# RELATIVISTIC FIELD SIMULATOR – Conformal Geometry, Ricci Flow, Geodesics
# ============================================================================

class RelativisticFieldSimulator:
    """Implements conformally flat metric g = e^(2Ω) η with Ω derived from data."""

    # Golden ratio constant (for detection only)
    PHI = (1 + math.sqrt(5)) / 2

    def __init__(self, attractor_point: Optional[Tuple[float, ...]] = None, curvature_scale: float = 1.0):
        """
        attractor_point: 5D coordinates that minimize Ω (peak of conformal factor).
                         If None, defaults to centroid of known framework coordinates.
        curvature_scale:  strength of curvature (k in Ω = -k * r²)
        """
        if attractor_point is None:
            self.attractor = None
        else:
            self.attractor = np.array(attractor_point)
        self.k = curvature_scale

    def _ensure_attractor(self):
        """Compute attractor from framework data if not already set."""
        if self.attractor is None:
            # Use frameworks from HybridFrameworkGenerator
            fw_coords = [np.array(fw["coordinates"]) for fw in HybridFrameworkGenerator.FRAMEWORKS.values()]
            self.attractor = np.mean(fw_coords, axis=0)

    def _conformal_factor(self, coords: Tuple[float, ...]) -> float:
        """Ω(x) = -k * |x - attractor|²."""
        self._ensure_attractor()
        x = np.array(coords)
        r2 = np.sum((x - self.attractor)**2)
        return -self.k * r2

    def _conformal_derivatives(self, coords: Tuple[float, ...]):
        """Analytic gradient and Hessian of Ω."""
        self._ensure_attractor()
        x = np.array(coords)
        grad = -2 * self.k * (x - self.attractor)
        hess = -2 * self.k * np.eye(5)
        return grad, hess

    def compute_curvature_tensor(self, coordinates: Tuple[float, ...]) -> Dict[str, float]:
        """
        Compute Ricci scalar and related invariants for the conformally flat metric.
        Returns a dictionary with keys: ricci_scalar, laplacian_omega, grad_sq, omega.
        """
        n = 5
        Ω = self._conformal_factor(coordinates)
        grad, hess = self._conformal_derivatives(coordinates)

        grad_sq = np.sum(grad**2)
        laplacian = np.trace(hess)

        # For conformally flat metric g = e^(2Ω) η, Ricci tensor components:
        # R_ij = -(n-2)(∇_i∇_jΩ - ∇_iΩ ∇_jΩ) - δ_ij (□Ω + (n-2)(∇Ω)^2)
        # Ricci scalar = e^(-2Ω) Σ_i R_ii  (since g^{ij}=e^{-2Ω} δ^{ij})

        Ricci_diag = np.zeros(n)
        for i in range(n):
            term1 = -(n-2) * (hess[i,i] - grad[i]**2)
            term2 = -(laplacian + (n-2)*grad_sq)
            Ricci_diag[i] = term1 + term2

        R_scalar = np.exp(-2*Ω) * np.sum(Ricci_diag)

        return {
            "ricci_scalar": float(R_scalar),
            "laplacian_omega": float(laplacian),
            "gradient_squared_omega": float(grad_sq),
            "omega": float(Ω)
        }

    def curvature_gradient_flow(self, start_coords: Tuple[float, ...],
                                steps: int = 10, dt: float = 0.01,
                                target_curvature: Optional[float] = None) -> List[Tuple[float, ...]]:
        """
        Evolve coordinates by gradient descent on |R| to reduce curvature.
        This approximates the effect of Ricci flow without full metric evolution.
        If target_curvature is given, stops when |R - target| < 0.01.
        """
        history = [list(start_coords)]
        current = np.array(start_coords)

        for step in range(steps):
            # Compute gradient of R numerically
            eps = 1e-4
            gradR = np.zeros(5)
            curv0 = self.compute_curvature_tensor(tuple(current))["ricci_scalar"]
            for i in range(5):
                cp = current.copy()
                cp[i] += eps
                Rp = self.compute_curvature_tensor(tuple(cp))["ricci_scalar"]
                cm = current.copy()
                cm[i] -= eps
                Rm = self.compute_curvature_tensor(tuple(cm))["ricci_scalar"]
                gradR[i] = (Rp - Rm) / (2*eps)

            # Move in direction of decreasing |R|
            current -= dt * np.sign(curv0) * gradR

            # Enforce bounds
            for i, val in enumerate(current):
                if i == 1:
                    current[i] = max(0.0, min(1.5, val))
                else:
                    current[i] = max(0.0, min(1.0, val))

            history.append(current.copy())

            if target_curvature is not None:
                new_R = self.compute_curvature_tensor(tuple(current))["ricci_scalar"]
                if abs(new_R - target_curvature) < 0.01:
                    break

        return [tuple(x) for x in history]

    def geodesic(self, start: Tuple[float, ...], end: Tuple[float, ...],
                 n_points: int = 20) -> List[Tuple[float, ...]]:
        """
        Solve geodesic equation d²x/dλ² + Γ(dx/dλ, dx/dλ) = 0.
        Returns list of points along geodesic from start to near end.
        """
        def geodesic_ode(λ, y):
            n = 5
            x = y[:n]
            v = y[n:]

            # Compute Christoffel symbols for conformal metric
            # Γᵏᵢⱼ = δᵏᵢ ∂ⱼΩ + δᵏⱼ ∂ᵢΩ - ηᵢⱼ ηᵏˡ ∂ₗΩ
            grad, _ = self._conformal_derivatives(tuple(x))
            acc = np.zeros(n)
            for k in range(n):
                for i in range(n):
                    for j in range(n):
                        term = 0.0
                        if k == i:
                            term += grad[j]
                        if k == j:
                            term += grad[i]
                        if i == j:
                            term -= grad[k]   # because ηᵢⱼ=δᵢⱼ and ηᵏˡ=δᵏˡ
                        acc[k] -= term * v[i] * v[j]
            return np.concatenate([v, acc])

        # Initial direction: unit vector toward end
        x0 = np.array(start)
        x1 = np.array(end)
        direction = x1 - x0
        norm = np.linalg.norm(direction)
        if norm < 1e-9:
            return [start]
        v0 = direction / norm
        y0 = np.concatenate([x0, v0])

        # Event: stop when close to end
        def near_end(λ, y):
            return np.linalg.norm(y[:5] - x1) - 0.01
        near_end.terminal = True
        near_end.direction = -1

        # Integrate until event or max step
        sol = solve_ivp(geodesic_ode, (0, 10.0), y0, events=near_end,
                        max_step=0.5, rtol=1e-6, atol=1e-8)

        # Extract positions at evenly spaced parameters
        if sol.t_events[0].size > 0:
            t_max = sol.t_events[0][0]
        else:
            t_max = sol.t[-1]

        t_eval = np.linspace(0, t_max, n_points)
        sol = solve_ivp(geodesic_ode, (0, t_max), y0, t_eval=t_eval,
                        rtol=1e-6, atol=1e-8)

        return [tuple(sol.y[:5, i]) for i in range(sol.y.shape[1])]

# ============================================================================
# HYBRID FRAMEWORK GENERATOR (with all original methods)
# ============================================================================

class HybridFrameworkGenerator:
    """Provides framework definitions and utilities."""

    FRAMEWORKS = {
        "SEMANTIC_GRAVITY": {
            "coordinates": (0.9, 0.8, 0.95, 0.4, 0.85),
            "core_pattern": "(semantic_field) creates (geometric_structure)",
            "mechanisms": [
                "Linguistic quantum entanglement",
                "Meaning-gravity coupling",
                "Semantic tensor curvature",
                "Grammar as constraint equations",
                "Conceptual mass generation",
                "Word-world isomorphism",
                "Semantic field equations",
                "Linguistic spacetime"
            ],
            "equations": [
                r"G_{\mu\nu}^{(\text{semantic})} = 8\pi G_s T_{\mu\nu}^{(\text{conceptual})} + \Lambda_s g_{\mu\nu}^{(\text{meaning})}",
                r"T_{\mu\nu}^{(\text{conceptual})} = \partial_\mu\psi^\dagger \partial_\nu\psi - g_{\mu\nu}\left[\frac{1}{2}g^{\rho\sigma}\partial_\rho\psi^\dagger \partial_\sigma\psi - V(\psi)\right]",
                r"(i\gamma^\mu\nabla_\mu - m_{\text{concept}})\psi_{\text{semantic}} = \lambda\psi_{\text{semantic}}^3",
                r"\langle \text{word} | \text{reality} \rangle = \int \mathcal{D}[\text{meaning}] \, e^{iS_{\text{semantic}}[\text{word},\text{reality}]}"
            ],
            "signature_metrics": {
                "novelty": 1.08,
                "alienness": 5.5,
                "elegance": 92.0,
                "density": 11.2,
                "coherence": 0.618,
                "ricci_scalar": -0.12,
                "cosmological_constant": 1.0,
                "planck_scale": 1.0
            },
            "seed_keywords": ["meaning", "language", "semantic", "word", "grammar", "linguistic", "gravity", "spacetime", "curvature"]
        },
        "AUTOPOIETIC_COMPUTATIONAL": {
            "coordinates": (0.7, 0.9, 0.6, 0.3, 1.0),
            "core_pattern": "(computation) creates (itself)",
            "mechanisms": [
                "Self-writing program execution",
                "Recursive Gödel encoding",
                "Bootstrap existence predicate",
                "Reality as computational fixed-point",
                "Autonomous code generation",
                "Self-modifying algorithms",
                "Autopoietic state machines",
                "Recursive type systems",
                "Gödelian curvature dynamics"
            ],
            "equations": [
                r"G_{\mu\nu}^{(\text{comp})} = 8\pi T_{\mu\nu}^{(\text{code})} + \Lambda_{\text{self\_reference}} g_{\mu\nu}^{(\text{Gödel})}",
                r"i\hbar \frac{\partial \psi(\text{code})}{\partial t} = \hat{H}_{\text{execute}} \psi(\text{code}) + V_{\text{self\_reference}} \psi(\text{code}^\dagger)",
                r"\exists x (F(x) \land \forall y (F(y) \rightarrow x = y))",
                r"\text{while True: reality = execute(reality\_code); reality\_code = encode\_with\_curvature(reality)}"
            ],
            "signature_metrics": {
                "novelty": 1.15,
                "alienness": 7.2,
                "elegance": 89.5,
                "density": 10.9,
                "coherence": 0.73,
                "ricci_scalar": 0.68,
                "cosmological_constant": 1.618,
                "planck_scale": 1.0
            },
            "seed_keywords": ["self", "recursive", "comput", "program", "algorithm", "code", "autonomous", "loop", "gödel", "fixed-point"]
        },
        "THERMODYNAMIC_EPISTEMIC": {
            "coordinates": (0.5, 0.4, 0.3, 0.6, 0.7),
            "core_pattern": "(knowledge) creates (entropy) creates (reality)",
            "mechanisms": [
                "Belief phase transitions",
                "Epistemic temperature gradients",
                "Information-mass equivalence",
                "Cognitive entropy pumps",
                "Knowledge pressure differentials",
                "Learning as heat transfer",
                "Understanding as crystallization",
                "Insight as critical point",
                "Epistemic spacetime curvature"
            ],
            "equations": [
                r"G_{\mu\nu}^{(\text{epistemic})} = 8\pi T_{\mu\nu}^{(\text{knowledge})} + \Lambda_{\text{understanding}} g_{\mu\nu}^{(\text{thermo})}",
                r"dS_{\text{epistemic}} \geq \frac{\delta Q_{\text{belief}}}{T_{\text{cognitive}}}",
                r"m_{\text{bit}} = \frac{k_B T_{\text{thought}} \ln 2}{c^2} \left(1 + \frac{R}{6\Lambda_{\text{understanding}}}\right)",
                r"\nabla \cdot \mathbf{J}_{\text{knowledge}} = -\frac{\partial \rho_{\text{belief}}}{\partial t}"
            ],
            "signature_metrics": {
                "novelty": 1.12,
                "alienness": 4.8,
                "elegance": 87.0,
                "density": 10.5,
                "coherence": 0.68,
                "ricci_scalar": 0.42,
                "cosmological_constant": 0.618,
                "planck_scale": 1.0
            },
            "seed_keywords": ["knowledge", "entropy", "heat", "temperature", "belief", "information", "epistemic", "thermo", "cognition"]
        },
        "FRACTAL_PARTICIPATORY": {
            "coordinates": (1.0, 0.7, 0.5, 0.8, 0.6),
            "core_pattern": "(observer_scale) creates (reality_scale)",
            "mechanisms": [
                "Multi-scale observer entanglement",
                "Fractal participation patterns",
                "Self-similar measurement",
                "Scale-invariant collapse",
                "Recursive observation hierarchy",
                "Holographic encoding of scale",
                "Power-law participation",
                "Renormalization group consciousness",
                "Fractal spacetime metric generation"
            ],
            "equations": [
                r"P(k) = C k^{-\alpha} e^{-k/\kappa} \times F(\theta)",
                r"O_\lambda(x) = \lambda^{-d_O} U(\lambda) O(x/\lambda) U^\dagger(\lambda)",
                r"\langle \psi | P | \psi \rangle_{\text{scale}} = \text{scale}^\alpha \langle \psi | P | \psi \rangle_0",
                r"D_f = \frac{\log N}{\log(1/s)}",
                r"ds^2 = \sum_{n=0}^\infty \lambda^{-2n} \left[g_{\mu\nu}^{(n)} dx_\mu^{(n)} dx_\nu^{(n)}\right]"
            ],
            "signature_metrics": {
                "novelty": 1.18,
                "alienness": 8.3,
                "elegance": 94.0,
                "density": 11.5,
                "coherence": 0.62,
                "ricci_scalar": 0.31,
                "cosmological_constant": 0.5,
                "planck_scale": 0.618
            },
            "seed_keywords": ["observer", "scale", "fractal", "hierarchical", "measurement", "participation", "holographic", "multi-scale"]
        },
        "CAUSAL_RECURSION_FIELD": {
            "coordinates": (0.6, 0.5, 0.4, 0.95, 0.8),
            "core_pattern": "(future) creates (past) creates (present)",
            "mechanisms": [
                "Causal field folding",
                "Time-loop stabilization",
                "Retrocausal feedback amplification",
                "Present as temporal attractor",
                "Causal knot formation",
                "Temporal standing waves",
                "Chronon entanglement networks",
                "Self-consistent history weaving",
                "Consistency enforcement loops"
            ],
            "equations": [
                r"\nabla_\mu C^{\mu\nu} = J^\nu_{\text{obs}} + \lambda \epsilon^{\mu\nu\rho\sigma} C_{\mu\nu} \wedge C_{\rho\sigma}",
                r"C_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu + [A_\mu, A_\nu]",
                r"\oint_\gamma \mathbf{C} \cdot d\mathbf{x} = \Phi_{\text{temporal}}",
                r"x_{t+1} = f\left(x_t, x_{t-1}, \int_{t+1}^{\infty} g(x_\tau) d\tau\right)"
            ],
            "signature_metrics": {
                "novelty": 1.22,
                "alienness": 7.8,
                "elegance": 91.5,
                "density": 11.0,
                "coherence": 0.65,
                "ricci_scalar": 0.95,
                "cosmological_constant": 2.0,
                "planck_scale": 0.5
            },
            "seed_keywords": ["time", "causal", "temporal", "future", "past", "present", "loop", "recursion", "chronon", "attractor"]
        }
    }

    @classmethod
    def get_framework(cls, name: str) -> Dict[str, Any]:
        return cls.FRAMEWORKS.get(name, cls.FRAMEWORKS["SEMANTIC_GRAVITY"])

    @classmethod
    def random_framework(cls) -> str:
        return random.choice(list(cls.FRAMEWORKS.keys()))

    @classmethod
    def get_nearest_framework(cls, coords: Tuple[float, ...]) -> str:
        min_dist = float('inf')
        best = "SEMANTIC_GRAVITY"
        for name, data in cls.FRAMEWORKS.items():
            dist = sum((a-b)**2 for a,b in zip(coords, data["coordinates"]))
            if dist < min_dist:
                min_dist = dist
                best = name
        return best

    @classmethod
    def get_framework_by_seed(cls, seed_text: str) -> str:
        seed_lower = seed_text.lower()
        framework_scores = {}
        for name, data in cls.FRAMEWORKS.items():
            score = 0
            for keyword in data.get("seed_keywords", []):
                if keyword in seed_lower:
                    score += 2
            framework_scores[name] = score
        if sum(framework_scores.values()) == 0:
            weights = {
                "SEMANTIC_GRAVITY": 0.25,
                "AUTOPOIETIC_COMPUTATIONAL": 0.20,
                "FRACTAL_PARTICIPATORY": 0.25,
                "CAUSAL_RECURSION_FIELD": 0.20,
                "THERMODYNAMIC_EPISTEMIC": 0.10
            }
            return random.choices(list(weights.keys()), weights=list(weights.values()))[0]
        return max(framework_scores.items(), key=lambda x: x[1])[0]

    @classmethod
    def get_framework_signature(cls, framework_name: str, metric: str) -> float:
        framework = cls.get_framework(framework_name)
        return framework["signature_metrics"].get(metric, 0.0)

    @classmethod
    def generate_framework_summary(cls, framework_name: str) -> Dict[str, Any]:
        fw = cls.get_framework(framework_name)
        coords = fw["coordinates"]
        metrics = fw["signature_metrics"]
        return {
            "name": framework_name.replace("_", " ").title(),
            "coordinates": coords,
            "core_pattern": fw["core_pattern"],
            "mechanism_count": len(fw["mechanisms"]),
            "equation_count": len(fw["equations"]),
            "metrics": metrics,
            "seed_keywords": fw.get("seed_keywords", []),
            "relativistic_structure": "yes" if "ricci_scalar" in metrics else "no"
        }

# ============================================================================
# SOPHIA PHASE TRANSITION DETECTOR & HYBRID GENERATOR (adapted to use geometry)
# ============================================================================

class SophiaPhaseTransition:
    """Golden ratio phase transition detection and hybrid framework generation."""

    PHI = (1 + math.sqrt(5)) / 2

    def __init__(self, field_simulator: Optional[RelativisticFieldSimulator] = None):
        self.field_sim = field_simulator or RelativisticFieldSimulator()

    @classmethod
    def is_sophia_point(cls, coherence: float, metrics: Dict[str, float]) -> bool:
        """Legacy detection (kept for compatibility)."""
        golden_coherence = 1 / cls.PHI
        conditions = [
            abs(coherence - golden_coherence) < 0.015,
            metrics.get("paradox_intensity", 0) > 2.0,
            metrics.get("innovation_score", 0) > 0.85,
            metrics.get("hybridization_index", 0) > 0.33,
            metrics.get("ricci_scalar", 1.0) > 0.3
        ]
        return all(conditions)

    def generate_hybrid_framework(self, seed_context: Optional[Dict] = None,
                                  enable_relativity: bool = True) -> Dict[str, Any]:
        """Generate a hybrid framework at Sophia point with geometric grounding."""
        frameworks = list(HybridFrameworkGenerator.FRAMEWORKS.keys())

        if seed_context and seed_context.get("key_concepts"):
            concepts = seed_context["key_concepts"]
            scored_frameworks = []
            for fw in frameworks:
                score = 0
                keywords = HybridFrameworkGenerator.FRAMEWORKS[fw].get("seed_keywords", [])
                for concept in concepts[:3]:
                    if any(keyword in concept for keyword in keywords):
                        score += 1
                scored_frameworks.append((fw, score))
            scored_frameworks.sort(key=lambda x: x[1], reverse=True)
            candidate_frameworks = [fw for fw, _ in scored_frameworks[:4]]
            parent1, parent2 = random.sample(candidate_frameworks, 2)
        else:
            parent1, parent2 = random.sample(frameworks, 2)

        coords1 = HybridFrameworkGenerator.FRAMEWORKS[parent1]["coordinates"]
        coords2 = HybridFrameworkGenerator.FRAMEWORKS[parent2]["coordinates"]

        # Weight by elegance
        metrics1 = HybridFrameworkGenerator.FRAMEWORKS[parent1]["signature_metrics"]
        metrics2 = HybridFrameworkGenerator.FRAMEWORKS[parent2]["signature_metrics"]
        weight1 = metrics1["elegance"] / (metrics1["elegance"] + metrics2["elegance"])
        weight2 = 1 - weight1

        # Blend coordinates
        if seed_context and "target_coordinates" in seed_context:
            target_coords = seed_context["target_coordinates"].to_tuple()
            blend_factor = 0.7
            hybrid_coords = tuple(
                (a*weight1 + b*weight2) * (1 - blend_factor) + target_coords[i] * blend_factor
                for i, (a, b) in enumerate(zip(coords1, coords2))
            )
        else:
            hybrid_coords = tuple(
                a*weight1 + b*weight2 + random.uniform(-0.05, 0.05)
                for a, b in zip(coords1, coords2)
            )

        # Compute curvature if relativity enabled
        curvature_data = None
        if enable_relativity:
            curvature_data = self.field_sim.compute_curvature_tensor(hybrid_coords)
            ricci = curvature_data["ricci_scalar"]
            is_sophia = GoldenRatioDetector.check_curvature(ricci)
        else:
            ricci = 0.0
            is_sophia = False

        # Blend mechanisms and equations
        mech_pool1 = HybridFrameworkGenerator.FRAMEWORKS[parent1]["mechanisms"]
        mech_pool2 = HybridFrameworkGenerator.FRAMEWORKS[parent2]["mechanisms"]
        eq_pool1 = HybridFrameworkGenerator.FRAMEWORKS[parent1]["equations"]
        eq_pool2 = HybridFrameworkGenerator.FRAMEWORKS[parent2]["equations"]

        seed_mechanisms = []
        if seed_context and seed_context.get("key_concepts"):
            for concept in seed_context["key_concepts"][:2]:
                seed_mechanisms.append(f"{concept} phase transition")
                seed_mechanisms.append(f"{concept} mediated coherence")
                seed_mechanisms.append(f"{concept} curvature dynamics")

        mechanisms = [
            random.choice(mech_pool1),
            random.choice(mech_pool2),
            random.choice(seed_mechanisms if seed_mechanisms else [
                "Golden ratio optimization",
                "Ricci flow coherence maximization",
                "Paradox entropy pump",
                "Phase boundary navigation",
                "Cosmological constant tuning"
            ]),
            f"{parent1.split('_')[0].lower()}-{parent2.split('_')[0].lower()} coupling"
        ]

        hybrid_equations = [
            random.choice(eq_pool1),
            random.choice(eq_pool2),
            self._create_hybrid_equation(parent1, parent2)
        ]

        # Generate hybrid name
        name1 = parent1.replace("_", " ").split()[0]
        name2 = parent2.replace("_", " ").split()[0]
        if seed_context and seed_context.get("key_concepts"):
            seed_concept = seed_context["key_concepts"][0].title()
            hybrid_name = f"{seed_concept}_{name1}-{name2}_HYBRID"
        else:
            hybrid_name = f"{name1}-{name2}_HYBRID"

        # Hybrid metrics
        hybrid_metrics = {
            "novelty": 1.25 + random.uniform(-0.05, 0.05),
            "alienness": 8.5 + random.uniform(-0.5, 0.5),
            "elegance": 95.0 + random.uniform(-2.0, 2.0),
            "density": 12.0 + random.uniform(-1.0, 1.0),
            "coherence": 0.618 + random.uniform(-0.01, 0.01),
            "ricci_scalar": ricci,
            "cosmological_constant": random.choice([0.618, 1.0, 1.618, 2.0]),
            "planck_scale": random.choice([0.5, 0.618, 1.0, 1.5]),
            "sophia_point": is_sophia
        }

        return {
            "name": hybrid_name,
            "coordinates": hybrid_coords,
            "mechanisms": mechanisms,
            "equations": hybrid_equations,
            "parent_frameworks": [parent1, parent2],
            "signature_metrics": hybrid_metrics,
            "is_sophia": is_sophia,
            "seed_influenced": seed_context is not None,
            "relativistic": enable_relativity,
            "curvature_data": curvature_data
        }

    @staticmethod
    def _create_hybrid_equation(parent1: str, parent2: str) -> str:
        components = {
            "SEMANTIC": ["G_{\\mu\\nu}", "T_{\\mu\\nu}", "\\psi", "\\phi"],
            "AUTOPOIETIC": ["\\hat{H}", "\\psi(\\text{code})", "\\Lambda_{\\text{self}}", "G"],
            "THERMODYNAMIC": ["S", "T", "Q", "\\rho", "\\mathbf{J}"],
            "FRACTAL": ["O_\\lambda", "P(k)", "D_f", "\\lambda"],
            "CAUSAL": ["C_{\\mu\\nu}", "\\nabla_\\mu", "\\oint", "x_t"]
        }
        type1 = parent1.split("_")[0]
        type2 = parent2.split("_")[0]
        comp1 = random.choice(components.get(type1, ["A", "B"]))
        comp2 = random.choice(components.get(type2, ["C", "D"]))
        templates = [
            rf"{comp1} \otimes {comp2} = \exp(iS/\hbar)",
            rf"[{comp1}, {comp2}] = i\hbar_{{\text{{hybrid}}}}",
            rf"\frac{{d{comp1}}}{{dt}} = \alpha {comp2} + \beta [{comp1}, {comp2}]",
            rf"\langle {comp1} | {comp2} \rangle = \int \mathcal{{D}}[\text{{field}}] e^{{iS_{{\text{{hybrid}}}}}}",
            rf"{comp1} \rightarrow {comp2} \text{{ via golden ratio optimization}}"
        ]
        return random.choice(templates)

# ============================================================================
# GOLDEN RATIO DETECTOR (emergent)
# ============================================================================

class GoldenRatioDetector:
    """Detect golden ratio properties in metric tensors or eigenvalues."""

    PHI = (1 + math.sqrt(5)) / 2
    TOLERANCE = 0.05

    @classmethod
    def check_metric(cls, metric: np.ndarray) -> bool:
        if metric.shape != (5,5):
            return False
        eigvals = np.linalg.eigvalsh(metric)
        eigvals = np.sort(eigvals)[::-1]
        for i in range(len(eigvals)):
            for j in range(i+1, len(eigvals)):
                ratio = eigvals[i] / eigvals[j]
                if abs(ratio - cls.PHI) < cls.TOLERANCE or abs(ratio - 1/cls.PHI) < cls.TOLERANCE:
                    return True
        return False

    @classmethod
    def check_curvature(cls, ricci_scalar: float, ricci_components: Optional[list] = None) -> bool:
        if abs(ricci_scalar - cls.PHI) < cls.TOLERANCE:
            return True
        if ricci_components and len(ricci_components) >= 2:
            sorted_comp = sorted(ricci_components, reverse=True)
            for i in range(len(sorted_comp)):
                for j in range(i+1, len(sorted_comp)):
                    if abs(sorted_comp[i]/sorted_comp[j] - cls.PHI) < cls.TOLERANCE:
                        return True
        return False

# ============================================================================
# LEGACY ONTOLOGY TYPES AND ENGINE (for backward compatibility)
# ============================================================================

class OntologyType(Enum):
    ALIEN = "Fluid-Participatory-Hyperdimensional"
    COUNTER = "Rigid-Objective-Reductive"
    BRIDGE = "Quantum-Biological-Middle"
    META = "Meta-Ontological-Hybrid"

@dataclass
class OntologyEngine:
    ontology_type: OntologyType
    name: str
    coordinates: Optional[OntologyCoordinates] = None
    axioms: List[str] = field(default_factory=list)
    predictions: List[str] = field(default_factory=list)
    is_meta: bool = False

    def __post_init__(self):
        if self.coordinates is None:
            if self.ontology_type == OntologyType.ALIEN:
                self.coordinates = OntologyCoordinates(0.8, 1.2, 0.3, 0.7, 0.6)
            elif self.ontology_type == OntologyType.COUNTER:
                self.coordinates = OntologyCoordinates(0.2, 0.3, 0.7, 0.2, 0.3)
            elif self.ontology_type == OntologyType.BRIDGE:
                self.coordinates = OntologyCoordinates(0.5, 0.7, 0.5, 0.5, 0.5)
            else:  # META
                self.coordinates = OntologyCoordinates(0.618, 0.618, 0.618, 0.618, 0.618)
                self.is_meta = True

    def generate_seed(self, text_seed: Optional[str] = None) -> str:
        if text_seed:
            words = text_seed.lower().split()
            if self.is_meta:
                if len(words) > 3:
                    return f"Meta-ontology of {words[0]} and {words[1]} creates {words[2]} framework"
                else:
                    return f"Meta-ontological phase space of {text_seed}"
            elif self.ontology_type == OntologyType.ALIEN:
                return f"Observer-dependent {text_seed} creates participatory reality"
            elif self.ontology_type == OntologyType.COUNTER:
                return f"Objective {text_seed} emerges from computational substrate"
            else:
                return f"Quantum-biological interface mediates {text_seed}"
        if self.is_meta:
            return random.choice([
                "Ontological phase space traversal",
                "Framework hybridization boundary",
                "Golden ratio coherence optimization",
                "Meta-axiomatic self-generation",
                "Phase transition in conceptual space",
                "Autopoietic framework creation",
                "Recursive ontology definition",
                "Semantic gravity field curvature",
                "Ricci flow in ontological space"
            ])
        elif self.ontology_type == OntologyType.ALIEN:
            return random.choice([
                "Observer-dependent reality collapses",
                "Multiple universes (Many-Worlds)",
                "Retrocausality via closed timelike curves",
                "Consciousness is fundamental to reality",
                "Quantum superposition of realities",
                "Holographic universe principle",
                "Observer-created reality",
                "Consciousness as measurement device"
            ])
        elif self.ontology_type == OntologyType.COUNTER:
            return random.choice([
                "Lorentz violation at Planck energies",
                "Digital black holes preserve information",
                "Consciousness emerges from computation",
                "Discrete spacetime lattice",
                "Cellular automaton universe",
                "Bohmian pilot-wave theory",
                "Deterministic quantum mechanics",
                "Computational universe hypothesis"
            ])
        else:
            return random.choice([
                "Quantum coherence in microtubules",
                "Information storage increases mass",
                "Dark matter as entropic gravity",
                "Conscious moments ~300ms collapse",
                "Orchestrated objective reduction",
                "Quantum biology in photosynthesis",
                "Neural microtubule quantum processing",
                "Biological quantum entanglement"
            ])

    def get_mechanisms(self, text_seed: Optional[str] = None) -> List[str]:
        base_mechanisms = []
        if self.is_meta:
            hybrid = SophiaPhaseTransition().generate_hybrid_framework()
            base_mechanisms = hybrid["mechanisms"]
        elif self.ontology_type == OntologyType.ALIEN:
            base_mechanisms = [
                "Observer effect amplification",
                "Retrocausal feedback loops",
                "Hyperdimensional folding",
                "Participatory reality weaving",
                "Consciousness-mediated collapse",
                "Quantum entanglement of observers",
                "Many-worlds branching",
                "Holographic boundary encoding"
            ]
        elif self.ontology_type == OntologyType.COUNTER:
            base_mechanisms = [
                "Planck-scale discreteness",
                "Causal set emergence",
                "Bohmian pilot-wave guidance",
                "Cellular automaton evolution",
                "Digital physics computation",
                "Discrete spacetime evolution",
                "Finite state transitions",
                "Algorithmic state progression"
            ]
        else:
            base_mechanisms = [
                "Orchestrated quantum coherence",
                "Entropic gravity coupling",
                "Information-mass equivalence",
                "Quantum biological interface",
                "Microtubule resonance",
                "Biological quantum tunneling",
                "Neural quantum computation",
                "Consciousness field mediation"
            ]
        if text_seed:
            words = text_seed.lower().split()
            if words:
                seed_word = words[0]
                enhanced = [
                    f"{seed_word}-mediated coherence",
                    f"{seed_word} phase transition",
                    f"{seed_word} entanglement dynamics",
                    f"{seed_word} curvature coupling"
                ]
                return random.sample(base_mechanisms, 2) + random.sample(enhanced, 1)
        return random.sample(base_mechanisms, 3)

# ============================================================================
# ORIGINAL PARADOX GENERATION CODE (simplified, kept for legacy)
# ============================================================================

_DEF = {
    "paradox_types": [
        "entropic", "temporal", "cosmic", "metaphysical", "linguistic", "Causal Loop", "Relativistic"
    ],
    "equations": {
        "entropic": [r"S = k_B \log W", r"\partial_\mu j^\mu = 0", r"\Delta S \geq 0", r"H = -\sum p_i \log p_i"],
        "temporal": [r"[H, Q] = 0", r"Z = \int \mathcal{D}\phi\, e^{i S[\phi]}", r"\Psi(t_2) = U(t_2, t_1) \Psi(t_1)", r"\partial_t \psi = -iH\psi"],
        "cosmic": [r"T^{\mu\nu}_{;\mu} = 0", r"G_{\mu\nu} = 8\pi T_{\mu\nu}", r"ds^2 = g_{\mu\nu}dx^\mu dx^\nu", r"R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu} = \Lambda g_{\mu\nu}"],
        "metaphysical": [r"e^{i\pi} + 1 = 0", r"\langle \mathcal{O} \rangle = Z^{-1}\int \mathcal{D}\phi\, \mathcal{O}\, e^{i S}", r"\forall x(Px \rightarrow Qx) \rightarrow (\exists x Px \rightarrow \exists x Qx)", r"\square p \rightarrow p"],
        "linguistic": [r"\top \leftrightarrow \neg \top", r"L: L \text{ is false}", r"\exists x \forall y (Rxy \leftrightarrow \neg Ryx)", r"G: G \text{ cannot be proven}"],
        "Causal Loop": [r"[H, Q] = 0", r"\oint d\tau = 0", r"x_{t+1} = f(x_t, x_{t-1})", r"\phi(t) = \int K(t,t')\phi(t')dt'"],
        "Relativistic": [r"G_{\mu\nu} = 8\pi T_{\mu\nu}", r"\nabla_\mu T^{\mu\nu} = 0", r"R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu} + \Lambda g_{\mu\nu} = 0", r"ds^2 = g_{\mu\nu}dx^\mu dx^\nu"]
    },
    "tones": {
        "poetic": ["A glance understood.", "We keep respect in the pauses.", "Say less; allow more to be understood.", "Held like falling, then slowly released.", "In the space between breaths.", "Whispered to the void.", "Echoes folding into silence."],
        "plain": ["Noted.", "In short.", "Net effect:", "Bottom line:", "Result:", "Conclusion:", "Observation:"],
        "academic": ["We observe.", "Accordingly.", "Hence.", "Therefore.", "Thus.", "Consequently.", "It follows that."],
        "oracular": ["Unannounced.", "In the hush between horizons.", "As foretold in the quiet.", "It returns by a different door.", "Whispered by stones.", "Written in starlight.", "Echoed from the future."]
    }
}

def coerce_list(x: Any) -> List[str]:
    out: List[str] = []
    if x is None:
        return out
    if isinstance(x, list):
        for v in x:
            out.extend(coerce_list(v))
        return out
    if isinstance(x, dict):
        out.extend([str(k) for k in x.keys()])
        for v in x.values():
            out.extend(coerce_list(v))
        return out
    s = str(x)
    if s.strip():
        out.append(s.strip())
    return out

def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def load_pool(root: Path) -> Dict[str, List[str]]:
    pool_mech: List[str] = []
    pool_concepts: List[str] = []
    filenames = ["concepts.json", "paradox_base.json", "adjectives.json", "nouns.json", "verbs.json"]
    for fn in filenames:
        data = load_json(root / fn)
        if data is None:
            continue
        if isinstance(data, list):
            pool_concepts.extend(coerce_list(data))
            continue
        if isinstance(data, dict):
            for key in data:
                if any(kw in key.lower() for kw in ["mechanism", "function", "process", "dynamic"]):
                    pool_mech.extend(coerce_list(data[key]))
                else:
                    pool_concepts.extend(coerce_list(data[key]))
    pool_mech = sorted({_norm(x) for x in pool_mech if _norm(x)})
    pool_concepts = sorted({_norm(x) for x in pool_concepts if _norm(x)})
    return {"mechanisms": pool_mech, "concepts": pool_concepts}

# ============================================================================
# ORIGINAL AXIOMFORGE CLASS (legacy)
# ============================================================================

class AxiomForgeHybrid:
    def __init__(self, data_root: str = "."):
        self.data_root = Path(data_root)
        self.pools = {
            "mechanisms": [
                "holographic accounting", "bulk–boundary reciprocity", "geodesic shear",
                "metric fluctuation", "entropic drift", "quantum decoherence",
                "wavefunction collapse", "entanglement propagation", "information erasure",
                "thermal equilibration", "ricci flow", "curvature mediation"
            ],
            "concepts": [
                "reality", "consciousness", "quantum", "entropy", "information",
                "time", "space", "causality", "observation", "measurement",
                "curvature", "metric"
            ]
        }
        self.ontologies = {
            "alien": OntologyEngine(ontology_type=OntologyType.ALIEN, name="Alien Ontology",
                axioms=["Reality is Malleable: Spacetime curves, quantum fields fluctuate",
                        "Reality is Subjective: Measurement creates reality, observers participate",
                        "Reality is Complex: 11 dimensions, string landscapes, multiverse branching"],
                predictions=["Observer-dependent reality collapses", "Multiple universes (Many-Worlds)",
                             "Retrocausality possible via closed timelike curves"]),
            "counter": OntologyEngine(ontology_type=OntologyType.COUNTER, name="Counter Ontology",
                axioms=["Reality is RIGID: Discrete spacetime lattice at Planck scale",
                        "Reality is OBJECTIVE: Exists independently of observers",
                        "Reality is REDUCTIVE: Simple rules generate complexity"],
                predictions=["Lorentz violation at Planck energies", "Digital black holes preserve information",
                             "Consciousness emerges from computation"]),
            "bridge": OntologyEngine(ontology_type=OntologyType.BRIDGE, name="Bridge Theories",
                axioms=["Consciousness is quantum-biological bridge state",
                        "Information is physical (has mass)",
                        "Gravity emerges from entanglement entropy"],
                predictions=["Quantum coherence in microtubules at 37°C",
                             "Information storage increases mass (Landauer limit)",
                             "Dark matter explained by entropic gravity"]),
            "meta": OntologyEngine(ontology_type=OntologyType.META, name="Meta Ontology",
                axioms=["Reality is self-generating ontological framework",
                        "Consciousness is phase transition in conceptual space",
                        "Existence is recursive definition"],
                predictions=["Golden ratio coherence optimization",
                             "Autopoietic framework creation",
                             "Meta-axiomatic self-generation"])
        }
        self.generated = {"alien": 0, "counter": 0, "bridge": 0, "meta": 0}

    def generate(self,
                 seed: Optional[str] = None,
                 ontology_name: Optional[str] = None,
                 ptype: Optional[str] = None,
                 count: int = 1,
                 tone: str = "poetic",
                 max_mech: int = 3) -> List[Dict[str, Any]]:
        results = []
        for _ in range(count):
            if ontology_name and ontology_name in self.ontologies:
                ontology = self.ontologies[ontology_name]
            else:
                ontology = random.choice(list(self.ontologies.values()))
            ont_key = ontology.name.lower().split()[0]
            self.generated[ont_key] = self.generated.get(ont_key, 0) + 1
            if seed:
                seed_text = seed
            else:
                seed_text = ontology.generate_seed()
            mechanisms = ontology.get_mechanisms(seed_text)[:max_mech]
            if len(seed_text.split()) > 2:
                axiom_text = f"{seed_text} — via {', '.join(mechanisms)}."
            else:
                axiom_text = f"{seed_text} via {', '.join(mechanisms)}."
            is_new = ontology.is_meta
            result = {
                "core_statement": seed_text,
                "mechanisms": mechanisms,
                "consequences": [f"Standard {ontology.name} implications"],
                "axiom_text": axiom_text,
                "paradox_type": ptype or "legacy",
                "ontology": {
                    "type": ontology.ontology_type.value,
                    "name": ontology.name,
                    "is_new": is_new,
                    "is_meta": ontology.is_meta
                },
                "seed_concept": seed_text,
                "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
                "metrics": {
                    "novelty": 0.8 + random.uniform(-0.1, 0.1) + (0.2 if ontology.is_meta else 0),
                    "alienness": 5.0 if ontology_name == "alien" else (7.0 if ontology.is_meta else 3.0),
                    "paradox_intensity": 1.0 + (0.5 if ontology.is_meta else 0),
                    "coherence": 0.5 + random.uniform(-0.1, 0.1) + (0.1 if ontology.is_meta else 0),
                    "ricci_scalar": random.uniform(-0.2, 0.2) if ontology.is_meta else 0.0
                },
                "insights": ["Legacy ontology generation" + (" with meta enhancements" if ontology.is_meta else "")]
            }
            results.append(result)
        return results

# ============================================================================
# MOGOPS OPERATORS (unchanged)
# ============================================================================

class MetaOntologyOperators:
    @staticmethod
    def CREATES(x: str, y: str, seed_context: Optional[Dict] = None) -> str:
        templates = [f"{x} creates {y}", f"{x} gives rise to {y}", f"From {x} emerges {y}",
                     f"{x} generates {y}", f"{x} manifests as {y}"]
        return random.choice(templates)

    @staticmethod
    def ENTAILS(x: str, y: str, seed_context: Optional[Dict] = None) -> str:
        templates = [f"{x} entails {y}", f"{x} implies {y}", f"{x} necessitates {y}",
                     f"{x} requires {y}", f"Given {x}, then {y}"]
        return random.choice(templates)

    @staticmethod
    def VIA(x: str, seed_context: Optional[Dict] = None) -> str:
        templates = [f"via {x}", f"through {x}", f"by means of {x}", f"mediated by {x}", f"employing {x}"]
        return random.choice(templates)

    @staticmethod
    def ENCODED_AS(x: str, seed_context: Optional[Dict] = None) -> str:
        templates = [f"encoded as {x}", f"formalized as {x}", f"expressed as {x}",
                     f"modeled by {x}", f"captured by {x}"]
        return random.choice(templates)

# ============================================================================
# META-ONTOLOGY ENGINE (new geometric core)
# ============================================================================

class MetaOntologyEngine:
    def __init__(self, data_root: str = "."):
        self.seed_processor = TextSeedProcessor(data_root)
        self.framework_gen = HybridFrameworkGenerator()
        # Compute attractor as centroid of framework coordinates
        fw_coords = [np.array(fw["coordinates"]) for fw in self.framework_gen.FRAMEWORKS.values()]
        attractor = np.mean(fw_coords, axis=0)
        self.field_sim = RelativisticFieldSimulator(attractor_point=tuple(attractor))
        self.operators = MetaOntologyOperators()
        self.generated = []
        self.phase_transitions = []
        self.stats = {
            "total": 0,
            "meta": 0,
            "phase_transitions": 0,
            "text_seeds_used": 0
        }

    def generate_meta_axiom(self, target_coords: Optional[OntologyCoordinates] = None,
                            concept_seed: Optional[str] = None,
                            seed_context: Optional[Dict] = None,
                            force_phase_transition: bool = False,
                            enable_relativity: bool = True) -> Dict[str, Any]:
        self.stats["total"] += 1
        if concept_seed:
            self.stats["text_seeds_used"] += 1

        if target_coords is None:
            if seed_context and "target_coordinates" in seed_context:
                target_coords = seed_context["target_coordinates"]
            else:
                target_coords = OntologyCoordinates(
                    random.random(),
                    random.uniform(0,1.5),
                    random.random(),
                    random.random(),
                    random.random()
                )

        if enable_relativity:
            curv_data = self.field_sim.compute_curvature_tensor(target_coords.to_tuple())
            ricci = curv_data["ricci_scalar"]
            is_sophia = GoldenRatioDetector.check_curvature(ricci)
        else:
            curv_data = {"ricci_scalar": 0.0, "laplacian_omega": 0.0, "gradient_squared_omega": 0.0, "omega": 0.0}
            ricci = 0.0
            is_sophia = False

        fw_name = self.framework_gen.get_nearest_framework(target_coords.to_tuple())
        framework = self.framework_gen.get_framework(fw_name)

        core = self._generate_core(framework["core_pattern"], concept_seed)
        mechanisms = self._generate_mechanisms(framework["mechanisms"], seed_context)
        equation = random.choice(framework["equations"])
        consequences = self._generate_consequences(fw_name, concept_seed)

        axiom_text = self._build_axiom(core, mechanisms, equation, consequences, seed_context)

        metrics = framework["signature_metrics"].copy()
        metrics.update({
            "ricci_scalar": ricci,
            "laplacian_omega": curv_data["laplacian_omega"],
            "curvature_gradient": curv_data["gradient_squared_omega"],
            "sophia_point": is_sophia
        })

        result = {
            "core_statement": core,
            "mechanisms": mechanisms,
            "consequences": consequences,
            "axiom_text": axiom_text,
            "ontology": {
                "type": "BRAND_NEW_FRAMEWORK",
                "name": fw_name.replace("_", " ").title(),
                "coordinates": target_coords.to_tuple(),
                "framework_family": fw_name,
                "sophia_point": is_sophia,
                "is_new": True,
                "is_meta": True
            },
            "seed_concept": concept_seed,
            "seed_context": seed_context,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "metrics": metrics,
            "meta_ontology": {
                "coordinates": target_coords.to_tuple(),
                "curvature_data": curv_data if enable_relativity else None,
                "phase_transition": is_sophia
            }
        }

        self.generated.append(result)
        if is_sophia:
            self.phase_transitions.append(result)
            self.stats["phase_transitions"] += 1
        self.stats["meta"] += 1
        return result

    def _generate_core(self, pattern: str, seed: Optional[str]) -> str:
        if seed:
            return seed
        return pattern.replace("(", "").replace(")", "").replace("_", " ")

    def _generate_mechanisms(self, base_mechs: List[str], ctx: Optional[Dict]) -> List[str]:
        return random.sample(base_mechs, min(3, len(base_mechs)))

    def _generate_consequences(self, fw: str, seed: Optional[str]) -> List[str]:
        return [f"Emergence of {fw.lower().replace('_', ' ')} framework"]

    def _build_axiom(self, core: str, mechs: List[str], eq: str, conseq: List[str], ctx: Optional[Dict]) -> str:
        via = self.operators.VIA(", ".join(mechs), ctx)
        encoded = self.operators.ENCODED_AS(eq, ctx)
        entails = self.operators.ENTAILS(core, conseq[0] if conseq else "ontological emergence", ctx)
        return f"{core} — {via}; {encoded}; {entails}."

    def explore_phase_space(self, steps: int = 50, seed_text: Optional[str] = None,
                            enable_relativity: bool = True) -> List[Dict[str, Any]]:
        trajectory = []
        current = OntologyCoordinates(0.5,0.5,0.5,0.5,0.5)
        for step in range(steps):
            if random.random() < 0.3:
                fw_name = self.framework_gen.get_nearest_framework(current.to_tuple())
                fw_coords = self.framework_gen.get_framework(fw_name)["coordinates"]
                current = OntologyCoordinates(
                    current.participation * 0.7 + fw_coords[0] * 0.3,
                    current.plasticity * 0.7 + fw_coords[1] * 0.3,
                    current.substrate * 0.7 + fw_coords[2] * 0.3,
                    current.temporal * 0.7 + fw_coords[3] * 0.3,
                    current.generative * 0.7 + fw_coords[4] * 0.3
                )
            else:
                current = OntologyCoordinates(
                    current.participation + random.uniform(-0.1,0.1),
                    current.plasticity + random.uniform(-0.1,0.1),
                    current.substrate + random.uniform(-0.1,0.1),
                    current.temporal + random.uniform(-0.1,0.1),
                    current.generative + random.uniform(-0.1,0.1)
                )
            axiom = self.generate_meta_axiom(target_coords=current, concept_seed=seed_text,
                                             enable_relativity=enable_relativity)
            trajectory.append({
                "step": step,
                "coordinates": current.to_tuple(),
                "axiom": axiom["core_statement"],
                "framework": axiom["ontology"]["framework_family"],
                "is_sophia": axiom["meta_ontology"]["phase_transition"],
                "coherence": axiom["metrics"].get("coherence", 0.5),
                "curvature": axiom["metrics"]["ricci_scalar"]
            })
        return trajectory

    def simulate_framework_evolution(self, framework_name: str, steps: int = 100) -> Dict[str, Any]:
        framework = self.framework_gen.get_framework(framework_name)
        coords = framework["coordinates"]
        flow = self.field_sim.curvature_gradient_flow(coords, steps=steps)
        return {
            "framework": framework_name,
            "initial_coords": coords,
            "flow": flow,
            "final_coords": flow[-1]
        }

    def explore_geodesic(self, start_coords: Tuple[float, ...], end_coords: Tuple[float, ...],
                         steps: int = 20) -> List[Dict[str, Any]]:
        path = self.field_sim.geodesic(start_coords, end_coords, n_points=steps)
        trajectory = []
        for i, coords in enumerate(path):
            target = OntologyCoordinates(*coords)
            axiom = self.generate_meta_axiom(target_coords=target, enable_relativity=True)
            trajectory.append({
                "step": i,
                "coordinates": coords,
                "axiom": axiom["core_statement"],
                "framework": axiom["ontology"]["framework_family"],
                "is_sophia": axiom["meta_ontology"]["phase_transition"],
                "coherence": axiom["metrics"].get("coherence", 0.5),
                "curvature": axiom["metrics"]["ricci_scalar"]
            })
        return trajectory

    def get_framework_summary(self, framework_name: str) -> Dict[str, Any]:
        return self.framework_gen.generate_framework_summary(framework_name)

    def compute_ricci_flow(self, coordinates: Tuple[float, ...], iterations: int = 10) -> List[Tuple[float, ...]]:
        return self.field_sim.curvature_gradient_flow(coordinates, steps=iterations)

    def get_stats(self) -> Dict[str, Any]:
        return self.stats

# ============================================================================
# ENHANCED HYBRID FORGE v3.3 (unified interface)
# ============================================================================

class MetaAxiomForge:
    def __init__(self, data_root: str = "."):
        self.data_root = Path(data_root)
        self.meta_engine = MetaOntologyEngine(data_root)
        self.legacy_forge = AxiomForgeHybrid(data_root)
        self.seed_processor = TextSeedProcessor(data_root)
        self.sophia = SophiaPhaseTransition(self.meta_engine.field_sim)
        self.generation_stats = {
            "total": 0,
            "legacy": {"alien": 0, "counter": 0, "bridge": 0, "meta": 0},
            "meta": 0,
            "phase_transitions": 0,
            "new_frameworks": 0,
            "text_seeds_used": 0,
            "relativistic_generations": 0
        }
        self.current_coordinates = OntologyCoordinates(0.5, 0.5, 0.5, 0.5, 0.5)

    def generate(self,
                 mode: str = "hybrid",
                 count: int = 1,
                 target_quadrant: Optional[str] = None,
                 explore_sophia: bool = False,
                 legacy_params: Optional[Dict] = None,
                 concept_seed: Optional[str] = None,
                 enable_relativity: bool = True) -> List[Dict[str, Any]]:
        results = []
        seed_context = None
        if concept_seed and isinstance(concept_seed, str) and concept_seed.strip():
            seed_context = self.seed_processor.process_text_seed(concept_seed)
            self.generation_stats["text_seeds_used"] += 1
            random.seed(seed_context["seed_hash"])
            np.random.seed(seed_context["seed_hash"] % (2**32))

        for _ in range(count):
            if mode == "meta" or (mode == "hybrid" and random.random() < 0.7):
                target_coords = None
                if target_quadrant and target_quadrant != "random":
                    quadrant_map = {
                        "semantic_gravity": OntologyCoordinates(0.9, 0.8, 0.95, 0.4, 0.85),
                        "autopoietic": OntologyCoordinates(0.7, 0.9, 0.6, 0.3, 1.0),
                        "thermodynamic": OntologyCoordinates(0.5, 0.4, 0.3, 0.6, 0.7),
                        "fractal": OntologyCoordinates(1.0, 0.7, 0.5, 0.8, 0.6),
                        "causal": OntologyCoordinates(0.6, 0.5, 0.4, 0.95, 0.8)
                    }
                    target_coords = quadrant_map.get(target_quadrant)
                elif seed_context and "target_coordinates" in seed_context:
                    target_coords = seed_context["target_coordinates"]

                if explore_sophia:
                    hybrid = self.sophia.generate_hybrid_framework(seed_context, enable_relativity)
                    coords_obj = OntologyCoordinates(*hybrid["coordinates"])
                    axiom = self.meta_engine.generate_meta_axiom(
                        target_coords=coords_obj,
                        concept_seed=concept_seed,
                        seed_context=seed_context,
                        enable_relativity=enable_relativity
                    )
                    # Override with hybrid details
                    axiom["ontology"]["name"] = hybrid["name"]
                    axiom["ontology"]["framework_family"] = "HYBRID"
                    axiom["ontology"]["sophia_point"] = hybrid["is_sophia"]
                    axiom["mechanisms"] = hybrid["mechanisms"]
                    axiom["equations"] = hybrid["equations"]
                    axiom["metrics"].update(hybrid["signature_metrics"])
                else:
                    axiom = self.meta_engine.generate_meta_axiom(
                        target_coords=target_coords,
                        concept_seed=concept_seed,
                        seed_context=seed_context,
                        enable_relativity=enable_relativity
                    )
                self.generation_stats["meta"] += 1
                self.generation_stats["new_frameworks"] += 1
                if axiom["meta_ontology"]["phase_transition"]:
                    self.generation_stats["phase_transitions"] += 1
                if enable_relativity:
                    self.generation_stats["relativistic_generations"] += 1
            else:
                if not legacy_params:
                    legacy_params = {}
                if concept_seed and not legacy_params.get("seed"):
                    legacy_params["seed"] = concept_seed
                if seed_context and seed_context.get("is_complex"):
                    ontology_name = "meta"
                else:
                    ontology_name = legacy_params.get("ontology", random.choice(["alien", "counter", "bridge", "meta"]))
                legacy_results = self.legacy_forge.generate(
                    seed=legacy_params.get("seed"),
                    ontology_name=ontology_name,
                    ptype=legacy_params.get("paradox_type"),
                    count=1,
                    tone=legacy_params.get("tone", "poetic"),
                    max_mech=legacy_params.get("max_mech", 3)
                )
                axiom = legacy_results[0]
                axiom["ontology"]["is_new"] = ontology_name == "meta" or axiom["ontology"].get("is_new", False)
                self.generation_stats["legacy"][ontology_name] += 1
            self.generation_stats["total"] += 1
            results.append(axiom)
        return results

    def explore_phase_space(self, steps: int = 50, seed_text: Optional[str] = None,
                            enable_relativity: bool = True) -> List[Dict[str, Any]]:
        return self.meta_engine.explore_phase_space(steps, seed_text, enable_relativity)

    def simulate_framework_evolution(self, framework_name: str, steps: int = 100) -> Dict[str, Any]:
        return self.meta_engine.simulate_framework_evolution(framework_name, steps)

    def explore_geodesic(self, start_coords: Tuple[float, ...], end_coords: Tuple[float, ...],
                         steps: int = 20) -> List[Dict[str, Any]]:
        return self.meta_engine.explore_geodesic(start_coords, end_coords, steps)

    def get_framework_summary(self, framework_name: str) -> Dict[str, Any]:
        return self.meta_engine.get_framework_summary(framework_name)

    def compute_ricci_flow(self, coordinates: Tuple[float, ...], iterations: int = 10) -> List[Tuple[float, ...]]:
        return self.meta_engine.compute_ricci_flow(coordinates, iterations)

    def get_stats(self) -> Dict[str, Any]:
        stats = self.generation_stats.copy()
        if stats["total"] > 0:
            stats["percentages"] = {
                "legacy": f"{(sum(stats['legacy'].values()) / stats['total']) * 100:.1f}%",
                "meta": f"{(stats['meta'] / stats['total']) * 100:.1f}%",
                "phase_transitions": f"{(stats['phase_transitions'] / max(1, stats['meta'])) * 100:.1f}%",
                "text_seeds": f"{(stats['text_seeds_used'] / stats['total']) * 100:.1f}%",
                "relativistic": f"{(stats['relativistic_generations'] / max(1, stats['meta'])) * 100:.1f}%"
            }
            legacy_counts = stats["legacy"]
            stats["most_productive_legacy"] = max(legacy_counts.items(), key=lambda x: x[1])[0]
        return stats

# ============================================================================
# FILE OUTPUT FUNCTIONS
# ============================================================================

def convert_to_serializable(obj: Any) -> Any:
    if isinstance(obj, OntologyCoordinates):
        return obj.to_tuple()
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_to_serializable(item) for item in obj)
    elif hasattr(obj, '__dict__'):
        try:
            return {k: convert_to_serializable(v) for k, v in obj.__dict__.items()}
        except:
            return str(obj)
    else:
        return obj

def write_output_files(results: List[Dict[str, Any]], output_format: str, base_filename: str = "axioms", is_trajectory: bool = False):
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    serializable_results = convert_to_serializable(results)

    if output_format in ("json", "both"):
        json_filename = output_dir / f"{base_filename}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON output written to: {json_filename}")

    if output_format in ("text", "both"):
        text_filename = output_dir / f"{base_filename}_{timestamp}.txt"
        with open(text_filename, 'w', encoding='utf-8') as f:
            if is_trajectory:
                f.write("Ontological Phase Space Exploration Trajectory\n")
                f.write("=" * 60 + "\n\n")
                for step in results:
                    f.write(f"Step {step['step']:3d}:\n")
                    f.write(f"  Coordinates: {step['coordinates']}\n")
                    f.write(f"  Framework: {step['framework']}\n")
                    f.write(f"  Axiom: {step['axiom']}\n")
                    if step.get('is_sophia'):
                        f.write("  ✨ SOPHIA POINT (phase transition)\n")
                    f.write(f"  Coherence: {step.get('coherence', 0):.3f}\n")
                    f.write(f"  Curvature: {step.get('curvature', 0):.3f}\n\n")
                sophia_points = sum(1 for step in results if step.get('is_sophia'))
                avg_coherence = np.mean([step.get('coherence', 0) for step in results])
                avg_curvature = np.mean([step.get('curvature', 0) for step in results])
                f.write("\n" + "=" * 60 + "\n")
                f.write(f"Exploration Summary:\n")
                f.write(f"  Total steps: {len(results)}\n")
                f.write(f"  Sophia points: {sophia_points}\n")
                f.write(f"  Average coherence: {avg_coherence:.3f}\n")
                f.write(f"  Average curvature: {avg_curvature:.3f}\n")
            else:
                for i, axiom in enumerate(results, 1):
                    f.write(f"=== Axiom {i} ===\n")
                    f.write(f"{axiom['axiom_text']}\n\n")
                    if axiom['ontology'].get('is_new'):
                        f.write(f"[NEW ONTOLOGY: {axiom['ontology']['name']}]\n")
                    if axiom.get('seed_context'):
                        f.write(f"[Seed-influenced generation]\n")
                    if axiom.get('meta_ontology', {}).get('curvature_data'):
                        f.write(f"[Relativistic framework]\n")
                    if 'metrics' in axiom:
                        f.write(f"\n📊 Metrics:\n")
                        for key, value in list(axiom['metrics'].items())[:5]:
                            f.write(f"  {key}: {value}\n")
                    if 'meta_ontology' in axiom and axiom['meta_ontology'].get('curvature_data'):
                        f.write(f"\n🎭 Ricci scalar: {axiom['meta_ontology']['curvature_data'].get('ricci_scalar', 'N/A')}\n")
                    f.write("\n" + "="*40 + "\n\n")
        print(f"✅ Text output written to: {text_filename}")

# ============================================================================
# COMMAND LINE INTERFACE v3.3
# ============================================================================

def parse_paradox_type(s: str) -> str:
    """Custom type for --paradox-type that maps simplified names to internal strings."""
    s_lower = s.lower()
    mapping = {
        "entropic": "entropic",
        "temporal": "temporal",
        "cosmic": "cosmic",
        "metaphysical": "metaphysical",
        "linguistic": "linguistic",
        "causal": "Causal Loop",       # map 'causal' to the exact string used internally
        "relativistic": "Relativistic",
        "random": "random"
    }
    if s_lower not in mapping:
        raise argparse.ArgumentTypeError(
            f"Invalid choice: '{s}'. Choose from: {list(mapping.keys())}"
        )
    return mapping[s_lower]

def main():
    parser = argparse.ArgumentParser(
        description="META-AXIOMFORGE v3.3 - Full Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --mode meta --count 3
  %(prog)s --mode hybrid --quadrant fractal
  %(prog)s --explore --steps 20
  %(prog)s --mode legacy --ontology alien --count 2
  %(prog)s --seed "quantum consciousness creates recursive reality" --mode meta
  %(prog)s --seed "semantic gravity framework" --explore --steps 30
  %(prog)s --mode meta --count 5 --outputfile json
  %(prog)s --simulate semantic_gravity --steps 100
  %(prog)s --geodesic "0.5,0.75,0.45,0.51,0.62 0.1,1.3,0.48,0.21,0.55" --geodesic-steps 12
  %(prog)s --no-relativity --mode meta --count 2
        """
    )

    parser.add_argument('--mode', choices=['meta', 'legacy', 'hybrid', 'explore'], default='hybrid',
                        help='Generation mode (default: hybrid)')
    parser.add_argument('--count', type=int, default=1, help='Number of axioms to generate')
    parser.add_argument('--quadrant', choices=['semantic_gravity', 'autopoietic', 'thermodynamic',
                                               'fractal', 'causal', 'random'], default='random',
                        help='Target ontological quadrant')
    parser.add_argument('--explore', action='store_true', help='Perform phase space exploration')
    parser.add_argument('--steps', type=int, default=50, help='Steps for phase space exploration')
    parser.add_argument('--simulate', type=str, help='Simulate framework evolution (framework name)')
    parser.add_argument('--simulate-steps', type=int, default=100, help='Steps for framework simulation')
    parser.add_argument('--geodesic', nargs=2, type=str,
                        help='Explore geodesic between two coordinate sets (format: "0.5,0.5,0.5,0.5,0.5 0.9,0.8,0.95,0.4,0.85")')
    parser.add_argument('--geodesic-steps', type=int, default=20, help='Steps for geodesic exploration')
    parser.add_argument('--ontology', choices=['alien', 'counter', 'bridge', 'meta'],
                        help='Legacy ontology (for legacy mode)')
    parser.add_argument('--paradox-type', type=parse_paradox_type, default='random',
                        help='Paradox type: entropic, temporal, cosmic, metaphysical, linguistic, causal, relativistic, random')
    parser.add_argument('--output', choices=['json', 'text', 'both'], default='text',
                        help='Console output format')
    parser.add_argument('--outputfile', choices=['json', 'text', 'both'],
                        help='File output format (writes to /output/ directory)')
    parser.add_argument('--filename', type=str, default='axioms', help='Base filename for output files')
    parser.add_argument('--seed', type=str, help='Text seed for controlled axiom generation')
    parser.add_argument('--numeric-seed', type=int, help='Numeric seed for reproducibility')
    parser.add_argument('--tone', choices=['poetic', 'plain', 'academic', 'oracular'], default='poetic',
                        help='Tone for axiom generation')
    parser.add_argument('--max-mech', type=int, default=3, help='Maximum number of mechanisms (for legacy mode)')
    parser.add_argument('--simple', action='store_true', help='Simple output format (web compatible)')
    parser.add_argument('--analyze-seed', action='store_true', help='Analyze seed text without generating axioms')
    parser.add_argument('--framework-summary', type=str, help='Get detailed summary of a framework')
    parser.add_argument('--ricci-flow', type=str,
                        help='Compute Ricci flow for coordinates (format: "0.5,0.5,0.5,0.5,0.5")')
    parser.add_argument('--ricci-iterations', type=int, default=10, help='Iterations for Ricci flow computation')
    parser.add_argument('--no-relativity', action='store_true', help='Disable relativistic enhancements')

    args = parser.parse_args()

    if args.numeric_seed:
        random.seed(args.numeric_seed)
        np.random.seed(args.numeric_seed)
        print(f"🔢 Using numeric seed: {args.numeric_seed}")
    elif args.seed:
        seed_hash = int(hashlib.sha256(args.seed.encode()).hexdigest()[:8], 16)
        random.seed(seed_hash)
        np.random.seed(seed_hash % (2**32))
        print(f"📝 Using text seed: '{args.seed}' (hash: {seed_hash})")

    print("="*70)
    print("META-AXIOMFORGE v3.3 - Full Integration")
    print("Beyond-God Tier Meta-Ontology Generator with Geometric Core")
    print("="*70)

    forge = MetaAxiomForge(data_root="./axiomforge")

    if args.analyze_seed and args.seed:
        print(f"\n🔍 Analyzing seed text: '{args.seed}'")
        print("-"*70)
        analysis = forge.seed_processor.process_text_seed(args.seed)
        for key, value in analysis["semantic_features"].items():
            print(f"  {key}: {value:.3f}")
        print(f"\nKey Concepts: {', '.join(analysis['key_concepts'])}")
        print(f"Preferred Framework: {analysis['preferred_framework'].replace('_', ' ').title()}")
        print(f"Suggested Tone: {analysis['suggested_tone']}")
        print(f"Target Coordinates: {analysis['target_coordinates'].to_tuple()}")
        if not (args.explore or args.mode == "explore" or args.simulate or args.geodesic or args.framework_summary or args.ricci_flow):
            return

    if args.framework_summary:
        print(f"\n📚 Framework Summary: {args.framework_summary}")
        print("-"*70)
        summary = forge.get_framework_summary(args.framework_summary)
        for key, value in summary.items():
            if key != "seed_keywords":
                print(f"  {key}: {value}")
        print(f"  seed_keywords: {', '.join(summary.get('seed_keywords', []))}")
        return

    if args.ricci_flow:
        print(f"\n🌀 Computing Ricci flow for coordinates: {args.ricci_flow}")
        print("-"*70)
        try:
            coords = tuple(map(float, args.ricci_flow.split(',')))
            if len(coords) != 5:
                print("Error: Need exactly 5 coordinates")
                return
            flow = forge.compute_ricci_flow(coords, args.ricci_iterations)
            print(f"Ricci Flow Evolution ({args.ricci_iterations} iterations):")
            for i, point in enumerate(flow):
                print(f"  Iteration {i:2d}: {point}")
            return
        except ValueError:
            print("Error: Invalid coordinate format. Use: 0.5,0.5,0.5,0.5,0.5")
            return

    if args.simulate:
        print(f"\n🧪 Simulating framework evolution: {args.simulate}")
        print("-"*70)
        sim = forge.simulate_framework_evolution(args.simulate, args.simulate_steps)
        print(f"Framework: {sim['framework']}")
        print(f"Initial coordinates: {sim['initial_coords']}")
        print(f"Final coordinates: {sim['final_coords']}")
        if args.outputfile:
            write_output_files([sim], args.outputfile, f"{args.simulate}_simulation")
        return

    if args.geodesic:
        print(f"\n🗺️  Exploring geodesic path")
        print("-"*70)
        try:
            coords1 = tuple(map(float, args.geodesic[0].split(',')))
            coords2 = tuple(map(float, args.geodesic[1].split(',')))
            if len(coords1) != 5 or len(coords2) != 5:
                print("Error: Need exactly 5 coordinates for each point")
                return
            trajectory = forge.explore_geodesic(coords1, coords2, args.geodesic_steps)
            print(f"Geodesic from {coords1} to {coords2}")
            print(f"Steps: {args.geodesic_steps}")
            if args.outputfile:
                write_output_files(trajectory, args.outputfile, f"geodesic_{args.geodesic_steps}", is_trajectory=True)
            if args.output in ['json', 'both']:
                serializable_traj = convert_to_serializable(trajectory)
                print(json.dumps(serializable_traj, indent=2))
            if args.output in ['text', 'both'] and not args.simple:
                print("\nGeodesic Trajectory (first 10 steps):")
                for step in trajectory[:10]:
                    print(f"Step {step['step']:2d}: {step['axiom'][:50]}... ({step['framework']})")
            return
        except ValueError:
            print("Error: Invalid coordinate format. Use: 0.5,0.5,0.5,0.5,0.5 0.9,0.8,0.95,0.4,0.85")
            return

    if args.explore or args.mode == "explore":
        print(f"\n🌌 Exploring ontological phase space ({args.steps} steps)...")
        if args.seed:
            print(f"   Guided by seed: '{args.seed}'")
        print("-"*70)
        trajectory = forge.explore_phase_space(steps=args.steps, seed_text=args.seed,
                                               enable_relativity=not args.no_relativity)
        if args.outputfile:
            write_output_files(trajectory, args.outputfile, f"{args.filename}_trajectory", is_trajectory=True)
        if args.output in ['json', 'both']:
            serializable_traj = convert_to_serializable(trajectory)
            print(json.dumps(serializable_traj, indent=2))
        if args.output in ['text', 'both']:
            print("\nPhase Space Exploration Trajectory:")
            for step in trajectory[:10]:
                print(f"Step {step['step']:3d}: {step['axiom'][:60]}...")
                print(f"       Framework: {step['framework']}")
                if step['is_sophia']:
                    print("       ✨ SOPHIA POINT (phase transition)")
                print()
            sophia_points = sum(1 for step in trajectory if step['is_sophia'])
            avg_coherence = np.mean([step['coherence'] for step in trajectory])
            print(f"\n📊 Exploration Summary:")
            print(f"   Sophia points discovered: {sophia_points}/{args.steps}")
            print(f"   Average coherence: {avg_coherence:.3f}")
        return

    print(f"\n🔮 Generating {args.count} axiom(s) in {args.mode} mode...")
    if args.quadrant != 'random':
        print(f"   Target quadrant: {args.quadrant}")
    if args.seed:
        print(f"   Using seed: '{args.seed}'")
    if not args.no_relativity:
        print(f"   With relativistic enhancements")
    print("-"*70)

    target_quadrant = None if args.quadrant == 'random' else args.quadrant
    legacy_params = None
    if args.mode == 'legacy':
        legacy_params = {
            "ontology": args.ontology or random.choice(["alien", "counter", "bridge", "meta"]),
            "paradox_type": args.paradox_type if args.paradox_type != 'random' else None,
            "tone": args.tone,
            "max_mech": args.max_mech
        }

    concept_seed = os.environ.get('CONCEPT_SEED')
    if not args.seed and concept_seed:
        args.seed = concept_seed

    results = forge.generate(
        mode=args.mode,
        count=args.count,
        target_quadrant=target_quadrant,
        explore_sophia=False,  # not directly exposed in CLI
        legacy_params=legacy_params,
        concept_seed=args.seed,
        enable_relativity=not args.no_relativity
    )

    if args.outputfile:
        write_output_files(results, args.outputfile, args.filename)

    if args.simple:
        if args.output == 'json':
            serializable_results = convert_to_serializable(results)
            print(json.dumps(serializable_results, indent=2))
        else:
            for i, axiom in enumerate(results, 1):
                print(f"\n=== Axiom {i} ===")
                print(axiom["axiom_text"])
                if axiom["ontology"]["is_new"]:
                    print(f"[NEW ONTOLOGY: {axiom['ontology']['name']}]")
                if axiom.get('seed_context'):
                    print(f"[Seed-influenced generation]")
                if axiom.get('meta_ontology', {}).get('curvature_data'):
                    print(f"[Relativistic framework]")
    elif args.output in ['json', 'both']:
        serializable_results = convert_to_serializable(results)
        print(json.dumps(serializable_results, indent=2))

    if args.output in ['text', 'both'] and not args.simple:
        for i, axiom in enumerate(results, 1):
            print(f"\n✨ AXIOM #{i}")
            print("-"*40)
            print(axiom["axiom_text"])
            if axiom["ontology"]["is_new"]:
                print(f"\n📐 BRAND NEW ONTOLOGY FRAMEWORK:")
                print(f"   Name: {axiom['ontology']['name']}")
                if axiom.get("meta_ontology"):
                    meta = axiom["meta_ontology"]
                    print(f"   Coordinates: {meta.get('coordinates', 'N/A')}")
                    if meta.get("phase_transition"):
                        print("   🎭 PHASE TRANSITION DETECTED!")
                    if meta.get("curvature_data"):
                        print(f"   📐 Ricci scalar: {meta['curvature_data'].get('ricci_scalar', 'N/A')}")
            if axiom.get("seed_context"):
                print(f"\n📝 SEED INFLUENCE: {axiom['seed_concept']}")
            print(f"\n📊 Key Metrics:")
            metrics = axiom.get("metrics", {})
            for key, value in list(metrics.items())[:5]:
                print(f"   {key}: {value}")
            insights = axiom.get("insights", [])
            if insights:
                print(f"\n💡 Insights: {', '.join(insights)}")

    stats = forge.get_stats()
    print(f"\n📈 SESSION STATISTICS")
    print(f"   Total axioms generated: {stats['total']}")
    if stats['meta'] > 0:
        print(f"   New ontology frameworks: {stats['new_frameworks']}")
        print(f"   Phase transitions: {stats['phase_transitions']}")
        print(f"   Relativistic generations: {stats['relativistic_generations']}")
    if any(stats['legacy'].values()):
        print(f"   Legacy ontologies: {dict(stats['legacy'])}")
    if stats['text_seeds_used'] > 0:
        print(f"   Text seeds used: {stats['text_seeds_used']}")

if __name__ == "__main__":
    main()

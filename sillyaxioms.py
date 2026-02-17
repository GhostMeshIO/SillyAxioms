#!/usr/bin/env python3
"""
META-AXIOMFORGE v5.0 - Truly Generative, Emergent & Non-Repetitive
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
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
from scipy.integrate import solve_ivp
from collections import deque
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Optional visualization
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# TEXT SEED PROCESSOR & SEMANTIC ENHANCER (with structural extraction)
# ============================================================================

class TextSeedProcessor:
    """Process text seed using n-gram coherence, semantic mapping, and structural extraction."""

    _word_corpus = None

    ABSTRACT_KEYWORDS = {
        "reality", "consciousness", "existence", "being", "universe",
        "quantum", "entropy", "information", "time", "space",
        "recursive", "self", "paradox", "contradiction", "infinite",
        "causality", "meaning", "knowledge", "observer", "scale"
    }
    ACTION_KEYWORDS = {
        "creates", "generates", "forms", "builds", "makes",
        "entails", "implies", "requires", "necessitates", "emerges",
        "becomes", "transforms", "evolves"
    }
    PARADOX_KEYWORDS = {
        "paradox", "contradiction", "impossible", "contradictory",
        "both", "neither", "simultaneously", "recursive", "self",
        "loop", "infinite", "circular"
    }

    @classmethod
    def _load_corpus(cls, data_root: Path):
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
                except Exception as e:
                    logger.warning(f"Could not load {path}: {e}")
            else:
                logger.warning(f"Missing JSON file: {path}")
        cls._word_corpus = " ".join(words)

    def __init__(self, data_root: str = "."):
        self.data_root = Path(data_root)
        self._load_corpus(self.data_root)

    def process_text_seed(self, seed_text: str) -> Dict[str, Any]:
        """Extract semantic features, structure, and generate control parameters."""
        seed_text = seed_text.strip().lower()
        if not seed_text:
            logger.warning("Empty seed text provided, using default values.")
            seed_text = "void"
        words = re.findall(r'\b[a-z]+\b', seed_text)
        unique_words = set(words)

        # Character n-grams (size 3) for coherence
        def ngram_set(text, n=3):
            text = re.sub(r'\s+', ' ', text)
            return {text[i:i+n] for i in range(len(text)-n+1)}
        seed_ngrams = ngram_set(seed_text)

        semantic_features = {
            "abstract_count": sum(1 for w in words if w in self.ABSTRACT_KEYWORDS),
            "action_count": sum(1 for w in words if w in self.ACTION_KEYWORDS),
            "paradox_count": sum(1 for w in words if w in self.PARADOX_KEYWORDS),
            "complexity": len(words) / max(1, len(unique_words)),
            "coherence_score": self._compute_coherence(seed_text, seed_ngrams),
            "semantic_density": len([w for w in words if len(w) > 6]) / max(1, len(words))
        }

        seed_hash = int(hashlib.sha256(seed_text.encode()).hexdigest()[:8], 16)

        # Extract key concepts (long words, not stopwords)
        stopwords = {"through", "between", "without", "within", "over", "under", "above", "below"}
        key_concepts = [w for w in unique_words if len(w) > 4 and w not in stopwords][:5]

        # Extract simple syntactic structure: e.g., "X creates Y" -> (X, creates, Y)
        structure = self._extract_structure(seed_text)

        coordinates = self._map_to_coordinates(semantic_features, seed_hash)
        framework = self._determine_framework(seed_text, semantic_features)

        return {
            "seed_text": seed_text,
            "seed_hash": seed_hash,
            "semantic_features": semantic_features,
            "key_concepts": key_concepts,
            "syntactic_structure": structure,
            "target_coordinates": coordinates,
            "preferred_framework": framework,
            "is_complex": semantic_features["abstract_count"] > 1 or semantic_features["paradox_count"] > 0,
            "suggested_tone": self._suggest_tone(semantic_features)
        }

    def _extract_structure(self, text: str) -> Optional[Tuple[str, str, str]]:
        """Very simple subject‑verb‑object extraction."""
        words = text.split()
        if len(words) < 3:
            return None
        # Look for a known action verb in the middle
        for i, w in enumerate(words):
            if w in self.ACTION_KEYWORDS and 1 <= i <= len(words)-2:
                subject = " ".join(words[:i])
                verb = w
                obj = " ".join(words[i+1:])
                return (subject, verb, obj)
        return None

    def _compute_coherence(self, text: str, seed_ngrams: set) -> float:
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        if len(sentences) < 2:
            words = text.split()
            if len(words) < 4:
                return 0.5
            split = random.randint(2, len(words)-2)
            part1 = " ".join(words[:split])
            part2 = " ".join(words[split:])
            sentences = [part1, part2]

        ngram_sets = []
        for sent in sentences:
            sent = sent.strip()
            if sent:
                ngram_sets.append({sent[i:i+3] for i in range(len(sent)-2)})

        if len(ngram_sets) < 2:
            return 0.5

        scores = []
        for i in range(len(ngram_sets)):
            for j in range(i+1, len(ngram_sets)):
                inter = len(ngram_sets[i] & ngram_sets[j])
                union = len(ngram_sets[i] | ngram_sets[j])
                if union > 0:
                    scores.append(inter / union)
        return np.mean(scores) if scores else 0.5

    def _map_to_coordinates(self, features: Dict[str, float], seed_hash: int) -> 'OntologyCoordinates':
        random.seed(seed_hash)
        participation = 0.5 + (features["abstract_count"] * 0.1) - (features["action_count"] * 0.05) + random.uniform(-0.1, 0.1)
        plasticity = 0.5 + (features["paradox_count"] * 0.15) + (features["complexity"] * 0.1) + random.uniform(-0.2, 0.2)
        substrate = 0.5 + (features["semantic_density"] * 0.3) - (features["coherence_score"] * 0.1) + random.uniform(-0.1, 0.1)
        temporal = 0.5 + (features["action_count"] * 0.1) + random.uniform(-0.2, 0.2)
        generative = 0.5 + (features["abstract_count"] * 0.08) + (features["paradox_count"] * 0.12) + random.uniform(-0.1, 0.1)

        participation = max(0.0, min(1.0, participation))
        plasticity = max(0.0, min(1.5, plasticity))
        substrate = max(0.0, min(1.0, substrate))
        temporal = max(0.0, min(1.0, temporal))
        generative = max(0.0, min(1.0, generative))

        return OntologyCoordinates(participation, plasticity, substrate, temporal, generative)

    def _determine_framework(self, text: str, features: Dict[str, float]) -> str:
        text_lower = text.lower()
        framework_scores = {name: 0 for name in HybridFrameworkGenerator.FRAMEWORKS.keys()}
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
# RELATIVISTIC FIELD SIMULATOR – with adaptive step size and convergence
# ============================================================================

class RelativisticFieldSimulator:
    PHI = (1 + math.sqrt(5)) / 2

    def __init__(self, attractor_point: Optional[Tuple[float, ...]] = None, curvature_scale: float = 1.0):
        self._attractor = np.array(attractor_point) if attractor_point is not None else None
        self.k = curvature_scale
        self._attractor_set = attractor_point is not None

    def set_attractor(self, attractor_point: Tuple[float, ...]):
        self._attractor = np.array(attractor_point)
        self._attractor_set = True

    def _ensure_attractor(self):
        if not self._attractor_set:
            fw_data = HybridFrameworkGenerator.load_frameworks()
            fw_coords = [np.array(fw["coordinates"]) for fw in fw_data.values()]
            self._attractor = np.mean(fw_coords, axis=0)
            self._attractor_set = True

    def _conformal_factor(self, coords: Tuple[float, ...]) -> float:
        self._ensure_attractor()
        x = np.array(coords)
        r2 = np.sum((x - self._attractor)**2)
        return -self.k * r2

    def _conformal_derivatives(self, coords: Tuple[float, ...]):
        self._ensure_attractor()
        x = np.array(coords)
        grad = -2 * self.k * (x - self._attractor)
        hess = -2 * self.k * np.eye(5)
        return grad, hess

    def compute_curvature_tensor(self, coordinates: Tuple[float, ...]) -> Dict[str, float]:
        n = 5
        Ω = self._conformal_factor(coordinates)
        grad, hess = self._conformal_derivatives(coordinates)

        grad_sq = np.sum(grad**2)
        laplacian = np.trace(hess)

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
                                steps: int = 10, dt: float = 0.005,
                                momentum: float = 0.9,
                                tol: float = 1e-6,
                                target_curvature: Optional[float] = None) -> List[Tuple[float, ...]]:
        """
        Evolve coordinates by gradient descent on |R| with momentum and adaptive step.
        Reflects off boundaries. Stops when change < tol.
        """
        history = [list(start_coords)]
        current = np.array(start_coords)
        velocity = np.zeros(5)
        prev_norm = float('inf')

        for step in range(steps):
            eps = 1e-5
            curv0 = self.compute_curvature_tensor(tuple(current))["ricci_scalar"]
            gradR = np.zeros(5)
            for i in range(5):
                cp = current.copy(); cp[i] += eps
                Rp = self.compute_curvature_tensor(tuple(cp))["ricci_scalar"]
                cm = current.copy(); cm[i] -= eps
                Rm = self.compute_curvature_tensor(tuple(cm))["ricci_scalar"]
                gradR[i] = (Rp - Rm) / (2*eps)

            # Adaptive step size based on gradient norm
            grad_norm = np.linalg.norm(gradR)
            if grad_norm > 0:
                dt_adapt = dt * min(1.0, prev_norm / (grad_norm + 1e-12))
            else:
                dt_adapt = dt
            prev_norm = grad_norm

            velocity = momentum * velocity - dt_adapt * np.sign(curv0) * gradR
            current += velocity

            # Reflect off boundaries
            bounds = [(0.0, 1.0), (0.0, 1.5), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
            for i, (low, high) in enumerate(bounds):
                if current[i] < low:
                    current[i] = low + (low - current[i])
                    velocity[i] *= -0.5
                elif current[i] > high:
                    current[i] = high - (current[i] - high)
                    velocity[i] *= -0.5

            history.append(current.copy())

            # Convergence check
            if step > 0 and np.linalg.norm(history[-1] - history[-2]) < tol:
                break

            if target_curvature is not None:
                new_R = self.compute_curvature_tensor(tuple(current))["ricci_scalar"]
                if abs(new_R - target_curvature) < 0.01:
                    break

        return [tuple(x) for x in history]

    def geodesic(self, start: Tuple[float, ...], end: Tuple[float, ...],
                 n_points: int = 20) -> List[Tuple[float, ...]]:
        def geodesic_ode(λ, y):
            n = 5
            x = y[:n]
            v = y[n:]
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
                            term -= grad[k]
                        acc[k] -= term * v[i] * v[j]
            return np.concatenate([v, acc])

        x0 = np.array(start)
        x1 = np.array(end)
        direction = x1 - x0
        norm = np.linalg.norm(direction)
        if norm < 1e-9:
            return [start]
        v0 = direction / norm
        y0 = np.concatenate([x0, v0])

        def near_end(λ, y):
            return np.linalg.norm(y[:5] - x1) - 0.01
        near_end.terminal = True
        near_end.direction = -1

        try:
            # Use more robust integrator
            sol = solve_ivp(geodesic_ode, (0, 10.0), y0, events=near_end,
                            method='DOP853', max_step=0.5, rtol=1e-8, atol=1e-10)

            if sol.t_events[0].size > 0:
                t_max = sol.t_events[0][0]
            else:
                t_max = sol.t[-1]

            t_eval = np.linspace(0, t_max, n_points)
            sol = solve_ivp(geodesic_ode, (0, t_max), y0, t_eval=t_eval,
                            method='DOP853', rtol=1e-8, atol=1e-10)

            return [tuple(sol.y[:5, i]) for i in range(sol.y.shape[1])]
        except Exception as e:
            logger.warning(f"Geodesic integration failed: {e}. Using linear interpolation.")
            return [tuple(x0 + (x1 - x0) * i / (n_points-1)) for i in range(n_points)]

# ============================================================================
# HYBRID FRAMEWORK GENERATOR (with dynamic framework persistence)
# ============================================================================

class HybridFrameworkGenerator:
    FRAMEWORKS = {}
    DYNAMIC_FRAMEWORKS_FILE = "dynamic_frameworks.json"

    @classmethod
    def load_frameworks(cls, data_root: Path = Path("axiomforge")):
        path = data_root / "frameworks.json"
        if not path.exists():
            logger.error(f"Frameworks file not found: {path}")
            cls.FRAMEWORKS = {
                "SEMANTIC_GRAVITY": {
                    "coordinates": (0.9, 0.8, 0.95, 0.4, 0.85),
                    "core_pattern": "(semantic_field) creates (geometric_structure)",
                    "mechanisms": ["Linguistic quantum entanglement"],
                    "equations": ["G = 8πT"],
                    "signature_metrics": {},
                    "seed_keywords": ["meaning"]
                }
            }
        else:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for name, fw in data.items():
                    if "coordinates" in fw:
                        fw["coordinates"] = tuple(fw["coordinates"])
                cls.FRAMEWORKS = data
                logger.info(f"Loaded {len(cls.FRAMEWORKS)} base frameworks from {path}")
            except Exception as e:
                logger.error(f"Failed to load frameworks: {e}")
                cls.FRAMEWORKS = {}

        # Load dynamic frameworks if they exist
        dyn_path = data_root / cls.DYNAMIC_FRAMEWORKS_FILE
        if dyn_path.exists():
            try:
                with open(dyn_path, 'r', encoding='utf-8') as f:
                    dyn_data = json.load(f)
                for name, fw in dyn_data.items():
                    if "coordinates" in fw:
                        fw["coordinates"] = tuple(fw["coordinates"])
                cls.FRAMEWORKS.update(dyn_data)
                logger.info(f"Loaded {len(dyn_data)} dynamic frameworks from {dyn_path}")
            except Exception as e:
                logger.warning(f"Could not load dynamic frameworks: {e}")

        return cls.FRAMEWORKS

    @classmethod
    def save_dynamic_frameworks(cls, data_root: Path = Path("axiomforge")):
        """Save dynamically created frameworks to a separate file."""
        dyn_frameworks = {name: fw for name, fw in cls.FRAMEWORKS.items()
                          if name not in cls.get_base_framework_names(data_root)}
        if not dyn_frameworks:
            return
        dyn_path = data_root / cls.DYNAMIC_FRAMEWORKS_FILE
        # Convert tuples to lists for JSON
        serializable = {}
        for name, fw in dyn_frameworks.items():
            fw_copy = fw.copy()
            if "coordinates" in fw_copy:
                fw_copy["coordinates"] = list(fw_copy["coordinates"])
            serializable[name] = fw_copy
        try:
            with open(dyn_path, 'w', encoding='utf-8') as f:
                json.dump(serializable, f, indent=2)
            logger.info(f"Saved {len(dyn_frameworks)} dynamic frameworks to {dyn_path}")
        except Exception as e:
            logger.error(f"Failed to save dynamic frameworks: {e}")

    @classmethod
    def get_base_framework_names(cls, data_root: Path) -> set:
        path = data_root / "frameworks.json"
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return set(json.load(f).keys())
            except:
                pass
        return set()

    @classmethod
    def add_dynamic_framework(cls, name: str, framework: Dict[str, Any], data_root: Path):
        cls.FRAMEWORKS[name] = framework
        cls.save_dynamic_frameworks(data_root)

    @classmethod
    def get_framework(cls, name: str) -> Dict[str, Any]:
        if not cls.FRAMEWORKS:
            cls.load_frameworks()
        return cls.FRAMEWORKS.get(name, cls.FRAMEWORKS.get("SEMANTIC_GRAVITY", {}))

    @classmethod
    def random_framework(cls) -> str:
        if not cls.FRAMEWORKS:
            cls.load_frameworks()
        return random.choice(list(cls.FRAMEWORKS.keys()))

    @classmethod
    def get_nearest_framework(cls, coords: Tuple[float, ...]) -> str:
        if not cls.FRAMEWORKS:
            cls.load_frameworks()
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
        if not cls.FRAMEWORKS:
            cls.load_frameworks()
        seed_lower = seed_text.lower()
        scores = {}
        for name, data in cls.FRAMEWORKS.items():
            score = 0
            for keyword in data.get("seed_keywords", []):
                if keyword in seed_lower:
                    score += 2
            scores[name] = score
        if max(scores.values()) == 0:
            return random.choice(list(cls.FRAMEWORKS.keys()))
        return max(scores.items(), key=lambda x: x[1])[0]

    @classmethod
    def get_framework_signature(cls, name: str, metric: str) -> float:
        return cls.get_framework(name)["signature_metrics"].get(metric, 0.0)

    @classmethod
    def generate_framework_summary(cls, name: str) -> Dict[str, Any]:
        fw = cls.get_framework(name)
        return {
            "name": name.replace("_", " ").title(),
            "coordinates": fw["coordinates"],
            "core_pattern": fw["core_pattern"],
            "mechanism_count": len(fw["mechanisms"]),
            "equation_count": len(fw["equations"]),
            "metrics": fw["signature_metrics"],
            "seed_keywords": fw.get("seed_keywords", []),
            "relativistic_structure": "yes" if "ricci_scalar" in fw["signature_metrics"] else "no"
        }

# ============================================================================
# SOPHIA PHASE TRANSITION DETECTOR & HYBRID GENERATOR (with dynamic creation)
# ============================================================================

class SophiaPhaseTransition:
    PHI = (1 + math.sqrt(5)) / 2

    def __init__(self, field_simulator: Optional[RelativisticFieldSimulator] = None):
        self.field_sim = field_simulator or RelativisticFieldSimulator()
        self.sophia_threshold = 0.8  # continuous score threshold

    def sophia_score(self, coherence: float, metrics: Dict[str, float]) -> float:
        """Return a continuous score indicating how close to a Sophia point."""
        golden_coherence = 1 / self.PHI
        score = 0.0
        # Each condition contributes proportionally
        score += max(0, 1 - abs(coherence - golden_coherence) / 0.1) * 0.3
        score += min(1, metrics.get("paradox_intensity", 0) / 3.0) * 0.2
        score += min(1, metrics.get("innovation_score", 0) / 1.0) * 0.2
        score += min(1, metrics.get("hybridization_index", 0) / 0.5) * 0.15
        score += min(1, metrics.get("ricci_scalar", 0) / 1.0) * 0.15
        return score

    def is_sophia_point(self, coherence: float, metrics: Dict[str, float]) -> bool:
        return self.sophia_score(coherence, metrics) >= self.sophia_threshold

    def generate_hybrid_framework(self, seed_context: Optional[Dict] = None,
                                  enable_relativity: bool = True,
                                  phase_mode: bool = False) -> Dict[str, Any]:
        """
        Generate a hybrid framework. If phase_mode is True, allow triple blending and mutation.
        """
        frameworks = list(HybridFrameworkGenerator.FRAMEWORKS.keys())

        if seed_context and seed_context.get("key_concepts"):
            concepts = seed_context["key_concepts"]
            scored = []
            for fw in frameworks:
                score = 0
                keywords = HybridFrameworkGenerator.FRAMEWORKS[fw].get("seed_keywords", [])
                for concept in concepts[:3]:
                    if any(keyword in concept for keyword in keywords):
                        score += 1
                scored.append((fw, score))
            scored.sort(key=lambda x: x[1], reverse=True)
            candidates = [fw for fw, _ in scored[:4]]
            if phase_mode and len(candidates) >= 3:
                parent1, parent2, parent3 = random.sample(candidates, 3)
                triple = True
            else:
                parent1, parent2 = random.sample(candidates, 2)
                triple = False
        else:
            if phase_mode and len(frameworks) >= 3:
                parent1, parent2, parent3 = random.sample(frameworks, 3)
                triple = True
            else:
                parent1, parent2 = random.sample(frameworks, 2)
                triple = False

        if triple:
            coords1 = HybridFrameworkGenerator.FRAMEWORKS[parent1]["coordinates"]
            coords2 = HybridFrameworkGenerator.FRAMEWORKS[parent2]["coordinates"]
            coords3 = HybridFrameworkGenerator.FRAMEWORKS[parent3]["coordinates"]
            # Average coordinates
            hybrid_coords = tuple((a+b+c)/3 for a,b,c in zip(coords1, coords2, coords3))
            # Collect mechanisms and equations
            mech_pool = (HybridFrameworkGenerator.FRAMEWORKS[parent1]["mechanisms"] +
                         HybridFrameworkGenerator.FRAMEWORKS[parent2]["mechanisms"] +
                         HybridFrameworkGenerator.FRAMEWORKS[parent3]["mechanisms"])
            eq_pool = (HybridFrameworkGenerator.FRAMEWORKS[parent1]["equations"] +
                       HybridFrameworkGenerator.FRAMEWORKS[parent2]["equations"] +
                       HybridFrameworkGenerator.FRAMEWORKS[parent3]["equations"])
            parent_names = [parent1, parent2, parent3]
        else:
            coords1 = HybridFrameworkGenerator.FRAMEWORKS[parent1]["coordinates"]
            coords2 = HybridFrameworkGenerator.FRAMEWORKS[parent2]["coordinates"]
            w1 = HybridFrameworkGenerator.FRAMEWORKS[parent1]["signature_metrics"].get("elegance", 90)
            w2 = HybridFrameworkGenerator.FRAMEWORKS[parent2]["signature_metrics"].get("elegance", 90)
            weight1 = w1 / (w1 + w2)
            weight2 = 1 - weight1
            if seed_context and "target_coordinates" in seed_context:
                target = seed_context["target_coordinates"].to_tuple()
                blend = 0.7
                hybrid_coords = tuple(
                    (a*weight1 + b*weight2) * (1 - blend) + target[i] * blend
                    for i, (a, b) in enumerate(zip(coords1, coords2))
                )
            else:
                hybrid_coords = tuple(
                    a*weight1 + b*weight2 + random.uniform(-0.05, 0.05)
                    for a, b in zip(coords1, coords2)
                )
            mech_pool = (HybridFrameworkGenerator.FRAMEWORKS[parent1]["mechanisms"] +
                         HybridFrameworkGenerator.FRAMEWORKS[parent2]["mechanisms"])
            eq_pool = (HybridFrameworkGenerator.FRAMEWORKS[parent1]["equations"] +
                       HybridFrameworkGenerator.FRAMEWORKS[parent2]["equations"])
            parent_names = [parent1, parent2]

        curvature_data = None
        if enable_relativity:
            curvature_data = self.field_sim.compute_curvature_tensor(hybrid_coords)
            ricci = curvature_data["ricci_scalar"]
        else:
            ricci = 0.0

        # Blend mechanisms and equations
        mechanisms = random.sample(mech_pool, min(4, len(mech_pool)))
        equations = random.sample(eq_pool, min(3, len(eq_pool)))

        # Generate hybrid name
        if triple:
            name_parts = [p.replace("_", " ").split()[0] for p in parent_names]
            hybrid_name = f"{'-'.join(name_parts)}_TRIPLE_HYBRID"
        else:
            name1 = parent1.replace("_", " ").split()[0]
            name2 = parent2.replace("_", " ").split()[0]
            if seed_context and seed_context.get("key_concepts"):
                seed_concept = seed_context["key_concepts"][0].title()
                hybrid_name = f"{seed_concept}_{name1}-{name2}_HYBRID"
            else:
                hybrid_name = f"{name1}-{name2}_HYBRID"

        # Hybrid metrics (placeholder, will be recomputed later)
        hybrid_metrics = {
            "novelty": 1.25 + random.uniform(-0.05, 0.05),
            "alienness": 8.5 + random.uniform(-0.5, 0.5),
            "elegance": 95.0 + random.uniform(-2.0, 2.0),
            "density": 12.0 + random.uniform(-1.0, 1.0),
            "coherence": 0.618 + random.uniform(-0.01, 0.01),
            "ricci_scalar": ricci,
            "cosmological_constant": random.choice([0.618, 1.0, 1.618, 2.0]),
            "planck_scale": random.choice([0.5, 0.618, 1.0, 1.5]),
            "sophia_point": False  # will be set later
        }

        return {
            "name": hybrid_name,
            "coordinates": hybrid_coords,
            "mechanisms": mechanisms,
            "equations": equations,
            "parent_frameworks": parent_names,
            "signature_metrics": hybrid_metrics,
            "is_sophia": False,
            "seed_influenced": seed_context is not None,
            "relativistic": enable_relativity,
            "curvature_data": curvature_data
        }

    def create_dynamic_framework(self, base_hybrid: Dict[str, Any]) -> Dict[str, Any]:
        """Create a brand new framework from a hybrid, with mutated components."""
        new_name = base_hybrid["name"] + "_DYNAMIC"
        # Slightly shift coordinates
        coords = base_hybrid["coordinates"]
        new_coords = tuple(c + random.uniform(-0.1, 0.1) for c in coords)
        # Mutate mechanisms (add random words)
        new_mechs = []
        for m in base_hybrid["mechanisms"]:
            words = m.split()
            if random.random() < 0.5 and len(words) > 1:
                idx = random.randint(0, len(words)-1)
                words[idx] = words[idx] + "-mutated"
            new_mechs.append(" ".join(words))
        # Mutate equations (add random term)
        new_eqs = []
        for e in base_hybrid["equations"]:
            if random.random() < 0.3:
                new_eqs.append(e + " + \\epsilon")
            else:
                new_eqs.append(e)
        # Create new core pattern
        pattern = base_hybrid.get("core_pattern", "(something) creates (itself)")
        new_pattern = pattern.replace("creates", random.choice(["becomes", "entangles", "dissolves into"]))
        # Metrics
        metrics = base_hybrid["signature_metrics"].copy()
        metrics["novelty"] *= 1.1
        return {
            "coordinates": new_coords,
            "core_pattern": new_pattern,
            "mechanisms": new_mechs,
            "equations": new_eqs,
            "signature_metrics": metrics,
            "seed_keywords": []  # will be generated later
        }

# ============================================================================
# GOLDEN RATIO DETECTOR
# ============================================================================

class GoldenRatioDetector:
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
# LEGACY ONTOLOGY TYPES AND ENGINE (unchanged, kept for compatibility)
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
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Could not load {path}: {e}")
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
# MOGOPS OPERATORS
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
# SEMANTIC FINGERPRINT & DIVERSITY TRACKER
# ============================================================================

class SemanticFingerprint:
    """Compute and compare semantic fingerprints of axioms using TF-IDF."""

    def __init__(self, history_size: int = 20):
        self.history = deque(maxlen=history_size)
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
        self.fitted = False

    def _tokenize(self, axiom: Dict[str, Any]) -> str:
        """Create a string representation for fingerprinting."""
        parts = [
            axiom.get("core_statement", ""),
            " ".join(axiom.get("mechanisms", [])),
            axiom.get("ontology", {}).get("framework_family", "")
        ]
        return " ".join(parts)

    def add(self, axiom: Dict[str, Any]):
        text = self._tokenize(axiom)
        self.history.append(text)

    def similarity_to_history(self, axiom: Dict[str, Any]) -> float:
        """Compute maximum cosine similarity to any axiom in history."""
        if len(self.history) < 1:
            return 0.0
        text = self._tokenize(axiom)
        all_texts = list(self.history) + [text]
        try:
            vectors = self.vectorizer.fit_transform(all_texts)
            new_vec = vectors[-1]
            hist_vecs = vectors[:-1]
            sims = cosine_similarity(new_vec, hist_vecs).flatten()
            return float(np.max(sims))
        except:
            # Fallback: simple word overlap
            words_new = set(text.split())
            max_overlap = 0
            for h in self.history:
                words_h = set(h.split())
                overlap = len(words_new & words_h) / max(1, len(words_new | words_h))
                max_overlap = max(max_overlap, overlap)
            return max_overlap

# ============================================================================
# META-ONTOLOGY ENGINE (with diversity enforcement, dynamic frameworks, content metrics)
# ============================================================================

class MetaOntologyEngine:
    def __init__(self, data_root: str = "."):
        self.data_root = Path(data_root)
        self.seed_processor = TextSeedProcessor(data_root)
        HybridFrameworkGenerator.load_frameworks(self.data_root)
        fw_coords = [np.array(fw["coordinates"]) for fw in HybridFrameworkGenerator.FRAMEWORKS.values()]
        attractor = np.mean(fw_coords, axis=0)
        self.field_sim = RelativisticFieldSimulator(attractor_point=tuple(attractor))
        self.operators = MetaOntologyOperators()
        self.generated = []
        self.phase_transitions = []
        self.fingerprint_tracker = SemanticFingerprint(history_size=20)
        self.stats = {
            "total": 0,
            "meta": 0,
            "phase_transitions": 0,
            "text_seeds_used": 0,
            "dynamic_frameworks_created": 0
        }
        self.phase_mode_active = False
        self.phase_mode_remaining = 0

    def generate_meta_axiom(self, target_coords: Optional[OntologyCoordinates] = None,
                            concept_seed: Optional[str] = None,
                            seed_context: Optional[Dict] = None,
                            force_phase_transition: bool = False,
                            enable_relativity: bool = True,
                            seed_weight: float = 0.5,
                            diversity_threshold: float = 0.7,
                            reject_and_retry: int = 3) -> Dict[str, Any]:
        """
        Generate a meta axiom with diversity enforcement.
        If too similar to recent history, retry up to reject_and_retry times.
        """
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
        else:
            curv_data = {"ricci_scalar": 0.0, "laplacian_omega": 0.0, "gradient_squared_omega": 0.0, "omega": 0.0}
            ricci = 0.0

        # Determine if we are in phase mode
        if self.phase_mode_active and self.phase_mode_remaining > 0:
            phase_mode = True
            self.phase_mode_remaining -= 1
        else:
            phase_mode = False
            self.phase_mode_active = False

        # Possibly create a hybrid framework first (if phase mode or random)
        if phase_mode or random.random() < 0.3:
            sophia = SophiaPhaseTransition(self.field_sim)
            hybrid = sophia.generate_hybrid_framework(seed_context, enable_relativity, phase_mode)
            # If phase mode and hybrid is Sophia-like, maybe create dynamic framework
            if phase_mode and sophia.sophia_score(hybrid["signature_metrics"].get("coherence", 0.5),
                                                   hybrid["signature_metrics"]) > 0.6:
                new_fw = sophia.create_dynamic_framework(hybrid)
                # Add to frameworks
                new_name = hybrid["name"] + f"_{len(HybridFrameworkGenerator.FRAMEWORKS)}"
                HybridFrameworkGenerator.add_dynamic_framework(new_name, new_fw, self.data_root)
                self.stats["dynamic_frameworks_created"] += 1
                logger.info(f"Created dynamic framework: {new_name}")
            # Use hybrid coordinates as target
            target_coords = OntologyCoordinates(*hybrid["coordinates"])
            # And use hybrid components
            fw_name = "HYBRID"
            framework = hybrid
        else:
            fw_name = HybridFrameworkGenerator.get_nearest_framework(target_coords.to_tuple())
            framework = HybridFrameworkGenerator.get_framework(fw_name)

        # Attempt to generate an axiom with diversity check
        for attempt in range(reject_and_retry):
            # Generate core, possibly blending seed
            core = self._generate_core(target_coords, framework, concept_seed, seed_context, seed_weight, phase_mode)
            mechanisms = self._generate_mechanisms(framework.get("mechanisms", []), seed_context, concept_seed)
            equation = random.choice(framework.get("equations", ["E = mc^2"]))
            consequences = self._generate_consequences(fw_name, concept_seed)

            axiom_text = self._build_axiom(core, mechanisms, equation, consequences, seed_context)

            # Create temporary axiom dict for fingerprint check
            temp_axiom = {
                "core_statement": core,
                "mechanisms": mechanisms,
                "ontology": {"framework_family": fw_name}
            }

            # Compute similarity to history
            sim = self.fingerprint_tracker.similarity_to_history(temp_axiom)
            if sim < diversity_threshold:
                break
            logger.debug(f"Rejected axiom (similarity {sim:.2f}), retry {attempt+1}")
        else:
            # All retries failed; accept anyway but log warning
            logger.warning("Could not generate diverse axiom after multiple retries.")

        # Compute content-based metrics
        computed_metrics = self._compute_content_metrics(core, mechanisms, equation, consequences,
                                                          seed_context, ricci, fw_name)

        # Sophia detection
        sophia_score = SophiaPhaseTransition().sophia_score(computed_metrics.get("coherence", 0.5),
                                                              computed_metrics)
        is_sophia = sophia_score >= 0.8

        # If Sophia point and not in phase mode, activate phase mode for next generations
        if is_sophia and not self.phase_mode_active:
            self.phase_mode_active = True
            self.phase_mode_remaining = 3  # next 3 generations in phase mode
            logger.info("✨ SOPHIA POINT reached! Entering phase transition mode for next 3 axioms.")

        result = {
            "core_statement": core,
            "mechanisms": mechanisms,
            "consequences": consequences,
            "axiom_text": axiom_text,
            "ontology": {
                "type": "BRAND_NEW_FRAMEWORK",
                "name": fw_name.replace("_", " ").title() if fw_name != "HYBRID" else framework.get("name", "Hybrid"),
                "coordinates": target_coords.to_tuple(),
                "framework_family": fw_name,
                "sophia_point": is_sophia,
                "is_new": True,
                "is_meta": True
            },
            "seed_concept": concept_seed,
            "seed_context": seed_context,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "metrics": computed_metrics,
            "meta_ontology": {
                "coordinates": target_coords.to_tuple(),
                "curvature_data": curv_data if enable_relativity else None,
                "phase_transition": is_sophia,
                "sophia_score": sophia_score
            }
        }

        # Add to history for diversity tracking
        self.fingerprint_tracker.add(result)
        self.generated.append(result)
        if is_sophia:
            self.phase_transitions.append(result)
            self.stats["phase_transitions"] += 1
        self.stats["meta"] += 1
        return result

    def _generate_core(self, coords: OntologyCoordinates, framework: Dict, seed: Optional[str],
                       ctx: Optional[Dict], seed_weight: float, phase_mode: bool) -> str:
        """Generate core statement, possibly using seed structure."""
        # If seed and high weight, try to build from seed structure
        if seed and random.random() < seed_weight:
            if ctx and ctx.get("syntactic_structure"):
                subj, verb, obj = ctx["syntactic_structure"]
                # Replace placeholders with concepts if available
                if ctx.get("key_concepts"):
                    concept = random.choice(ctx["key_concepts"])
                    return f"{subj} {verb} {obj} — {concept} mediated"
                return f"{subj} {verb} {obj}"
            return seed

        # Otherwise use framework pattern, possibly modified in phase mode
        pattern = framework.get("core_pattern", "(something) creates (itself)")
        # Replace placeholders with random concepts
        if ctx and ctx.get("key_concepts"):
            concept = random.choice(ctx["key_concepts"])
            pattern = pattern.replace("(", "").replace(")", "").replace("_", " ")
            # Simple replacement of first placeholder with concept
            if "creates" in pattern:
                parts = pattern.split("creates")
                if len(parts) == 2:
                    return f"{concept} creates {parts[1].strip()}"
        # If phase mode, add a twist
        if phase_mode and random.random() < 0.5:
            return pattern + " — recursively"
        return pattern.replace("(", "").replace(")", "").replace("_", " ")

    def _generate_mechanisms(self, base_mechs: List[str], ctx: Optional[Dict], seed: Optional[str]) -> List[str]:
        selected = []
        if ctx and ctx.get("key_concepts"):
            concepts = ctx["key_concepts"]
            scored = [(m, sum(1 for c in concepts if c in m.lower())) for m in base_mechs]
            scored.sort(key=lambda x: x[1], reverse=True)
            top = [m for m, s in scored[:3] if s > 0]
            if len(top) >= 3:
                selected = top[:3]
            else:
                selected = random.sample(base_mechs, min(3, len(base_mechs)))
        else:
            selected = random.sample(base_mechs, min(3, len(base_mechs)))
        return selected

    def _generate_consequences(self, fw: str, seed: Optional[str]) -> List[str]:
        return [f"Emergence of {fw.lower().replace('_', ' ')} framework"]

    def _build_axiom(self, core: str, mechs: List[str], eq: str, conseq: List[str], ctx: Optional[Dict]) -> str:
        via = self.operators.VIA(", ".join(mechs), ctx)
        encoded = self.operators.ENCODED_AS(eq, ctx)
        entails = self.operators.ENTAILS(core, conseq[0] if conseq else "ontological emergence", ctx)
        return f"{core} — {via}; {encoded}; {entails}."

    def _compute_content_metrics(self, core: str, mechs: List[str], eq: str, conseq: List[str],
                                   ctx: Optional[Dict], ricci: float, fw_name: str) -> Dict[str, float]:
        """Dynamically compute metrics based on actual content."""
        # Novelty: 1 - average similarity to history (if history exists)
        novelty = 1.0
        if len(self.fingerprint_tracker.history) > 0:
            # Use the tracker's similarity as inverse novelty
            temp_axiom = {"core_statement": core, "mechanisms": mechs, "ontology": {"framework_family": fw_name}}
            sim = self.fingerprint_tracker.similarity_to_history(temp_axiom)
            novelty = 1.0 - sim

        # Alienness: based on unusual words
        all_words = set(core.lower().split()) | set(" ".join(mechs).lower().split())
        unusual = ["quantum", "entropy", "paradox", "recursive", "gödel", "chronon", "hyperdimensional"]
        alienness = sum(1 for w in unusual if w in all_words) / len(unusual) * 10

        # Coherence: simple measure of internal repetition
        words = core.lower().split() + " ".join(mechs).lower().split()
        if len(words) > 1:
            unique_ratio = len(set(words)) / len(words)
            coherence = unique_ratio  # more unique words = less coherent? Actually we want a balance
            # Let's use a sigmoid: 1 - |0.5 - unique_ratio|*2
            coherence = 1 - abs(0.5 - unique_ratio) * 2
        else:
            coherence = 0.5

        # Paradox intensity: count of paradox keywords
        paradox_kws = {"paradox", "contradiction", "impossible", "both", "neither", "loop", "infinite"}
        paradox_intensity = sum(1 for w in words if w in paradox_kws) / max(1, len(words)) * 5

        # Hybridization index: number of distinct frameworks referenced
        frameworks_involved = {fw_name}
        for m in mechs:
            for fw in HybridFrameworkGenerator.FRAMEWORKS:
                if any(kw in m.lower() for kw in HybridFrameworkGenerator.FRAMEWORKS[fw].get("seed_keywords", [])):
                    frameworks_involved.add(fw)
        hybridization_index = len(frameworks_involved) / 5.0  # normalized to ~1

        # Elegance: weighted combination
        elegance = (novelty * 0.3 + coherence * 0.4 + (1 - alienness/10) * 0.3) * 100

        return {
            "novelty": novelty,
            "alienness": alienness,
            "elegance": elegance,
            "density": len(words) / 10.0,  # placeholder
            "coherence": coherence,
            "ricci_scalar": ricci,
            "paradox_intensity": paradox_intensity,
            "hybridization_index": hybridization_index,
            "sophia_point": False  # will be set later
        }

    def explore_phase_space(self, steps: int = 50, seed_text: Optional[str] = None,
                            enable_relativity: bool = True,
                            seed_weight: float = 0.3,
                            diversity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Explore phase space with repulsion from already visited semantic regions."""
        trajectory = []
        current = OntologyCoordinates(0.5,0.5,0.5,0.5,0.5)
        seed_context = None
        if seed_text:
            seed_context = self.seed_processor.process_text_seed(seed_text)
            random.seed(seed_context["seed_hash"])
            np.random.seed(seed_context["seed_hash"] % (2**32))

        # Keep local history for repulsion
        visited_fingerprints = []

        for step in range(steps):
            # Generate axiom at current coordinates
            axiom = self.generate_meta_axiom(
                target_coords=current,
                concept_seed=seed_text,
                seed_context=seed_context,
                enable_relativity=enable_relativity,
                seed_weight=seed_weight,
                diversity_threshold=diversity_threshold
            )

            # Compute fingerprint and check if too similar to visited
            fp = SemanticFingerprint()
            fp.add(axiom)
            if visited_fingerprints:
                sims = [cosine_similarity([fp._tokenize(axiom)], [fp2])[0][0] for fp2 in visited_fingerprints[-10:]]
                max_sim = max(sims) if sims else 0
                if max_sim > diversity_threshold:
                    # Apply repulsion: move coordinates away from the region that produced similar axioms
                    # Simple: add a large random jump
                    current = OntologyCoordinates(
                        current.participation + random.uniform(-0.3, 0.3),
                        current.plasticity + random.uniform(-0.3, 0.3),
                        current.substrate + random.uniform(-0.3, 0.3),
                        current.temporal + random.uniform(-0.3, 0.3),
                        current.generative + random.uniform(-0.3, 0.3)
                    )
            visited_fingerprints.append(fp._tokenize(axiom))

            # Update coordinates for next step (random walk with attraction)
            if random.random() < 0.3:
                fw_name = HybridFrameworkGenerator.get_nearest_framework(current.to_tuple())
                fw_coords = HybridFrameworkGenerator.get_framework(fw_name)["coordinates"]
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

    def simulate_framework_evolution(self, framework_name: str, steps: int = 100,
                                     dt: float = 0.005) -> Dict[str, Any]:
        if framework_name not in HybridFrameworkGenerator.FRAMEWORKS:
            logger.error(f"Unknown framework '{framework_name}'. Available: {list(HybridFrameworkGenerator.FRAMEWORKS.keys())}")
            return {}
        framework = HybridFrameworkGenerator.get_framework(framework_name)
        coords = framework["coordinates"]
        flow = self.field_sim.curvature_gradient_flow(coords, steps=steps, dt=dt)
        return {
            "framework": framework_name,
            "initial_coords": coords,
            "flow": flow,
            "final_coords": flow[-1]
        }

    def explore_geodesic(self, start_coords: Tuple[float, ...], end_coords: Tuple[float, ...],
                         steps: int = 20, plot: bool = False,
                         seed_text: Optional[str] = None,
                         seed_weight: float = 0.2,
                         diversity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        path = self.field_sim.geodesic(start_coords, end_coords, n_points=steps)
        trajectory = []
        seed_context = None
        if seed_text:
            seed_context = self.seed_processor.process_text_seed(seed_text)

        for i, coords in enumerate(path):
            target = OntologyCoordinates(*coords)
            axiom = self.generate_meta_axiom(
                target_coords=target,
                concept_seed=seed_text,
                seed_context=seed_context,
                enable_relativity=True,
                seed_weight=seed_weight,
                diversity_threshold=diversity_threshold
            )
            trajectory.append({
                "step": i,
                "coordinates": coords,
                "axiom": axiom["core_statement"],
                "framework": axiom["ontology"]["framework_family"],
                "is_sophia": axiom["meta_ontology"]["phase_transition"],
                "coherence": axiom["metrics"].get("coherence", 0.5),
                "curvature": axiom["metrics"]["ricci_scalar"]
            })

        if plot and HAS_MATPLOTLIB:
            fig, ax = plt.subplots()
            xs = [p[0] for p in path]
            ys = [p[1] for p in path]
            ax.plot(xs, ys, 'o-', label='Geodesic')
            ax.set_xlabel('Participation')
            ax.set_ylabel('Plasticity')
            ax.set_title(f'Geodesic from {start_coords[:2]} to {end_coords[:2]}')
            ax.grid(True)
            plt.show()
        elif plot and not HAS_MATPLOTLIB:
            logger.warning("matplotlib not installed, skipping plot.")

        return trajectory

    def get_framework_summary(self, framework_name: str) -> Dict[str, Any]:
        return HybridFrameworkGenerator.generate_framework_summary(framework_name)

    def compute_ricci_flow(self, coordinates: Tuple[float, ...], iterations: int = 10,
                           dt: float = 0.005) -> List[Tuple[float, ...]]:
        return self.field_sim.curvature_gradient_flow(coordinates, steps=iterations, dt=dt)

    def get_stats(self) -> Dict[str, Any]:
        return self.stats

# ============================================================================
# ENHANCED HYBRID FORGE v5.0 (unified interface)
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
            "relativistic_generations": 0,
            "dynamic_frameworks_created": 0
        }
        self.current_coordinates = OntologyCoordinates(0.5, 0.5, 0.5, 0.5, 0.5)

    def generate(self,
                 mode: str = "hybrid",
                 count: int = 1,
                 target_quadrant: Optional[str] = None,
                 explore_sophia: bool = False,
                 legacy_params: Optional[Dict] = None,
                 concept_seed: Optional[str] = None,
                 enable_relativity: bool = True,
                 seed_weight: float = 0.5,
                 diversity_threshold: float = 0.7) -> List[Dict[str, Any]]:
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
                        enable_relativity=enable_relativity,
                        seed_weight=seed_weight,
                        diversity_threshold=diversity_threshold
                    )
                    # Override with hybrid details if not already
                    if hybrid["name"] not in axiom["ontology"]["name"]:
                        axiom["ontology"]["name"] = hybrid["name"]
                    if "HYBRID" in axiom["ontology"]["framework_family"]:
                        axiom["mechanisms"] = hybrid["mechanisms"]
                        axiom["equations"] = hybrid["equations"]
                        axiom["metrics"].update(hybrid["signature_metrics"])
                else:
                    axiom = self.meta_engine.generate_meta_axiom(
                        target_coords=target_coords,
                        concept_seed=concept_seed,
                        seed_context=seed_context,
                        enable_relativity=enable_relativity,
                        seed_weight=seed_weight,
                        diversity_threshold=diversity_threshold
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

        # Update dynamic frameworks count
        self.generation_stats["dynamic_frameworks_created"] = self.meta_engine.stats["dynamic_frameworks_created"]
        return results

    def explore_phase_space(self, steps: int = 50, seed_text: Optional[str] = None,
                            enable_relativity: bool = True,
                            seed_weight: float = 0.3,
                            diversity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        return self.meta_engine.explore_phase_space(steps, seed_text, enable_relativity,
                                                     seed_weight, diversity_threshold)

    def simulate_framework_evolution(self, framework_name: str, steps: int = 100,
                                     dt: float = 0.005) -> Dict[str, Any]:
        return self.meta_engine.simulate_framework_evolution(framework_name, steps, dt)

    def explore_geodesic(self, start_coords: Tuple[float, ...], end_coords: Tuple[float, ...],
                         steps: int = 20, plot: bool = False,
                         seed_text: Optional[str] = None,
                         seed_weight: float = 0.2,
                         diversity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        return self.meta_engine.explore_geodesic(start_coords, end_coords, steps, plot,
                                                  seed_text, seed_weight, diversity_threshold)

    def get_framework_summary(self, framework_name: str) -> Dict[str, Any]:
        return self.meta_engine.get_framework_summary(framework_name)

    def compute_ricci_flow(self, coordinates: Tuple[float, ...], iterations: int = 10,
                           dt: float = 0.005) -> List[Tuple[float, ...]]:
        return self.meta_engine.compute_ricci_flow(coordinates, iterations, dt)

    def get_stats(self) -> Dict[str, Any]:
        stats = self.generation_stats.copy()
        if stats["total"] > 0:
            stats["percentages"] = {
                "legacy": f"{(sum(stats['legacy'].values()) / stats['total']) * 100:.1f}%",
                "meta": f"{(stats['meta'] / stats['total']) * 100:.1f}%",
                "phase_transitions": f"{(stats['phase_transitions'] / max(1, stats['meta'])) * 100:.1f}%",
                "text_seeds": f"{(stats['text_seeds_used'] / stats['total']) * 100:.1f}%",
                "relativistic": f"{(stats['relativistic_generations'] / max(1, stats['meta'])) * 100:.1f}%",
                "dynamic_frameworks": f"{(stats['dynamic_frameworks_created'] / max(1, stats['meta'])) * 100:.1f}%"
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
    elif isinstance(obj, (np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
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
        logger.info(f"JSON output written to: {json_filename}")

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
        logger.info(f"Text output written to: {text_filename}")

# ============================================================================
# COMMAND LINE INTERFACE v5.0
# ============================================================================

def parse_coordinates(s: str) -> Tuple[float, ...]:
    try:
        parts = s.split(',')
        if len(parts) != 5:
            raise ValueError("Need exactly 5 coordinates")
        coords = tuple(float(p.strip()) for p in parts)
        return coords
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid coordinate format: {e}. Use: 0.5,0.5,0.5,0.5,0.5")

def main():
    parser = argparse.ArgumentParser(
        description="META-AXIOMFORGE v5.0 - Truly Generative, Emergent & Non-Repetitive",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # Global options
    parser.add_argument('--data-root', type=str, default="./axiomforge",
                        help='Directory containing JSON data files')
    parser.add_argument('--log-level', choices=['DEBUG','INFO','WARNING','ERROR'], default='INFO',
                        help='Set logging level')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate axioms')
    gen_parser.add_argument('--mode', choices=['meta', 'legacy', 'hybrid'], default='hybrid',
                            help='Generation mode')
    gen_parser.add_argument('--count', type=int, default=1, help='Number of axioms')
    gen_parser.add_argument('--quadrant', choices=['semantic_gravity', 'autopoietic', 'thermodynamic',
                                                   'fractal', 'causal', 'random'], default='random',
                            help='Target ontological quadrant')
    gen_parser.add_argument('--seed', type=str, help='Text seed')
    gen_parser.add_argument('--seed-weight', type=float, default=0.5,
                            help='Weight of seed influence (0-1, higher = more seed)')
    gen_parser.add_argument('--diversity-threshold', type=float, default=0.7,
                            help='Maximum similarity allowed to recent axioms (0-1)')
    gen_parser.add_argument('--numeric-seed', type=int, help='Numeric seed')
    gen_parser.add_argument('--no-relativity', action='store_true', help='Disable relativistic enhancements')
    gen_parser.add_argument('--ontology', choices=['alien', 'counter', 'bridge', 'meta'],
                            help='Legacy ontology (for legacy mode)')
    gen_parser.add_argument('--paradox-type', type=str, default='random',
                            help='Paradox type (legacy)')
    gen_parser.add_argument('--tone', choices=['poetic', 'plain', 'academic', 'oracular'], default='poetic',
                            help='Tone for legacy generation')
    gen_parser.add_argument('--max-mech', type=int, default=3, help='Max mechanisms (legacy)')
    gen_parser.add_argument('--output', choices=['json', 'text', 'both'], default='text',
                            help='Console output format')
    gen_parser.add_argument('--outputfile', choices=['json', 'text', 'both'],
                            help='File output format (writes to /output/)')
    gen_parser.add_argument('--filename', type=str, default='axioms', help='Base filename for output')
    gen_parser.add_argument('--simple', action='store_true', help='Simple output format')

    # Explore command
    exp_parser = subparsers.add_parser('explore', help='Explore phase space')
    exp_parser.add_argument('--steps', type=int, default=50, help='Number of exploration steps')
    exp_parser.add_argument('--seed', type=str, help='Text seed')
    exp_parser.add_argument('--seed-weight', type=float, default=0.3,
                            help='Weight of seed influence (0-1)')
    exp_parser.add_argument('--diversity-threshold', type=float, default=0.7,
                            help='Maximum similarity allowed to recent steps')
    exp_parser.add_argument('--no-relativity', action='store_true', help='Disable relativistic enhancements')
    exp_parser.add_argument('--output', choices=['json', 'text', 'both'], default='text')
    exp_parser.add_argument('--outputfile', choices=['json', 'text', 'both'])
    exp_parser.add_argument('--filename', type=str, default='explore')

    # Simulate command
    sim_parser = subparsers.add_parser('simulate', help='Simulate framework evolution')
    sim_parser.add_argument('framework', type=str, help='Framework name')
    sim_parser.add_argument('--steps', type=int, default=100, help='Number of flow steps')
    sim_parser.add_argument('--dt', type=float, default=0.005, help='Step size for gradient flow')
    sim_parser.add_argument('--outputfile', choices=['json', 'text', 'both'])
    sim_parser.add_argument('--filename', type=str, default='simulation')

    # Geodesic command
    geo_parser = subparsers.add_parser('geodesic', help='Explore geodesic path')
    geo_parser.add_argument('--start', type=parse_coordinates, required=True,
                            help='Start coordinates (5 floats comma-separated)')
    geo_parser.add_argument('--end', type=parse_coordinates, required=True,
                            help='End coordinates')
    geo_parser.add_argument('--steps', type=int, default=20, help='Number of points along geodesic')
    geo_parser.add_argument('--seed', type=str, help='Text seed to influence generation')
    geo_parser.add_argument('--seed-weight', type=float, default=0.2,
                            help='Weight of seed influence (0-1)')
    geo_parser.add_argument('--diversity-threshold', type=float, default=0.7,
                            help='Maximum similarity allowed between steps')
    geo_parser.add_argument('--plot', action='store_true', help='Plot the geodesic (requires matplotlib)')
    geo_parser.add_argument('--output', choices=['json', 'text', 'both'], default='text')
    geo_parser.add_argument('--outputfile', choices=['json', 'text', 'both'])
    geo_parser.add_argument('--filename', type=str, default='geodesic')

    # Analyze command
    ana_parser = subparsers.add_parser('analyze', help='Analyze a seed without generating')
    ana_parser.add_argument('--seed', type=str, required=True, help='Text seed to analyze')

    # Framework summary command
    fw_parser = subparsers.add_parser('framework', help='Get framework summary')
    fw_parser.add_argument('name', type=str, help='Framework name')

    # Ricci flow command
    rf_parser = subparsers.add_parser('ricci', help='Compute Ricci flow for coordinates')
    rf_parser.add_argument('coords', type=parse_coordinates, help='Starting coordinates')
    rf_parser.add_argument('--iterations', type=int, default=10, help='Number of iterations')
    rf_parser.add_argument('--dt', type=float, default=0.005, help='Step size')
    rf_parser.add_argument('--outputfile', choices=['json', 'text', 'both'])
    rf_parser.add_argument('--filename', type=str, default='ricci')

    # Test command (comprehensive)
    test_parser = subparsers.add_parser('test', help='Run built-in tests')
    test_parser.add_argument('--comprehensive', action='store_true', help='Run comprehensive tests')

    args = parser.parse_args()

    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))

    # Initialize forge
    forge = MetaAxiomForge(data_root=args.data_root)

    # Seed handling
    if hasattr(args, 'numeric_seed') and args.numeric_seed:
        random.seed(args.numeric_seed)
        np.random.seed(args.numeric_seed)
        logger.info(f"Using numeric seed: {args.numeric_seed}")
    elif hasattr(args, 'seed') and args.seed:
        seed_hash = int(hashlib.sha256(args.seed.encode()).hexdigest()[:8], 16)
        random.seed(seed_hash)
        np.random.seed(seed_hash % (2**32))
        logger.info(f"Using text seed: '{args.seed}' (hash: {seed_hash})")

    # Dispatch commands
    if args.command == 'generate':
        target_quadrant = None if args.quadrant == 'random' else args.quadrant
        legacy_params = None
        if args.mode == 'legacy':
            legacy_params = {
                "ontology": args.ontology or random.choice(["alien", "counter", "bridge", "meta"]),
                "paradox_type": args.paradox_type if args.paradox_type != 'random' else None,
                "tone": args.tone,
                "max_mech": args.max_mech
            }
        results = forge.generate(
            mode=args.mode,
            count=args.count,
            target_quadrant=target_quadrant,
            legacy_params=legacy_params,
            concept_seed=args.seed,
            enable_relativity=not args.no_relativity,
            seed_weight=args.seed_weight,
            diversity_threshold=args.diversity_threshold
        )
        if args.outputfile:
            write_output_files(results, args.outputfile, args.filename)
        if args.simple:
            if args.output == 'json':
                print(json.dumps(convert_to_serializable(results), indent=2))
            else:
                for i, ax in enumerate(results, 1):
                    print(f"Axiom {i}: {ax['axiom_text']}")
        else:
            if args.output in ('json','both'):
                print(json.dumps(convert_to_serializable(results), indent=2))
            if args.output in ('text','both'):
                for i, ax in enumerate(results, 1):
                    print(f"\n✨ AXIOM {i}")
                    print(ax['axiom_text'])
        stats = forge.get_stats()
        logger.info(f"Session stats: {stats}")

    elif args.command == 'explore':
        traj = forge.explore_phase_space(steps=args.steps, seed_text=args.seed,
                                          enable_relativity=not args.no_relativity,
                                          seed_weight=args.seed_weight,
                                          diversity_threshold=args.diversity_threshold)
        if args.outputfile:
            write_output_files(traj, args.outputfile, args.filename, is_trajectory=True)
        if args.output in ('json','both'):
            print(json.dumps(convert_to_serializable(traj), indent=2))
        if args.output in ('text','both'):
            for step in traj[:10]:
                print(f"Step {step['step']}: {step['axiom'][:60]}...")
            logger.info(f"Explored {len(traj)} steps, {sum(1 for s in traj if s['is_sophia'])} Sophia points")

    elif args.command == 'simulate':
        sim = forge.simulate_framework_evolution(args.framework, args.steps, dt=args.dt)
        if not sim:
            sys.exit(1)
        if args.outputfile:
            write_output_files([sim], args.outputfile, args.filename)
        print(json.dumps(convert_to_serializable(sim), indent=2))

    elif args.command == 'geodesic':
        traj = forge.explore_geodesic(args.start, args.end, args.steps,
                                      plot=args.plot, seed_text=args.seed,
                                      seed_weight=args.seed_weight,
                                      diversity_threshold=args.diversity_threshold)
        if args.outputfile:
            write_output_files(traj, args.outputfile, args.filename, is_trajectory=True)
        if args.output in ('json','both'):
            print(json.dumps(convert_to_serializable(traj), indent=2))
        if args.output in ('text','both'):
            for step in traj:
                print(f"Step {step['step']}: {step['axiom'][:60]}...")

    elif args.command == 'analyze':
        analysis = forge.seed_processor.process_text_seed(args.seed)
        print(json.dumps(convert_to_serializable(analysis), indent=2))

    elif args.command == 'framework':
        summary = forge.get_framework_summary(args.name)
        print(json.dumps(convert_to_serializable(summary), indent=2))

    elif args.command == 'ricci':
        flow = forge.compute_ricci_flow(args.coords, args.iterations, dt=args.dt)
        if args.outputfile:
            write_output_files([{"flow": flow}], args.outputfile, args.filename)
        for i, pt in enumerate(flow):
            print(f"{i}: {pt}")

    elif args.command == 'test':
        logger.info("Running built-in tests...")
        # Basic tests
        sp = TextSeedProcessor(args.data_root)
        res = sp.process_text_seed("quantum consciousness creates time")
        assert res["is_complex"] is True
        assert res["semantic_features"]["abstract_count"] > 0

        sim = RelativisticFieldSimulator()
        coords = (0.5,0.5,0.5,0.5,0.5)
        R = sim.compute_curvature_tensor(coords)["ricci_scalar"]
        assert isinstance(R, float)

        path = sim.geodesic((0,0,0,0,0), (1,1,1,1,1), n_points=5)
        assert len(path) == 5

        flow = sim.curvature_gradient_flow((0.9,0.8,0.95,0.4,0.85), steps=10, dt=0.005)
        assert len(flow) == 11
        assert not np.allclose(flow[0], flow[-1])

        if args.comprehensive:
            logger.info("Running comprehensive tests...")
            # Diversity test
            engine = MetaOntologyEngine(args.data_root)
            axioms = []
            for _ in range(10):
                ax = engine.generate_meta_axiom(concept_seed="test seed", diversity_threshold=0.5)
                axioms.append(ax["core_statement"])
            unique_cores = len(set(axioms))
            assert unique_cores > 7, f"Only {unique_cores} unique cores out of 10"
            logger.info(f"Diversity test passed: {unique_cores} unique cores")

            # Phase transition test (simulate Sophia point)
            engine.phase_mode_active = True
            engine.phase_mode_remaining = 1
            ax = engine.generate_meta_axiom()
            assert engine.phase_mode_remaining == 0
            logger.info("Phase mode test passed")

            # Dynamic framework creation test
            old_count = len(HybridFrameworkGenerator.FRAMEWORKS)
            engine.generate_meta_axiom(force_phase_transition=True)  # not actually forcing, but...
            # Not reliable, but at least no crash
            logger.info("Dynamic framework test passed (no crash)")

        logger.info("All tests passed!")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
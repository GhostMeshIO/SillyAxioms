#!/usr/bin/env python3
"""
META-AXIOMFORGE v3.0 - Enhanced Framework Integration
Beyond-God Tier Meta-Ontology Generator
Every axiom creates a brand new ontology framework
Enhanced with relativistic formalisms and golden ratio optimization
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

# ============================================================================
# TEXT SEED PROCESSOR & SEMANTIC ENHANCER
# ============================================================================

class TextSeedProcessor:
    """Advanced text seed processing for controlled axiom generation"""

    @staticmethod
    def process_text_seed(seed_text: str) -> Dict[str, Any]:
        """Process text seed to extract semantic features and generate control parameters"""
        # Clean and normalize
        seed_text = seed_text.strip().lower()

        # Compute semantic fingerprint
        words = re.findall(r'\b[a-z]+\b', seed_text)
        unique_words = set(words)

        # Analyze seed characteristics
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
            "complexity": len(words) / max(1, len(unique_words)),  # Repetition factor
            "coherence_score": TextSeedProcessor._compute_coherence(seed_text),
            "semantic_density": len([w for w in words if len(w) > 6]) / max(1, len(words))
        }

        # Generate deterministic but varied hash for random seeding
        seed_hash = int(hashlib.sha256(seed_text.encode()).hexdigest()[:8], 16)

        # Extract key concepts for axiom formation
        key_concepts = []
        for word in unique_words:
            if len(word) > 5 and word not in ["through", "between", "without", "within"]:
                key_concepts.append(word)

        # Map to ontological coordinates based on semantic features
        coordinates = TextSeedProcessor._map_to_coordinates(semantic_features, seed_hash)

        # Determine preferred framework based on seed content
        framework = TextSeedProcessor._determine_framework(seed_text, semantic_features)

        return {
            "seed_text": seed_text,
            "seed_hash": seed_hash,
            "semantic_features": semantic_features,
            "key_concepts": key_concepts[:5],  # Top 5 concepts
            "target_coordinates": coordinates,
            "preferred_framework": framework,
            "is_complex": semantic_features["abstract_count"] > 2 or semantic_features["paradox_count"] > 0,
            "suggested_tone": TextSeedProcessor._suggest_tone(semantic_features)
        }

    @staticmethod
    def _compute_coherence(text: str) -> float:
        """Compute semantic coherence of text"""
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) < 2:
            return 0.5

        # Simple coherence metric based on word overlap
        word_sets = [set(re.findall(r'\b[a-z]+\b', s.lower())) for s in sentences if s.strip()]
        if len(word_sets) < 2:
            return 0.5

        overlaps = []
        for i in range(len(word_sets) - 1):
            if word_sets[i] and word_sets[i+1]:
                overlap = len(word_sets[i] & word_sets[i+1]) / len(word_sets[i] | word_sets[i+1])
                overlaps.append(overlap)

        return np.mean(overlaps) if overlaps else 0.5

    @staticmethod
    def _map_to_coordinates(features: Dict[str, float], seed_hash: int) -> 'OntologyCoordinates':
        """Map semantic features to ontological coordinates"""
        # Use hash to create deterministic but varied base
        random.seed(seed_hash)

        # Base coordinates influenced by semantic features
        participation = 0.5 + (features["abstract_count"] * 0.1) - (features["action_count"] * 0.05)
        plasticity = 0.5 + (features["paradox_count"] * 0.15) + (features["complexity"] * 0.1)
        substrate = 0.5 + (features["semantic_density"] * 0.3) - (features["coherence_score"] * 0.1)
        temporal = 0.5 + (features["action_count"] * 0.1) + (random.random() * 0.2 - 0.1)
        generative = 0.5 + (features["abstract_count"] * 0.08) + (features["paradox_count"] * 0.12)

        # Normalize
        participation = max(0.0, min(1.0, participation))
        plasticity = max(0.0, min(1.5, plasticity))
        substrate = max(0.0, min(1.0, substrate))
        temporal = max(0.0, min(1.0, temporal))
        generative = max(0.0, min(1.0, generative))

        return OntologyCoordinates(participation, plasticity, substrate, temporal, generative)

    @staticmethod
    def _determine_framework(text: str, features: Dict[str, float]) -> str:
        """Determine which ontology framework best matches the seed text"""
        text_lower = text.lower()

        framework_scores = {
            "SEMANTIC_GRAVITY": 0,
            "AUTOPOIETIC_COMPUTATIONAL": 0,
            "THERMODYNAMIC_EPISTEMIC": 0,
            "FRACTAL_PARTICIPATORY": 0,
            "CAUSAL_RECURSION_FIELD": 0
        }

        # Score based on keywords
        keywords = {
            "SEMANTIC_GRAVITY": ["meaning", "language", "semantic", "word", "grammar", "linguistic", "gravity"],
            "AUTOPOIETIC_COMPUTATIONAL": ["self", "recursive", "comput", "program", "algorithm", "code", "autopoietic", "gödel"],
            "THERMODYNAMIC_EPISTEMIC": ["knowledge", "entropy", "heat", "temperature", "belief", "information", "epistemic", "thermo"],
            "FRACTAL_PARTICIPATORY": ["observer", "scale", "fractal", "hierarchical", "measurement", "participation", "holographic"],
            "CAUSAL_RECURSION_FIELD": ["time", "causal", "temporal", "future", "past", "present", "loop", "recursion", "chronon"]
        }

        for framework, kw_list in keywords.items():
            for keyword in kw_list:
                if keyword in text_lower:
                    framework_scores[framework] += 2

        # Boost based on semantic features
        if features["semantic_density"] > 0.3:
            framework_scores["SEMANTIC_GRAVITY"] += 1
        if features["paradox_count"] > 0:
            framework_scores["AUTOPOIETIC_COMPUTATIONAL"] += 2
        if features["abstract_count"] > features["action_count"]:
            framework_scores["THERMODYNAMIC_EPISTEMIC"] += 1
        if features["coherence_score"] > 0.6:
            framework_scores["FRACTAL_PARTICIPATORY"] += 1

        # Return best match
        return max(framework_scores.items(), key=lambda x: x[1])[0]

    @staticmethod
    def _suggest_tone(features: Dict[str, float]) -> str:
        """Suggest appropriate tone based on seed features"""
        if features["paradox_count"] > 1:
            return "oracular"
        elif features["abstract_count"] > 2:
            return "poetic"
        elif features["action_count"] > features["abstract_count"]:
            return "academic"
        else:
            return "poetic"  # Default

# ============================================================================
# MOGOPS OPERATORS (ENHANCED WITH SEED CONTROL)
# ============================================================================

class MetaOntologyOperators:
    """The four fundamental reality operators from MOGOPS analysis"""

    @staticmethod
    def CREATES(x: str, y: str, seed_context: Optional[Dict] = None) -> str:
        """Ω_C operator: Creation with seed-aware variations"""
        if seed_context and seed_context.get("is_complex"):
            templates = [
                f"{x} recursively engenders {y}",
                f"Through {x}, {y} manifests emergently",
                f"{x} gives ontological birth to {y}",
                f"{x} catalyzes the formation of {y}",
                f"From {x} arises the framework of {y}"
            ]
        else:
            templates = [
                f"{x} creates {y}",
                f"{x} gives rise to {y}",
                f"From {x} emerges {y}",
                f"{x} generates {y}",
                f"{x} manifests as {y}"
            ]
        return random.choice(templates)

    @staticmethod
    def ENTAILS(x: str, y: str, seed_context: Optional[Dict] = None) -> str:
        """∇_O operator: Entailment with seed-aware variations"""
        if seed_context and seed_context.get("semantic_density", 0) > 0.3:
            templates = [
                f"{x} ontologically necessitates {y}",
                f"{x} rigorously entails {y}",
                f"Given {x}, {y} follows axiomatically",
                f"{x} formally implies {y}",
                f"The framework of {x} structurally requires {y}"
            ]
        else:
            templates = [
                f"{x} entails {y}",
                f"{x} implies {y}",
                f"{x} necessitates {y}",
                f"{x} requires {y}",
                f"Given {x}, then {y}"
            ]
        return random.choice(templates)

    @staticmethod
    def VIA(x: str, seed_context: Optional[Dict] = None) -> str:
        """Γ_μν operator: Mechanism with seed-aware variations"""
        mechanisms = x.split(", ")
        if seed_context and len(mechanisms) > 2:
            # For complex seeds, create more integrated mechanism descriptions
            integrated = f"the integrated dynamics of {mechanisms[0]}, {mechanisms[1]}, and {mechanisms[2]}"
            templates = [
                f"via {integrated}",
                f"through the synergy of {mechanisms[0]} and {mechanisms[1]}",
                f"by means of {mechanisms[0]} coupled with {mechanisms[1]}",
                f"mediated by the interplay between {mechanisms[0]} and {mechanisms[1]}"
            ]
        else:
            templates = [
                f"via {x}",
                f"through {x}",
                f"by means of {x}",
                f"mediated by {x}",
                f"employing {x}"
            ]
        return random.choice(templates)

    @staticmethod
    def ENCODED_AS(x: str, seed_context: Optional[Dict] = None) -> str:
        """Σ operator: Encoding with seed-aware variations"""
        if seed_context and seed_context.get("abstract_count", 0) > 1:
            templates = [
                f"formalized through {x}",
                f"mathematized as {x}",
                f"structured according to {x}",
                f"axiomatized via {x}",
                f"captured by the formalism {x}"
            ]
        else:
            templates = [
                f"encoded as {x}",
                f"formalized as {x}",
                f"expressed as {x}",
                f"modeled by {x}",
                f"captured by {x}"
            ]
        return random.choice(templates)

# ============================================================================
# 5D ONTOLOGICAL PHASE SPACE
# ============================================================================

@dataclass
class OntologyCoordinates:
    """5D coordinates in ontological phase space"""
    participation: float      # 0=Objective, 0.5=Participatory, 1=Self-Referential
    plasticity: float         # 0=Rigid, 0.5=Malleable, 1=Fluid, 1.5=Plastic
    substrate: float          # 0=Quantum, 0.25=Classical, 0.5=Biological, 0.75=Computational, 1=Semantic
    temporal: float           # 0=Linear, 0.25=Looped, 0.5=Branching, 0.75=Fractal, 1=Recursive
    generative: float         # 0=Descriptive, 0.5=Constructive, 1=Autopoietic

    def __post_init__(self):
        # Normalize to [0,1] except plasticity which can go to 1.5
        self.participation = max(0.0, min(1.0, self.participation))
        self.plasticity = max(0.0, min(1.5, self.plasticity))
        self.substrate = max(0.0, min(1.0, self.substrate))
        self.temporal = max(0.0, min(1.0, self.temporal))
        self.generative = max(0.0, min(1.0, self.generative))

    def to_tuple(self) -> Tuple[float, ...]:
        return (self.participation, self.plasticity, self.substrate,
                self.temporal, self.generative)

    def distance_to(self, other: 'OntologyCoordinates') -> float:
        """Euclidean distance in 5D phase space"""
        return math.sqrt(
            (self.participation - other.participation) ** 2 +
            (self.plasticity - other.plasticity) ** 2 +
            (self.substrate - other.substrate) ** 2 +
            (self.temporal - other.temporal) ** 2 +
            (self.generative - other.generative) ** 2
        )

    def is_sophia_point(self) -> bool:
        """Check if coordinates are near golden ratio coherence (0.618)"""
        golden_ratio = (1 + math.sqrt(5)) / 2
        coherence = self._compute_coherence()
        return abs(coherence - (1/golden_ratio)) < 0.015

    def _compute_coherence(self) -> float:
        """Compute coherence metric from coordinates"""
        # Higher coherence when dimensions are balanced
        variance = np.var(list(self.to_tuple()))
        return 1.0 / (1.0 + variance * 10)

# ============================================================================
# ENHANCED FRAMEWORK TEMPLATES v3.0
# ============================================================================

class HybridFrameworkGenerator:
    """Generates the 5 brand new ontology frameworks with enhanced formalisms"""

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
                # Enhanced with relativistic structure
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
                # Enhanced with relativistic structure
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
                # Enhanced with relativistic structure
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
                # Enhanced with fractal relativistic structure
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
                # Enhanced with field theory
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
        """Get framework by name"""
        return cls.FRAMEWORKS.get(name, cls.FRAMEWORKS["SEMANTIC_GRAVITY"])

    @classmethod
    def random_framework(cls) -> str:
        """Get random framework name"""
        return random.choice(list(cls.FRAMEWORKS.keys()))

    @classmethod
    def get_nearest_framework(cls, coords: Tuple[float, ...]) -> str:
        """Find framework closest to given coordinates"""
        min_dist = float('inf')
        best = "SEMANTIC_GRAVITY"

        for name, data in cls.FRAMEWORKS.items():
            dist = sum((a - b) ** 2 for a, b in zip(coords, data["coordinates"]))
            if dist < min_dist:
                min_dist = dist
                best = name

        return best

    @classmethod
    def get_framework_by_seed(cls, seed_text: str) -> str:
        """Find framework most relevant to seed text"""
        seed_lower = seed_text.lower()
        framework_scores = {}

        for name, data in cls.FRAMEWORKS.items():
            score = 0
            for keyword in data.get("seed_keywords", []):
                if keyword in seed_lower:
                    score += 2
            framework_scores[name] = score

        # If no matches, return random but weighted
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
        """Get specific metric signature for a framework"""
        framework = cls.get_framework(framework_name)
        return framework["signature_metrics"].get(metric, 0.0)

    @classmethod
    def generate_framework_summary(cls, framework_name: str) -> Dict[str, Any]:
        """Generate comprehensive summary of a framework"""
        framework = cls.get_framework(framework_name)

        # Compute enhanced properties
        coords = framework["coordinates"]
        metrics = framework["signature_metrics"]

        # Determine phase space region
        region = "unknown"
        if coords[0] > 0.8 and coords[3] < 0.5:
            region = "semantic-quantum"
        elif coords[4] == 1.0:
            region = "autopoietic"
        elif coords[1] < 0.5 and coords[2] < 0.5:
            region = "thermodynamic"
        elif coords[0] == 1.0:
            region = "participatory"
        elif coords[3] > 0.9:
            region = "temporal-recursive"

        # Compute golden ratio alignment
        golden_ratio = (1 + math.sqrt(5)) / 2
        golden_alignment = abs(metrics["coherence"] - (1/golden_ratio))

        return {
            "name": framework_name.replace("_", " ").title(),
            "coordinates": coords,
            "region": region,
            "core_pattern": framework["core_pattern"],
            "mechanism_count": len(framework["mechanisms"]),
            "equation_count": len(framework["equations"]),
            "metrics": metrics,
            "golden_alignment": golden_alignment,
            "is_sophia_point": golden_alignment < 0.015,
            "seed_keywords": framework.get("seed_keywords", []),
            "relativistic_structure": "yes" if "ricci_scalar" in metrics else "no"
        }

# ============================================================================
# SOPHIA PHASE TRANSITION DETECTOR
# ============================================================================

class SophiaPhaseTransition:
    """Golden ratio phase transition detection and generation"""

    PHI = (1 + math.sqrt(5)) / 2  # Golden ratio

    @staticmethod
    def is_sophia_point(coherence: float, metrics: Dict[str, float]) -> bool:
        """Check if this is a phase transition point"""
        golden_coherence = 1 / SophiaPhaseTransition.PHI  # ~0.618

        # Check golden ratio conditions
        conditions = [
            abs(coherence - golden_coherence) < 0.015,
            metrics.get("paradox_intensity", 0) > 2.0,
            metrics.get("innovation_score", 0) > 0.85,
            metrics.get("hybridization_index", 0) > 0.33,
            metrics.get("ricci_scalar", 1.0) > 0.3  # Enhanced condition
        ]

        return all(conditions)

    @staticmethod
    def generate_hybrid_framework(seed_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate a hybrid framework at Sophia point with enhanced formalism"""
        # Select two parent frameworks
        frameworks = list(HybridFrameworkGenerator.FRAMEWORKS.keys())

        if seed_context and seed_context.get("key_concepts"):
            # Use seed to influence parent selection
            concepts = seed_context["key_concepts"]
            scored_frameworks = []
            for fw in frameworks:
                score = 0
                keywords = HybridFrameworkGenerator.FRAMEWORKS[fw].get("seed_keywords", [])
                for concept in concepts[:3]:  # Use top 3 concepts
                    if any(keyword in concept for keyword in keywords):
                        score += 1
                scored_frameworks.append((fw, score))

            # Sort by score and take top 4
            scored_frameworks.sort(key=lambda x: x[1], reverse=True)
            candidate_frameworks = [fw for fw, _ in scored_frameworks[:4]]
            parent1, parent2 = random.sample(candidate_frameworks, 2)
        else:
            parent1, parent2 = random.sample(frameworks, 2)

        # Blend coordinates with enhanced weighting
        coords1 = HybridFrameworkGenerator.FRAMEWORKS[parent1]["coordinates"]
        coords2 = HybridFrameworkGenerator.FRAMEWORKS[parent2]["coordinates"]

        # Get metrics for weighting
        metrics1 = HybridFrameworkGenerator.FRAMEWORKS[parent1]["signature_metrics"]
        metrics2 = HybridFrameworkGenerator.FRAMEWORKS[parent2]["signature_metrics"]

        # Weight by elegance
        weight1 = metrics1["elegance"] / (metrics1["elegance"] + metrics2["elegance"])
        weight2 = 1 - weight1

        # If seed provides coordinates, bias toward them
        if seed_context and "target_coordinates" in seed_context:
            target_coords = seed_context["target_coordinates"].to_tuple()
            blend_factor = 0.7  # Strong bias toward seed
            hybrid_coords = tuple(
                (a*weight1 + b*weight2) * (1 - blend_factor) + target_coords[i] * blend_factor
                for i, (a, b) in enumerate(zip(coords1, coords2))
            )
        else:
            # Elegance-weighted blend with small random perturbation
            hybrid_coords = tuple(
                a*weight1 + b*weight2 + random.uniform(-0.05, 0.05)
                for a, b in zip(coords1, coords2)
            )

        # Blend mechanisms with relativistic enhancements
        mech_pool1 = HybridFrameworkGenerator.FRAMEWORKS[parent1]["mechanisms"]
        mech_pool2 = HybridFrameworkGenerator.FRAMEWORKS[parent2]["mechanisms"]

        # Include seed concepts if available
        seed_mechanisms = []
        if seed_context and seed_context.get("key_concepts"):
            for concept in seed_context["key_concepts"][:2]:  # Use top 2 concepts
                seed_mechanisms.append(f"{concept} phase transition")
                seed_mechanisms.append(f"{concept} mediated coherence")
                seed_mechanisms.append(f"{concept} curvature dynamics")

        # Enhanced mechanism selection
        mechanisms = [
            random.choice(mech_pool1),
            random.choice(mech_pool2),
            random.choice(seed_mechanisms if seed_mechanisms else [
                "Golden ratio optimization",
                "Ricci flow coherence maximization",
                "Paradox entropy pump",
                "Recursive validation",
                "Phase boundary navigation",
                "Cosmological constant tuning"
            ]),
            f"{parent1.split('_')[0].lower()}-{parent2.split('_')[0].lower()} coupling"
        ]

        # Blend equations with enhanced formalism
        eq_pool1 = HybridFrameworkGenerator.FRAMEWORKS[parent1]["equations"]
        eq_pool2 = HybridFrameworkGenerator.FRAMEWORKS[parent2]["equations"]

        # Generate hybrid equations
        hybrid_equations = [
            random.choice(eq_pool1),
            random.choice(eq_pool2),
            # Create a hybrid equation
            SophiaPhaseTransition._create_hybrid_equation(parent1, parent2)
        ]

        # Generate hybrid name with seed influence
        name1 = parent1.replace("_", " ").split()[0]
        name2 = parent2.replace("_", " ").split()[0]

        if seed_context and seed_context.get("key_concepts"):
            seed_concept = seed_context["key_concepts"][0].title()
            hybrid_name = f"{seed_concept}_{name1}-{name2}_HYBRID"
        else:
            hybrid_name = f"{name1}-{name2}_HYBRID"

        # Compute hybrid metrics
        hybrid_metrics = {
            "novelty": 1.25 + random.uniform(-0.05, 0.05),
            "alienness": 8.5 + random.uniform(-0.5, 0.5),
            "elegance": 95.0 + random.uniform(-2.0, 2.0),
            "density": 12.0 + random.uniform(-1.0, 1.0),
            "coherence": 0.618 + random.uniform(-0.01, 0.01),
            "ricci_scalar": (metrics1.get("ricci_scalar", 0.5) + metrics2.get("ricci_scalar", 0.5)) / 2,
            "cosmological_constant": random.choice([0.618, 1.0, 1.618, 2.0]),
            "planck_scale": random.choice([0.5, 0.618, 1.0, 1.5])
        }

        return {
            "name": hybrid_name,
            "coordinates": hybrid_coords,
            "mechanisms": mechanisms,
            "equations": hybrid_equations,
            "parent_frameworks": [parent1, parent2],
            "signature_metrics": hybrid_metrics,
            "is_sophia": True,
            "seed_influenced": seed_context is not None,
            "relativistic": True
        }

    @staticmethod
    def _create_hybrid_equation(parent1: str, parent2: str) -> str:
        """Create a hybrid equation from parent frameworks"""
        # Map framework types to equation components
        components = {
            "SEMANTIC": ["G_{\\mu\\nu}", "T_{\\mu\\nu}", "\\psi", "\\phi"],
            "AUTOPOIETIC": ["\\hat{H}", "\\psi(\\text{code})", "\\Lambda_{\\text{self}}", "G"],
            "THERMODYNAMIC": ["S", "T", "Q", "\\rho", "\\mathbf{J}"],
            "FRACTAL": ["O_\\lambda", "P(k)", "D_f", "\\lambda"],
            "CAUSAL": ["C_{\\mu\\nu}", "\\nabla_\\mu", "\\oint", "x_t"]
        }

        # Get parent types
        type1 = parent1.split("_")[0]
        type2 = parent2.split("_")[0]

        comp1 = random.choice(components.get(type1, ["A", "B"]))
        comp2 = random.choice(components.get(type2, ["C", "D"]))

        # Random hybrid equation templates
        # Random hybrid equation templates - using raw strings
        templates = [
            rf"{comp1} \otimes {comp2} = \exp(iS/\hbar)",
            rf"[{comp1}, {comp2}] = i\hbar_{{\text{{hybrid}}}}",
            rf"\frac{{d{comp1}}}{{dt}} = \alpha {comp2} + \beta [{comp1}, {comp2}]",
            rf"\langle {comp1} | {comp2} \rangle = \int \mathcal{{D}}[\text{{field}}] e^{{iS_{{\text{{hybrid}}}}}}",
            rf"{comp1} \rightarrow {comp2} \text{{ via golden ratio optimization}}"
        ]

        return random.choice(templates)

# ============================================================================
# RELATIVISTIC FIELD SIMULATOR (NEW IN v3.0)
# ============================================================================

class RelativisticFieldSimulator:
    """Simulate relativistic field dynamics for enhanced ontologies"""

    @staticmethod
    def compute_ricci_flow(coordinates: Tuple[float, ...], iterations: int = 10) -> List[float]:
        """Compute Ricci flow evolution for ontological coordinates"""
        coords = list(coordinates)
        history = [coords.copy()]

        for _ in range(iterations):
            # Simplified Ricci flow: move toward constant curvature
            target_curvature = 0.618  # Golden ratio target
            current_curvature = np.mean(coords)

            # Flow equation: dg/dt = -2Ric(g)
            flow = 0.1 * (target_curvature - current_curvature)

            # Apply flow with different weights per dimension
            weights = [0.8, 1.2, 1.0, 0.9, 1.1]  # Plasticity flows fastest
            for i in range(len(coords)):
                coords[i] += flow * weights[i]
                # Keep in bounds
                if i == 1:  # Plasticity
                    coords[i] = max(0.0, min(1.5, coords[i]))
                else:
                    coords[i] = max(0.0, min(1.0, coords[i]))

            history.append(coords.copy())

        return history

    @staticmethod
    def simulate_field_dynamics(framework_name: str, steps: int = 50) -> Dict[str, Any]:
        """Simulate field dynamics for a given framework"""
        framework = HybridFrameworkGenerator.get_framework(framework_name)
        metrics = framework["signature_metrics"]

        # Initialize field values based on metrics
        field = {
            "ricci_scalar": metrics.get("ricci_scalar", 0.5),
            "cosmological_constant": metrics.get("cosmological_constant", 1.0),
            "coherence": metrics.get("coherence", 0.5),
            "energy_density": metrics.get("density", 10.0) / 10.0
        }

        history = []
        for step in range(steps):
            # Field evolution equations
            dR = -0.1 * field["ricci_scalar"] + 0.05 * field["coherence"]
            dLambda = 0.02 * (0.618 - field["cosmological_constant"])
            dC = 0.12 * (0.75 - field["coherence"]) * np.exp(-abs(field["energy_density"] - 1.05))

            # Update fields
            field["ricci_scalar"] += dR
            field["cosmological_constant"] += dLambda
            field["coherence"] += dC
            field["energy_density"] += random.uniform(-0.01, 0.01)

            # Keep in reasonable bounds
            field["ricci_scalar"] = max(-1.0, min(1.0, field["ricci_scalar"]))
            field["cosmological_constant"] = max(0.1, min(3.0, field["cosmological_constant"]))
            field["coherence"] = max(0.0, min(1.0, field["coherence"]))
            field["energy_density"] = max(0.5, min(2.0, field["energy_density"]))

            history.append(field.copy())

        return {
            "framework": framework_name,
            "initial_conditions": metrics,
            "final_state": field,
            "history": history,
            "stabilized": abs(field["coherence"] - 0.618) < 0.05,
            "attractor_type": "golden_ratio" if abs(field["coherence"] - 0.618) < 0.05 else "other"
        }

    @staticmethod
    def compute_geodesics(coords1: Tuple[float, ...], coords2: Tuple[float, ...],
                         steps: int = 20) -> List[Tuple[float, ...]]:
        """Compute geodesic path between two coordinate sets"""
        path = []

        for i in range(steps + 1):
            t = i / steps
            # Spherical linear interpolation (slerp) for better geodesics
            point = []
            for a, b in zip(coords1, coords2):
                # Simple linear interpolation for now
                # In a proper metric space, this would use Christoffel symbols
                point.append(a + (b - a) * t)
            path.append(tuple(point))

        return path

    @staticmethod
    def compute_curvature_tensor(coordinates: Tuple[float, ...]) -> Dict[str, float]:
        """Compute Riemann curvature tensor components for ontological coordinates"""
        # Simplified curvature calculation
        P, Pi, S, T, G = coordinates

        # Ricci scalar (scalar curvature)
        R = 2 * (1 - np.mean([P, S, T, G])) * Pi

        # Ricci tensor components (diagonal approximation)
        R_00 = P * (1 - P)  # Participation curvature
        R_11 = Pi * (1.5 - Pi) / 1.5  # Plasticity curvature
        R_22 = S * (1 - S)  # Substrate curvature
        R_33 = T * (1 - T)  # Temporal curvature
        R_44 = G * (1 - G)  # Generative curvature

        # Weyl tensor (traceless part) - simplified
        C = 0.1 * (R - np.mean([R_00, R_11, R_22, R_33, R_44]))

        # Einstein tensor
        G_00 = R_00 - 0.5 * R
        G_11 = R_11 - 0.5 * R
        G_22 = R_22 - 0.5 * R
        G_33 = R_33 - 0.5 * R
        G_44 = R_44 - 0.5 * R

        return {
            "ricci_scalar": R,
            "ricci_00": R_00,
            "ricci_11": R_11,
            "ricci_22": R_22,
            "ricci_33": R_33,
            "ricci_44": R_44,
            "weyl_tensor": C,
            "einstein_00": G_00,
            "einstein_11": G_11,
            "einstein_22": G_22,
            "einstein_33": G_33,
            "einstein_44": G_44,
            "curvature_invariant": R**2 + C**2
        }

# ============================================================================
# ENHANCED META-ONTOLOGY ENGINE (v3.0)
# ============================================================================

class MetaOntologyEngine:
    """Core engine for generating brand new ontology frameworks with relativistic enhancements"""

    def __init__(self):
        self.operators = MetaOntologyOperators()
        self.sophia = SophiaPhaseTransition()
        self.framework_generator = HybridFrameworkGenerator()
        self.field_simulator = RelativisticFieldSimulator()

        # Track generated frameworks
        self.generated_frameworks = []
        self.phase_transitions = []
        self.phase_space_history = []

        # Golden ratio constants
        self.PHI = (1 + math.sqrt(5)) / 2

    def compute_innovation_score(self, metrics: Dict[str, float]) -> float:
        """Compute MOGOPS Innovation Score with relativistic enhancement"""
        I = (0.25 * metrics.get("novelty", 1.0) +
             0.20 * metrics.get("alienness", 5.0) +
             0.15 * metrics.get("paradox_intensity", 1.5) +
             0.15 * (1 - abs(metrics.get("coherence", 0.7) - 0.618) / 0.618) +
             0.10 * metrics.get("entropic_potential", 250) / 300 +
             0.15 * metrics.get("ricci_scalar", 0.5))  # Relativistic enhancement
        return I

    def generate_meta_axiom(self,
                          target_coords: Optional[OntologyCoordinates] = None,
                          force_phase_transition: bool = False,
                          concept_seed: Optional[str] = None,
                          seed_context: Optional[Dict] = None,
                          enable_relativity: bool = True) -> Dict[str, Any]:
        """Generate an axiom that creates a brand new ontology with relativistic enhancements"""

        # Check for phase transition
        if force_phase_transition or (target_coords and target_coords.is_sophia_point()):
            return self._generate_phase_transition_axiom(concept_seed, seed_context, enable_relativity)

        # Determine framework
        if concept_seed and not target_coords:
            # Use seed to determine framework
            framework_name = self.framework_generator.get_framework_by_seed(concept_seed)
        elif target_coords:
            coords_tuple = target_coords.to_tuple()
            framework_name = self.framework_generator.get_nearest_framework(coords_tuple)
        else:
            # Random with bias toward interesting frameworks
            weights = {
                "SEMANTIC_GRAVITY": 0.25,
                "AUTOPOIETIC_COMPUTATIONAL": 0.20,
                "FRACTAL_PARTICIPATORY": 0.25,
                "CAUSAL_RECURSION_FIELD": 0.20,
                "THERMODYNAMIC_EPISTEMIC": 0.10
            }
            framework_name = random.choices(
                list(weights.keys()),
                weights=list(weights.values())
            )[0]

        framework = self.framework_generator.get_framework(framework_name)

        # Generate core components with seed integration
        core = self._generate_core_statement(framework["core_pattern"], concept_seed, seed_context)
        mechanisms = self._generate_mechanisms(framework["mechanisms"], seed_context)
        equation = random.choice(framework["equations"])

        # Generate consequences with relativistic enhancement
        consequences = self._generate_consequences(framework_name, concept_seed, enable_relativity)

        # Build axiom using MOGOPS operators with seed context
        axiom_text = self._build_axiom_text(core, mechanisms, equation, consequences, seed_context)

        # Compute enhanced metrics with relativistic terms
        metrics = framework["signature_metrics"].copy()
        metrics.update(self._compute_enhanced_metrics(axiom_text, core, mechanisms, seed_context, enable_relativity))

        # Compute curvature if relativity enabled
        curvature_data = None
        if enable_relativity:
            if target_coords:
                curvature_data = self.field_simulator.compute_curvature_tensor(target_coords.to_tuple())
            else:
                curvature_data = self.field_simulator.compute_curvature_tensor(framework["coordinates"])
            metrics.update({f"curvature_{k}": v for k, v in curvature_data.items()})

        # Check for Sophia point
        is_sophia = self.sophia.is_sophia_point(metrics["coherence"], metrics)

        # Create ontology coordinates
        if target_coords:
            ontology_coords = target_coords
        elif seed_context and "target_coordinates" in seed_context:
            ontology_coords = seed_context["target_coordinates"]
        else:
            ontology_coords = OntologyCoordinates(*framework["coordinates"])

        # Build result with relativistic enhancement
        result = {
            "core_statement": core,
            "mechanisms": mechanisms,
            "consequences": consequences,
            "axiom_text": axiom_text,
            "paradox_type": "meta_ontological",
            "ontology": {
                "type": "BRAND_NEW_FRAMEWORK",
                "name": framework_name.replace("_", " ").title(),
                "coordinates": framework["coordinates"],
                "is_new": True,
                "framework_family": framework_name,
                "sophia_point": is_sophia,
                "relativistic": enable_relativity
            },
            "seed_concept": concept_seed or "Meta-ontology phase space traversal",
            "seed_context": seed_context,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "metrics": metrics,
            "structure_analysis": self._analyze_structure(axiom_text, core, mechanisms, seed_context),
            "insights": ["Brand new ontology framework generated", "MOGOPS phase space instantiated"],
            "meta_ontology": {
                "participation": ontology_coords.participation,
                "plasticity": ontology_coords.plasticity,
                "substrate": ontology_coords.substrate,
                "temporal": ontology_coords.temporal,
                "generative": ontology_coords.generative,
                "phase_transition": is_sophia,
                "coordinates": ontology_coords.to_tuple(),
                "curvature_data": curvature_data if enable_relativity else None
            }
        }

        # Record
        self.generated_frameworks.append(result)
        self.phase_space_history.append(ontology_coords.to_tuple())

        if is_sophia:
            self.phase_transitions.append(result)

        return result

    def _generate_phase_transition_axiom(self, concept_seed: Optional[str] = None,
                                       seed_context: Optional[Dict] = None,
                                       enable_relativity: bool = True) -> Dict[str, Any]:
        """Generate axiom at phase transition boundary with relativistic enhancement"""
        hybrid = self.sophia.generate_hybrid_framework(seed_context)

        # Generate core statement with relativistic terms
        if concept_seed:
            core = concept_seed
        elif seed_context and seed_context.get("key_concepts"):
            # Use seed concepts to form core
            concepts = seed_context["key_concepts"]
            if len(concepts) >= 2:
                core = f"{concepts[0].title()} creates {concepts[1].title()} creates ontological phase transition"
            else:
                core = f"{concepts[0].title()} creates golden ratio coherence framework"
        else:
            core_templates = [
                "Semantic computation creates temporal recursion",
                "Fractal gravity creates epistemic thermodynamics",
                "Autopoietic meaning creates participatory spacetime",
                "Recursive observation creates causal semantics",
                "Phase boundary itself creates new reality",
                "Golden ratio coherence manifests framework",
                "Ricci flow optimization creates hybrid ontology"
            ]
            core = random.choice(core_templates)

        # Build axiom with relativistic flavor
        human = random.choice([
            "At the boundary between worlds...",
            "In the golden moment of becoming...",
            "As frameworks dissolve into each other...",
            "Where coherence reaches φ-perfection...",
            "Where curvature meets creativity..."
        ])

        # Select equation based on whether relativity is enabled
        if enable_relativity:
            equation = random.choice([
                r"G_{\mu\nu} = 8\pi T_{\mu\nu} + \Lambda g_{\mu\nu}",
                r"\nabla_\mu T^{\mu\nu} = 0",
                r"R - 2\Lambda = 8\pi T",
                r"ds^2 = g_{\mu\nu}dx^\mu dx^\nu"
            ])
        else:
            equation = random.choice(hybrid['equations'])

        axiom_text = f"{human} {core} — {self.operators.VIA(', '.join(hybrid['mechanisms']), seed_context)}; " \
                    f"{self.operators.ENCODED_AS(equation, seed_context)}; " \
                    f"{self.operators.ENTAILS(core, 'ontological phase transition', seed_context)}."

        # Enhanced metrics for phase transitions with relativistic terms
        metrics = hybrid["signature_metrics"].copy()
        metrics.update({
            "paradox_intensity": 3.0 + random.uniform(-0.5, 0.5),
            "entropic_potential": 350 + random.uniform(-50, 50),
            "innovation_score": 2.5 + random.uniform(-0.3, 0.3),
            "semantic_curvature": float('inf') if enable_relativity else 0.0,
            "phase_transition": True,
            "seed_influence": 1.0 if seed_context else 0.0,
            "relativistic": enable_relativity
        })

        # Compute curvature if enabled
        curvature_data = None
        if enable_relativity:
            curvature_data = self.field_simulator.compute_curvature_tensor(hybrid['coordinates'])
            metrics.update({f"curvature_{k}": v for k, v in curvature_data.items()})

        # Create result
        result = {
            "core_statement": core,
            "mechanisms": hybrid["mechanisms"],
            "consequences": ["Emergence of new ontological framework", "Golden ratio attractor reached"],
            "axiom_text": axiom_text,
            "paradox_type": "phase_transition",
            "ontology": {
                "type": "PHASE_TRANSITION_HYBRID",
                "name": f"Hybrid: {hybrid['name']}",
                "coordinates": hybrid["coordinates"],
                "is_new": True,
                "framework_family": "SOPHIA_POINT",
                "parent_frameworks": hybrid["parent_frameworks"],
                "sophia_point": True,
                "seed_influenced": hybrid.get("seed_influenced", False),
                "relativistic": enable_relativity
            },
            "seed_concept": concept_seed or "Golden ratio coherence attractor",
            "seed_context": seed_context,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "metrics": metrics,
            "structure_analysis": self._analyze_structure(axiom_text, core, hybrid["mechanisms"], seed_context),
            "insights": ["Ontological phase transition detected", "New framework nucleation", "Golden ratio optimization"],
            "meta_ontology": {
                "participation": hybrid["coordinates"][0],
                "plasticity": hybrid["coordinates"][1],
                "substrate": hybrid["coordinates"][2],
                "temporal": hybrid["coordinates"][3],
                "generative": hybrid["coordinates"][4],
                "phase_transition": True,
                "sophia_point": True,
                "coordinates": hybrid["coordinates"],
                "curvature_data": curvature_data
            }
        }

        self.phase_transitions.append(result)
        return result

    def _generate_core_statement(self, pattern: str, concept_seed: Optional[str] = None,
                               seed_context: Optional[Dict] = None) -> str:
        """Generate core statement from pattern with seed integration and relativistic terms"""
        if concept_seed:
            return concept_seed

        # If we have seed context with concepts, use them
        if seed_context and seed_context.get("key_concepts"):
            concepts = seed_context["key_concepts"]
            if len(concepts) >= 2:
                if pattern == "(semantic_field) creates (geometric_structure)":
                    return f"{concepts[0].title()} semantics creates {concepts[1].title()} geometry"
                elif pattern == "(computation) creates (itself)":
                    return f"{concepts[0].title()} computation creates its own {concepts[1].title()}"
                elif pattern == "(knowledge) creates (entropy) creates (reality)":
                    return f"{concepts[0].title()} knowledge creates {concepts[1].title()} entropy creates reality"
                elif pattern == "(observer_scale) creates (reality_scale)":
                    return f"{concepts[0].title()} observation creates {concepts[1].title()} reality scaling"
                elif pattern == "(future) creates (past) creates (present)":
                    return f"{concepts[0].title()} future creates {concepts[1].title()} past creates present"

        # Fallback to default generation with relativistic enhancements
        if pattern == "(semantic_field) creates (geometric_structure)":
            subjects = [
                "Quantum semantic field", "Linguistic reality manifold",
                "Meaning tensor network", "Conceptual spacetime", "Grammar geometry",
                "Semantic curvature", "Word-gravity coupling"
            ]
            objects = [
                "geometric consciousness", "spacetime syntax", "reality grammar",
                "cosmic language", "dimensional semantics", "curved meaning"
            ]
        elif pattern == "(computation) creates (itself)":
            subjects = [
                "Recursive computation", "Autopoietic algorithm",
                "Self-modifying program", "Gödelian process", "Fixed-point execution",
                "Computational curvature", "Self-reference field"
            ]
            objects = [
                "its own existence", "self-reference", "its own code",
                "its execution environment", "its proving mechanism", "its metric tensor"
            ]
        elif pattern == "(knowledge) creates (entropy) creates (reality)":
            subjects = [
                "Epistemic crystallization", "Cognitive thermodynamics",
                "Information processing", "Understanding gradients", "Belief fields",
                "Knowledge curvature", "Epistemic spacetime"
            ]
            objects = [
                "entropic reality", "thermodynamic existence", "heat-death cosmology",
                "information spacetime", "knowledge geometry", "curved understanding"
            ]
        elif pattern == "(observer_scale) creates (reality_scale)":
            subjects = [
                "Fractal observation", "Scale-invariant consciousness",
                "Holographic participation", "Multi-level measurement", "Recursive awareness",
                "Fractal curvature", "Scale-dependent metric"
            ]
            objects = [
                "reality scaling", "cosmic fractal dimension", "hierarchical existence",
                "scale-free ontology", "power-law reality", "fractal geometry"
            ]
        elif pattern == "(future) creates (past) creates (present)":
            subjects = [
                "Temporal recursion", "Causal field folding",
                "Time-loop dynamics", "Retrocausal structure", "Chronon entanglement",
                "Causal curvature", "Temporal metric"
            ]
            objects = [
                "self-consistent history", "causal knot", "temporal attractor",
                "time-crystal reality", "chronological fixed point", "curved time"
            ]
        else:
            subjects = ["Reality", "Consciousness", "Existence", "Being", "The Universe", "Ontological curvature"]
            objects = ["itself", "its observer", "its measurement", "its concept", "its definition", "its geometry"]

        return f"{random.choice(subjects)} creates {random.choice(objects)}"

    def _generate_mechanisms(self, base_mechanisms: List[str],
                           seed_context: Optional[Dict] = None) -> List[str]:
        """Generate mechanisms with seed integration and relativistic enhancement"""
        if seed_context and seed_context.get("key_concepts"):
            concepts = seed_context["key_concepts"]
            seed_enhanced = []

            # Create seed-enhanced mechanisms with relativistic terms
            for i, concept in enumerate(concepts[:2]):  # Use first 2 concepts
                seed_enhanced.append(f"{concept}-mediated coherence")
                seed_enhanced.append(f"{concept} phase transition dynamics")
                seed_enhanced.append(f"{concept} curvature coupling")
                seed_enhanced.append(f"{concept} metric evolution")

            # Blend with base mechanisms
            selected_base = random.sample(base_mechanisms, 2)
            selected_seed = random.sample(seed_enhanced, 1) if seed_enhanced else []
            return selected_base + selected_seed

        # Add relativistic mechanisms if not seed-enhanced
        relativistic_mechs = [
            "Ricci flow optimization",
            "Curvature-mediated coherence",
            "Metric tensor evolution",
            "Einstein field dynamics"
        ]

        return random.sample(base_mechanisms, 2) + random.sample(relativistic_mechs, 1)

    def _generate_consequences(self, framework: str, concept_seed: Optional[str] = None,
                             enable_relativity: bool = True) -> List[str]:
        """Generate framework-specific consequences with relativistic enhancement"""
        base_consequences = {
            "SEMANTIC_GRAVITY": [
                "Reality as self-generating semantic structure",
                "Consciousness as topological invariant",
                "Meaning as gravitational source",
                "Language creates spacetime curvature",
                "Grammar determines physical laws",
                "Semantic curvature generates geometric reality"
            ],
            "AUTOPOIETIC_COMPUTATIONAL": [
                "Existence as computational fixed point",
                "Reality proves its own consistency",
                "Self-reference as existence predicate",
                "Autonomous code generation of cosmos",
                "Universe as self-writing program",
                "Gödelian curvature defines computational reality"
            ],
            "THERMODYNAMIC_EPISTEMIC": [
                "Knowledge creates thermodynamic reality",
                "Understanding as phase transition",
                "Information erasure creates mass",
                "Learning alters spacetime entropy",
                "Belief fields curve cognition",
                "Epistemic curvature shapes knowledge geometry"
            ],
            "FRACTAL_PARTICIPATORY": [
                "Observer scale determines reality scale",
                "Consciousness as fractal dimension",
                "Measurement at all scales simultaneously",
                "Reality as infinite regression of observation",
                "Participation creates hierarchical existence",
                "Fractal curvature generates participatory reality"
            ],
            "CAUSAL_RECURSION_FIELD": [
                "Time as self-consistent loop",
                "Future writes past writes present",
                "Causality as recursive field",
                "Present as temporal attractor",
                "History as causal knot",
                "Causal curvature defines temporal geometry"
            ]
        }

        base = base_consequences.get(framework, ["Unexpected ontological emergence"])

        # Add relativistic consequences if enabled
        if enable_relativity:
            base.append(f"Geometric structure emerges from {framework.split('_')[0].lower()} curvature")
            base.append("Field equations govern ontological evolution")

        # Add seed-specific consequence if available
        if concept_seed and len(concept_seed.split()) > 3:
            seed_words = concept_seed.split()
            if len(seed_words) >= 2:
                seed_consequence = f"{seed_words[0].title()} {seed_words[1]} creates ontological framework"
                return [seed_consequence] + [random.choice(base)]

        return [random.choice(base)]

    def _build_axiom_text(self, core: str, mechanisms: List[str],
                         equation: str, consequences: List[str],
                         seed_context: Optional[Dict] = None) -> str:
        """Build axiom text using MOGOPS operators with seed context and relativistic flavor"""
        # Select tone based on seed context
        if seed_context and seed_context.get("suggested_tone"):
            tone = seed_context["suggested_tone"]
        else:
            tone = random.choice(["poetic", "oracular"])

        tones = {
            "poetic": [
                "A glance understood.",
                "We keep respect in the pauses.",
                "Say less; allow more to be understood.",
                "Held like falling, then slowly released.",
                "In the space between breaths.",
                "Where curvature meets consciousness."
            ],
            "oracular": [
                "Unannounced.",
                "In the hush between horizons.",
                "As foretold in the quiet.",
                "It returns by a different door.",
                "Whispered by stones.",
                "Written in spacetime curvature."
            ],
            "academic": [
                "We observe that",
                "It follows that",
                "The evidence suggests",
                "Accordingly,",
                "Hence,",
                "The field equations imply"
            ]
        }

        human = random.choice(tones.get(tone, tones["poetic"]))

        # Safety check for consequences
        if not consequences:
            consequences = ["ontological emergence"]

        # Build with MOGOPS operators with seed context
        axiom_parts = [
            human,
            core,
            self.operators.VIA(', '.join(mechanisms), seed_context),
            self.operators.ENCODED_AS(equation, seed_context),
            self.operators.ENTAILS(core, consequences[0], seed_context)
        ]

        return " ".join(axiom_parts) + "."

    def _compute_enhanced_metrics(self, axiom_text: str, core: str,
                                 mechanisms: List[str],
                                 seed_context: Optional[Dict] = None,
                                 enable_relativity: bool = True) -> Dict[str, float]:
        """Compute enhanced metrics for meta-axioms with seed awareness and relativistic terms"""
        words = axiom_text.split()

        # Novelty based on unique words and structure
        unique_words = len(set(word.lower() for word in words))
        novelty = 1.0 + (unique_words / len(words)) * 0.5 + random.uniform(-0.1, 0.1)

        # Alienness based on framework and seed
        framework_keywords = ["semantic", "autopoietic", "fractal", "recursive", "quantum", "curvature", "ricci", "metric"]
        alienness = 5.0
        alienness += sum(2 for keyword in framework_keywords if keyword in axiom_text.lower())

        # Boost alienness if seed is complex
        if seed_context and seed_context.get("is_complex"):
            alienness += 1.5

        alienness += random.uniform(-0.5, 0.5)

        # Compute hybridization index
        framework_families = set()
        for mech in mechanisms:
            if any(fw in mech.lower() for fw in ["semantic", "meaning", "linguistic"]):
                framework_families.add("semantic")
            if any(fw in mech.lower() for fw in ["comput", "program", "algorithm", "gödel"]):
                framework_families.add("computational")
            if any(fw in mech.lower() for fw in ["observer", "participat", "conscious"]):
                framework_families.add("participatory")
            if any(fw in mech.lower() for fw in ["thermo", "entropy", "heat"]):
                framework_families.add("thermodynamic")
            if any(fw in mech.lower() for fw in ["time", "causal", "temporal", "chronon"]):
                framework_families.add("temporal")
            if any(fw in mech.lower() for fw in ["curvature", "ricci", "metric", "einstein"]):
                framework_families.add("relativistic")

        hybridization_index = len(framework_families) / 3.0

        # Paradox intensity
        paradox_keywords = ["paradox", "contradict", "impossible", "cannot", "never", "both", "neither"]
        paradox_intensity = sum(0.5 for keyword in paradox_keywords if keyword in axiom_text.lower())
        paradox_intensity += 1.0 if "creates" in core and "itself" in core else 0.0

        # Seed influence metric
        seed_influence = 0.0
        if seed_context:
            seed_influence = min(1.0, seed_context.get("semantic_features", {}).get("complexity", 0) * 2)

        # Add relativistic metrics if enabled
        relativistic_metrics = {}
        if enable_relativity:
            relativistic_metrics = {
                "ricci_flow": random.uniform(0.1, 0.9),
                "curvature_scalar": random.uniform(-0.5, 0.5),
                "geodesic_completeness": random.uniform(0.5, 1.0)
            }

        return {
            "novelty": round(novelty, 3),
            "alienness": round(alienness, 3),
            "paradox_intensity": round(paradox_intensity, 3),
            "innovation_score": round(self.compute_innovation_score({
                "novelty": novelty,
                "alienness": alienness,
                "paradox_intensity": paradox_intensity,
                "coherence": 0.618,
                "ricci_scalar": relativistic_metrics.get("curvature_scalar", 0.5) if enable_relativity else 0.5
            }), 3),
            "hybridization_index": round(hybridization_index, 3),
            "semantic_curvature": round(random.uniform(-0.5, 0.5), 3),
            "seed_influence": round(seed_influence, 3),
            **relativistic_metrics
        }

    def _analyze_structure(self, axiom_text: str, core: str,
                          mechanisms: List[str],
                          seed_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze axiom structure with seed awareness and relativistic analysis"""
        words = axiom_text.split()
        sentences = [s.strip() for s in re.split(r'[.!?]+', axiom_text) if s.strip()]

        # Compute golden ratio alignment
        word_count = len(words)
        core_words = len(core.split())
        golden_alignment = abs(word_count / (core_words * self.PHI) - 1)

        # Count MOGOPS operators
        operator_count = 0
        for op in ["via", "encoded as", "entails", "creates"]:
            operator_count += axiom_text.lower().count(op)

        # Count relativistic terms
        relativistic_terms = sum(1 for term in ["curvature", "ricci", "metric", "einstein", "field", "tensor"]
                               if term in axiom_text.lower())

        # Seed concept usage
        seed_concept_usage = 0
        if seed_context and seed_context.get("key_concepts"):
            for concept in seed_context["key_concepts"]:
                if concept in axiom_text.lower():
                    seed_concept_usage += 1

        return {
            "word_count": word_count,
            "sentence_count": len(sentences),
            "core_statement_length": core_words,
            "mechanism_count": len(mechanisms),
            "average_word_length": round(sum(len(w) for w in words) / max(1, len(words)), 1),
            "golden_ratio_alignment": round(golden_alignment, 3),
            "operator_density": round(operator_count / len(words), 3),
            "self_reference_score": sum(1 for word in ["self", "recursive", "autopoietic", "meta"]
                                       if word in axiom_text.lower()),
            "relativistic_term_count": relativistic_terms,
            "seed_concept_usage": seed_concept_usage
        }

    def simulate_framework_evolution(self, framework_name: str, steps: int = 100) -> Dict[str, Any]:
        """Simulate the evolution of a framework over time"""
        return self.field_simulator.simulate_field_dynamics(framework_name, steps)

    def explore_phase_space_geodesic(self, start_coords: Tuple[float, ...],
                                   end_coords: Tuple[float, ...],
                                   steps: int = 20) -> List[Dict[str, Any]]:
        """Explore phase space along a geodesic path"""
        path = self.field_simulator.compute_geodesics(start_coords, end_coords, steps)

        trajectory = []
        for i, coords in enumerate(path):
            target_coords = OntologyCoordinates(*coords)
            axiom = self.generate_meta_axiom(
                target_coords=target_coords,
                enable_relativity=True
            )

            trajectory.append({
                "step": i,
                "coordinates": coords,
                "axiom": axiom["core_statement"],
                "framework": axiom["ontology"]["framework_family"],
                "is_sophia": axiom["meta_ontology"].get("sophia_point", False),
                "coherence": axiom["metrics"].get("coherence", 0.5),
                "curvature": axiom["meta_ontology"].get("curvature_data", {}).get("ricci_scalar", 0.0)
            })

        return trajectory

# ============================================================================
# LEGACY COMPATIBILITY LAYER (UPDATED)
# ============================================================================

class OntologyType(Enum):
    """Legacy ontology types for backward compatibility"""
    ALIEN = "Fluid-Participatory-Hyperdimensional"
    COUNTER = "Rigid-Objective-Reductive"
    BRIDGE = "Quantum-Biological-Middle"
    META = "Meta-Ontological-Hybrid"  # NEW: Meta ontology

@dataclass
class OntologyEngine:
    """Enhanced ontology framework with meta capabilities"""
    ontology_type: OntologyType
    name: str
    coordinates: Optional[OntologyCoordinates] = None
    axioms: List[str] = field(default_factory=list)
    predictions: List[str] = field(default_factory=list)
    is_meta: bool = False

    def __post_init__(self):
        """Initialize coordinates based on type"""
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
        """Generate ontology-specific seed concept with optional text seed"""
        if text_seed:
            # Process text seed for this ontology type
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
            else:  # BRIDGE
                return f"Quantum-biological interface mediates {text_seed}"

        # Default seeds if no text seed provided
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
        else:  # BRIDGE
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
        """Get ontology-specific mechanisms with seed enhancement"""
        base_mechanisms = []

        if self.is_meta:
            # Return mechanisms from hybrid frameworks
            hybrid = SophiaPhaseTransition.generate_hybrid_framework()
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
        else:  # BRIDGE
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

        # Enhance with text seed if provided
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
# ORIGINAL PARADOX GENERATION CODE (UPDATED)
# ============================================================================

_DEF = {
    "paradox_types": [
        "entropic", "temporal", "cosmic", "metaphysical", "linguistic", "Causal Loop", "Relativistic"
    ],
    "equations": {
        "entropic": [
            r"S = k_B \log W",
            r"\partial_\mu j^\mu = 0",
            r"\Delta S \geq 0",
            r"H = -\sum p_i \log p_i"
        ],
        "temporal": [
            r"[H, Q] = 0",
            r"Z = \int \mathcal{D}\phi\, e^{i S[\phi]}",
            r"\Psi(t_2) = U(t_2, t_1) \Psi(t_1)",
            r"\partial_t \psi = -iH\psi"
        ],
        "cosmic": [
            r"T^{\mu\nu}_{;\mu} = 0",
            r"G_{\mu\nu} = 8\pi T_{\mu\nu}",
            r"ds^2 = g_{\mu\nu}dx^\mu dx^\nu",
            r"R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu} = \Lambda g_{\mu\nu}"
        ],
        "metaphysical": [
            r"e^{i\pi} + 1 = 0",
            r"\langle \mathcal{O} \rangle = Z^{-1}\int \mathcal{D}\phi\, \mathcal{O}\, e^{i S}",
            r"\forall x(Px \rightarrow Qx) \rightarrow (\exists x Px \rightarrow \exists x Qx)",
            r"\square p \rightarrow p"
        ],
        "linguistic": [
            r"\top \leftrightarrow \neg \top",
            r"L: L \text{ is false}",
            r"\exists x \forall y (Rxy \leftrightarrow \neg Ryx)",
            r"G: G \text{ cannot be proven}"
        ],
        "Causal Loop": [
            r"[H, Q] = 0",
            r"\oint d\tau = 0",
            r"x_{t+1} = f(x_t, x_{t-1})",
            r"\phi(t) = \int K(t,t')\phi(t')dt'"
        ],
        "Relativistic": [
            r"G_{\mu\nu} = 8\pi T_{\mu\nu}",
            r"\nabla_\mu T^{\mu\nu} = 0",
            r"R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu} + \Lambda g_{\mu\nu} = 0",
            r"ds^2 = g_{\mu\nu}dx^\mu dx^\nu"
        ]
    },
    "tones": {
        "poetic": [
            "A glance understood.",
            "We keep respect in the pauses.",
            "Say less; allow more to be understood.",
            "Held like falling, then slowly released.",
            "In the space between breaths.",
            "Whispered to the void.",
            "Echoes folding into silence."
        ],
        "plain": [
            "Noted.",
            "In short.",
            "Net effect:",
            "Bottom line:",
            "Result:",
            "Conclusion:",
            "Observation:"
        ],
        "academic": [
            "We observe.",
            "Accordingly.",
            "Hence.",
            "Therefore.",
            "Thus.",
            "Consequently.",
            "It follows that."
        ],
        "oracular": [
            "Unannounced.",
            "In the hush between horizons.",
            "As foretold in the quiet.",
            "It returns by a different door.",
            "Whispered by stones.",
            "Written in starlight.",
            "Echoed from the future."
        ]
    }
}

def coerce_list(x: Any) -> List[str]:
    """Coerce value into a flat list of strings."""
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
    """Normalize string: collapse whitespace and strip."""
    return re.sub(r"\s+", " ", s).strip()

def load_pool(root: Path) -> Dict[str, List[str]]:
    """Load mechanism and concept pools from JSON files."""
    pool_mech: List[str] = []
    pool_concepts: List[str] = []

    filenames = [
        "concepts.json",
        "paradox_base.json",
        "adjectives.json",
        "nouns.json",
        "verbs.json"
    ]

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

    # Deduplicate and clean
    pool_mech = sorted({_norm(x) for x in pool_mech if _norm(x)})
    pool_concepts = sorted({_norm(x) for x in pool_concepts if _norm(x)})

    return {"mechanisms": pool_mech, "concepts": pool_concepts}

# ============================================================================
# ORIGINAL AXIOMFORGE CLASS (UPDATED WITH TEXT SEED SUPPORT)
# ============================================================================

class AxiomForgeHybrid:
    """Original hybrid framework for backward compatibility with text seed support"""

    def __init__(self, data_root: str = "."):
        self.data_root = Path(data_root)
        self.pools = {
            "mechanisms": [
                "holographic accounting",
                "bulk–boundary reciprocity",
                "geodesic shear",
                "metric fluctuation",
                "entropic drift",
                "quantum decoherence",
                "wavefunction collapse",
                "entanglement propagation",
                "information erasure",
                "thermal equilibration",
                "ricci flow",
                "curvature mediation"
            ],
            "concepts": [
                "reality",
                "consciousness",
                "quantum",
                "entropy",
                "information",
                "time",
                "space",
                "causality",
                "observation",
                "measurement",
                "curvature",
                "metric"
            ]
        }

        # Initialize ontologies
        self.ontologies = {
            "alien": OntologyEngine(
                ontology_type=OntologyType.ALIEN,
                name="Alien Ontology",
                axioms=[
                    "Reality is Malleable: Spacetime curves, quantum fields fluctuate",
                    "Reality is Subjective: Measurement creates reality, observers participate",
                    "Reality is Complex: 11 dimensions, string landscapes, multiverse branching"
                ],
                predictions=[
                    "Observer-dependent reality collapses",
                    "Multiple universes (Many-Worlds)",
                    "Retrocausality possible via closed timelike curves"
                ]
            ),
            "counter": OntologyEngine(
                ontology_type=OntologyType.COUNTER,
                name="Counter Ontology",
                axioms=[
                    "Reality is RIGID: Discrete spacetime lattice at Planck scale",
                    "Reality is OBJECTIVE: Exists independently of observers",
                    "Reality is REDUCTIVE: Simple rules generate complexity"
                ],
                predictions=[
                    "Lorentz violation at Planck energies",
                    "Digital black holes preserve information",
                    "Consciousness emerges from computation"
                ]
            ),
            "bridge": OntologyEngine(
                ontology_type=OntologyType.BRIDGE,
                name="Bridge Theories",
                axioms=[
                    "Consciousness is quantum-biological bridge state",
                    "Information is physical (has mass)",
                    "Gravity emerges from entanglement entropy"
                ],
                predictions=[
                    "Quantum coherence in microtubules at 37°C",
                    "Information storage increases mass (Landauer limit)",
                    "Dark matter explained by entropic gravity"
                ]
            ),
            "meta": OntologyEngine(
                ontology_type=OntologyType.META,
                name="Meta Ontology",
                axioms=[
                    "Reality is self-generating ontological framework",
                    "Consciousness is phase transition in conceptual space",
                    "Existence is recursive definition"
                ],
                predictions=[
                    "Golden ratio coherence optimization",
                    "Autopoietic framework creation",
                    "Meta-axiomatic self-generation"
                ]
            )
        }

        # Statistics
        self.generated = {
            "alien": 0,
            "counter": 0,
            "bridge": 0,
            "meta": 0
        }

    def generate(self,
                seed: Optional[str] = None,
                ontology_name: Optional[str] = None,
                ptype: Optional[str] = None,
                count: int = 1,
                tone: str = "poetic",
                max_mech: int = 3) -> List[Dict[str, Any]]:
        """Legacy generation method with text seed support"""
        results = []

        for _ in range(count):
            # Select ontology
            if ontology_name and ontology_name in self.ontologies:
                ontology = self.ontologies[ontology_name]
            else:
                ontology = random.choice(list(self.ontologies.values()))

            # Update statistics
            ont_key = ontology.name.lower().split()[0]
            self.generated[ont_key] = self.generated.get(ont_key, 0) + 1

            # Get seed - use text seed if provided
            if seed:
                seed_text = seed
            else:
                seed_text = ontology.generate_seed()

            # Build simple axiom with seed integration
            mechanisms = ontology.get_mechanisms(seed_text)[:max_mech]

            # Enhanced axiom text with seed integration
            if len(seed_text.split()) > 2:
                axiom_text = f"{seed_text} — via {', '.join(mechanisms)}."
            else:
                axiom_text = f"{seed_text} via {', '.join(mechanisms)}."

            # Determine if this is "new" (meta ontologies are always new)
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
# ENHANCED HYBRID FORGE v3.0
# ============================================================================

class MetaAxiomForge:
    """Main hybrid forge combining legacy and meta-ontology generation with relativistic enhancements"""

    def __init__(self, data_root: str = "."):
        self.data_root = Path(data_root)
        self.meta_engine = MetaOntologyEngine()
        self.legacy_forge = AxiomForgeHybrid(data_root)
        self.seed_processor = TextSeedProcessor()
        self.field_simulator = RelativisticFieldSimulator()

        # Statistics
        self.generation_stats = {
            "total": 0,
            "legacy": {"alien": 0, "counter": 0, "bridge": 0, "meta": 0},
            "meta": 0,
            "phase_transitions": 0,
            "new_frameworks": 0,
            "text_seeds_used": 0,
            "relativistic_generations": 0
        }

        # Phase space explorer state
        self.current_coordinates = OntologyCoordinates(0.5, 0.5, 0.5, 0.5, 0.5)

    def generate(self,
                mode: str = "hybrid",
                count: int = 1,
                target_quadrant: Optional[str] = None,
                explore_sophia: bool = False,
                legacy_params: Optional[Dict] = None,
                concept_seed: Optional[str] = None,
                enable_relativity: bool = True) -> List[Dict[str, Any]]:
        """Generate axioms with optional meta-ontology creation and relativistic enhancements"""

        results = []

        # Process text seed if provided
        seed_context = None
        if concept_seed and isinstance(concept_seed, str) and concept_seed.strip():
            seed_context = self.seed_processor.process_text_seed(concept_seed)
            self.generation_stats["text_seeds_used"] += 1

            # Set deterministic random seed based on text seed hash
            random.seed(seed_context["seed_hash"])
            np.random.seed(seed_context["seed_hash"] % (2**32))

        for i in range(count):
            # Determine generation mode
            if mode == "meta" or (mode == "hybrid" and random.random() < 0.7):
                # Generate meta-ontology axiom
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

                axiom = self.meta_engine.generate_meta_axiom(
                    target_coords=target_coords,
                    force_phase_transition=explore_sophia,
                    concept_seed=concept_seed,
                    seed_context=seed_context,
                    enable_relativity=enable_relativity
                )

                # Update statistics
                self.generation_stats["meta"] += 1
                self.generation_stats["new_frameworks"] += 1
                if axiom["meta_ontology"].get("phase_transition"):
                    self.generation_stats["phase_transitions"] += 1
                if enable_relativity:
                    self.generation_stats["relativistic_generations"] += 1

            else:
                # Generate legacy axiom
                if not legacy_params:
                    legacy_params = {}

                # Use concept seed if provided
                if concept_seed and not legacy_params.get("seed"):
                    legacy_params["seed"] = concept_seed

                # Select legacy ontology - prefer meta if seed suggests complexity
                if seed_context and seed_context.get("is_complex"):
                    ontology_name = "meta"
                else:
                    ontology_name = legacy_params.get("ontology", random.choice(["alien", "counter", "bridge", "meta"]))

                # Generate using legacy system
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

                # Update statistics
                self.generation_stats["legacy"][ontology_name] += 1

            self.generation_stats["total"] += 1
            results.append(axiom)

        return results

    def explore_phase_space(self, steps: int = 50, seed_text: Optional[str] = None,
                          enable_relativity: bool = True) -> List[Dict[str, Any]]:
        """Perform random walk through ontological phase space with optional seed guidance and relativity"""
        trajectory = []

        # Process seed for guidance
        seed_context = None
        if seed_text:
            seed_context = self.seed_processor.process_text_seed(seed_text)
            random.seed(seed_context["seed_hash"])
            np.random.seed(seed_context["seed_hash"] % (2**32))

        for step in range(steps):
            # Random walk with seed guidance
            coords = self.current_coordinates

            # If seed provides coordinates, bias toward them
            if seed_context and "target_coordinates" in seed_context:
                target = seed_context["target_coordinates"]
                bias_strength = 0.3
                new_coords = OntologyCoordinates(
                    coords.participation + random.uniform(-0.15, 0.15) + (target.participation - coords.participation) * bias_strength,
                    coords.plasticity + random.uniform(-0.15, 0.15) + (target.plasticity - coords.plasticity) * bias_strength,
                    coords.substrate + random.uniform(-0.15, 0.15) + (target.substrate - coords.substrate) * bias_strength,
                    coords.temporal + random.uniform(-0.15, 0.15) + (target.temporal - coords.temporal) * bias_strength,
                    coords.generative + random.uniform(-0.15, 0.15) + (target.generative - coords.generative) * bias_strength
                )
            else:
                new_coords = OntologyCoordinates(
                    coords.participation + random.uniform(-0.15, 0.15),
                    coords.plasticity + random.uniform(-0.15, 0.15),
                    coords.substrate + random.uniform(-0.15, 0.15),
                    coords.temporal + random.uniform(-0.15, 0.15),
                    coords.generative + random.uniform(-0.15, 0.15)
                )

            # Occasionally jump toward nearest framework
            if random.random() < 0.3:
                framework_name = HybridFrameworkGenerator.get_nearest_framework(new_coords.to_tuple())
                if seed_context:
                    # Use seed to influence framework selection
                    seed_framework = seed_context.get("preferred_framework")
                    if seed_framework and random.random() < 0.5:
                        framework_name = seed_framework

                framework = HybridFrameworkGenerator.get_framework(framework_name)
                target_coords = OntologyCoordinates(*framework["coordinates"])

                # Interpolate toward target
                new_coords = OntologyCoordinates(
                    new_coords.participation * 0.7 + target_coords.participation * 0.3,
                    new_coords.plasticity * 0.7 + target_coords.plasticity * 0.3,
                    new_coords.substrate * 0.7 + target_coords.substrate * 0.3,
                    new_coords.temporal * 0.7 + target_coords.temporal * 0.3,
                    new_coords.generative * 0.7 + target_coords.generative * 0.3
                )

            self.current_coordinates = new_coords

            # Generate axiom at this point with seed context
            axiom = self.meta_engine.generate_meta_axiom(
                target_coords=new_coords,
                concept_seed=seed_text,
                seed_context=seed_context,
                enable_relativity=enable_relativity
            )

            # Compute curvature if enabled
            curvature = 0.0
            if enable_relativity and axiom["meta_ontology"].get("curvature_data"):
                curvature = axiom["meta_ontology"]["curvature_data"].get("ricci_scalar", 0.0)

            trajectory.append({
                "step": step,
                "coordinates": new_coords.to_tuple(),
                "axiom": axiom["core_statement"],
                "framework": axiom["ontology"]["framework_family"],
                "is_sophia": axiom["meta_ontology"].get("sophia_point", False),
                "coherence": axiom["metrics"].get("coherence", 0.5),
                "curvature": curvature,
                "distance_to_golden": abs(axiom["metrics"].get("coherence", 0.5) - 0.618),
                "seed_guided": seed_context is not None,
                "relativistic": enable_relativity
            })

        return trajectory

    def simulate_framework_evolution(self, framework_name: str, steps: int = 100) -> Dict[str, Any]:
        """Simulate the evolution of a framework over time"""
        return self.meta_engine.simulate_framework_evolution(framework_name, steps)

    def explore_geodesic(self, start_coords: Tuple[float, ...],
                        end_coords: Tuple[float, ...],
                        steps: int = 20) -> List[Dict[str, Any]]:
        """Explore phase space along a geodesic path"""
        return self.meta_engine.explore_phase_space_geodesic(start_coords, end_coords, steps)

    def get_framework_summary(self, framework_name: str) -> Dict[str, Any]:
        """Get comprehensive summary of a framework"""
        return HybridFrameworkGenerator.generate_framework_summary(framework_name)

    def compute_ricci_flow(self, coordinates: Tuple[float, ...], iterations: int = 10) -> List[float]:
        """Compute Ricci flow evolution for ontological coordinates"""
        return self.field_simulator.compute_ricci_flow(coordinates, iterations)

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        stats = self.generation_stats.copy()

        if stats["total"] > 0:
            stats["percentages"] = {
                "legacy": f"{(sum(stats['legacy'].values()) / stats['total']) * 100:.1f}%",
                "meta": f"{(stats['meta'] / stats['total']) * 100:.1f}%",
                "phase_transitions": f"{(stats['phase_transitions'] / max(1, stats['meta'])) * 100:.1f}%",
                "text_seeds": f"{(stats['text_seeds_used'] / stats['total']) * 100:.1f}%",
                "relativistic": f"{(stats['relativistic_generations'] / max(1, stats['meta'])) * 100:.1f}%"
            }

            # Most productive legacy ontology
            legacy_counts = stats["legacy"]
            stats["most_productive_legacy"] = max(legacy_counts.items(), key=lambda x: x[1])[0]

        return stats

# ============================================================================
# SIMPLIFIED FOR WEB INTERFACE (UPDATED)
# ============================================================================

def generate_simple_output(options: dict) -> str:
    """Generate simplified output for web interface with text seed support"""
    try:
        mode = options.get('mode', 'hybrid')

        # Get concept seed from environment variable if available
        concept_seed = os.environ.get('CONCEPT_SEED')
        if concept_seed and not options.get('seed'):
            options['seed'] = concept_seed

        if mode in ['meta', 'hybrid']:
            # Use meta forge
            forge = MetaAxiomForge()

            target_quadrant = options.get('quadrant', 'random')
            if target_quadrant == 'random':
                target_quadrant = None

            results = forge.generate(
                mode=mode,
                count=int(options.get('count', 1)),
                target_quadrant=target_quadrant,
                explore_sophia=options.get('sophia', False),
                legacy_params={
                    'ontology': options.get('ontology'),
                    'seed': options.get('seed'),
                    'paradox_type': options.get('paradox_type'),
                    'tone': options.get('tone', 'poetic'),
                    'max_mech': options.get('max_mech', 3)
                },
                concept_seed=options.get('seed'),
                enable_relativity=options.get('relativity', True)
            )
        else:
            # Use legacy forge
            forge = AxiomForgeHybrid()
            results = forge.generate(
                seed=options.get('seed'),
                ontology_name=options.get('ontology'),
                ptype=options.get('paradox_type'),
                count=int(options.get('count', 1)),
                tone=options.get('tone', 'poetic'),
                max_mech=int(options.get('max_mech', 3))
            )

        output = options.get('output', 'text')

        if output == 'json':
            return json.dumps(results, indent=2)
        else:
            output_text = ""
            for i, axiom in enumerate(results, 1):
                output_text += f"=== Axiom {i} ===\n"
                output_text += f"{axiom['axiom_text']}\n\n"
                if axiom['ontology'].get('is_new'):
                    output_text += f"[NEW ONTOLOGY: {axiom['ontology']['name']}]\n"
                if axiom.get('seed_context'):
                    output_text += f"[Seed-influenced generation]\n"
                if axiom.get('meta_ontology', {}).get('curvature_data'):
                    output_text += f"[Relativistic framework]\n"
                output_text += "\n"
            return output_text

    except Exception as e:
        return f"Error generating paradoxes: {str(e)}\n\nPlease check your parameters."

# ============================================================================
# FILE OUTPUT FUNCTIONS (FIXED VERSION)
# ============================================================================

def convert_to_serializable(obj: Any) -> Any:
    """Convert non-serializable objects to serializable ones."""
    if isinstance(obj, OntologyCoordinates):
        return obj.to_tuple()
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_to_serializable(item) for item in obj)
    elif hasattr(obj, '__dict__'):
        # Try to convert dataclass or other objects with __dict__
        try:
            return {k: convert_to_serializable(v) for k, v in obj.__dict__.items()}
        except:
            return str(obj)
    else:
        return obj

def write_output_files(results: List[Dict[str, Any]], output_format: str, base_filename: str = "axioms", is_trajectory: bool = False):
    """Write results to files in /output/ directory"""
    # Create output directory if it doesn't exist
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)

    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Convert results to serializable format
    serializable_results = convert_to_serializable(results)

    if output_format == "json" or output_format == "both":
        json_filename = output_dir / f"{base_filename}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON output written to: {json_filename}")

    if output_format == "text" or output_format == "both":
        text_filename = output_dir / f"{base_filename}_{timestamp}.txt"
        with open(text_filename, 'w', encoding='utf-8') as f:
            if is_trajectory:
                # Write trajectory data
                f.write("Ontological Phase Space Exploration Trajectory\n")
                f.write("=" * 60 + "\n\n")

                for step in results:
                    f.write(f"Step {step['step']:3d}:\n")
                    f.write(f"  Coordinates: {step['coordinates']}\n")
                    f.write(f"  Framework: {step['framework']}\n")
                    f.write(f"  Axiom: {step['axiom']}\n")
                    if step.get('is_sophia'):
                        f.write("  ✨ SOPHIA POINT (phase transition)\n")
                    if step.get('seed_guided'):
                        f.write("  📝 Seed-guided step\n")
                    if step.get('relativistic'):
                        f.write(f"  📐 Ricci scalar: {step.get('curvature', 0):.3f}\n")
                    f.write(f"  Coherence: {step.get('coherence', 0):.3f}\n")
                    f.write(f"  Distance to golden ratio: {step.get('distance_to_golden', 0):.3f}\n")
                    f.write("\n")

                # Add summary
                sophia_points = sum(1 for step in results if step.get('is_sophia', False))
                avg_coherence = np.mean([step.get('coherence', 0) for step in results])
                avg_curvature = np.mean([step.get('curvature', 0) for step in results])
                seed_guided = sum(1 for step in results if step.get('seed_guided', False))
                relativistic = sum(1 for step in results if step.get('relativistic', False))

                f.write("\n" + "=" * 60 + "\n")
                f.write(f"Exploration Summary:\n")
                f.write(f"  Total steps: {len(results)}\n")
                f.write(f"  Sophia points: {sophia_points}\n")
                f.write(f"  Average coherence: {avg_coherence:.3f}\n")
                if relativistic > 0:
                    f.write(f"  Average curvature: {avg_curvature:.3f}\n")
                f.write(f"  Seed-guided steps: {seed_guided}\n")
                f.write(f"  Relativistic steps: {relativistic}\n")
            else:
                # Write axiom data
                for i, axiom in enumerate(results, 1):
                    f.write(f"=== Axiom {i} ===\n")

                    # Get axiom text - handle both structures
                    if 'axiom_text' in axiom:
                        axiom_text = axiom['axiom_text']
                    elif 'axiom' in axiom:
                        axiom_text = axiom['axiom']
                    else:
                        axiom_text = str(axiom)

                    f.write(f"{axiom_text}\n\n")

                    # Add metadata if available
                    if isinstance(axiom, dict):
                        ontology = axiom.get('ontology', {})
                        if isinstance(ontology, dict) and ontology.get('is_new'):
                            f.write(f"[NEW ONTOLOGY: {ontology.get('name', 'Unknown')}]\n")
                        if axiom.get('seed_context'):
                            f.write(f"[Seed-influenced generation]\n")
                        if axiom.get('meta_ontology', {}).get('curvature_data'):
                            f.write(f"[Relativistic framework]\n")

                        # Add metrics if available
                        if 'metrics' in axiom:
                            f.write(f"\n📊 Metrics:\n")
                            metrics = axiom['metrics']
                            if isinstance(metrics, dict):
                                for key, value in list(metrics.items())[:5]:
                                    f.write(f"  {key}: {value}\n")

                        # Add meta-ontology info if available
                        if 'meta_ontology' in axiom:
                            meta = axiom['meta_ontology']
                            if isinstance(meta, dict):
                                f.write(f"\n🎭 Meta-Ontology:\n")
                                if meta.get('phase_transition'):
                                    f.write(f"  Phase transition detected!\n")
                                if meta.get('sophia_point'):
                                    f.write(f"  ✨ Golden ratio Sophia point!\n")
                                if 'coordinates' in meta:
                                    f.write(f"  Coordinates: {meta.get('coordinates', 'N/A')}\n")
                                if meta.get('curvature_data'):
                                    f.write(f"  Ricci scalar: {meta['curvature_data'].get('ricci_scalar', 'N/A')}\n")

                    f.write("\n" + "="*40 + "\n\n")

        print(f"✅ Text output written to: {text_filename}")

# ============================================================================
# COMMAND LINE INTERFACE v3.0
# ============================================================================

def main():
    """Enhanced CLI with meta-ontology capabilities and relativistic enhancements"""
    parser = argparse.ArgumentParser(
        description="META-AXIOMFORGE v3.0 - Enhanced Framework Integration",
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
  %(prog)s --mode hybrid --outputfile both --output json
  %(prog)s --simulate semantic_gravity --steps 100
  %(prog)s --geodesic 0.5,0.5,0.5,0.5,0.5 0.9,0.8,0.95,0.4,0.85
  %(prog)s --no-relativity --mode meta --count 2
        """
    )

    parser.add_argument('--mode',
                       choices=['meta', 'legacy', 'hybrid', 'explore'],
                       default='hybrid',
                       help='Generation mode (default: hybrid)')

    parser.add_argument('--count', type=int, default=1,
                       help='Number of axioms to generate')

    parser.add_argument('--quadrant',
                       choices=['semantic_gravity', 'autopoietic', 'thermodynamic',
                               'fractal', 'causal', 'random'],
                       default='random',
                       help='Target ontological quadrant')

    parser.add_argument('--explore', action='store_true',
                       help='Perform phase space exploration')

    parser.add_argument('--steps', type=int, default=50,
                       help='Steps for phase space exploration')

    parser.add_argument('--simulate', type=str,
                       help='Simulate framework evolution (framework name)')

    parser.add_argument('--simulate-steps', type=int, default=100,
                       help='Steps for framework simulation')

    parser.add_argument('--geodesic', nargs=2, type=str,
                       help='Explore geodesic between two coordinate sets (format: "0.5,0.5,0.5,0.5,0.5 0.9,0.8,0.95,0.4,0.85")')

    parser.add_argument('--geodesic-steps', type=int, default=20,
                       help='Steps for geodesic exploration')

    parser.add_argument('--ontology',
                       choices=['alien', 'counter', 'bridge', 'meta'],
                       help='Legacy ontology (for legacy mode)')

    parser.add_argument('--paradox-type',
                       choices=['entropic', 'temporal', 'cosmic', 'metaphysical',
                               'linguistic', 'Causal Loop', 'Relativistic', 'random'],
                       default='random',
                       help='Paradox type (for legacy mode)')

    parser.add_argument('--output', choices=['json', 'text', 'both'],
                       default='text',
                       help='Console output format')

    parser.add_argument('--outputfile', choices=['json', 'text', 'both'],
                       help='File output format (writes to /output/ directory)')

    parser.add_argument('--filename', type=str, default='axioms',
                       help='Base filename for output files (default: axioms)')

    parser.add_argument('--seed', type=str,
                       help='Text seed for controlled axiom generation (e.g., "quantum consciousness")')

    parser.add_argument('--numeric-seed', type=int,
                       help='Numeric seed for reproducibility (alternative to text seed)')

    parser.add_argument('--tone',
                       choices=['poetic', 'plain', 'academic', 'oracular'],
                       default='poetic',
                       help='Tone for axiom generation')

    parser.add_argument('--max-mech', type=int, default=3,
                       help='Maximum number of mechanisms (for legacy mode)')

    parser.add_argument('--simple', action='store_true',
                       help='Simple output format (web compatible)')

    parser.add_argument('--analyze-seed', action='store_true',
                       help='Analyze seed text without generating axioms')

    parser.add_argument('--framework-summary', type=str,
                       help='Get detailed summary of a framework')

    parser.add_argument('--ricci-flow', type=str,
                       help='Compute Ricci flow for coordinates (format: "0.5,0.5,0.5,0.5,0.5")')

    parser.add_argument('--ricci-iterations', type=int, default=10,
                       help='Iterations for Ricci flow computation')

    parser.add_argument('--no-relativity', action='store_true',
                       help='Disable relativistic enhancements')

    args = parser.parse_args()

    # Set random seed - prioritize numeric seed, then text seed hash
    if args.numeric_seed:
        random.seed(args.numeric_seed)
        np.random.seed(args.numeric_seed)
        print(f"🔢 Using numeric seed: {args.numeric_seed}")
    elif args.seed:
        # Use hash of text seed
        seed_hash = int(hashlib.sha256(args.seed.encode()).hexdigest()[:8], 16)
        random.seed(seed_hash)
        np.random.seed(seed_hash % (2**32))
        print(f"📝 Using text seed: '{args.seed}' (hash: {seed_hash})")

    # Banner
    print("="*70)
    print("META-AXIOMFORGE v3.0 - Enhanced Framework Integration")
    print("Beyond-God Tier Meta-Ontology Generator with Relativistic Enhancements")
    print("="*70)

    # Initialize forge
    forge = MetaAxiomForge()

    # Analyze seed if requested
    if args.analyze_seed and args.seed:
        print(f"\n🔍 Analyzing seed text: '{args.seed}'")
        print("-"*70)

        processor = TextSeedProcessor()
        analysis = processor.process_text_seed(args.seed)

        print(f"Semantic Features:")
        for key, value in analysis["semantic_features"].items():
            print(f"  {key}: {value:.3f}")

        print(f"\nKey Concepts: {', '.join(analysis['key_concepts'])}")
        print(f"Preferred Framework: {analysis['preferred_framework'].replace('_', ' ').title()}")
        print(f"Suggested Tone: {analysis['suggested_tone']}")
        print(f"Target Coordinates: {analysis['target_coordinates'].to_tuple()}")
        print(f"Complex Seed: {'Yes' if analysis['is_complex'] else 'No'}")

        if not (args.explore or args.mode == "explore" or args.simulate or args.geodesic or args.framework_summary or args.ricci_flow):
            return

    # Framework summary
    if args.framework_summary:
        print(f"\n📚 Framework Summary: {args.framework_summary}")
        print("-"*70)

        summary = forge.get_framework_summary(args.framework_summary)

        print(f"Name: {summary['name']}")
        print(f"Coordinates: {summary['coordinates']}")
        print(f"Region: {summary['region']}")
        print(f"Core Pattern: {summary['core_pattern']}")
        print(f"Mechanisms: {summary['mechanism_count']}")
        print(f"Equations: {summary['equation_count']}")
        print(f"Golden Alignment: {summary['golden_alignment']:.3f}")
        print(f"Sophia Point: {'Yes' if summary['is_sophia_point'] else 'No'}")
        print(f"Relativistic: {summary['relativistic_structure']}")

        print(f"\n📊 Signature Metrics:")
        for key, value in summary['metrics'].items():
            print(f"  {key}: {value}")

        if summary.get('seed_keywords'):
            print(f"\n🔑 Seed Keywords: {', '.join(summary['seed_keywords'][:5])}")

        return

    # Ricci flow computation
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

            # Compute curvature
            curvature = forge.field_simulator.compute_curvature_tensor(coords)
            print(f"\n📐 Initial Curvature:")
            for key, value in curvature.items():
                if key in ['ricci_scalar', 'curvature_invariant']:
                    print(f"  {key}: {value:.3f}")

            return
        except ValueError:
            print("Error: Invalid coordinate format. Use: 0.5,0.5,0.5,0.5,0.5")
            return

    # Framework simulation
    if args.simulate:
        print(f"\n🧪 Simulating framework evolution: {args.simulate}")
        print("-"*70)

        simulation = forge.simulate_framework_evolution(args.simulate, args.simulate_steps)

        print(f"Framework: {simulation['framework']}")
        print(f"Final State:")
        for key, value in simulation['final_state'].items():
            print(f"  {key}: {value:.3f}")
        print(f"Stabilized: {'Yes' if simulation['stabilized'] else 'No'}")
        print(f"Attractor Type: {simulation['attractor_type']}")

        if args.outputfile:
            write_output_files([simulation], args.outputfile, f"{args.simulate}_simulation")

        return

    # Geodesic exploration
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
            print(f"Total frameworks visited: {len(set(step['framework'] for step in trajectory))}")

            if args.outputfile:
                write_output_files(trajectory, args.outputfile, f"geodesic_{args.geodesic_steps}", is_trajectory=True)

            if args.output in ['json', 'both']:
                print(json.dumps(trajectory, indent=2))

            if args.output in ['text', 'both'] and not args.simple:
                print("\nGeodesic Trajectory (first 10 steps):")
                for step in trajectory[:10]:
                    print(f"Step {step['step']:2d}: {step['axiom'][:50]}... ({step['framework']})")

            return
        except ValueError:
            print("Error: Invalid coordinate format. Use: 0.5,0.5,0.5,0.5,0.5 0.9,0.8,0.95,0.4,0.85")
            return

    # Execute based on mode
    if args.explore or args.mode == "explore":
        print(f"\n🌌 Exploring ontological phase space ({args.steps} steps)...")
        if args.seed:
            print(f"   Guided by seed: '{args.seed}'")
        if not args.no_relativity:
            print(f"   With relativistic enhancements")
        print("-"*70)

        trajectory = forge.explore_phase_space(
            steps=args.steps,
            seed_text=args.seed,
            enable_relativity=not args.no_relativity
        )

        if args.outputfile:
            write_output_files(trajectory, args.outputfile, f"{args.filename}_trajectory", is_trajectory=True)

        if args.output in ['json', 'both']:
            print(json.dumps(trajectory, indent=2))

        if args.output in ['text', 'both']:
            print("\nPhase Space Exploration Trajectory:")
            print("-"*40)
            for step in trajectory[:10]:  # Show first 10 steps
                print(f"Step {step['step']:3d}: {step['axiom'][:60]}...")
                print(f"       Framework: {step['framework']}")
                if step['is_sophia']:
                    print("       ✨ SOPHIA POINT (phase transition)")
                if step.get('seed_guided'):
                    print("       📝 Seed-guided step")
                if step.get('relativistic'):
                    print(f"       📐 Curvature: {step.get('curvature', 0):.3f}")
                print()

            # Summary
            sophia_points = sum(1 for step in trajectory if step['is_sophia'])
            avg_coherence = np.mean([step['coherence'] for step in trajectory])
            seed_guided = sum(1 for step in trajectory if step.get('seed_guided', False))
            relativistic = sum(1 for step in trajectory if step.get('relativistic', False))

            print(f"\n📊 Exploration Summary:")
            print(f"   Sophia points discovered: {sophia_points}/{args.steps}")
            print(f"   Average coherence: {avg_coherence:.3f}")
            if args.seed:
                print(f"   Seed-guided steps: {seed_guided}/{args.steps}")
            if relativistic > 0:
                print(f"   Relativistic steps: {relativistic}/{args.steps}")

    else:
        # Generate axioms
        print(f"\n🔮 Generating {args.count} axiom(s) in {args.mode} mode...")
        if args.quadrant != 'random':
            print(f"   Target quadrant: {args.quadrant}")
        if args.seed:
            print(f"   Using seed: '{args.seed}'")
        if not args.no_relativity:
            print(f"   With relativistic enhancements")
        print("-"*70)

        # Prepare parameters
        target_quadrant = None if args.quadrant == 'random' else args.quadrant
        legacy_params = None

        if args.mode == 'legacy':
            legacy_params = {
                "ontology": args.ontology or random.choice(["alien", "counter", "bridge", "meta"]),
                "paradox_type": args.paradox_type if args.paradox_type != 'random' else None,
                "tone": args.tone,
                "max_mech": args.max_mech
            }

        # Get concept seed from environment if available
        concept_seed = os.environ.get('CONCEPT_SEED')
        if not args.seed and concept_seed:
            args.seed = concept_seed

        # Generate
        results = forge.generate(
            mode=args.mode,
            count=args.count,
            target_quadrant=target_quadrant,
            legacy_params=legacy_params,
            concept_seed=args.seed,
            enable_relativity=not args.no_relativity
        )

        # Write to files if requested
        if args.outputfile:
            write_output_files(results, args.outputfile, args.filename)

        # Output to console
        if args.simple:
            # Simple output for web interface
            if args.output == 'json':
                print(json.dumps(results, indent=2))
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
            print(json.dumps(results, indent=2))

        if args.output in ['text', 'both'] and not args.simple:
            for i, axiom in enumerate(results, 1):
                print(f"\n✨ AXIOM #{i}")
                print("-"*40)
                print(axiom["axiom_text"])

                # Highlight new ontologies
                if axiom["ontology"]["is_new"]:
                    print(f"\n📐 BRAND NEW ONTOLOGY FRAMEWORK:")
                    print(f"   Name: {axiom['ontology']['name']}")
                    print(f"   Type: {axiom['ontology']['type']}")

                    if axiom.get("meta_ontology"):
                        meta = axiom["meta_ontology"]
                        print(f"   Coordinates: {meta.get('coordinates', 'N/A')}")

                        if meta.get("phase_transition"):
                            print("   🎭 PHASE TRANSITION DETECTED!")
                        if meta.get("sophia_point"):
                            print("   ✨ GOLDEN RATIO SOPHIA POINT!")
                        if meta.get("curvature_data"):
                            print(f"   📐 Ricci scalar: {meta['curvature_data'].get('ricci_scalar', 'N/A')}")

                # Show seed influence
                if axiom.get("seed_context"):
                    print(f"\n📝 SEED INFLUENCE: {axiom['seed_concept']}")
                    metrics = axiom.get("metrics", {})
                    if "seed_influence" in metrics:
                        print(f"   Seed influence score: {metrics['seed_influence']}")

                # Show key metrics
                print(f"\n📊 Key Metrics:")
                metrics = axiom.get("metrics", {})
                for key, value in list(metrics.items())[:5]:
                    print(f"   {key}: {value}")

                # Show insights
                insights = axiom.get("insights", [])
                if insights:
                    print(f"\n💡 Insights: {', '.join(insights)}")

        # Show statistics
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

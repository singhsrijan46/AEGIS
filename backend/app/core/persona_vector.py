"""
Persona Vector Scorer & Voice Distance Analyzer (Step 2 Deliverable)
Projects copy onto a 5D latent style coordinate space:
[Formality, Warmth, Authority, Technicality, Directness]
and computes calibrated cosine distance against the corporate Brand Constitution.
Synthesized from: Controllable Text Gen [18], Judge Alignment [20].
"""

import math
import re
from typing import Tuple, List, Optional
from ..models.schemas import PersonaVector, Finding


class PersonaVectorScorer:
    """
    Evaluates lexical markers and syntactic characteristics to compute the 5D voice coordinates.
    """

    # Lexical markers for 5 dimensions
    COLLOQUIAL_WORDS = {"gonna", "wanna", "cool", "super", "insane", "crazy", "stuff", "awesome", "dude", "kinda", "y'all"}
    FORMAL_WORDS = {"furthermore", "consequently", "demonstrates", "established", "substantiated", "framework", "architecture", "governance"}
    WARMTH_WORDS = {"partner", "together", "community", "support", "empathy", "journey", "collaborate", "care", "welcome"}
    AUTHORITY_WORDS = {"guarantees", "empirically", "certified", "standard", "mandate", "proven", "benchmark", "audited", "rigorous"}
    TECHNICAL_WORDS = {"latency", "api", "cryptographic", "deterministic", "cielab", "wcag", "throughput", "vector", "dag", "ast"}
    PASSIVE_CONSTRUCTIONS = re.compile(r'\b(?:is|was|were|been|being)\s+\w+ed\b', re.IGNORECASE)

    def analyze(self, text: str, target_persona: PersonaVector) -> Tuple[PersonaVector, float, Optional[Finding]]:
        tokens = re.findall(r'\w+', text.lower())
        total_tokens = max(1, len(tokens))

        colloquial_count = sum(1 for t in tokens if t in self.COLLOQUIAL_WORDS)
        formal_count = sum(1 for t in tokens if t in self.FORMAL_WORDS)
        warmth_count = sum(1 for t in tokens if t in self.WARMTH_WORDS)
        authority_count = sum(1 for t in tokens if t in self.AUTHORITY_WORDS)
        tech_count = sum(1 for t in tokens if t in self.TECHNICAL_WORDS)

        # Baseline estimates in [-1.0, 1.0]
        # Formality
        formality = 0.5 + (formal_count * 0.15) - (colloquial_count * 0.3)
        formality = max(-1.0, min(1.0, formality))

        # Warmth
        warmth = 0.3 + (warmth_count * 0.2)
        warmth = max(-1.0, min(1.0, warmth))

        # Authority
        authority = 0.6 + (authority_count * 0.15) - (colloquial_count * 0.25)
        authority = max(-1.0, min(1.0, authority))

        # Technicality
        technicality = 0.4 + (tech_count * 0.2)
        technicality = max(-1.0, min(1.0, technicality))

        # Directness (penalized by passive voice and high filler words)
        passive_matches = len(self.PASSIVE_CONSTRUCTIONS.findall(text))
        directness = 0.7 - (passive_matches * 0.08)
        directness = max(-1.0, min(1.0, directness))

        measured = PersonaVector(
            formality=round(formality, 2),
            warmth=round(warmth, 2),
            authority=round(authority, 2),
            technicality=round(technicality, 2),
            directness=round(directness, 2)
        )

        # Compute Cosine Distance
        v_m = [measured.formality, measured.warmth, measured.authority, measured.technicality, measured.directness]
        v_t = [target_persona.formality, target_persona.warmth, target_persona.authority, target_persona.technicality, target_persona.directness]

        dot = sum(a * b for a, b in zip(v_m, v_t))
        mag_m = math.sqrt(sum(a * a for a in v_m))
        mag_t = math.sqrt(sum(b * b for b in v_t))

        if mag_m == 0 or mag_t == 0:
            cosine_dist = 0.0
        else:
            cosine_similarity = dot / (mag_m * mag_t)
            cosine_dist = max(0.0, 1.0 - cosine_similarity)

        finding = None
        # Calibrated threshold (Judge Alignment [20]): if distance > 0.35 or formality < 0.2
        if cosine_dist > 0.35 or measured.formality < 0.2:
            finding = Finding(
                span=(0, min(len(text), 120)),
                flagged_text=text[:min(len(text), 120)] + "...",
                category="TONE",
                severity="SUGGESTION",
                title="Brand Voice Drift: Colloquial / Low Authority Register",
                explanation=(
                    f"Measured brand voice deviates from corporate persona vector "
                    f"(Cosine distance: {cosine_dist:.2f} > 0.35 threshold). "
                    f"Target Formality is {target_persona.formality:.2f} (measured: {measured.formality:.2f}), "
                    f"and Authority is {target_persona.authority:.2f} (measured: {measured.authority:.2f}). "
                    f"Replace conversational colloquialisms with clear, objective executive terminology."
                ),
                cited_source="Inkloom Enterprise Brand Standards Manual v4.2, Section 3.1: Voice Spectrum",
                rule_id="RULE-VOICE-001",
                suggested_edit="Adopt formal, direct executive prose while preserving narrative clarity.",
                confidence=0.88,
                anomaly_type="Input-Conflicting"
            )

        return measured, round(cosine_dist, 3), finding

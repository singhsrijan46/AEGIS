"""
Brand Vault Compiler & Brand Constitution (Step 1 Deliverable)
Translates unstructured brand guidelines into structured JSON rule trees,
hierarchical micro-rule DAGs, design tokens, and the 5D target persona vector.
Synthesized from: Constitutional AI [9], Controllable Text Gen [18], Judge Alignment [20].
"""

from typing import List, Dict, Any, Optional
from ..models.schemas import BrandRule, PersonaVector


class BrandVault:
    def __init__(self):
        # Target 5D Persona Vector (Constitutional AI [9] & Controllable Gen [18])
        self.target_persona = PersonaVector(
            formality=0.65,
            warmth=0.40,
            authority=0.85,
            technicality=0.60,
            directness=0.75
        )

        # Official Color Swatches (CIELAB matching target)
        self.official_palette = {
            "PRIMARY_TEAL": "#00A896",
            "NAVY_DARK": "#0F2537",
            "DEEP_BACKGROUND": "#070D18",
            "ACCENT_BLUE": "#2563EB",
            "EMERALD_GREEN": "#10B981",
            "AMBER_WARNING": "#F59E0B",
            "CRIMSON_BLOCKER": "#DC2626",
            "NEUTRAL_LIGHT": "#F8FAFC",
            "CARD_BORDER": "#E2E8F0"
        }

        # Logo Geometric Constraints
        self.logo_constraints = {
            "min_clear_space_multiplier": 0.5,  # 0.5 * Height of logo
            "allowed_aspect_ratio": 3.2,        # Width / Height = 3.2 (+/- 5%)
            "max_aspect_ratio_drift": 0.05
        }

        # Banned & Discouraged Lexicon Mapping (Vale AST Engine)
        self.prohibited_lexicon = {
            "cheap": {
                "replacement": "cost-effective",
                "severity": "WARNING",
                "rationale": "Devalues enterprise positioning. Use 'cost-effective' or 'capital-efficient'."
            },
            "dirt cheap": {
                "replacement": "high ROI",
                "severity": "BLOCKER",
                "rationale": "Colloquial terminology forbidden in public enterprise documentation."
            },
            "simple": {
                "replacement": "intuitive",
                "severity": "SUGGESTION",
                "rationale": "Can imply lack of advanced capabilities. Prefer 'intuitive' or 'frictionless'."
            },
            "rockstar": {
                "replacement": "seasoned specialist",
                "severity": "WARNING",
                "rationale": "Unprofessional tech slang prohibited by corporate communication policy."
            },
            "ninja": {
                "replacement": "domain expert",
                "severity": "WARNING",
                "rationale": "Clichéd informal jargon prohibited in B2B copy."
            },
            "game changer": {
                "replacement": "paradigm-shifting innovation",
                "severity": "SUGGESTION",
                "rationale": "Overused promotional cliché. Quantify technical benefit instead."
            },
            "guaranteed 10x roi": {
                "replacement": "empirically validated ROI boost",
                "severity": "BLOCKER",
                "rationale": "Violates FTC Act § 5 and SEC Rule 206(4)-1. Unqualified performance guarantees carry legal exposure."
            },
            "the only": {
                "replacement": "a leading enterprise",
                "severity": "BLOCKER",
                "rationale": "Unsubstantiated absolute superlative. Prohibited unless supported by third-party analyst audit."
            },
            "#1 in the industry": {
                "replacement": "Gartner-recognized leader",
                "severity": "BLOCKER",
                "rationale": "Unqualified superlative requires official analyst citation and temporal stamp."
            }
        }

        # Mandatory Trademarks on First Mention
        self.trademark_registry = {
            "AEGIS-Brand": "AEGIS-Brand™",
            "AEGIS": "AEGIS™",
            "Inkloom Verity": "AEGIS-Brand™",
            "VeriBrand AI": "AEGIS-Brand™",
            "E-AFV": "E-AFV™"
        }

        # Hierarchical Directed Acyclic Graph (DAG) of Micro-Rules
        self.rules: List[BrandRule] = self._compile_default_rules()

    def _compile_default_rules(self) -> List[BrandRule]:
        return [
            BrandRule(
                id="RULE-LEX-001",
                category="LEXICAL",
                name="Banned Colloquial & Devaluing Vocabulary",
                description="Flags words like 'cheap', 'ninja', 'rockstar' that erode defense-grade brand stature.",
                severity="WARNING",
                source_document="AEGIS-Brand™ Global Governance & Defense Standard v4.0",
                section="Section 2.4: Approved Executive Vocabulary",
                page=18,
                rule_type="regex",
                active=True
            ),
            BrandRule(
                id="RULE-LEX-002",
                category="LEXICAL",
                name="Mandatory Trademark Placement on First Mention",
                description="AEGIS-Brand and associated product marks must carry the ™ symbol on their first occurrence.",
                severity="WARNING",
                source_document="AEGIS IP & Global Trademark Register 2026",
                section="Section 1.1: Trademark Disclosures",
                page=4,
                rule_type="regex",
                active=True
            ),
            BrandRule(
                id="RULE-VOICE-001",
                category="TONE",
                name="5D Persona Coordinate Compliance",
                description="Draft tone must align with target persona (Formality >= 0.6, Authority >= 0.8).",
                severity="SUGGESTION",
                source_document="AEGIS-Brand™ Global Governance & Defense Standard v4.0",
                section="Section 3.1: Voice Spectrum & Archetypes",
                page=27,
                rule_type="vector",
                active=True
            ),
            BrandRule(
                id="RULE-FACT-001",
                category="FACT",
                name="Enterprise Single Source of Truth (SSOT) Alignment",
                description="All quantitative claims, uptime metrics, pricing, and certifications must match active SSOT records.",
                severity="BLOCKER",
                source_document="Enterprise Master Product & SLA Register Q4 2026",
                section="Section 4: Technical Specifications & SLA Commitments",
                page=42,
                rule_type="kg_fact",
                active=True
            ),
            BrandRule(
                id="RULE-FACT-002",
                category="FACT",
                name="Temporal Validity & Expiration Safeguard",
                description="Prevents quoting expired statistics, deprecated pricing plans, or obsolete SLA guarantees.",
                severity="BLOCKER",
                source_document="Enterprise Master Product & SLA Register Q4 2026",
                section="Section 5.2: Deprecation Schedules",
                page=45,
                rule_type="kg_fact",
                active=True
            ),
            BrandRule(
                id="RULE-REG-001",
                category="REGULATORY",
                name="FTC & SEC Superlative Substantiation",
                description="Claims of '#1', 'only', or 'guaranteed returns' are prohibited without verified audit disclaimers.",
                severity="BLOCKER",
                source_document="Corporate Legal Compliance Handbook",
                section="Section 7: Regulatory Promotional Guardrails (FTC § 5)",
                page=88,
                rule_type="regex",
                active=True
            ),
            BrandRule(
                id="RULE-VIS-001",
                category="VISUAL",
                name="CIELAB Colorimetric Tolerance (ΔE00 < 2.0)",
                description="Asset colors must not deviate by more than 2.0 ΔE from official corporate palette.",
                severity="WARNING",
                source_document="AEGIS Design System & Token Specifications",
                section="Section 1.2: Brand Color Tokens & Print Tolerances",
                page=8,
                rule_type="wcag",
                active=True
            ),
            BrandRule(
                id="RULE-VIS-002",
                category="VISUAL",
                name="WCAG 2.1 AA/AAA Contrast Enforcement",
                description="Text-over-background must achieve at least 4.5:1 contrast for normal text and 3.0:1 for headers.",
                severity="BLOCKER",
                source_document="Digital Accessibility Guidelines (ADA Title III & WCAG 2.1)",
                section="Section 2: Color Contrast Ratios",
                page=12,
                rule_type="wcag",
                active=True
            ),
            BrandRule(
                id="RULE-VIS-003",
                category="VISUAL",
                name="Logo Exclusion Safe-Zone Buffer (0.5H)",
                description="No graphic elements, lines, or text may encroach within 0.5 times the logo height.",
                severity="WARNING",
                source_document="AEGIS-Brand™ Global Governance & Defense Standard v4.0",
                section="Section 1.5: Logo Protection Clear Space",
                page=15,
                rule_type="logo_box",
                active=True
            )
        ]

    def get_all_rules(self) -> List[BrandRule]:
        return self.rules

    def get_rule_by_id(self, rule_id: str) -> Optional[BrandRule]:
        for r in self.rules:
            if r.id == rule_id:
                return r
        return None

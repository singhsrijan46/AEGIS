"""
Unified Brand Governance Engine (Master Pipeline Orchestrator)
Integrates all 6 verification subsystems across the 20-paper composite architecture:
1. Brand Vault & Temporal Knowledge Graph SSOT
2. Deterministic Vale AST Linter
3. E-AFV Atomic Fact Decomposition & Decoupled CoVe Questioning
4. FacTool Python Calculator & RAGAS Quality Gate
5. Persona Vector 5D Cosine Distance
6. OpenCV CIELAB ΔE00 & WCAG 2.1 Visual Auditor
7. MPED Intent-Preserving Rewriter & Cryptographic SHA-256 Ledger
"""

from typing import List, Dict, Any, Optional
from ..models.schemas import (
    Finding,
    VisualFinding,
    DocumentAuditRequest,
    DocumentAuditResponse,
    AuditSummary,
    PersonaVector
)
from .brand_vault import BrandVault
from .temporal_kg import TemporalKnowledgeGraph
from .hybrid_retriever import AirGappedHybridRetriever
from .presidio_privacy import PrivacyGateway
from .vale_linter import ValeLinter
from .fact_decomposer import AtomicFactDecomposer
from .fact_calculator import DeterministicFactCalculator
from .ragas_evaluator import RagasClaimEvaluator
from .persona_vector import PersonaVectorScorer
from .vision_wcag import MultimodalVisualAuditor
from .mped_rewriter import MinimalPerturbationRewriter
from .triage_router import RiskTriageRouter
from .audit_ledger import CryptographicAuditLedger


class UnifiedBrandGovernanceEngine:
    def __init__(self):
        self.vault = BrandVault()
        self.kg = TemporalKnowledgeGraph()
        self.retriever = AirGappedHybridRetriever()
        self.privacy = PrivacyGateway()
        self.linter = ValeLinter(self.vault)
        self.decomposer = AtomicFactDecomposer()
        self.calculator = DeterministicFactCalculator()
        self.ragas = RagasClaimEvaluator(self.kg, self.retriever)
        self.persona_scorer = PersonaVectorScorer()
        self.vision_auditor = MultimodalVisualAuditor(self.vault.official_palette, self.vault.logo_constraints)
        self.rewriter = MinimalPerturbationRewriter()
        self.triage = RiskTriageRouter()
        self.ledger = CryptographicAuditLedger()

    def audit_document(self, request: DocumentAuditRequest) -> DocumentAuditResponse:
        raw_text = request.text
        findings: List[Finding] = []
        visual_findings: List[VisualFinding] = []

        # -------------------------------------------------------------
        # STAGE 1: AIR-GAPPED PRIVACY & PII SANITIZATION PRE-CHECK
        # -------------------------------------------------------------
        sanitized_text, pii_count = self.privacy.sanitize(raw_text)

        # -------------------------------------------------------------
        # STAGE 2: DETERMINISTIC PROSE & LEXICON LINTING (Vale AST)
        # -------------------------------------------------------------
        vale_findings = self.linter.lint(raw_text)
        findings.extend(vale_findings)

        # -------------------------------------------------------------
        # STAGE 3: ATOMIC CLAIM EXTRACTION & FACT VERIFICATION (E-AFV, CoVe, FacTool, RAGAS)
        # -------------------------------------------------------------
        # 3a. Deterministic Math & Calculation check
        math_result = self.calculator.verify_math_in_text(raw_text)
        if math_result and not math_result.is_correct:
            # Find span of math claim
            import re
            m = self.calculator.PERCENT_CHANGE_REGEX.search(raw_text)
            span = m.span() if m else (0, len(raw_text))
            findings.append(Finding(
                span=span,
                flagged_text=raw_text[span[0]:span[1]],
                category="MATH",
                severity="BLOCKER",
                title=f"Statistical Arithmetic Discrepancy ({math_result.claimed_value} claimed vs {math_result.computed_value} actual)",
                explanation=(
                    f"Claimed growth of {math_result.claimed_value} is mathematically incorrect. "
                    f"Deterministic formula computes: {math_result.formula}. "
                    f"Publishing erroneous mathematical claims triggers deceptive marketing exposure under FTC § 5."
                ),
                cited_source="FacTool Deterministic Arithmetic Validator & Product Impact Brief",
                rule_id="RULE-FACT-001",
                suggested_edit=f"increased conversions by {math_result.computed_value}",
                confidence=1.0,
                anomaly_type="Fact-Conflicting",
                math_details={
                    "claimed": math_result.claimed_value,
                    "computed": math_result.computed_value,
                    "formula": math_result.formula,
                    "discrepancy": round(math_result.discrepancy_percent, 1)
                }
            ))

        # 3b. Atomic proposition extraction and RAGAS fact checking
        propositions = self.decomposer.decompose(raw_text)
        for prop in propositions:
            ragas_finding = self.ragas.evaluate_proposition(prop, raw_text)
            if ragas_finding:
                # Avoid duplicate spans if already flagged by math or vale
                if not any(f.span == ragas_finding.span for f in findings):
                    findings.append(ragas_finding)

        # -------------------------------------------------------------
        # STAGE 4: VOICE & TONE VECTOR DISTANCE (5D Coordinates)
        # -------------------------------------------------------------
        measured_persona, voice_distance, tone_finding = self.persona_scorer.analyze(raw_text, self.vault.target_persona)
        if tone_finding:
            findings.append(tone_finding)

        # -------------------------------------------------------------
        # STAGE 5: MULTIMODAL VISUAL & ACCESSIBILITY AUDITING
        # -------------------------------------------------------------
        for asset in request.images:
            asset_findings = self.vision_auditor.audit_asset(asset)
            visual_findings.extend(asset_findings)

        # -------------------------------------------------------------
        # STAGE 6: RISK TRIAGE, COMPLIANCE SCORING & CERTIFICATION
        # -------------------------------------------------------------
        summary: AuditSummary = self.triage.compute_triage(findings, visual_findings)

        # If Green Tier, automatically issue SHA-256 certificate
        if summary.tier == "GREEN":
            cert = self.ledger.issue_certificate(
                document_id=request.document_id,
                text=raw_text,
                score=summary.compliance_score,
                tier=summary.tier,
                status=summary.publishing_status
            )
            summary.cryptographic_token = cert.token

        return DocumentAuditResponse(
            document_id=request.document_id,
            title=request.title,
            summary=summary,
            findings=findings,
            visual_findings=visual_findings,
            scrubbed_pii_count=pii_count,
            persona_distance=voice_distance,
            measured_persona=measured_persona,
            target_persona=self.vault.target_persona
        )

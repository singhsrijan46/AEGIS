"""
Risk Triage & Tiered Approval Routing Engine (Step 5 Deliverable)
Evaluates findings to compute the composite Compliance Score (0-100)
and assigns drafts to Green, Amber, or Red Tier escalation queues.
"""

from typing import List, Dict, Any, Tuple
from ..models.schemas import Finding, VisualFinding, AuditSummary


class RiskTriageRouter:
    """
    Computes weighted compliance penalties:
    - BLOCKER: -25 points
    - WARNING: -10 points
    - SUGGESTION: -3 points
    """

    def compute_triage(self, findings: List[Finding], visual_findings: List[VisualFinding]) -> AuditSummary:
        blockers = sum(1 for f in findings if f.severity == "BLOCKER") + sum(1 for vf in visual_findings if vf.severity == "BLOCKER")
        warnings = sum(1 for f in findings if f.severity == "WARNING") + sum(1 for vf in visual_findings if vf.severity == "WARNING")
        suggestions = sum(1 for f in findings if f.severity == "SUGGESTION") + sum(1 for vf in visual_findings if vf.severity == "SUGGESTION")

        total = len(findings) + len(visual_findings)

        # Base score 100
        score = 100.0 - (blockers * 25.0) - (warnings * 10.0) - (suggestions * 3.0)
        score = max(0.0, min(100.0, round(score, 1)))

        # Tier assignment
        if blockers == 0 and score >= 90.0:
            tier = "GREEN"
            publishing_status = "AUTO_APPROVED"
        elif blockers == 0 and score >= 70.0:
            tier = "AMBER"
            publishing_status = "BRAND_REVIEW_REQUIRED"
        else:
            tier = "RED"
            publishing_status = "LEGAL_BLOCKED"

        return AuditSummary(
            total_findings=total,
            blockers=blockers,
            warnings=warnings,
            suggestions=suggestions,
            compliance_score=score,
            tier=tier,
            publishing_status=publishing_status
        )

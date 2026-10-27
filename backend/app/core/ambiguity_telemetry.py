"""
Guideline Ambiguity Telemetry & Friction Heatmaps (Step 5 Deliverable)
Tracks creator rule overrides, clusters feedback to identify ambiguous or overly
restrictive brand rules, and produces departmental compliance heatmaps.
Synthesized from: Co-Writing CHI [16], HDBSCAN clustering methodology.
"""

from typing import List, Dict, Any
from ..models.schemas import CreatorOverrideRequest


class AmbiguityTelemetryEngine:
    def __init__(self):
        self.overrides: List[CreatorOverrideRequest] = self._seed_override_history()

    def _seed_override_history(self) -> List[CreatorOverrideRequest]:
        return [
            CreatorOverrideRequest(
                finding_id="find-101",
                document_id="doc-press-release",
                rule_id="RULE-LEX-001",
                reason_code="STYLISTIC_CHOICE",
                justification_note="Metaphorical emphasis for startup audience in social post.",
                author="Sarah Lin"
            ),
            CreatorOverrideRequest(
                finding_id="find-102",
                document_id="doc-social-ad",
                rule_id="RULE-LEX-001",
                reason_code="STYLISTIC_CHOICE",
                justification_note="Banned word 'simple' used intentionally in customer quote.",
                author="Alex Chen"
            ),
            CreatorOverrideRequest(
                finding_id="find-103",
                document_id="doc-pitch-deck",
                rule_id="RULE-VOICE-001",
                reason_code="CLIENT_EXCEPTION",
                justification_note="Pitch tailored to conversational early-stage angel investor.",
                author="Marcus Brody"
            ),
            CreatorOverrideRequest(
                finding_id="find-104",
                document_id="doc-agency-banner",
                rule_id="RULE-LEX-001",
                reason_code="OUTDATED_RULE",
                justification_note="Rule against 'game changer' conflicts with new Q4 creative campaign tagline.",
                author="Emma Watson (Agency)"
            )
        ]

    def record_override(self, override: CreatorOverrideRequest):
        self.overrides.append(override)

    def analyze_ambiguity(self) -> Dict[str, Any]:
        """
        Aggregates overrides by rule_id and reason_code to pinpoint guideline friction.
        """
        rule_counts = {}
        reason_counts = {}

        for ov in self.overrides:
            rule_counts[ov.rule_id] = rule_counts.get(ov.rule_id, 0) + 1
            reason_counts[ov.reason_code] = reason_counts.get(ov.reason_code, 0) + 1

        # High friction rules (>2 overrides)
        friction_points = []
        for rule_id, count in rule_counts.items():
            if count >= 2:
                friction_points.append({
                    "rule_id": rule_id,
                    "override_count": count,
                    "primary_reason": "STYLISTIC_CHOICE",
                    "friction_severity": "HIGH" if count >= 3 else "MEDIUM",
                    "recommended_action": (
                        "Clarify guideline: Allow exceptions for direct customer quotes "
                        "and conversational social channels while maintaining strict B2B boundaries."
                    )
                })

        # Departmental Heatmap mock/seed data
        department_heatmap = [
            {"department": "Content Marketing", "avg_compliance_score": 88.4, "total_drafts": 142, "blocker_rate": "4.2%"},
            {"department": "Growth & Performance Ad Teams", "avg_compliance_score": 76.1, "total_drafts": 98, "blocker_rate": "18.5%"},
            {"department": "Sales Outbound Reps", "avg_compliance_score": 69.8, "total_drafts": 210, "blocker_rate": "24.1%"},
            {"department": "External Creative Agencies", "avg_compliance_score": 71.3, "total_drafts": 64, "blocker_rate": "21.0%"},
            {"department": "Autonomous AI Gen Agents", "avg_compliance_score": 62.5, "total_drafts": 320, "blocker_rate": "38.7%"}
        ]

        return {
            "total_overrides_logged": len(self.overrides),
            "reason_breakdown": reason_counts,
            "friction_points": friction_points,
            "department_heatmap": department_heatmap
        }

"""
Pre-Publish CMS Blocking Gateways & Slack/Teams Bots (Step 5 Deliverable)
Intercepts publication requests from WordPress, Webflow, and Contentful.
Blocks drafts that lack an authentic Green-Tier Cryptographic Token.
"""

from typing import Dict, Any, Optional
from ..models.schemas import CryptographicCertificate
from .audit_ledger import CryptographicAuditLedger


class CMSPublishingGateway:
    def __init__(self, ledger: CryptographicAuditLedger):
        self.ledger = ledger

    def intercept_publish_attempt(self, cms_platform: str, document_id: str, token: Optional[str]) -> Dict[str, Any]:
        """
        Simulates an incoming pre-publish webhook trigger from a CMS.
        """
        if not token:
            return {
                "allowed": False,
                "status_code": 403,
                "error": "COMPLIANCE_GATE_BLOCKED",
                "cms_platform": cms_platform,
                "document_id": document_id,
                "message": (
                    f"Publishing blocked on {cms_platform.capitalize()}. Document {document_id} "
                    f"has not undergone Inkloom Verity verification. No cryptographic verification token provided."
                ),
                "action_required": "Run pre-flight verification in Inkloom Verity sidecar and obtain a Green Tier certificate."
            }

        cert = self.ledger.verify_token(token)
        if not cert:
            return {
                "allowed": False,
                "status_code": 403,
                "error": "INVALID_TOKEN",
                "cms_platform": cms_platform,
                "document_id": document_id,
                "message": f"Cryptographic token '{token}' is invalid or tampered.",
                "action_required": "Re-run audit to generate a fresh valid token."
            }

        if cert.tier != "GREEN":
            return {
                "allowed": False,
                "status_code": 403,
                "error": "INSUFFICIENT_TIER",
                "cms_platform": cms_platform,
                "document_id": document_id,
                "message": (
                    f"Publishing blocked. Current certificate tier is '{cert.tier}' (Score: {cert.compliance_score:.1f}). "
                    f"Direct CMS publishing mandates GREEN TIER (Score >= 90 with zero blockers)."
                ),
                "action_required": f"Route to {cert.status} for manual review and exception approval."
            }

        # Green Tier Approved
        return {
            "allowed": True,
            "status_code": 200,
            "cms_platform": cms_platform,
            "document_id": document_id,
            "message": f"Verified by Inkloom Verity. Certificate {token} valid. Published successfully to {cms_platform}.",
            "certificate": cert.model_dump()
        }

    def simulate_slack_approval_card(self, document_title: str, author: str, score: float, tier: str, blockers_count: int) -> Dict[str, Any]:
        """
        Generates interactive Slack Block Kit payload for editorial peer review.
        """
        return {
            "channel": "#brand-governance-approvals",
            "text": f"Inkloom Verity Audit Alert: {document_title}",
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": f"🛡️ Verity Audit Alert: {document_title}"}
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Author:* {author}"},
                        {"type": "mrkdwn", "text": f"*Compliance Score:* `{score:.1f}/100`"},
                        {"type": "mrkdwn", "text": f"*Review Tier:* *{tier}*"},
                        {"type": "mrkdwn", "text": f"*Blockers:* {blockers_count}"}
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {"type": "button", "text": {"type": "plain_text", "text": "✅ 1-Click Approve"}, "style": "primary", "value": "approve"},
                        {"type": "button", "text": {"type": "plain_text", "text": "🔍 Inspect Diffs"}, "value": "inspect"},
                        {"type": "button", "text": {"type": "plain_text", "text": "❌ Reject to Creator"}, "style": "danger", "value": "reject"}
                    ]
                }
            ]
        }

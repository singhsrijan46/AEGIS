import pytest
from backend.app.core.engine import UnifiedBrandGovernanceEngine
from backend.app.core.cms_gateways import CMSPublishingGateway
from backend.app.models.schemas import DocumentAuditRequest, VisualAssetInput


def test_end_to_end_bad_draft_audit():
    engine = UnifiedBrandGovernanceEngine()
    cms = CMSPublishingGateway(engine.ledger)

    bad_draft = (
        "AEGIS-Brand is dirt cheap and provides guaranteed 10X ROI. "
        "It is the only FedRAMP High certified solution offering 99.999% uptime for $49/month. "
        "We increased conversions by 310% from 2.1% to 6.5%. "
        "Contact sales@aegis-defense.internal for Project Titan rollout."
    )

    request = DocumentAuditRequest(
        document_id="draft-001",
        title="Q4 Press Release",
        author="Growth Marketer",
        text=bad_draft,
        images=[
            VisualAssetInput(
                filename="card.png",
                dominant_hexes=["#00B8A5"],
                has_logo=True,
                logo_bbox=[5, 5, 320, 100],
                has_alt_text=False,
                alt_text=""
            )
        ]
    )

    response = engine.audit_document(request)

    # 1. PII should be sanitized
    assert response.scrubbed_pii_count >= 2

    # 2. Score should be penalized into RED tier due to multiple blockers
    assert response.summary.tier == "RED"
    assert response.summary.blockers >= 4
    assert response.summary.compliance_score < 70.0
    assert response.summary.publishing_status == "LEGAL_BLOCKED"

    # 3. CMS publish should be blocked
    block_result = cms.intercept_publish_attempt("wordpress", "draft-001", response.summary.cryptographic_token)
    assert block_result["allowed"] is False
    assert block_result["status_code"] == 403


def test_end_to_end_compliant_draft_audit():
    engine = UnifiedBrandGovernanceEngine()
    cms = CMSPublishingGateway(engine.ledger)

    good_draft = (
        "AEGIS-Brand™ delivers cost-effective enterprise brand governance with an audited 99.95% contractual uptime SLA. "
        "Our SOC 2 Type II certified infrastructure empowers enterprise marketing teams to accelerate pre-publication reviews. "
        "Verified customer benchmarks demonstrate an average 31% conversion uplift across active deployments."
    )

    request = DocumentAuditRequest(
        document_id="draft-002",
        title="Compliant Case Study",
        author="Senior Brand Director",
        text=good_draft,
        images=[]
    )

    response = engine.audit_document(request)

    # Compliant draft should achieve GREEN tier with 0 blockers
    assert response.summary.blockers == 0
    assert response.summary.compliance_score >= 90.0
    assert response.summary.tier == "GREEN"
    assert response.summary.publishing_status == "AUTO_APPROVED"
    assert response.summary.cryptographic_token is not None

    # CMS publish should succeed with 200 OK
    publish_result = cms.intercept_publish_attempt("webflow", "draft-002", response.summary.cryptographic_token)
    assert publish_result["allowed"] is True
    assert publish_result["status_code"] == 200

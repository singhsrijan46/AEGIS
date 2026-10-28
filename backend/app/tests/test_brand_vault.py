import pytest
from backend.app.core.brand_vault import BrandVault
from backend.app.core.temporal_kg import TemporalKnowledgeGraph
from backend.app.core.presidio_privacy import PrivacyGateway


def test_brand_vault_rules_and_tokens():
    vault = BrandVault()
    rules = vault.get_all_rules()
    assert len(rules) >= 8

    # Verify official color palette contains primary teal and navy
    assert "#00A896" in vault.official_palette.values()
    assert "#0F2537" in vault.official_palette.values()

    # Verify banned lexicon
    assert "cheap" in vault.prohibited_lexicon
    assert vault.prohibited_lexicon["cheap"]["replacement"] == "cost-effective"

    # Verify trademark registry
    assert vault.trademark_registry["AEGIS-Brand"] == "AEGIS-Brand™"
    assert vault.trademark_registry["AEGIS"] == "AEGIS™"


def test_temporal_kg_queries():
    kg = TemporalKnowledgeGraph()
    facts = kg.get_all_facts()
    assert len(facts) >= 8

    # Query active SLA
    results = kg.query_fact("Uptime SLA Guarantee")
    assert len(results) > 0
    assert results[0]["is_temporally_valid"] is True
    assert "99.95%" in results[0]["fact"].value

    # Query deprecated pricing
    deprecated_results = kg.query_fact("Startup Pricing")
    assert len(deprecated_results) > 0
    # $49 tier expired on 2025-09-30
    assert deprecated_results[0]["fact"].status == "DEPRECATED"


def test_presidio_privacy_sanitizer():
    gateway = PrivacyGateway()
    raw = "Contact cto@inkloom.internal or call 415-555-0199 regarding Project Titan deployment on 192.168.1.45."
    sanitized, count = gateway.sanitize(raw)
    assert count >= 4
    assert "cto@inkloom.internal" not in sanitized
    assert "415-555-0199" not in sanitized
    assert "Project Titan" not in sanitized
    assert "192.168.1.45" not in sanitized

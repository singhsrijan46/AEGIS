import pytest
from backend.app.core.fact_decomposer import AtomicFactDecomposer
from backend.app.core.fact_calculator import DeterministicFactCalculator
from backend.app.core.ragas_evaluator import RagasClaimEvaluator
from backend.app.core.temporal_kg import TemporalKnowledgeGraph
from backend.app.core.hybrid_retriever import AirGappedHybridRetriever
from backend.app.core.vale_linter import ValeLinter
from backend.app.core.brand_vault import BrandVault


def test_fact_decomposition():
    decomposer = AtomicFactDecomposer()
    text = "Inkloom is the only platform delivering 99.999% uptime with FedRAMP High certification for $49/month."
    propositions = decomposer.decompose(text)
    assert len(propositions) >= 4

    types = {p.claim_type for p in propositions}
    assert "SLA" in types
    assert "SECURITY" in types
    assert "PRICING" in types
    assert "SUPERLATIVE" in types


def test_deterministic_fact_calculator():
    calc = DeterministicFactCalculator()
    # Claim: increased conversions by 310% from 2.1% to 6.5% -> actual is ~209.5%
    bad_text = "Our platform increased conversions by 310% from 2.1% to 6.5%."
    res = calc.verify_math_in_text(bad_text)
    assert res is not None
    assert res.is_correct is False
    assert "209.5%" in res.computed_value
    assert res.claimed_value == "310.0%"

    # Correct claim: increased by 50% from 2.0% to 3.0%
    good_text = "We boosted conversions by 50% from 2.0% to 3.0%."
    good_res = calc.verify_math_in_text(good_text)
    assert good_res is not None
    assert good_res.is_correct is True


def test_ragas_and_vale_evaluations():
    vault = BrandVault()
    kg = TemporalKnowledgeGraph()
    retriever = AirGappedHybridRetriever()
    linter = ValeLinter(vault)
    ragas = RagasClaimEvaluator(kg, retriever)
    decomposer = AtomicFactDecomposer()

    text = "Inkloom Verity is cheap and delivers 99.999% uptime with FedRAMP High certification."
    
    # Vale linter should catch 'cheap' and missing ™
    vale_findings = linter.lint(text)
    assert any("cheap" in f.flagged_text.lower() for f in vale_findings)
    assert any("Inkloom Verity" in f.flagged_text for f in vale_findings)

    # Ragas should catch 99.999% uptime and FedRAMP High
    props = decomposer.decompose(text)
    ragas_findings = []
    for p in props:
        f = ragas.evaluate_proposition(p, text)
        if f:
            ragas_findings.append(f)

    assert any(f.title == "Unsupported SLA Guarantee (99.999%)" for f in ragas_findings)
    assert any(f.title == "Hallucinated Security Certification (FedRAMP High)" for f in ragas_findings)

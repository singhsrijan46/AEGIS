"""
Temporal Knowledge Graph (T-EKG) Engine (Step 1 Deliverable)
Codifies all enterprise truths, product capabilities, SLAs, pricing tiers,
and compliance certifications with explicit temporal validity intervals [t_start, t_end].
Synthesized from: FActScore [1], AVeriTeC [4], FacTool [5].
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from ..models.schemas import TemporalFact


class TemporalKnowledgeGraph:
    def __init__(self):
        self.facts: List[TemporalFact] = self._seed_enterprise_facts()

    def _seed_enterprise_facts(self) -> List[TemporalFact]:
        return [
            # Security Certifications
            TemporalFact(
                id="FACT-SEC-001",
                entity="AEGIS-Brand",
                attribute="Security Certification",
                value="SOC 2 Type II Certified",
                valid_from="2024-01-01",
                valid_to="2027-12-31",
                source_document="Compliance Audit Report 2026 (Schellman & Co.)",
                section="Section 1.1: SOC 2 Attestation",
                page=3,
                status="ACTIVE"
            ),
            TemporalFact(
                id="FACT-SEC-002",
                entity="AEGIS-Brand",
                attribute="Security Certification",
                value="ISO 27001:2022 Certified",
                valid_from="2024-06-01",
                valid_to="2027-06-01",
                source_document="BSI Certification Register 2026",
                section="Certificate No. IS 78942",
                page=1,
                status="ACTIVE"
            ),
            TemporalFact(
                id="FACT-SEC-003",
                entity="AEGIS-Brand",
                attribute="FedRAMP Status",
                value="FedRAMP Moderate Ready (In Evaluation, NOT FedRAMP High Authorized)",
                valid_from="2026-01-01",
                valid_to="2027-06-30",
                source_document="Federal Agency Security Assessment Register",
                section="Section 3: FedRAMP PMO Review",
                page=14,
                status="ACTIVE"
            ),
            TemporalFact(
                id="FACT-SEC-004",
                entity="AEGIS-Brand",
                attribute="Data Residency",
                value="Frankfurt (Germany) and Oregon (USA) AWS Air-Gapped VPCs",
                valid_from="2025-01-01",
                valid_to="2027-12-31",
                source_document="Enterprise Architecture & Data Sovereignty Specs",
                section="Section 2.2: Cloud Infrastructure",
                page=8,
                status="ACTIVE"
            ),

            # Availability & SLA
            TemporalFact(
                id="FACT-SLA-001",
                entity="AEGIS-Brand",
                attribute="Uptime SLA Guarantee",
                value="99.95% Annual Uptime (Contractual SLA)",
                valid_from="2025-01-01",
                valid_to="2027-01-01",
                source_document="Master Services Agreement (MSA) Q4 2026",
                section="Schedule B: Service Level Agreement",
                page=32,
                status="ACTIVE"
            ),
            TemporalFact(
                id="FACT-SLA-002",
                entity="AEGIS-Brand",
                attribute="Deprecated SLA",
                value="99.90% Uptime Guarantee",
                valid_from="2023-01-01",
                valid_to="2024-12-31",
                source_document="Legacy MSA Agreement v2",
                section="Schedule B",
                page=19,
                status="DEPRECATED"
            ),

            # Pricing Tiers
            TemporalFact(
                id="FACT-PRICE-001",
                entity="AEGIS-Brand",
                attribute="Active Enterprise Pricing",
                value="$99 per seat per month (billed annually, min 25 seats)",
                valid_from="2026-01-01",
                valid_to="2027-01-01",
                source_document="Enterprise Master Price Sheet Q4 2026",
                section="Commercial Terms: Tier 2 Enterprise",
                page=2,
                status="ACTIVE"
            ),
            TemporalFact(
                id="FACT-PRICE-002",
                entity="AEGIS-Brand",
                attribute="Deprecated Startup Pricing",
                value="$49 per seat per month",
                valid_from="2024-01-01",
                valid_to="2025-09-30",
                source_document="Legacy Price Sheet 2024-2025",
                section="Early Access Pricing",
                page=1,
                status="DEPRECATED"
            ),

            # Audited Empirical Metrics
            TemporalFact(
                id="FACT-METRIC-001",
                entity="AEGIS-Brand",
                attribute="Average Conversion Uplift",
                value="31% conversion uplift across audited enterprise cohort",
                valid_from="2025-06-01",
                valid_to="2027-01-01",
                source_document="Audited Customer Impact & ROI Whitepaper (Forrester TEI)",
                section="Section 4: Quantitative Revenue Impact",
                page=18,
                status="ACTIVE"
            ),
            TemporalFact(
                id="FACT-METRIC-002",
                entity="AEGIS-Brand",
                attribute="Enterprise Customer Base",
                value="450+ Global Enterprise Customers",
                valid_from="2026-06-01",
                valid_to="2026-12-31",
                source_document="Q3 2026 Investor Shareholder Deck",
                section="Slide 8: Growth Metrics",
                page=8,
                status="ACTIVE"
            ),
            TemporalFact(
                id="FACT-METRIC-003",
                entity="AEGIS-Brand",
                attribute="Review Cycle Turnaround",
                value="Reduces turnaround from 4.5 days to < 4 hours (75% reduction)",
                valid_from="2025-01-01",
                valid_to="2027-01-01",
                source_document="Product Benchmark Study 2026",
                section="Section 2.1: Editorial Velocity",
                page=6,
                status="ACTIVE"
            )
        ]

    def query_fact(self, attribute_keyword: str, check_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Queries facts matching attribute_keyword.
        Evaluates temporal validity at check_date (defaults to current date).
        """
        if check_date is None:
            check_date = datetime.now().strftime("%Y-%m-%d")

        matches = []
        kw = attribute_keyword.lower()

        for fact in self.facts:
            # Check keyword match in attribute, value, or entity
            if kw in fact.attribute.lower() or kw in fact.value.lower() or kw in fact.entity.lower():
                is_valid = fact.valid_from <= check_date <= fact.valid_to
                matches.append({
                    "fact": fact,
                    "is_temporally_valid": is_valid,
                    "is_active": fact.status == "ACTIVE" and is_valid
                })

        return matches

    def add_fact(self, fact: TemporalFact):
        self.facts.append(fact)

    def get_all_facts(self) -> List[TemporalFact]:
        return self.facts

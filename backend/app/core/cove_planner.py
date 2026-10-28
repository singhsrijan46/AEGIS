"""
Chain-of-Verification (CoVe) Decoupled Question Planner (Step 2 Deliverable)
Constructs independent, non-confirmatory queries to validate atomic propositions
without circular hallucination or draft context bias.
Synthesized from: Chain-of-Verification [2], Meta AI.
"""

from typing import Dict, Any
from .fact_decomposer import AtomicProposition


class DecoupledCoVePlanner:
    def plan_question(self, proposition: AtomicProposition) -> Dict[str, Any]:
        """
        Generates decoupled query and lookup key based on proposition type.
        """
        claim_type = proposition.claim_type

        if claim_type == "SECURITY":
            return {
                "verification_question": "What active security and regulatory certifications does AEGIS hold in official records?",
                "search_key": "Security Certification",
                "expected_domain": "Compliance & Security"
            }
        elif claim_type == "SLA":
            return {
                "verification_question": "What is AEGIS's active contractual uptime SLA percentage in standard enterprise contracts?",
                "search_key": "Uptime SLA Guarantee",
                "expected_domain": "SLA & Infrastructure"
            }
        elif claim_type == "PRICING":
            return {
                "verification_question": "What is the current official per-seat monthly price listed in the master price sheet for 2026?",
                "search_key": "Active Enterprise Pricing",
                "expected_domain": "Commercial Pricing"
            }
        elif claim_type == "SUPERLATIVE":
            return {
                "verification_question": "Does AEGIS have independent third-party audit documentation substantiating absolute market exclusivity or #1 ranking?",
                "search_key": "Superlative Substantiation",
                "expected_domain": "Legal & Regulatory"
            }
        elif claim_type == "METRIC":
            return {
                "verification_question": "What is the audited percentage increase and conversion metric documented in customer case studies?",
                "search_key": "Average Conversion Uplift",
                "expected_domain": "Empirical Metrics"
            }
        else:
            return {
                "verification_question": f"What official records substantiate the claim: '{proposition.proposition}'?",
                "search_key": proposition.proposition,
                "expected_domain": "General Verification"
            }

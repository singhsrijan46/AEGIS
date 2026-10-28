"""
E-AFV: Enterprise-Atomic Fact Verification Decomposer (Step 2 Deliverable)
Decomposes compound sentences into independent atomic propositions.
Synthesized from: FActScore [1], SAFE [3].
"""

import re
from typing import List, Dict, Any, Tuple


class AtomicProposition:
    def __init__(self, raw_sentence: str, proposition: str, span: Tuple[int, int], claim_type: str, extracted_entities: List[str]):
        self.raw_sentence = raw_sentence
        self.proposition = proposition
        self.span = span  # Character offsets in document
        self.claim_type = claim_type  # 'METRIC', 'SLA', 'PRICING', 'SECURITY', 'SUPERLATIVE', 'GENERAL'
        self.extracted_entities = extracted_entities


class AtomicFactDecomposer:
    """
    Decomposes sentences containing numbers, percentages, certifications,
    pricing, uptime, or superlatives into atomic testable units.
    """

    # Patterns for empirical assertions
    NUMERIC_PATTERN = re.compile(r'\b(?:\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?|\d+(?:\.\d+)?X|\b\d{2,}\b)')
    SUPERLATIVE_PATTERN = re.compile(r'\b(?:the only|world\'s best|#1 in the industry|unrivaled|guaranteed|unmatched)\b', re.IGNORECASE)
    SECURITY_PATTERN = re.compile(r'\b(?:SOC ?2(?: Type II)?|ISO 27001|FedRAMP(?: High| Moderate)?|HIPAA|GDPR)\b', re.IGNORECASE)
    PRICING_PATTERN = re.compile(r'\$\d+(?:/month| per user| per seat|/seat)?', re.IGNORECASE)
    SLA_PATTERN = re.compile(r'99\.\d+%|\buptime\b', re.IGNORECASE)

    def decompose(self, text: str) -> List[AtomicProposition]:
        propositions = []
        # Split text into sentences without breaking on decimal numbers (e.g. 99.999% or $49.99)
        sentence_matches = list(re.finditer(r'(?:(?:\d+\.\d+)|[^.!?])+(?:[.!?]+(?:\s+|$)|$)', text))

        for match in sentence_matches:
            sentence = match.group(0).strip()
            if not sentence:
                continue
            s_start = match.start()

            # 1. Check for Security Certification claims
            sec_matches = list(self.SECURITY_PATTERN.finditer(sentence))
            for sm in sec_matches:
                cert_name = sm.group(0)
                propositions.append(AtomicProposition(
                    raw_sentence=sentence,
                    proposition=f"AEGIS holds active certification: {cert_name}",
                    span=(s_start + sm.start(), s_start + sm.end()),
                    claim_type="SECURITY",
                    extracted_entities=[cert_name]
                ))

            # 2. Check for SLA / Uptime claims
            sla_matches = list(re.finditer(r'(?:99\.\d+%\s*(?:uptime|availability|sla)?|\buptime\b)', sentence, re.IGNORECASE))
            for sm in sla_matches:
                matched_val = sm.group(0)
                propositions.append(AtomicProposition(
                    raw_sentence=sentence,
                    proposition=f"AEGIS guarantees SLA uptime: {matched_val}",
                    span=(s_start + sm.start(), s_start + sm.end()),
                    claim_type="SLA",
                    extracted_entities=[matched_val]
                ))

            # 3. Check for Pricing claims
            price_matches = list(self.PRICING_PATTERN.finditer(sentence))
            for pm in price_matches:
                propositions.append(AtomicProposition(
                    raw_sentence=sentence,
                    proposition=f"AEGIS active enterprise price is: {pm.group(0)}",
                    span=(s_start + pm.start(), s_start + pm.end()),
                    claim_type="PRICING",
                    extracted_entities=[pm.group(0)]
                ))

            # 4. Check for Superlative claims
            sup_matches = list(self.SUPERLATIVE_PATTERN.finditer(sentence))
            for sup in sup_matches:
                propositions.append(AtomicProposition(
                    raw_sentence=sentence,
                    proposition=f"AEGIS asserts unverified superlative: {sup.group(0)}",
                    span=(s_start + sup.start(), s_start + sup.end()),
                    claim_type="SUPERLATIVE",
                    extracted_entities=[sup.group(0)]
                ))

            # 5. Check for Statistical / Conversion change math
            # e.g. "increased conversions by 310% from 2.1% to 6.5%"
            math_match = re.search(r'(?:increase|boost|grow|lift)\w*\s+.*?by\s+(\d+(?:\.\d+)?%?)\s+from\s+(\d+(?:\.\d+)?%?)\s+to\s+(\d+(?:\.\d+)?%?)', sentence, re.IGNORECASE)
            if math_match:
                claimed_delta, start_val, end_val = math_match.groups()
                propositions.append(AtomicProposition(
                    raw_sentence=sentence,
                    proposition=f"Statistical assertion claiming change by {claimed_delta} from {start_val} to {end_val}",
                    span=(s_start + math_match.start(), s_start + math_match.end()),
                    claim_type="METRIC",
                    extracted_entities=[claimed_delta, start_val, end_val]
                ))

        return propositions

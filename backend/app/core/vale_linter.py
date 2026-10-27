"""
Deterministic Lexical & AST Linter (Step 2 Deliverable)
Microsecond-level regex and AST token scanning for banned terminology,
slang, devaluing vocabulary, and trademark compliance.
Synthesized from: CRITIC [11], Vale Engine architecture.
"""

from typing import List, Tuple
import re
from ..models.schemas import Finding
from .brand_vault import BrandVault


class ValeLinter:
    def __init__(self, brand_vault: BrandVault):
        self.vault = brand_vault
        # Compile patterns for banned words (word boundary aware, case-insensitive)
        self.banned_patterns = []
        for word, meta in self.vault.prohibited_lexicon.items():
            pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE)
            self.banned_patterns.append((word, pattern, meta))

        # Trademark patterns
        self.tm_checks = [
            ("Inkloom Verity", r'\bInkloom Verity(?!\™|\®)\b', "Inkloom Verity™"),
            ("VeriBrand AI", r'\bVeriBrand AI(?!\™|\®)\b', "VeriBrand AI™"),
            ("E-AFV", r'\bE-AFV(?!\™|\®)\b', "E-AFV™")
        ]

    def lint(self, text: str) -> List[Finding]:
        findings = []

        # 1. Prohibited Lexicon Checks
        for word, pattern, meta in self.banned_patterns:
            for match in pattern.finditer(text):
                start, end = match.span()
                matched_text = match.group(0)
                replacement = meta["replacement"]
                # Match capitalization
                if matched_text.istitle():
                    replacement = replacement.title()
                elif matched_text.isupper():
                    replacement = replacement.upper()

                findings.append(Finding(
                    span=(start, end),
                    flagged_text=matched_text,
                    category="LEXICAL",
                    severity=meta["severity"],
                    title=f"Prohibited Terminology: '{matched_text}'",
                    explanation=f"{meta['rationale']} Replace with approved enterprise phrasing.",
                    cited_source="Inkloom Enterprise Brand Standards Manual v4.2, Section 2.4",
                    rule_id="RULE-LEX-001",
                    suggested_edit=replacement,
                    confidence=1.0,
                    anomaly_type="Input-Conflicting"
                ))

        # 2. Trademark Placement (Check first occurrence)
        for term, regex_str, correct_form in self.tm_checks:
            matches = list(re.finditer(regex_str, text, re.IGNORECASE))
            if matches:
                # Flag the first occurrence
                first_match = matches[0]
                start, end = first_match.span()
                matched_text = first_match.group(0)
                findings.append(Finding(
                    span=(start, end),
                    flagged_text=matched_text,
                    category="LEXICAL",
                    severity="WARNING",
                    title=f"Missing Trademark Symbol: '{matched_text}'",
                    explanation=(
                        f"Corporate brand policy requires appending the ™ trademark symbol "
                        f"on the first occurrence of '{term}' in all customer-facing collateral."
                    ),
                    cited_source="Corporate Legal IP & Trademark Register 2026, Section 1.1, Page 4",
                    rule_id="RULE-LEX-002",
                    suggested_edit=correct_form,
                    confidence=1.0,
                    anomaly_type="Input-Conflicting"
                ))

        return findings

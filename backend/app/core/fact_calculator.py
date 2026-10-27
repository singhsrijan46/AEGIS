"""
FacTool Deterministic Math & Statistics Calculator (Step 2 Deliverable)
Verifies numeric, statistical, and algorithmic assertions deterministically
without relying on LLM arithmetic hallucinations.
Synthesized from: FacTool [5].
"""

import re
from typing import Optional, Dict, Any


class MathVerificationResult:
    def __init__(self, is_correct: bool, claimed_value: str, computed_value: str, formula: str, discrepancy_percent: float):
        self.is_correct = is_correct
        self.claimed_value = claimed_value
        self.computed_value = computed_value
        self.formula = formula
        self.discrepancy_percent = discrepancy_percent


class DeterministicFactCalculator:
    """
    Parses and deterministically evaluates percentage changes and arithmetic assertions.
    """

    # e.g., "increased conversions by 310% from 2.1% to 6.5%"
    PERCENT_CHANGE_REGEX = re.compile(
        r'(?:increase|boost|grow|lift|surge|expand)\w*\s+.*?by\s+(\d+(?:\.\d+)?)\s*%\s+from\s+(\d+(?:\.\d+)?)\s*%\s+to\s+(\d+(?:\.\d+)?)\s*%',
        re.IGNORECASE
    )

    def verify_math_in_text(self, text: str) -> Optional[MathVerificationResult]:
        match = self.PERCENT_CHANGE_REGEX.search(text)
        if not match:
            return None

        claimed_str, start_str, end_str = match.groups()
        try:
            claimed_pct = float(claimed_str)
            v_start = float(start_str)
            v_end = float(end_str)

            if v_start <= 0:
                return None

            actual_pct = ((v_end - v_start) / v_start) * 100.0
            diff = abs(claimed_pct - actual_pct)

            # If discrepancy is greater than 1% relative error
            is_correct = diff < 1.0

            formula = f"(({v_end} - {v_start}) / {v_start}) * 100% = {actual_pct:.1f}%"

            return MathVerificationResult(
                is_correct=is_correct,
                claimed_value=f"{claimed_pct:.1f}%",
                computed_value=f"{actual_pct:.1f}%",
                formula=formula,
                discrepancy_percent=diff
            )
        except Exception:
            return None

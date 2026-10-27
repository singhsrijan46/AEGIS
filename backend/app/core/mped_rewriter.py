"""
Minimal Perturbation Edit Distance (MPED) Intent-Preserving Rewriter (Step 4 Deliverable)
Replaces violating text spans [s_start, s_end] with targeted, minimal-edit replacements
that satisfy compliance while preserving author rhythm, tone, and rhetorical cadence.
Synthesized from: TIGERScore [12], Directional Stimulus [19], Self-Refine [10], Co-Writing CHI [16].
"""

import difflib
from typing import Dict, Any, Tuple


def compute_levenshtein_distance(s1: str, s2: str) -> int:
    """
    Standard dynamic programming Levenshtein distance.
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]


class MinimalPerturbationRewriter:
    def __init__(self):
        pass

    def generate_span_diff(self, full_text: str, span: Tuple[int, int], replacement: str) -> Dict[str, Any]:
        """
        Applies a span-level replacement and computes character diff metrics.
        Ensures surrounding context is completely frozen (token masking).
        """
        start, end = span
        original_span = full_text[start:end]
        modified_text = full_text[:start] + replacement + full_text[end:]

        lev_dist = compute_levenshtein_distance(original_span, replacement)
        orig_len = max(1, len(original_span))
        perturbation_ratio = round((lev_dist / orig_len) * 100.0, 1)

        # Word-level diff sequence for UI rendering
        s = difflib.SequenceMatcher(None, original_span, replacement)
        diff_chunks = []
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            diff_chunks.append({
                "tag": tag,  # 'equal', 'replace', 'delete', 'insert'
                "original": original_span[i1:i2],
                "replacement": replacement[j1:j2]
            })

        return {
            "original_span": original_span,
            "suggested_span": replacement,
            "levenshtein_distance": lev_dist,
            "perturbation_ratio_percent": perturbation_ratio,
            "diff_chunks": diff_chunks,
            "modified_full_text": modified_text
        }

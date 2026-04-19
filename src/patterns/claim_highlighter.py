"""
Suspicious-claim identification — refactored into src/patterns/.
"""

from typing import List

from src.utils import (
    split_into_sentences,
    contains_vague_source,
    contains_extreme_language,
    contains_evidence_markers,
    contains_conspiracy_markers,
)


class ClaimHighlighter:
    """
    Identifies sentences that require fact-checking based on a suspicion score.

    Scoring weights
    ---------------
    * Vague source reference  → +2
    * Conspiracy marker       → +2
    * Extreme language        → +1
    * No evidence markers     → +1

    Sentences scoring ≥ 3 are flagged; the top 5 are returned.
    """

    _THRESHOLD = 3
    _MAX_CLAIMS = 5

    def identify_suspicious_claims(self, text: str) -> List[str]:
        """
        Return up to ``_MAX_CLAIMS`` suspicious sentences from *text*.

        Args:
            text: Full article text.

        Returns:
            List of sentenced strings with high suspicion scores, capped at 5.
        """
        if not text:
            return []

        flagged: List[str] = []

        for sentence in split_into_sentences(text):
            score = 0
            if contains_vague_source(sentence):
                score += 2
            if contains_conspiracy_markers(sentence):
                score += 2
            if contains_extreme_language(sentence):
                score += 1
            if not contains_evidence_markers(sentence):
                score += 1

            if score >= self._THRESHOLD:
                flagged.append(sentence.strip())

        return flagged[: self._MAX_CLAIMS]

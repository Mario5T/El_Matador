"""
Emotional tone analysis — refactored into src/patterns/.
"""

from typing import Dict


class EmotionalAnalyzer:
    """
    Classifies the dominant emotional tone of an article based on
    pattern-detection results.
    """

    def analyze_emotional_tone(
        self, patterns: Dict[str, float], text: str  # noqa: ARG002 (text reserved)
    ) -> str:
        """
        Return a descriptive emotional-tone label.

        Priority (highest → lowest):
        1. Highly emotional and manipulative
        2. Sensationalized and attention-seeking
        3. Conspiratorial and fear-inducing
        4. Moderately emotional
        5. Neutral and analytical

        Args:
            patterns: Output of ``PatternDetector.detect_patterns()``.
            text: Raw article text (reserved for future enrichment).

        Returns:
            Human-readable emotional tone string.
        """
        em  = patterns.get("emotional_manipulation", 0)
        sen = patterns.get("sensational_phrases", 0)
        con = patterns.get("conspiracy_framing", 0)

        if em > 3:
            return "Highly emotional and manipulative"
        if sen > 3:
            return "Sensationalized and attention-seeking"
        if con > 0:
            return "Conspiratorial and fear-inducing"
        if em > 0:
            return "Moderately emotional"
        return "Neutral and analytical"

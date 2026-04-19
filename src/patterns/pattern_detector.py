"""
Pattern detection module — refactored into src/patterns/.

All keyword lists and detection logic live here; utility helpers are
imported from src.utils to avoid duplication.
"""

from typing import Dict

from src.utils import count_keywords, count_phrases


class PatternDetector:
    """
    Detects linguistic patterns associated with misinformation in news articles.

    All keyword / phrase lists are class-level constants so they are created
    once per import, not once per detect_patterns() call.
    """

    # ------------------------------------------------------------------
    # Keyword / phrase lists (class-level constants)
    # ------------------------------------------------------------------

    SENSATIONAL_KEYWORDS = [
        "SHOCKING", "BREAKING", "UNBELIEVABLE", "EXPOSED",
        "REVEALED", "SECRET", "HIDDEN", "TRUTH", "BOMBSHELL",
        "EXPLOSIVE", "STUNNING", "INCREDIBLE",
    ]

    VAGUE_SOURCE_PATTERNS = [
        "sources say", "experts claim", "reports suggest",
        "allegedly", "rumored", "according to sources",
        "insiders say", "it is believed", "some say", "many believe",
    ]

    CONSPIRACY_KEYWORDS = [
        "cover-up", "cover up", "conspiracy", "they don't want you to know",
        "mainstream media", "wake up", "sheeple", "hidden truth",
        "secret agenda", "deep state", "false flag", "controlled by",
    ]

    EMOTIONAL_KEYWORDS = [
        "outrage", "terrifying", "devastating", "horrifying",
        "shocking", "disgusting", "appalling", "outrageous",
        "scandalous", "alarming", "disturbing",
    ]

    BALANCE_INDICATORS = [
        "however", "although", "on the other hand", "but",
        "despite", "nevertheless", "yet", "while", "whereas",
        "conversely", "alternatively",
    ]

    EVIDENCE_INDICATORS = [
        "study", "research", "data", "statistics", "percent",
        "according to", "published", "journal", "university",
        "professor", "analysis", "survey", "report",
    ]

    EXTREME_ADJECTIVES = [
        "always", "never", "every", "all", "none", "completely",
        "totally", "absolutely", "definitely", "entirely",
        "utterly", "wholly",
    ]

    CLICKBAIT_PATTERNS = [
        "you won't believe", "what happened next",
        "will shock you", "doctors hate", "one weird trick",
        "this is why", "the reason why", "you need to see",
    ]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def detect_patterns(self, text: str) -> Dict[str, float]:
        """
        Detect linguistic patterns associated with misinformation.

        Args:
            text: Article text to analyse.

        Returns:
            Dictionary with the following keys:

            * ``sensational_phrases``   – count (int)
            * ``excessive_caps``        – ratio 0.0–1.0
            * ``vague_sources``         – count (int)
            * ``conspiracy_framing``    – count (int)
            * ``emotional_manipulation``– count (int)
            * ``one_sided``             – score 0.0–1.0 (higher = more one-sided)
            * ``no_evidence``           – score 0.0–1.0 (higher = less evidence)
            * ``extreme_adjectives``    – count (int)
            * ``clickbait``             – count (int)
        """
        _empty: Dict[str, float] = {
            "sensational_phrases": 0,
            "excessive_caps": 0.0,
            "vague_sources": 0,
            "conspiracy_framing": 0,
            "emotional_manipulation": 0,
            "one_sided": 0.0,
            "no_evidence": 0.0,
            "extreme_adjectives": 0,
            "clickbait": 0,
        }
        if not text:
            return _empty

        patterns: Dict[str, float] = {}

        patterns["sensational_phrases"] = count_keywords(
            text, self.SENSATIONAL_KEYWORDS
        )

        words = text.split()
        if words:
            caps_words = [w for w in words if w.isupper() and len(w) > 2]
            patterns["excessive_caps"] = len(caps_words) / len(words)
        else:
            patterns["excessive_caps"] = 0.0

        patterns["vague_sources"] = count_phrases(
            text, self.VAGUE_SOURCE_PATTERNS
        )
        patterns["conspiracy_framing"] = count_keywords(
            text, self.CONSPIRACY_KEYWORDS
        )
        patterns["emotional_manipulation"] = count_keywords(
            text, self.EMOTIONAL_KEYWORDS
        )

        balance_count = count_phrases(text, self.BALANCE_INDICATORS)
        patterns["one_sided"] = max(0.0, 1.0 - min(1.0, balance_count / 3.0))

        evidence_count = count_keywords(text, self.EVIDENCE_INDICATORS)
        patterns["no_evidence"] = max(0.0, 1.0 - min(1.0, evidence_count / 5.0))

        patterns["extreme_adjectives"] = count_keywords(
            text, self.EXTREME_ADJECTIVES
        )
        patterns["clickbait"] = count_phrases(text, self.CLICKBAIT_PATTERNS)

        return patterns

"""
Unit tests for src.patterns.PatternDetector
=============================================
Covers detect_patterns() output structure, value ranges, and key detections.
"""

import pytest

from src.patterns.pattern_detector import PatternDetector


@pytest.fixture
def detector():
    return PatternDetector()


EXPECTED_KEYS = {
    "sensational_phrases",
    "excessive_caps",
    "vague_sources",
    "conspiracy_framing",
    "emotional_manipulation",
    "one_sided",
    "no_evidence",
    "extreme_adjectives",
    "clickbait",
}


class TestPatternDetectorStructure:
    def test_returns_all_keys(self, detector):
        result = detector.detect_patterns("Some article text here.")
        assert EXPECTED_KEYS == set(result.keys())

    def test_empty_text_returns_zeros(self, detector):
        result = detector.detect_patterns("")
        assert result["sensational_phrases"] == 0
        assert result["excessive_caps"] == 0.0
        assert result["one_sided"] == 0.0

    def test_caps_ratio_in_unit_range(self, detector):
        result = detector.detect_patterns("SHOUTING ALL THE WAY")
        assert 0.0 <= result["excessive_caps"] <= 1.0

    def test_one_sided_in_unit_range(self, detector):
        result = detector.detect_patterns("This is the only truth.")
        assert 0.0 <= result["one_sided"] <= 1.0

    def test_no_evidence_in_unit_range(self, detector):
        result = detector.detect_patterns("Fake news everywhere!")
        assert 0.0 <= result["no_evidence"] <= 1.0


class TestSensationalDetection:
    def test_all_caps_sensational(self, detector):
        text = "SHOCKING BREAKING news EXPOSED today"
        result = detector.detect_patterns(text)
        assert result["sensational_phrases"] >= 2

    def test_no_sensational(self, detector):
        text = "A peer-reviewed study found moderate results."
        result = detector.detect_patterns(text)
        assert result["sensational_phrases"] == 0


class TestVagueSourceDetection:
    def test_vague_source(self, detector):
        text = "Sources say the election was rigged. Many believe this."
        result = detector.detect_patterns(text)
        assert result["vague_sources"] >= 2

    def test_credible_attribution(self, detector):
        # PatternDetector matches "according to sources" (with 'sources'), not bare
        # "according to"; this sentence has neither — expect 0 vague-source matches.
        text = "According to the published CDC report, vaccination rates rose."
        result = detector.detect_patterns(text)
        assert result["vague_sources"] == 0


class TestConspiracyDetection:
    def test_conspiracy_keywords(self, detector):
        text = "The deep state cover-up is ongoing. It's a false flag."
        result = detector.detect_patterns(text)
        assert result["conspiracy_framing"] >= 2

    def test_no_conspiracy(self, detector):
        text = "The government released a budget report for review."
        result = detector.detect_patterns(text)
        assert result["conspiracy_framing"] == 0


class TestBalancedArticle:
    def test_balanced_article_low_one_sided(self, detector):
        text = (
            "Scientists found X. However, other researchers dispute this. "
            "Although the data is promising, critics argue otherwise. "
            "Despite the controversy, the study was peer-reviewed."
        )
        result = detector.detect_patterns(text)
        assert result["one_sided"] < 0.5

    def test_evidence_rich_article_low_no_evidence(self, detector):
        text = (
            "A new study published in Nature journal found that research data "
            "shows a 20 percent improvement. The university analysis confirms "
            "this through a survey of 5,000 participants."
        )
        result = detector.detect_patterns(text)
        assert result["no_evidence"] < 0.5


class TestClickbaitDetection:
    def test_clickbait_phrase(self, detector):
        text = "You won't believe what happened next when doctors hate this."
        result = detector.detect_patterns(text)
        assert result["clickbait"] >= 1

    def test_no_clickbait(self, detector):
        text = "The annual report was released by the treasury department."
        result = detector.detect_patterns(text)
        assert result["clickbait"] == 0

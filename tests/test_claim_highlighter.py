"""
Unit tests for src.patterns.ClaimHighlighter
=============================================
Uses monkeypatching and edge cases to validate suspicious-claim extraction.
"""

import pytest

from src.patterns.claim_highlighter import ClaimHighlighter


@pytest.fixture
def highlighter():
    return ClaimHighlighter()


class TestClaimHighlighterBasic:
    def test_empty_text_returns_empty(self, highlighter):
        assert highlighter.identify_suspicious_claims("") == []

    def test_returns_list(self, highlighter):
        result = highlighter.identify_suspicious_claims("Normal sentence.")
        assert isinstance(result, list)

    def test_max_five_claims(self, highlighter):
        # Text with many suspicious sentences
        repeating = (
            "Sources say the deep state cover-up is real! " * 10
        )
        result = highlighter.identify_suspicious_claims(repeating)
        assert len(result) <= 5

    def test_high_suspicion_sentence_flagged(self, highlighter):
        text = (
            "Sources say the deep state is covering up the false flag operation. "
            "A normal sentence about weather follows."
        )
        result = highlighter.identify_suspicious_claims(text)
        assert len(result) >= 1
        assert any("deep state" in c.lower() or "sources say" in c.lower() for c in result)

    def test_clean_article_no_claims(self, highlighter):
        text = (
            "A peer-reviewed study published in Nature journal found that 80 percent "
            "of participants showed improvement. The research data was analysed by "
            "professors at Stanford University."
        )
        result = highlighter.identify_suspicious_claims(text)
        # Credible article should produce few or no flagged claims
        assert len(result) == 0

    def test_claims_are_strings(self, highlighter):
        text = "Sources say the cover-up is massive and absolutely shocking."
        result = highlighter.identify_suspicious_claims(text)
        for claim in result:
            assert isinstance(claim, str)

    def test_whitespace_stripped(self, highlighter):
        text = "  Sources say it is believed the conspiracy is real.  "
        result = highlighter.identify_suspicious_claims(text)
        for claim in result:
            assert claim == claim.strip()

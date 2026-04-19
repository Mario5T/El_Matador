"""
Unit tests for src.utils.text_utils
====================================
Covers: clean_text_for_model, count_keywords, count_phrases,
        split_into_sentences, and all contains_* sentence-level helpers.
"""

import pytest

from src.utils.text_utils import (
    clean_text_for_model,
    count_keywords,
    count_phrases,
    split_into_sentences,
    contains_vague_source,
    contains_extreme_language,
    contains_evidence_markers,
    contains_conspiracy_markers,
)


# ── clean_text_for_model ─────────────────────────────────────────────────────

class TestCleanTextForModel:
    def test_lowercases(self):
        assert clean_text_for_model("HELLO World") == "hello world"

    def test_strips_html(self):
        assert clean_text_for_model("<b>foo</b>") == "foo"

    def test_removes_non_alpha(self):
        result = clean_text_for_model("hello-world! 2024")
        assert result == "hello world"

    def test_collapses_whitespace(self):
        assert clean_text_for_model("foo   bar\t\nbaz") == "foo bar baz"

    def test_empty_string(self):
        assert clean_text_for_model("") == ""

    def test_numbers_removed(self):
        assert clean_text_for_model("score: 95%") == "score"

    def test_non_string_coerced(self):
        # Should not raise — str() coercion expected
        result = clean_text_for_model(12345)
        assert isinstance(result, str)


# ── count_keywords ───────────────────────────────────────────────────────────

class TestCountKeywords:
    def test_basic_count(self):
        assert count_keywords("The SHOCKING truth", ["shocking"]) == 1

    def test_case_insensitive(self):
        assert count_keywords("SHOCKING shocking Shocking", ["shocking"]) == 3

    def test_multiple_keywords(self):
        n = count_keywords("breaking news — explosive revelations", ["breaking", "explosive"])
        assert n == 2

    def test_empty_text(self):
        assert count_keywords("", ["shocking"]) == 0

    def test_empty_keywords(self):
        assert count_keywords("some text", []) == 0

    def test_no_match(self):
        assert count_keywords("ordinary article", ["shocking", "breaking"]) == 0

    def test_substring_match(self):
        # "all" is in "calling" — substring semantics are by design
        assert count_keywords("calling", ["all"]) == 1


# ── count_phrases ────────────────────────────────────────────────────────────

class TestCountPhrases:
    def test_basic_phrase(self):
        assert count_phrases("sources say the sky is blue", ["sources say"]) == 1

    def test_multi_phrase(self):
        n = count_phrases("sources say this. many believe that.", ["sources say", "many believe"])
        assert n == 2

    def test_empty_text(self):
        assert count_phrases("", ["sources say"]) == 0

    def test_empty_phrases(self):
        assert count_phrases("some text", []) == 0

    def test_case_insensitive(self):
        assert count_phrases("SOURCES SAY nothing", ["sources say"]) == 1

    def test_no_match(self):
        assert count_phrases("legitimate article with data", ["sources say"]) == 0


# ── split_into_sentences ──────────────────────────────────────────────────────

class TestSplitIntoSentences:
    def test_simple_split(self):
        sentences = split_into_sentences("Hello there. How are you? I am fine!")
        assert len(sentences) == 3

    def test_newline_split(self):
        sentences = split_into_sentences("Line one\nLine two\nLine three")
        assert len(sentences) == 3

    def test_empty_string(self):
        assert split_into_sentences("") == []

    def test_single_sentence(self):
        result = split_into_sentences("Just one sentence")
        assert result == ["Just one sentence"]

    def test_strips_whitespace(self):
        result = split_into_sentences("  hello.   world.  ")
        assert all(s == s.strip() for s in result)

    def test_no_empty_strings(self):
        result = split_into_sentences("A. . B.")
        assert all(s for s in result)


# ── contains_vague_source ─────────────────────────────────────────────────────

class TestContainsVagueSource:
    @pytest.mark.parametrize("sentence", [
        "Sources say the president will resign.",
        "Experts claim vaccines are unsafe.",
        "It is believed the deal is done.",
        "According to sources, the leak happened.",
        "Many believe the election was stolen.",
    ])
    def test_true_cases(self, sentence):
        assert contains_vague_source(sentence) is True

    @pytest.mark.parametrize("sentence", [
        "Dr Smith published a peer-reviewed study.",
        "The CDC released official guidelines.",
        "",
    ])
    def test_false_cases(self, sentence):
        assert contains_vague_source(sentence) is False


# ── contains_extreme_language ─────────────────────────────────────────────────

class TestContainsExtremeLanguage:
    def test_extreme_word_detected(self):
        assert contains_extreme_language("This is absolutely terrifying news") is True

    def test_no_extreme_words(self):
        assert contains_extreme_language("Researchers noticed a moderate trend") is False

    def test_empty_string(self):
        assert contains_extreme_language("") is False

    def test_case_insensitive(self):
        assert contains_extreme_language("SHOCKING revelation") is True


# ── contains_evidence_markers ─────────────────────────────────────────────────

class TestContainsEvidenceMarkers:
    def test_study_present(self):
        assert contains_evidence_markers("A new study shows promising results") is True

    def test_statistical_reference(self):
        assert contains_evidence_markers("Statistics show that 80 percent agree") is True

    def test_no_evidence(self):
        assert contains_evidence_markers("Trust me, it will happen soon") is False

    def test_empty_string(self):
        assert contains_evidence_markers("") is False


# ── contains_conspiracy_markers ───────────────────────────────────────────────

class TestContainsConspiracyMarkers:
    @pytest.mark.parametrize("sentence", [
        "There's a cover-up at the highest levels.",
        "The deep state is controlling everything.",
        "False flag operation exposed!",
        "They don't want you to know the truth.",
    ])
    def test_true_cases(self, sentence):
        assert contains_conspiracy_markers(sentence) is True

    def test_false_case(self):
        assert contains_conspiracy_markers("The committee reviewed the budget today.") is False

    def test_empty_string(self):
        assert contains_conspiracy_markers("") is False

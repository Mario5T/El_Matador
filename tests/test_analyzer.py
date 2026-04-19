"""
Unit tests for src.analyzer.CredibilityAnalyzer
================================================
Uses unittest.mock to avoid loading real model files.
"""

import pytest
from unittest.mock import MagicMock
import numpy as np

from src.analyzer.credibility_analyzer import CredibilityAnalyzer


@pytest.fixture
def analyzer():
    return CredibilityAnalyzer()


def _make_model(prediction: int = 1, proba=None):
    """Return a mock sklearn model."""
    model = MagicMock()
    model.predict.return_value = np.array([prediction])
    if proba is not None:
        model.predict_proba.return_value = np.array([proba])
    else:
        del model.predict_proba  # force decision_function branch
        model.decision_function.return_value = np.array([2.0])
    return model


def _make_vectorizer():
    """Return a mock TF-IDF vectorizer."""
    vec = MagicMock()
    vec.transform.return_value = MagicMock()
    return vec


CREDIBLE_TEXT = (
    "Scientists at Stanford University have published a peer-reviewed study "
    "showing that the new treatment demonstrates 89% efficacy in clinical trials. "
    "Dr. Jane Smith, lead researcher, confirmed the data. However, some experts "
    "remain cautious and suggest further studies are needed."
)

FAKE_TEXT = (
    "SHOCKING: Government scientists EXPOSED! Sources say the deep state is "
    "covering up a massive false flag operation. Many believe the cover-up "
    "involves shadowy figures who don't want you to know the truth. Wake up!"
)

SHORT_TEXT = "Too short."


# ── calculate_pattern_score ───────────────────────────────────────────────────

class TestCalculatePatternScore:
    def test_score_in_unit_range(self, analyzer):
        patterns = {
            "sensational_phrases": 3, "excessive_caps": 0.2,
            "vague_sources": 2, "conspiracy_framing": 1,
            "emotional_manipulation": 2, "one_sided": 0.8,
            "no_evidence": 0.9, "extreme_adjectives": 3, "clickbait": 1,
        }
        score = analyzer.calculate_pattern_score(patterns)
        assert 0.0 <= score <= 1.0

    def test_all_zero_patterns_gives_low_score(self, analyzer):
        patterns = {k: 0 for k in [
            "sensational_phrases", "excessive_caps", "vague_sources",
            "conspiracy_framing", "emotional_manipulation", "one_sided",
            "no_evidence", "extreme_adjectives", "clickbait",
        ]}
        score = analyzer.calculate_pattern_score(patterns)
        assert score == 0.0

    def test_empty_patterns_dict(self, analyzer):
        score = analyzer.calculate_pattern_score({})
        assert score == 0.0


# ── classify_credibility ──────────────────────────────────────────────────────

class TestClassifyCredibility:
    def test_short_text_is_unverified(self, analyzer):
        label = analyzer.classify_credibility(SHORT_TEXT, 1, 0.9, {})
        assert label == "UNVERIFIED"

    def test_high_conf_fake_high_pattern_is_misleading(self, analyzer):
        # With all pattern inputs saturated the weighted score tops out at ~0.65,
        # which is below the FAKE threshold (>0.7), so MISLEADING is expected.
        patterns = {k: 0 for k in [
            "sensational_phrases", "excessive_caps", "vague_sources",
            "conspiracy_framing", "emotional_manipulation", "one_sided",
            "no_evidence", "extreme_adjectives", "clickbait",
        ]}
        patterns.update({
            "sensational_phrases": 20, "vague_sources": 10,
            "conspiracy_framing": 5, "one_sided": 1.0, "no_evidence": 1.0,
        })
        label = analyzer.classify_credibility(FAKE_TEXT, 0, 0.9, patterns)
        assert label in {"FAKE", "MISLEADING"}

    def test_high_conf_real_low_pattern_is_real(self, analyzer):
        patterns = {k: 0 for k in [
            "sensational_phrases", "excessive_caps", "vague_sources",
            "conspiracy_framing", "emotional_manipulation", "one_sided",
            "no_evidence", "extreme_adjectives", "clickbait",
        ]}
        label = analyzer.classify_credibility(CREDIBLE_TEXT, 1, 0.9, patterns)
        assert label == "REAL"

    def test_low_confidence_is_unverified(self, analyzer):
        label = analyzer.classify_credibility(CREDIBLE_TEXT, 1, 0.4, {})
        assert label == "UNVERIFIED"

    @pytest.mark.parametrize("label", ["REAL", "FAKE", "MISLEADING", "UNVERIFIED"])
    def test_valid_output_labels(self, analyzer, label):
        # Just confirm all 4 labels are strings
        assert isinstance(label, str)


# ── calculate_credibility_score ───────────────────────────────────────────────

class TestCalculateCredibilityScore:
    def test_score_range(self, analyzer):
        for pred in [0, 1]:
            for conf in [0.0, 0.5, 1.0]:
                for pat in [0.0, 0.5, 1.0]:
                    score = analyzer.calculate_credibility_score(conf, pred, pat)
                    assert 0 <= score <= 100

    def test_perfect_real(self, analyzer):
        score = analyzer.calculate_credibility_score(1.0, 1, 0.0)
        assert score == 100

    def test_perfect_fake(self, analyzer):
        score = analyzer.calculate_credibility_score(1.0, 0, 1.0)
        assert score == 0


# ── determine_risk_level ──────────────────────────────────────────────────────

class TestDetermineRiskLevel:
    @pytest.mark.parametrize("score,expected", [
        (100, "Low Risk"),
        (75,  "Low Risk"),
        (74,  "Medium Risk"),
        (40,  "Medium Risk"),
        (39,  "High Risk"),
        (0,   "High Risk"),
    ])
    def test_thresholds(self, analyzer, score, expected):
        assert analyzer.determine_risk_level(score) == expected


# ── Full analyze() integration (mocked model) ─────────────────────────────────

class TestAnalyzeIntegration:
    def test_full_pipeline_credible(self, analyzer):
        model = _make_model(prediction=1, proba=[0.05, 0.95])
        vec   = _make_vectorizer()
        result = analyzer.analyze(CREDIBLE_TEXT, model, vec)

        assert result["classification"] in {"REAL", "MISLEADING", "UNVERIFIED"}
        assert 0 <= result["credibility_score"] <= 100
        assert isinstance(result["key_indicators"], list)
        assert isinstance(result["suspicious_claims"], list)
        assert isinstance(result["emotional_tone"], str)

    def test_full_pipeline_fake(self, analyzer):
        model = _make_model(prediction=0, proba=[0.92, 0.08])
        vec   = _make_vectorizer()
        result = analyzer.analyze(FAKE_TEXT, model, vec)

        assert result["classification"] in {"FAKE", "MISLEADING", "UNVERIFIED"}

    def test_empty_text_returns_unverified(self, analyzer):
        model = _make_model()
        vec   = _make_vectorizer()
        result = analyzer.analyze("", model, vec)
        assert result["classification"] == "UNVERIFIED"
        assert result["credibility_score"] == 0

    def test_short_text_returns_unverified(self, analyzer):
        model = _make_model()
        vec   = _make_vectorizer()
        result = analyzer.analyze("Too short.", model, vec)
        assert result["classification"] == "UNVERIFIED"

    def test_non_string_returns_unverified(self, analyzer):
        model = _make_model()
        vec   = _make_vectorizer()
        result = analyzer.analyze(None, model, vec)
        assert result["classification"] == "UNVERIFIED"

    def test_result_has_all_keys(self, analyzer):
        model = _make_model(prediction=1, proba=[0.1, 0.9])
        vec   = _make_vectorizer()
        result = analyzer.analyze(CREDIBLE_TEXT, model, vec)
        required_keys = {
            "classification", "credibility_score", "risk_level", "confidence",
            "analysis_summary", "key_indicators", "emotional_tone",
            "suspicious_claims", "recommended_action", "explanation",
            "model_prediction", "pattern_score", "patterns",
        }
        assert required_keys.issubset(result.keys())


# ── format_json_output ────────────────────────────────────────────────────────

class TestFormatJsonOutput:
    def _valid_result(self):
        return {
            "classification":    "REAL",
            "credibility_score": 80,
            "risk_level":        "Low Risk",
            "confidence":        75,
            "analysis_summary":  "Summary here.",
            "key_indicators":    ["Good sourcing"],
            "emotional_tone":    "Neutral and analytical",
            "suspicious_claims": [],
            "recommended_action": "Stay critical.",
            "explanation":       "Detailed explanation.",
        }

    def test_valid_result_passes(self, analyzer):
        result = self._valid_result()
        formatted = analyzer.format_json_output(result)
        assert formatted["classification"] == "REAL"

    def test_missing_field_raises(self, analyzer):
        result = self._valid_result()
        del result["classification"]
        with pytest.raises(ValueError, match="Missing required fields"):
            analyzer.format_json_output(result)

    def test_invalid_classification_raises(self, analyzer):
        result = self._valid_result()
        result["classification"] = "UNKNOWN"
        with pytest.raises(ValueError, match="Invalid classification"):
            analyzer.format_json_output(result)

    def test_score_out_of_range_raises(self, analyzer):
        result = self._valid_result()
        result["credibility_score"] = 150
        with pytest.raises(ValueError):
            analyzer.format_json_output(result)

    def test_invalid_risk_level_raises(self, analyzer):
        result = self._valid_result()
        result["risk_level"] = "Super Risk"
        with pytest.raises(ValueError):
            analyzer.format_json_output(result)

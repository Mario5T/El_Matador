"""
Unit tests for the CredibilityAnalyzer class.
"""

from credibility_analyzer import CredibilityAnalyzer


def test_calculate_pattern_score_empty_patterns():
    """Test pattern score calculation with empty patterns."""
    analyzer = CredibilityAnalyzer()
    patterns = {
        "sensational_phrases": 0,
        "excessive_caps": 0.0,
        "vague_sources": 0,
        "conspiracy_framing": 0,
        "emotional_manipulation": 0,
        "one_sided": 0.0,
        "no_evidence": 0.0,
        "extreme_adjectives": 0,
        "clickbait": 0
    }
    score = analyzer.calculate_pattern_score(patterns)
    assert score == 0.0, f"Expected 0.0, got {score}"
    assert 0.0 <= score <= 1.0, f"Score {score} out of range [0.0, 1.0]"
    print("✓ test_calculate_pattern_score_empty_patterns passed")


def test_calculate_pattern_score_high_patterns():
    """Test pattern score calculation with high pattern values."""
    analyzer = CredibilityAnalyzer()
    patterns = {
        "sensational_phrases": 10,
        "excessive_caps": 0.5,
        "vague_sources": 5,
        "conspiracy_framing": 3,
        "emotional_manipulation": 8,
        "one_sided": 0.9,
        "no_evidence": 0.8,
        "extreme_adjectives": 12,
        "clickbait": 4
    }
    score = analyzer.calculate_pattern_score(patterns)
    assert 0.0 <= score <= 1.0, f"Score {score} out of range [0.0, 1.0]"
    assert score > 0.5, f"Expected score > 0.5 with high patterns, got {score}"
    print("✓ test_calculate_pattern_score_high_patterns passed")


def test_calculate_pattern_score_range():
    """Test that pattern score is always in valid range."""
    analyzer = CredibilityAnalyzer()
    patterns = {
        "sensational_phrases": 3,
        "excessive_caps": 0.2,
        "vague_sources": 2,
        "conspiracy_framing": 1,
        "emotional_manipulation": 2,
        "one_sided": 0.5,
        "no_evidence": 0.6,
        "extreme_adjectives": 4,
        "clickbait": 1
    }
    score = analyzer.calculate_pattern_score(patterns)
    assert 0.0 <= score <= 1.0, f"Score {score} out of range [0.0, 1.0]"
    print("✓ test_calculate_pattern_score_range passed")


def test_classify_credibility_insufficient_text():
    """Test classification with insufficient text (< 50 chars)."""
    analyzer = CredibilityAnalyzer()
    short_text = "Too short"
    patterns = {}
    classification = analyzer.classify_credibility(short_text, 1, 0.9, patterns)
    assert classification == "UNVERIFIED", f"Expected UNVERIFIED, got {classification}"
    print("✓ test_classify_credibility_insufficient_text passed")


def test_classify_credibility_fake_high_confidence():
    """Test classification when model predicts fake with high confidence."""
    analyzer = CredibilityAnalyzer()
    text = "This is a long enough text for analysis with more than fifty characters."
    patterns = {
        "sensational_phrases": 10,
        "excessive_caps": 0.3,
        "vague_sources": 5,
        "conspiracy_framing": 3,
        "emotional_manipulation": 8,
        "one_sided": 0.9,
        "no_evidence": 0.8,
        "extreme_adjectives": 12,
        "clickbait": 4
    }
    classification = analyzer.classify_credibility(text, 0, 0.85, patterns)
    assert classification == "FAKE", f"Expected FAKE, got {classification}"
    print("✓ test_classify_credibility_fake_high_confidence passed")


def test_classify_credibility_real_high_confidence():
    """Test classification when model predicts real with high confidence."""
    analyzer = CredibilityAnalyzer()
    text = "This is a long enough text for analysis with more than fifty characters."
    patterns = {
        "sensational_phrases": 0,
        "excessive_caps": 0.0,
        "vague_sources": 0,
        "conspiracy_framing": 0,
        "emotional_manipulation": 0,
        "one_sided": 0.1,
        "no_evidence": 0.2,
        "extreme_adjectives": 0,
        "clickbait": 0
    }
    classification = analyzer.classify_credibility(text, 1, 0.85, patterns)
    assert classification == "REAL", f"Expected REAL, got {classification}"
    print("✓ test_classify_credibility_real_high_confidence passed")


def test_classify_credibility_misleading():
    """Test classification for misleading content."""
    analyzer = CredibilityAnalyzer()
    text = "This is a long enough text for analysis with more than fifty characters."
    patterns = {
        "sensational_phrases": 2,
        "excessive_caps": 0.1,
        "vague_sources": 2,
        "conspiracy_framing": 0,
        "emotional_manipulation": 1,
        "one_sided": 0.5,
        "no_evidence": 0.5,
        "extreme_adjectives": 3,
        "clickbait": 1
    }
    classification = analyzer.classify_credibility(text, 1, 0.85, patterns)
    assert classification == "MISLEADING", f"Expected MISLEADING, got {classification}"
    print("✓ test_classify_credibility_misleading passed")


def test_classify_credibility_low_confidence():
    """Test classification with low model confidence."""
    analyzer = CredibilityAnalyzer()
    text = "This is a long enough text for analysis with more than fifty characters."
    patterns = {}
    classification = analyzer.classify_credibility(text, 1, 0.3, patterns)
    assert classification == "UNVERIFIED", f"Expected UNVERIFIED, got {classification}"
    print("✓ test_classify_credibility_low_confidence passed")


def test_classify_credibility_valid_values():
    """Test that classification always returns valid values."""
    analyzer = CredibilityAnalyzer()
    text = "This is a long enough text for analysis with more than fifty characters."
    patterns = {}
    valid_classifications = {"REAL", "FAKE", "MISLEADING", "UNVERIFIED"}
    
    # Test various combinations
    for prediction in [0, 1]:
        for confidence in [0.3, 0.6, 0.9]:
            classification = analyzer.classify_credibility(
                text, prediction, confidence, patterns
            )
            assert classification in valid_classifications, \
                f"Invalid classification: {classification}"
    print("✓ test_classify_credibility_valid_values passed")


def test_calculate_credibility_score_real_prediction():
    """Test credibility score calculation with real prediction."""
    analyzer = CredibilityAnalyzer()
    score = analyzer.calculate_credibility_score(0.9, 1, 0.2)
    assert 0 <= score <= 100, f"Score {score} out of range [0, 100]"
    assert score > 50, f"Expected score > 50 for real prediction, got {score}"
    print("✓ test_calculate_credibility_score_real_prediction passed")


def test_calculate_credibility_score_fake_prediction():
    """Test credibility score calculation with fake prediction."""
    analyzer = CredibilityAnalyzer()
    score = analyzer.calculate_credibility_score(0.9, 0, 0.8)
    assert 0 <= score <= 100, f"Score {score} out of range [0, 100]"
    assert score < 50, f"Expected score < 50 for fake prediction, got {score}"
    print("✓ test_calculate_credibility_score_fake_prediction passed")


def test_calculate_credibility_score_range():
    """Test that credibility score is always in valid range [0, 100]."""
    analyzer = CredibilityAnalyzer()
    # Test various combinations
    for prediction in [0, 1]:
        for confidence in [0.0, 0.5, 1.0]:
            for pattern_score in [0.0, 0.5, 1.0]:
                score = analyzer.calculate_credibility_score(
                    confidence, prediction, pattern_score
                )
                assert 0 <= score <= 100, f"Score {score} out of range [0, 100]"
                assert isinstance(score, int), f"Score {score} is not an integer"
    print("✓ test_calculate_credibility_score_range passed")


def test_calculate_credibility_score_pattern_penalty():
    """Test that higher pattern scores reduce credibility score."""
    analyzer = CredibilityAnalyzer()
    # Same model prediction and confidence, different pattern scores
    score_low_patterns = analyzer.calculate_credibility_score(0.8, 1, 0.1)
    score_high_patterns = analyzer.calculate_credibility_score(0.8, 1, 0.9)
    
    assert score_low_patterns > score_high_patterns, \
        f"Expected {score_low_patterns} > {score_high_patterns}"
    print("✓ test_calculate_credibility_score_pattern_penalty passed")


def test_calculate_credibility_score_model_prediction_effect():
    """Test that model prediction of 1 (credible) increases base score."""
    analyzer = CredibilityAnalyzer()
    # Same confidence and patterns, different predictions
    score_fake = analyzer.calculate_credibility_score(0.8, 0, 0.3)
    score_real = analyzer.calculate_credibility_score(0.8, 1, 0.3)
    
    assert score_real > score_fake, f"Expected {score_real} > {score_fake}"
    print("✓ test_calculate_credibility_score_model_prediction_effect passed")


if __name__ == "__main__":
    test_calculate_pattern_score_empty_patterns()
    test_calculate_pattern_score_high_patterns()
    test_calculate_pattern_score_range()
    test_classify_credibility_insufficient_text()
    test_classify_credibility_fake_high_confidence()
    test_classify_credibility_real_high_confidence()
    test_classify_credibility_misleading()
    test_classify_credibility_low_confidence()
    test_classify_credibility_valid_values()
    test_calculate_credibility_score_real_prediction()
    test_calculate_credibility_score_fake_prediction()
    test_calculate_credibility_score_range()
    test_calculate_credibility_score_pattern_penalty()
    test_calculate_credibility_score_model_prediction_effect()
    
    print("\n✅ All tests passed!")

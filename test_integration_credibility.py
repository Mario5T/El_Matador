"""
Integration test to verify CredibilityAnalyzer works with PatternDetector.
"""

from credibility_analyzer import CredibilityAnalyzer
from pattern_detector import PatternDetector


def test_integration_with_pattern_detector():
    """Test that CredibilityAnalyzer integrates correctly with PatternDetector."""
    analyzer = CredibilityAnalyzer()
    detector = PatternDetector()
    
    # Test with a fake news-like text
    fake_text = """
    SHOCKING REVELATION! Sources say that experts claim this UNBELIEVABLE truth
    has been HIDDEN from you! The mainstream media doesn't want you to know about
    this DEVASTATING cover-up. Wake up sheeple! This is absolutely terrifying and
    completely outrageous. You won't believe what happened next!
    """
    
    # Detect patterns
    patterns = detector.detect_patterns(fake_text)
    
    # Verify patterns were detected
    assert patterns["sensational_phrases"] > 0
    assert patterns["vague_sources"] > 0
    assert patterns["conspiracy_framing"] > 0
    
    # Calculate pattern score
    pattern_score = analyzer.calculate_pattern_score(patterns)
    assert 0.0 <= pattern_score <= 1.0
    assert pattern_score > 0.3  # Should be high for this text
    
    # Test classification
    classification = analyzer.classify_credibility(fake_text, 0, 0.9, patterns)
    assert classification in ["FAKE", "MISLEADING"]
    
    # Test credibility score
    score = analyzer.calculate_credibility_score(0.9, 0, pattern_score)
    assert 0 <= score <= 100
    assert score < 50  # Should be low for fake prediction
    
    print("✓ test_integration_with_pattern_detector passed")


def test_integration_with_credible_text():
    """Test with credible-looking text."""
    analyzer = CredibilityAnalyzer()
    detector = PatternDetector()
    
    # Test with a credible news-like text
    credible_text = """
    According to a study published in the Journal of Science, researchers at
    Stanford University found that 65 percent of participants showed improvement.
    The research, led by Dr. Jane Smith, analyzed data from over 1,000 subjects.
    However, the study also noted some limitations in the methodology. Despite
    these concerns, the findings suggest potential applications in healthcare.
    """
    
    # Detect patterns
    patterns = detector.detect_patterns(credible_text)
    
    # Verify low pattern detection
    assert patterns["sensational_phrases"] == 0
    assert patterns["vague_sources"] == 0
    assert patterns["conspiracy_framing"] == 0
    
    # Calculate pattern score
    pattern_score = analyzer.calculate_pattern_score(patterns)
    assert 0.0 <= pattern_score <= 1.0
    assert pattern_score < 0.5  # Should be low for this text
    
    # Test classification
    classification = analyzer.classify_credibility(credible_text, 1, 0.9, patterns)
    assert classification in ["REAL", "MISLEADING"]
    
    # Test credibility score
    score = analyzer.calculate_credibility_score(0.9, 1, pattern_score)
    assert 0 <= score <= 100
    assert score > 50  # Should be high for real prediction
    
    print("✓ test_integration_with_credible_text passed")


if __name__ == "__main__":
    test_integration_with_pattern_detector()
    test_integration_with_credible_text()
    
    print("\n✅ All integration tests passed!")

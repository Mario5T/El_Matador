"""
Test script for Task 8: Key indicator extraction and text generation methods.
"""

from credibility_analyzer import CredibilityAnalyzer


def test_extract_key_indicators():
    """Test the extract_key_indicators method."""
    analyzer = CredibilityAnalyzer()
    
    # Test with high suspicious patterns
    patterns_high = {
        "sensational_phrases": 5,
        "excessive_caps": 0.15,
        "vague_sources": 3,
        "conspiracy_framing": 2,
        "emotional_manipulation": 4,
        "one_sided": 0.8,
        "no_evidence": 0.75,
        "extreme_adjectives": 7,
        "clickbait": 2
    }
    
    indicators = analyzer.extract_key_indicators(patterns_high, "test text")
    print("Test 1 - High suspicious patterns:")
    print(f"  Indicators count: {len(indicators)}")
    print(f"  Indicators: {indicators}")
    assert len(indicators) > 0, "Should have at least one indicator"
    assert "High use of sensational language" in indicators
    assert "Excessive capitalization detected" in indicators
    print("  ✓ Passed\n")
    
    # Test with low/no patterns (should return default indicators)
    patterns_low = {
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
    
    indicators = analyzer.extract_key_indicators(patterns_low, "test text")
    print("Test 2 - Low/no patterns:")
    print(f"  Indicators count: {len(indicators)}")
    print(f"  Indicators: {indicators}")
    assert len(indicators) > 0, "Should always have at least one indicator"
    assert "Balanced language and structure" in indicators
    print("  ✓ Passed\n")


def test_generate_analysis_summary():
    """Test the generate_analysis_summary method."""
    analyzer = CredibilityAnalyzer()
    
    # Test FAKE classification
    summary = analyzer.generate_analysis_summary(
        "FAKE",
        25,
        ["High use of sensational language", "Multiple vague source references"]
    )
    print("Test 3 - FAKE classification summary:")
    print(f"  Summary: {summary}")
    assert "FAKE" in summary or "misinformation" in summary
    assert "25/100" in summary
    assert len(summary.split(". ")) >= 2, "Should have 2-4 sentences"
    print("  ✓ Passed\n")
    
    # Test REAL classification
    summary = analyzer.generate_analysis_summary(
        "REAL",
        85,
        ["Balanced language and structure", "Appropriate use of sources"]
    )
    print("Test 4 - REAL classification summary:")
    print(f"  Summary: {summary}")
    assert "credible" in summary.lower()
    assert "85/100" in summary
    print("  ✓ Passed\n")


def test_generate_recommended_action():
    """Test the generate_recommended_action method."""
    analyzer = CredibilityAnalyzer()
    
    # Test High Risk
    action = analyzer.generate_recommended_action("High Risk")
    print("Test 5 - High Risk action:")
    print(f"  Action: {action}")
    assert "caution" in action.lower() or "verify" in action.lower()
    print("  ✓ Passed\n")
    
    # Test Medium Risk
    action = analyzer.generate_recommended_action("Medium Risk")
    print("Test 6 - Medium Risk action:")
    print(f"  Action: {action}")
    assert "caution" in action.lower() or "cross-reference" in action.lower()
    print("  ✓ Passed\n")
    
    # Test Low Risk
    action = analyzer.generate_recommended_action("Low Risk")
    print("Test 7 - Low Risk action:")
    print(f"  Action: {action}")
    assert "credible" in action.lower() or "appears" in action.lower()
    print("  ✓ Passed\n")


def test_generate_explanation():
    """Test the generate_explanation method."""
    analyzer = CredibilityAnalyzer()
    
    patterns = {
        "sensational_phrases": 5,
        "excessive_caps": 0.15,
        "vague_sources": 3,
        "conspiracy_framing": 2,
        "emotional_manipulation": 4,
        "one_sided": 0.8,
        "no_evidence": 0.75,
        "extreme_adjectives": 7,
        "clickbait": 2
    }
    
    indicators = [
        "High use of sensational language",
        "Multiple vague source references",
        "Emotional manipulation tactics detected"
    ]
    
    explanation = analyzer.generate_explanation("FAKE", 25, patterns, indicators)
    print("Test 8 - Detailed explanation:")
    print(f"  Explanation length: {len(explanation)} chars")
    print(f"  Explanation: {explanation[:200]}...")
    assert "FAKE" in explanation
    assert "25/100" in explanation
    assert "pattern" in explanation.lower()
    assert len(explanation) > 100, "Should be a detailed explanation"
    print("  ✓ Passed\n")


if __name__ == "__main__":
    print("=" * 70)
    print("Testing Task 8: Key Indicator Extraction and Text Generation")
    print("=" * 70 + "\n")
    
    test_extract_key_indicators()
    test_generate_analysis_summary()
    test_generate_recommended_action()
    test_generate_explanation()
    
    print("=" * 70)
    print("All tests passed! ✓")
    print("=" * 70)

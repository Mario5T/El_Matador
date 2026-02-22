"""
Integration test for Task 8 methods with the full CredibilityAnalyzer.
"""

from credibility_analyzer import CredibilityAnalyzer


def test_full_workflow():
    """Test the full workflow using all Task 8 methods together."""
    analyzer = CredibilityAnalyzer()
    
    # Simulate a suspicious article analysis
    patterns = {
        "sensational_phrases": 6,
        "excessive_caps": 0.12,
        "vague_sources": 4,
        "conspiracy_framing": 1,
        "emotional_manipulation": 5,
        "one_sided": 0.85,
        "no_evidence": 0.8,
        "extreme_adjectives": 8,
        "clickbait": 1
    }
    
    # Calculate pattern score
    pattern_score = analyzer.calculate_pattern_score(patterns)
    print(f"Pattern score: {pattern_score:.2f}")
    
    # Classify credibility
    classification = analyzer.classify_credibility(
        "This is a test article with sufficient length for analysis.",
        0,  # Model predicts fake
        0.85,  # High confidence
        patterns
    )
    print(f"Classification: {classification}")
    
    # Calculate credibility score
    credibility_score = analyzer.calculate_credibility_score(0.85, 0, pattern_score)
    print(f"Credibility score: {credibility_score}")
    
    # Determine risk level
    risk_level = analyzer.determine_risk_level(credibility_score)
    print(f"Risk level: {risk_level}")
    
    # Extract key indicators (Task 8)
    key_indicators = analyzer.extract_key_indicators(patterns, "test text")
    print(f"Key indicators ({len(key_indicators)}): {key_indicators[:3]}")
    
    # Generate analysis summary (Task 8)
    summary = analyzer.generate_analysis_summary(classification, credibility_score, key_indicators)
    print(f"\nAnalysis Summary:\n{summary}")
    
    # Generate recommended action (Task 8)
    action = analyzer.generate_recommended_action(risk_level)
    print(f"\nRecommended Action:\n{action}")
    
    # Generate explanation (Task 8)
    explanation = analyzer.generate_explanation(classification, credibility_score, patterns, key_indicators)
    print(f"\nExplanation:\n{explanation}")
    
    # Verify all outputs are valid
    assert classification in ["REAL", "FAKE", "MISLEADING", "UNVERIFIED"]
    assert 0 <= credibility_score <= 100
    assert risk_level in ["Low Risk", "Medium Risk", "High Risk"]
    assert len(key_indicators) > 0
    assert len(summary) > 0
    assert len(action) > 0
    assert len(explanation) > 0
    
    # Verify summary is 2-4 sentences
    sentence_count = len([s for s in summary.split(". ") if s.strip()])
    assert 2 <= sentence_count <= 5, f"Summary should have 2-4 sentences, got {sentence_count}"
    
    print("\n✓ Full workflow integration test passed!")


def test_edge_cases():
    """Test edge cases for Task 8 methods."""
    analyzer = CredibilityAnalyzer()
    
    # Test with empty patterns
    empty_patterns = {}
    indicators = analyzer.extract_key_indicators(empty_patterns, "test")
    assert len(indicators) > 0, "Should return default indicators for empty patterns"
    print(f"✓ Empty patterns handled: {indicators}")
    
    # Test with UNVERIFIED classification
    summary = analyzer.generate_analysis_summary("UNVERIFIED", 50, ["Insufficient information"])
    assert "cannot be reliably assessed" in summary or "UNVERIFIED" in summary
    print(f"✓ UNVERIFIED summary: {summary[:100]}...")
    
    # Test with MISLEADING classification
    summary = analyzer.generate_analysis_summary("MISLEADING", 55, ["Mixed signals"])
    assert "misleading" in summary.lower()
    print(f"✓ MISLEADING summary: {summary[:100]}...")
    
    # Test explanation with minimal patterns
    minimal_patterns = {
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
    explanation = analyzer.generate_explanation("REAL", 90, minimal_patterns, ["Balanced language"])
    assert "REAL" in explanation
    assert "90/100" in explanation
    print(f"✓ Minimal patterns explanation: {explanation[:100]}...")
    
    print("\n✓ All edge cases handled correctly!")


if __name__ == "__main__":
    print("=" * 70)
    print("Integration Test for Task 8 Methods")
    print("=" * 70 + "\n")
    
    test_full_workflow()
    print("\n" + "=" * 70 + "\n")
    test_edge_cases()
    
    print("\n" + "=" * 70)
    print("All integration tests passed! ✓")
    print("=" * 70)

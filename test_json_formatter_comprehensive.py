"""
Comprehensive test for JSON formatter without requiring model files.
"""

import json
from credibility_analyzer import CredibilityAnalyzer


def test_all_classification_types():
    """Test format_json_output with all valid classification types."""
    analyzer = CredibilityAnalyzer()
    
    classifications = ["REAL", "FAKE", "MISLEADING", "UNVERIFIED"]
    
    for classification in classifications:
        result = {
            "classification": classification,
            "credibility_score": 50,
            "risk_level": "Medium Risk",
            "confidence": 60,
            "analysis_summary": f"Test for {classification}",
            "key_indicators": ["Test indicator"],
            "emotional_tone": "Neutral",
            "suspicious_claims": [],
            "recommended_action": "Test action",
            "explanation": "Test explanation"
        }
        
        formatted = analyzer.format_json_output(result)
        assert formatted["classification"] == classification
        print(f"✓ Classification '{classification}' validated")


def test_all_risk_levels():
    """Test format_json_output with all valid risk levels."""
    analyzer = CredibilityAnalyzer()
    
    risk_levels = ["Low Risk", "Medium Risk", "High Risk"]
    
    for risk_level in risk_levels:
        result = {
            "classification": "REAL",
            "credibility_score": 50,
            "risk_level": risk_level,
            "confidence": 60,
            "analysis_summary": f"Test for {risk_level}",
            "key_indicators": ["Test indicator"],
            "emotional_tone": "Neutral",
            "suspicious_claims": [],
            "recommended_action": "Test action",
            "explanation": "Test explanation"
        }
        
        formatted = analyzer.format_json_output(result)
        assert formatted["risk_level"] == risk_level
        print(f"✓ Risk level '{risk_level}' validated")


def test_score_boundaries():
    """Test format_json_output with boundary score values."""
    analyzer = CredibilityAnalyzer()
    
    test_scores = [0, 1, 50, 99, 100]
    
    for score in test_scores:
        result = {
            "classification": "REAL",
            "credibility_score": score,
            "risk_level": "Low Risk",
            "confidence": score,
            "analysis_summary": "Test",
            "key_indicators": ["Test"],
            "emotional_tone": "Neutral",
            "suspicious_claims": [],
            "recommended_action": "Action",
            "explanation": "Explanation"
        }
        
        formatted = analyzer.format_json_output(result)
        assert formatted["credibility_score"] == score
        assert formatted["confidence"] == score
        print(f"✓ Score {score} validated")


def test_empty_lists():
    """Test format_json_output with empty lists."""
    analyzer = CredibilityAnalyzer()
    
    result = {
        "classification": "REAL",
        "credibility_score": 80,
        "risk_level": "Low Risk",
        "confidence": 85,
        "analysis_summary": "Test",
        "key_indicators": [],  # Empty list
        "emotional_tone": "Neutral",
        "suspicious_claims": [],  # Empty list
        "recommended_action": "Action",
        "explanation": "Explanation"
    }
    
    formatted = analyzer.format_json_output(result)
    assert formatted["key_indicators"] == []
    assert formatted["suspicious_claims"] == []
    print("✓ Empty lists validated")


def test_large_lists():
    """Test format_json_output with large lists."""
    analyzer = CredibilityAnalyzer()
    
    result = {
        "classification": "FAKE",
        "credibility_score": 20,
        "risk_level": "High Risk",
        "confidence": 75,
        "analysis_summary": "Test",
        "key_indicators": [f"Indicator {i}" for i in range(10)],
        "emotional_tone": "Highly emotional",
        "suspicious_claims": [f"Claim {i}" for i in range(5)],
        "recommended_action": "Action",
        "explanation": "Explanation"
    }
    
    formatted = analyzer.format_json_output(result)
    assert len(formatted["key_indicators"]) == 10
    assert len(formatted["suspicious_claims"]) == 5
    print("✓ Large lists validated")


def test_json_serialization():
    """Test that formatted output is JSON serializable."""
    analyzer = CredibilityAnalyzer()
    
    result = {
        "classification": "MISLEADING",
        "credibility_score": 55,
        "risk_level": "Medium Risk",
        "confidence": 70,
        "analysis_summary": "This article contains misleading elements.",
        "key_indicators": [
            "High use of sensational language",
            "Multiple vague source references",
            "Emotional manipulation tactics detected"
        ],
        "emotional_tone": "Moderately emotional",
        "suspicious_claims": [
            "Sources say this is unprecedented",
            "Experts claim this will change everything"
        ],
        "recommended_action": "Approach with caution and verify claims",
        "explanation": "The article shows patterns of misinformation."
    }
    
    formatted = analyzer.format_json_output(result)
    
    # Serialize to JSON
    json_string = json.dumps(formatted, indent=2)
    assert len(json_string) > 0
    
    # Deserialize back
    parsed = json.loads(json_string)
    assert parsed == formatted
    
    # Verify structure
    assert isinstance(parsed["classification"], str)
    assert isinstance(parsed["credibility_score"], int)
    assert isinstance(parsed["key_indicators"], list)
    
    print("✓ JSON serialization/deserialization validated")


def test_unicode_and_special_characters():
    """Test format_json_output with unicode and special characters."""
    analyzer = CredibilityAnalyzer()
    
    result = {
        "classification": "REAL",
        "credibility_score": 75,
        "risk_level": "Low Risk",
        "confidence": 80,
        "analysis_summary": "Test with émojis 🔍 and spëcial çharacters",
        "key_indicators": ["Indicator with 中文", "Indicator with العربية"],
        "emotional_tone": "Neutral with 'quotes' and \"double quotes\"",
        "suspicious_claims": ["Claim with newline\ncharacter"],
        "recommended_action": "Action with tab\tcharacter",
        "explanation": "Explanation with backslash \\ and forward slash /"
    }
    
    formatted = analyzer.format_json_output(result)
    
    # Should be JSON serializable
    json_string = json.dumps(formatted, ensure_ascii=False)
    parsed = json.loads(json_string)
    
    assert "émojis" in parsed["analysis_summary"]
    assert "中文" in parsed["key_indicators"][0]
    
    print("✓ Unicode and special characters validated")


if __name__ == "__main__":
    print("Running comprehensive JSON formatter tests...\n")
    
    test_all_classification_types()
    print()
    test_all_risk_levels()
    print()
    test_score_boundaries()
    print()
    test_empty_lists()
    test_large_lists()
    test_json_serialization()
    test_unicode_and_special_characters()
    
    print("\n✅ All comprehensive tests passed!")

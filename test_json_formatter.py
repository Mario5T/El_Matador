"""
Test script for JSON formatter validation.
"""

from credibility_analyzer import CredibilityAnalyzer


def test_format_json_output_valid():
    """Test format_json_output with valid input."""
    analyzer = CredibilityAnalyzer()
    
    # Valid analysis result
    valid_result = {
        "classification": "MISLEADING",
        "credibility_score": 55,
        "risk_level": "Medium Risk",
        "confidence": 70,
        "analysis_summary": "This is a test summary.",
        "key_indicators": ["Indicator 1", "Indicator 2"],
        "emotional_tone": "Neutral",
        "suspicious_claims": ["Claim 1"],
        "recommended_action": "Verify claims",
        "explanation": "Detailed explanation here."
    }
    
    formatted = analyzer.format_json_output(valid_result)
    
    # Verify all fields are present
    assert "classification" in formatted
    assert "credibility_score" in formatted
    assert "risk_level" in formatted
    assert "confidence" in formatted
    assert "analysis_summary" in formatted
    assert "key_indicators" in formatted
    assert "emotional_tone" in formatted
    assert "suspicious_claims" in formatted
    assert "recommended_action" in formatted
    assert "explanation" in formatted
    
    # Verify values match
    assert formatted["classification"] == "MISLEADING"
    assert formatted["credibility_score"] == 55
    assert formatted["risk_level"] == "Medium Risk"
    
    print("✓ Valid input test passed")


def test_format_json_output_missing_field():
    """Test format_json_output with missing field."""
    analyzer = CredibilityAnalyzer()
    
    # Missing 'explanation' field
    invalid_result = {
        "classification": "REAL",
        "credibility_score": 85,
        "risk_level": "Low Risk",
        "confidence": 90,
        "analysis_summary": "Test summary",
        "key_indicators": ["Indicator"],
        "emotional_tone": "Neutral",
        "suspicious_claims": [],
        "recommended_action": "Action"
        # Missing 'explanation'
    }
    
    try:
        analyzer.format_json_output(invalid_result)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Missing required fields" in str(e)
        assert "explanation" in str(e)
        print("✓ Missing field test passed")


def test_format_json_output_invalid_type():
    """Test format_json_output with invalid data type."""
    analyzer = CredibilityAnalyzer()
    
    # credibility_score should be int, not string
    invalid_result = {
        "classification": "FAKE",
        "credibility_score": "25",  # Wrong type
        "risk_level": "High Risk",
        "confidence": 80,
        "analysis_summary": "Test",
        "key_indicators": ["Test"],
        "emotional_tone": "Emotional",
        "suspicious_claims": [],
        "recommended_action": "Action",
        "explanation": "Explanation"
    }
    
    try:
        analyzer.format_json_output(invalid_result)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "incorrect type" in str(e)
        assert "credibility_score" in str(e)
        print("✓ Invalid type test passed")


def test_format_json_output_invalid_classification():
    """Test format_json_output with invalid classification value."""
    analyzer = CredibilityAnalyzer()
    
    invalid_result = {
        "classification": "INVALID",  # Not in valid set
        "credibility_score": 50,
        "risk_level": "Medium Risk",
        "confidence": 60,
        "analysis_summary": "Test",
        "key_indicators": ["Test"],
        "emotional_tone": "Neutral",
        "suspicious_claims": [],
        "recommended_action": "Action",
        "explanation": "Explanation"
    }
    
    try:
        analyzer.format_json_output(invalid_result)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid classification value" in str(e)
        print("✓ Invalid classification test passed")


def test_format_json_output_score_out_of_range():
    """Test format_json_output with score out of valid range."""
    analyzer = CredibilityAnalyzer()
    
    invalid_result = {
        "classification": "REAL",
        "credibility_score": 150,  # Out of range
        "risk_level": "Low Risk",
        "confidence": 90,
        "analysis_summary": "Test",
        "key_indicators": ["Test"],
        "emotional_tone": "Neutral",
        "suspicious_claims": [],
        "recommended_action": "Action",
        "explanation": "Explanation"
    }
    
    try:
        analyzer.format_json_output(invalid_result)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must be in range [0, 100]" in str(e)
        print("✓ Score out of range test passed")


def test_format_json_output_invalid_list_items():
    """Test format_json_output with non-string items in list."""
    analyzer = CredibilityAnalyzer()
    
    invalid_result = {
        "classification": "MISLEADING",
        "credibility_score": 45,
        "risk_level": "Medium Risk",
        "confidence": 65,
        "analysis_summary": "Test",
        "key_indicators": ["Valid", 123],  # Non-string item
        "emotional_tone": "Neutral",
        "suspicious_claims": [],
        "recommended_action": "Action",
        "explanation": "Explanation"
    }
    
    try:
        analyzer.format_json_output(invalid_result)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must be strings" in str(e)
        print("✓ Invalid list items test passed")


if __name__ == "__main__":
    print("Testing JSON formatter validation...\n")
    
    test_format_json_output_valid()
    test_format_json_output_missing_field()
    test_format_json_output_invalid_type()
    test_format_json_output_invalid_classification()
    test_format_json_output_score_out_of_range()
    test_format_json_output_invalid_list_items()
    
    print("\n✅ All JSON formatter tests passed!")

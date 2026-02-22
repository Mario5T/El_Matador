"""
Test that format_json_output meets all requirements from Requirement 14.
"""

import json
from credibility_analyzer import CredibilityAnalyzer


def test_requirement_14_1():
    """
    Requirement 14.1: THE JSON_Formatter SHALL output valid JSON conforming 
    to the specified schema
    """
    analyzer = CredibilityAnalyzer()
    
    result = {
        "classification": "REAL",
        "credibility_score": 85,
        "risk_level": "Low Risk",
        "confidence": 90,
        "analysis_summary": "Test summary",
        "key_indicators": ["Indicator 1"],
        "emotional_tone": "Neutral",
        "suspicious_claims": [],
        "recommended_action": "Action",
        "explanation": "Explanation"
    }
    
    formatted = analyzer.format_json_output(result)
    
    # Must be valid JSON
    json_string = json.dumps(formatted)
    parsed = json.loads(json_string)
    
    assert parsed == formatted
    print("✓ Requirement 14.1: Valid JSON output confirmed")


def test_requirement_14_2():
    """
    Requirement 14.2: THE JSON_Formatter SHALL include exactly these fields: 
    classification, credibility_score, risk_level, confidence, analysis_summary, 
    key_indicators, emotional_tone, suspicious_claims, recommended_action, explanation
    """
    analyzer = CredibilityAnalyzer()
    
    result = {
        "classification": "FAKE",
        "credibility_score": 25,
        "risk_level": "High Risk",
        "confidence": 80,
        "analysis_summary": "Test",
        "key_indicators": ["Test"],
        "emotional_tone": "Emotional",
        "suspicious_claims": ["Claim"],
        "recommended_action": "Action",
        "explanation": "Explanation"
    }
    
    formatted = analyzer.format_json_output(result)
    
    # Check all required fields are present
    required_fields = [
        "classification", "credibility_score", "risk_level", "confidence",
        "analysis_summary", "key_indicators", "emotional_tone", 
        "suspicious_claims", "recommended_action", "explanation"
    ]
    
    for field in required_fields:
        assert field in formatted, f"Missing field: {field}"
    
    # Check no extra fields
    assert len(formatted) == len(required_fields)
    
    print("✓ Requirement 14.2: All required fields present, no extra fields")


def test_requirement_14_3():
    """
    Requirement 14.3: THE JSON_Formatter SHALL use string type for: 
    classification, risk_level, analysis_summary, emotional_tone, 
    recommended_action, explanation
    """
    analyzer = CredibilityAnalyzer()
    
    result = {
        "classification": "MISLEADING",
        "credibility_score": 50,
        "risk_level": "Medium Risk",
        "confidence": 65,
        "analysis_summary": "Summary text",
        "key_indicators": ["Indicator"],
        "emotional_tone": "Tone text",
        "suspicious_claims": [],
        "recommended_action": "Action text",
        "explanation": "Explanation text"
    }
    
    formatted = analyzer.format_json_output(result)
    
    # Verify string types
    string_fields = [
        "classification", "risk_level", "analysis_summary", 
        "emotional_tone", "recommended_action", "explanation"
    ]
    
    for field in string_fields:
        assert isinstance(formatted[field], str), f"{field} is not a string"
    
    print("✓ Requirement 14.3: String type fields validated")


def test_requirement_14_4():
    """
    Requirement 14.4: THE JSON_Formatter SHALL use integer type for: 
    credibility_score, confidence
    """
    analyzer = CredibilityAnalyzer()
    
    result = {
        "classification": "REAL",
        "credibility_score": 88,
        "risk_level": "Low Risk",
        "confidence": 92,
        "analysis_summary": "Test",
        "key_indicators": ["Test"],
        "emotional_tone": "Neutral",
        "suspicious_claims": [],
        "recommended_action": "Action",
        "explanation": "Explanation"
    }
    
    formatted = analyzer.format_json_output(result)
    
    # Verify integer types
    assert isinstance(formatted["credibility_score"], int)
    assert isinstance(formatted["confidence"], int)
    
    # Verify they're not floats
    assert not isinstance(formatted["credibility_score"], float)
    assert not isinstance(formatted["confidence"], float)
    
    print("✓ Requirement 14.4: Integer type fields validated")


def test_requirement_14_5():
    """
    Requirement 14.5: THE JSON_Formatter SHALL use array type for: 
    key_indicators, suspicious_claims
    """
    analyzer = CredibilityAnalyzer()
    
    result = {
        "classification": "FAKE",
        "credibility_score": 30,
        "risk_level": "High Risk",
        "confidence": 75,
        "analysis_summary": "Test",
        "key_indicators": ["Indicator 1", "Indicator 2"],
        "emotional_tone": "Emotional",
        "suspicious_claims": ["Claim 1", "Claim 2", "Claim 3"],
        "recommended_action": "Action",
        "explanation": "Explanation"
    }
    
    formatted = analyzer.format_json_output(result)
    
    # Verify array types
    assert isinstance(formatted["key_indicators"], list)
    assert isinstance(formatted["suspicious_claims"], list)
    
    # Verify all items are strings
    for item in formatted["key_indicators"]:
        assert isinstance(item, str)
    for item in formatted["suspicious_claims"]:
        assert isinstance(item, str)
    
    print("✓ Requirement 14.5: Array type fields validated")


def test_requirement_14_6():
    """
    Requirement 14.6: THE JSON_Formatter SHALL output only JSON without 
    additional text or formatting
    """
    analyzer = CredibilityAnalyzer()
    
    result = {
        "classification": "UNVERIFIED",
        "credibility_score": 45,
        "risk_level": "Medium Risk",
        "confidence": 55,
        "analysis_summary": "Test",
        "key_indicators": ["Test"],
        "emotional_tone": "Neutral",
        "suspicious_claims": [],
        "recommended_action": "Action",
        "explanation": "Explanation"
    }
    
    formatted = analyzer.format_json_output(result)
    
    # The output should be a plain dictionary that can be serialized to JSON
    # No additional formatting or text should be added
    assert isinstance(formatted, dict)
    
    # Serialize and verify it's clean JSON
    json_string = json.dumps(formatted)
    
    # Should not contain any extra formatting markers
    assert not json_string.startswith("```")
    assert "json" not in json_string.lower() or "json" in str(formatted.values())
    
    print("✓ Requirement 14.6: Clean JSON output without extra formatting")


def test_requirement_14_7():
    """
    Requirement 14.7: FOR ALL outputs, parsing the JSON SHALL succeed 
    without errors
    """
    analyzer = CredibilityAnalyzer()
    
    # Test multiple different outputs
    test_cases = [
        {
            "classification": "REAL",
            "credibility_score": 90,
            "risk_level": "Low Risk",
            "confidence": 95,
            "analysis_summary": "High credibility article",
            "key_indicators": ["Balanced language", "Good sources"],
            "emotional_tone": "Neutral and analytical",
            "suspicious_claims": [],
            "recommended_action": "Content appears credible",
            "explanation": "Strong indicators of credibility"
        },
        {
            "classification": "FAKE",
            "credibility_score": 15,
            "risk_level": "High Risk",
            "confidence": 85,
            "analysis_summary": "Low credibility article",
            "key_indicators": ["Sensational language", "No evidence"],
            "emotional_tone": "Highly emotional",
            "suspicious_claims": ["Claim 1", "Claim 2"],
            "recommended_action": "Verify through other sources",
            "explanation": "Multiple red flags detected"
        },
        {
            "classification": "MISLEADING",
            "credibility_score": 55,
            "risk_level": "Medium Risk",
            "confidence": 70,
            "analysis_summary": "Mixed credibility",
            "key_indicators": ["Some issues detected"],
            "emotional_tone": "Moderately emotional",
            "suspicious_claims": ["One claim"],
            "recommended_action": "Cross-reference claims",
            "explanation": "Some concerns present"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        formatted = analyzer.format_json_output(test_case)
        
        # Must be serializable
        json_string = json.dumps(formatted)
        
        # Must be parseable
        parsed = json.loads(json_string)
        
        # Parsed result must match original
        assert parsed == formatted
        
        print(f"  ✓ Test case {i+1}: JSON parsing successful")
    
    print("✓ Requirement 14.7: All outputs parse successfully")


def test_validation_errors():
    """Test that validation properly catches errors."""
    analyzer = CredibilityAnalyzer()
    
    # Test missing field
    try:
        analyzer.format_json_output({"classification": "REAL"})
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Missing required fields" in str(e)
        print("  ✓ Missing field validation works")
    
    # Test invalid type
    try:
        analyzer.format_json_output({
            "classification": "REAL",
            "credibility_score": "not an int",
            "risk_level": "Low Risk",
            "confidence": 90,
            "analysis_summary": "Test",
            "key_indicators": [],
            "emotional_tone": "Neutral",
            "suspicious_claims": [],
            "recommended_action": "Action",
            "explanation": "Explanation"
        })
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "incorrect type" in str(e)
        print("  ✓ Type validation works")
    
    # Test invalid classification value
    try:
        analyzer.format_json_output({
            "classification": "INVALID",
            "credibility_score": 50,
            "risk_level": "Medium Risk",
            "confidence": 60,
            "analysis_summary": "Test",
            "key_indicators": [],
            "emotional_tone": "Neutral",
            "suspicious_claims": [],
            "recommended_action": "Action",
            "explanation": "Explanation"
        })
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid classification" in str(e)
        print("  ✓ Classification value validation works")
    
    # Test score out of range
    try:
        analyzer.format_json_output({
            "classification": "REAL",
            "credibility_score": 150,
            "risk_level": "Low Risk",
            "confidence": 90,
            "analysis_summary": "Test",
            "key_indicators": [],
            "emotional_tone": "Neutral",
            "suspicious_claims": [],
            "recommended_action": "Action",
            "explanation": "Explanation"
        })
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must be in range [0, 100]" in str(e)
        print("  ✓ Score range validation works")
    
    print("✓ Validation error handling confirmed")


if __name__ == "__main__":
    print("Testing Requirements 14.1-14.7 compliance...\n")
    
    test_requirement_14_1()
    test_requirement_14_2()
    test_requirement_14_3()
    test_requirement_14_4()
    test_requirement_14_5()
    test_requirement_14_6()
    test_requirement_14_7()
    print()
    test_validation_errors()
    
    print("\n✅ All requirements validated successfully!")
    print("\nRequirements 14.1-14.7 are fully satisfied by the implementation.")

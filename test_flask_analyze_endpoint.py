"""
Test the Flask /analyze endpoint integration.

This test verifies that the /analyze endpoint correctly integrates with
the CredibilityAnalyzer and returns properly formatted JSON responses.
"""

import json
from app import app


def get_test_client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    return app.test_client()


def test_analyze_endpoint_with_valid_text():
    """Test /analyze endpoint with valid article text."""
    client = get_test_client()
    test_article = """
    Breaking news: Scientists have discovered a new species of butterfly in the Amazon rainforest.
    The discovery was made by researchers from the University of São Paulo during a three-month
    expedition. The butterfly, which has distinctive blue and green markings, was found in a
    remote area of the rainforest. According to Dr. Maria Silva, lead researcher on the project,
    this discovery highlights the importance of preserving biodiversity in the Amazon.
    """
    
    response = client.post(
        '/analyze',
        data=json.dumps({'text': test_article}),
        content_type='application/json'
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = json.loads(response.data)
    
    # Verify all required fields are present
    required_fields = [
        'classification', 'credibility_score', 'risk_level', 'confidence',
        'analysis_summary', 'key_indicators', 'emotional_tone',
        'suspicious_claims', 'recommended_action', 'explanation'
    ]
    
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    # Verify data types
    assert isinstance(data['classification'], str), "classification must be string"
    assert data['classification'] in ['REAL', 'FAKE', 'MISLEADING', 'UNVERIFIED'], \
        f"Invalid classification: {data['classification']}"
    
    assert isinstance(data['credibility_score'], int), "credibility_score must be int"
    assert 0 <= data['credibility_score'] <= 100, \
        f"credibility_score out of range: {data['credibility_score']}"
    
    assert isinstance(data['risk_level'], str), "risk_level must be string"
    assert data['risk_level'] in ['Low Risk', 'Medium Risk', 'High Risk'], \
        f"Invalid risk_level: {data['risk_level']}"
    
    assert isinstance(data['confidence'], int), "confidence must be int"
    assert 0 <= data['confidence'] <= 100, f"confidence out of range: {data['confidence']}"
    
    assert isinstance(data['analysis_summary'], str), "analysis_summary must be string"
    assert len(data['analysis_summary']) > 0, "analysis_summary cannot be empty"
    
    assert isinstance(data['key_indicators'], list), "key_indicators must be list"
    assert len(data['key_indicators']) > 0, "key_indicators cannot be empty"
    
    assert isinstance(data['emotional_tone'], str), "emotional_tone must be string"
    assert len(data['emotional_tone']) > 0, "emotional_tone cannot be empty"
    
    assert isinstance(data['suspicious_claims'], list), "suspicious_claims must be list"
    
    assert isinstance(data['recommended_action'], str), "recommended_action must be string"
    assert len(data['recommended_action']) > 0, "recommended_action cannot be empty"
    
    assert isinstance(data['explanation'], str), "explanation must be string"
    assert len(data['explanation']) > 0, "explanation cannot be empty"
    
    print("✓ test_analyze_endpoint_with_valid_text passed")


def test_analyze_endpoint_missing_text_field():
    """Test /analyze endpoint with missing text field."""
    client = get_test_client()
    response = client.post(
        '/analyze',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = json.loads(response.data)
    assert 'error' in data, "Error message should be present"
    print("✓ test_analyze_endpoint_missing_text_field passed")


def test_analyze_endpoint_empty_text():
    """Test /analyze endpoint with empty text."""
    client = get_test_client()
    response = client.post(
        '/analyze',
        data=json.dumps({'text': ''}),
        content_type='application/json'
    )
    
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = json.loads(response.data)
    assert 'error' in data, "Error message should be present"
    print("✓ test_analyze_endpoint_empty_text passed")


def test_analyze_endpoint_whitespace_only():
    """Test /analyze endpoint with whitespace-only text."""
    client = get_test_client()
    response = client.post(
        '/analyze',
        data=json.dumps({'text': '   \n\t  '}),
        content_type='application/json'
    )
    
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = json.loads(response.data)
    assert 'error' in data, "Error message should be present"
    print("✓ test_analyze_endpoint_whitespace_only passed")


def test_analyze_endpoint_insufficient_text():
    """Test /analyze endpoint with text shorter than 50 characters."""
    client = get_test_client()
    response = client.post(
        '/analyze',
        data=json.dumps({'text': 'Short text'}),
        content_type='application/json'
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = json.loads(response.data)
    
    # Should return UNVERIFIED for insufficient text
    assert data['classification'] == 'UNVERIFIED', \
        f"Expected UNVERIFIED, got {data['classification']}"
    assert 'INSUFFICIENT INFORMATION' in data['explanation'], \
        "Explanation should mention insufficient information"
    print("✓ test_analyze_endpoint_insufficient_text passed")


def test_analyze_endpoint_with_sensational_text():
    """Test /analyze endpoint with sensational article text."""
    client = get_test_client()
    sensational_article = """
    SHOCKING REVELATION! You won't believe what scientists discovered!
    BREAKING: The mainstream media doesn't want you to know this TRUTH!
    Sources say that this UNBELIEVABLE discovery will change everything!
    Experts claim this is the most DEVASTATING news of the century!
    According to reports, this TERRIFYING information has been hidden from the public!
    """
    
    response = client.post(
        '/analyze',
        data=json.dumps({'text': sensational_article}),
        content_type='application/json'
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = json.loads(response.data)
    
    # Should detect sensational patterns in key indicators
    # The actual credibility score depends on the model, but indicators should be present
    has_sensational = any('sensational' in indicator.lower() 
                          for indicator in data['key_indicators'])
    has_emotional = any('emotional' in indicator.lower() 
                        for indicator in data['key_indicators'])
    has_vague = any('vague' in indicator.lower() 
                    for indicator in data['key_indicators'])
    
    # At least one of these indicators should be detected
    assert has_sensational or has_emotional or has_vague, \
        f"Should detect suspicious patterns. Key indicators: {data['key_indicators']}"
    print("✓ test_analyze_endpoint_with_sensational_text passed")


def test_predict_endpoint_still_works():
    """Test that the existing /predict endpoint still functions correctly."""
    client = get_test_client()
    test_text = "This is a test article about news."
    
    response = client.post(
        '/predict',
        data=json.dumps({'text': test_text}),
        content_type='application/json'
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = json.loads(response.data)
    
    # Verify existing /predict endpoint fields
    assert 'label' in data, "label field should be present"
    assert 'label_text' in data, "label_text field should be present"
    assert 'disclaimer' in data, "disclaimer field should be present"
    print("✓ test_predict_endpoint_still_works passed")


def run_all_tests():
    """Run all tests."""
    print("\n=== Running Flask /analyze endpoint integration tests ===\n")
    
    try:
        test_analyze_endpoint_with_valid_text()
        test_analyze_endpoint_missing_text_field()
        test_analyze_endpoint_empty_text()
        test_analyze_endpoint_whitespace_only()
        test_analyze_endpoint_insufficient_text()
        test_analyze_endpoint_with_sensational_text()
        test_predict_endpoint_still_works()
        
        print("\n=== All tests passed! ===\n")
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)

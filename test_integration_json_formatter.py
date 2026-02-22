"""
Integration test for JSON formatter with actual analyze() output.
"""

import joblib
from credibility_analyzer import CredibilityAnalyzer


def test_format_json_with_analyze_output():
    """Test that format_json_output works with actual analyze() output."""
    
    # Load model and vectorizer
    try:
        model = joblib.load('best_model.joblib')
        vectorizer = joblib.load('tfidf_vectorizer.joblib')
    except FileNotFoundError:
        print("⚠ Model files not found, skipping integration test")
        return
    
    analyzer = CredibilityAnalyzer()
    
    # Test with a sample article
    test_article = """
    Breaking news: Scientists have discovered a shocking new finding that will 
    change everything you know about health. According to sources, this amazing 
    discovery could revolutionize medicine forever. Experts claim this is the 
    most important breakthrough in decades. You won't believe what they found!
    """
    
    # Run analysis
    analysis_result = analyzer.analyze(test_article, model, vectorizer)
    
    print("Analysis result keys:", list(analysis_result.keys()))
    print("\nAnalysis result:")
    for key, value in analysis_result.items():
        print(f"  {key}: {value if not isinstance(value, list) else f'[{len(value)} items]'}")
    
    # Format the output
    try:
        formatted_output = analyzer.format_json_output(analysis_result)
        print("\n✓ Successfully formatted analysis output")
        print(f"  Classification: {formatted_output['classification']}")
        print(f"  Credibility Score: {formatted_output['credibility_score']}")
        print(f"  Risk Level: {formatted_output['risk_level']}")
        print(f"  Confidence: {formatted_output['confidence']}")
        
        # Verify it's JSON serializable
        import json
        json_string = json.dumps(formatted_output, indent=2)
        print("\n✓ Output is valid JSON")
        print(f"  JSON length: {len(json_string)} characters")
        
        # Verify we can parse it back
        parsed = json.loads(json_string)
        assert parsed == formatted_output
        print("✓ JSON can be parsed back correctly")
        
        print("\n✅ Integration test passed!")
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        raise


if __name__ == "__main__":
    print("Testing JSON formatter integration with analyze()...\n")
    test_format_json_with_analyze_output()

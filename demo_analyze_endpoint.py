"""
Demo script to test the /analyze endpoint manually.

This script demonstrates how to use the /analyze endpoint with sample articles.
"""

import json
import requests

# Sample articles for testing
CREDIBLE_ARTICLE = """
A new study published in the Journal of Climate Science reveals that global temperatures 
have risen by 1.2 degrees Celsius since pre-industrial times. The research, conducted by 
scientists at the University of Cambridge, analyzed temperature data from over 10,000 
weather stations worldwide. Dr. Sarah Johnson, lead author of the study, stated that 
the findings are consistent with previous climate models. The study was peer-reviewed 
and funded by the National Science Foundation.
"""

SENSATIONAL_ARTICLE = """
SHOCKING! You won't believe what the government is hiding from you! BREAKING NEWS that 
the mainstream media doesn't want you to know! Sources say this will change EVERYTHING! 
Experts claim this is the most DEVASTATING revelation of the century! According to 
reports, this TERRIFYING truth has been covered up for years! Wake up, people!
"""

MISLEADING_ARTICLE = """
Scientists discover miracle cure that doctors don't want you to know about! This amazing 
breakthrough could revolutionize healthcare forever. Sources close to the research say 
that pharmaceutical companies are trying to suppress this information. While some studies 
suggest potential benefits, the evidence is still preliminary and requires further 
investigation.
"""


def test_analyze_endpoint(article_text, description):
    """Test the /analyze endpoint with a given article."""
    print(f"\n{'='*70}")
    print(f"Testing: {description}")
    print(f"{'='*70}")
    
    url = "http://localhost:5000/analyze"
    headers = {"Content-Type": "application/json"}
    data = {"text": article_text}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\nClassification: {result['classification']}")
            print(f"Credibility Score: {result['credibility_score']}/100")
            print(f"Risk Level: {result['risk_level']}")
            print(f"Confidence: {result['confidence']}/100")
            print(f"\nAnalysis Summary:")
            print(f"  {result['analysis_summary']}")
            print(f"\nKey Indicators:")
            for indicator in result['key_indicators']:
                print(f"  - {indicator}")
            print(f"\nEmotional Tone: {result['emotional_tone']}")
            print(f"\nSuspicious Claims: {len(result['suspicious_claims'])} found")
            if result['suspicious_claims']:
                for i, claim in enumerate(result['suspicious_claims'][:3], 1):
                    print(f"  {i}. {claim[:100]}...")
            print(f"\nRecommended Action:")
            print(f"  {result['recommended_action']}")
            
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Flask server.")
        print("Please start the server with: python app.py")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run demo tests."""
    print("\n" + "="*70)
    print("Flask /analyze Endpoint Demo")
    print("="*70)
    print("\nThis demo requires the Flask server to be running.")
    print("Start it with: python app.py")
    print("\nPress Ctrl+C to exit at any time.")
    
    input("\nPress Enter to continue...")
    
    # Test with different article types
    test_analyze_endpoint(CREDIBLE_ARTICLE, "Credible Scientific Article")
    test_analyze_endpoint(SENSATIONAL_ARTICLE, "Sensational Article")
    test_analyze_endpoint(MISLEADING_ARTICLE, "Misleading Article")
    
    print("\n" + "="*70)
    print("Demo completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

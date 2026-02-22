"""
Unit tests for PatternDetector class
"""

from pattern_detector import PatternDetector


def test_pattern_detector_empty_text():
    """Test pattern detector with empty text"""
    detector = PatternDetector()
    patterns = detector.detect_patterns("")
    
    assert patterns["sensational_phrases"] == 0
    assert patterns["excessive_caps"] == 0.0
    assert patterns["vague_sources"] == 0
    assert patterns["conspiracy_framing"] == 0
    assert patterns["emotional_manipulation"] == 0
    assert patterns["one_sided"] == 0.0
    assert patterns["no_evidence"] == 0.0
    assert patterns["extreme_adjectives"] == 0
    assert patterns["clickbait"] == 0
    
    print("✓ test_pattern_detector_empty_text passed")


def test_pattern_detector_sensational_phrases():
    """Test detection of sensational phrases"""
    detector = PatternDetector()
    text = "SHOCKING news! This UNBELIEVABLE story was EXPOSED today. The HIDDEN TRUTH REVEALED!"
    patterns = detector.detect_patterns(text)
    
    assert patterns["sensational_phrases"] > 0, "Should detect sensational phrases"
    print(f"  Detected {patterns['sensational_phrases']} sensational phrases")
    print("✓ test_pattern_detector_sensational_phrases passed")


def test_pattern_detector_excessive_caps():
    """Test detection of excessive capitalization"""
    detector = PatternDetector()
    text = "THIS IS ALL CAPS TEXT WITH MANY WORDS IN CAPITALS"
    patterns = detector.detect_patterns(text)
    
    assert patterns["excessive_caps"] > 0.5, "Should detect high ratio of caps"
    print(f"  Excessive caps ratio: {patterns['excessive_caps']:.2f}")
    print("✓ test_pattern_detector_excessive_caps passed")


def test_pattern_detector_vague_sources():
    """Test detection of vague source references"""
    detector = PatternDetector()
    text = "Sources say that experts claim this is true. Reports suggest it happened."
    patterns = detector.detect_patterns(text)
    
    assert patterns["vague_sources"] >= 3, "Should detect vague source references"
    print(f"  Detected {patterns['vague_sources']} vague source references")
    print("✓ test_pattern_detector_vague_sources passed")


def test_pattern_detector_conspiracy_framing():
    """Test detection of conspiracy framing language"""
    detector = PatternDetector()
    text = "This is a cover-up! The mainstream media doesn't want you to know the truth. Wake up!"
    patterns = detector.detect_patterns(text)
    
    assert patterns["conspiracy_framing"] > 0, "Should detect conspiracy framing"
    print(f"  Detected {patterns['conspiracy_framing']} conspiracy markers")
    print("✓ test_pattern_detector_conspiracy_framing passed")


def test_pattern_detector_emotional_manipulation():
    """Test detection of emotional manipulation"""
    detector = PatternDetector()
    text = "This is outrageous and terrifying! The devastating and horrifying truth is shocking."
    patterns = detector.detect_patterns(text)
    
    assert patterns["emotional_manipulation"] > 0, "Should detect emotional manipulation"
    print(f"  Detected {patterns['emotional_manipulation']} emotional manipulation keywords")
    print("✓ test_pattern_detector_emotional_manipulation passed")


def test_pattern_detector_one_sided():
    """Test detection of one-sided narratives"""
    detector = PatternDetector()
    
    # One-sided text (no balance indicators)
    one_sided_text = "This is bad. This is wrong. This is terrible. Everything is negative."
    patterns = detector.detect_patterns(one_sided_text)
    assert patterns["one_sided"] > 0.5, "Should detect one-sided narrative"
    
    # Balanced text (with balance indicators)
    balanced_text = "This is one view. However, there is another perspective. Although some say this, others say that."
    patterns = detector.detect_patterns(balanced_text)
    assert patterns["one_sided"] < 0.5, "Should detect balanced narrative"
    
    print("✓ test_pattern_detector_one_sided passed")


def test_pattern_detector_no_evidence():
    """Test detection of lack of evidence"""
    detector = PatternDetector()
    
    # Text with no evidence markers
    no_evidence_text = "This is just an opinion. I think this is true. Everyone knows this."
    patterns = detector.detect_patterns(no_evidence_text)
    assert patterns["no_evidence"] > 0.5, "Should detect lack of evidence"
    
    # Text with evidence markers
    evidence_text = "According to a study published in Nature, research shows that data indicates statistics prove this."
    patterns = detector.detect_patterns(evidence_text)
    assert patterns["no_evidence"] < 0.5, "Should detect presence of evidence"
    
    print("✓ test_pattern_detector_no_evidence passed")


def test_pattern_detector_extreme_adjectives():
    """Test detection of extreme adjectives"""
    detector = PatternDetector()
    text = "This is always true. Everyone never does this. All people completely agree. Absolutely definitely."
    patterns = detector.detect_patterns(text)
    
    assert patterns["extreme_adjectives"] > 0, "Should detect extreme adjectives"
    print(f"  Detected {patterns['extreme_adjectives']} extreme adjectives")
    print("✓ test_pattern_detector_extreme_adjectives passed")


def test_pattern_detector_clickbait():
    """Test detection of clickbait patterns"""
    detector = PatternDetector()
    text = "You won't believe what happened next! This number will shock you. Doctors hate this one weird trick."
    patterns = detector.detect_patterns(text)
    
    assert patterns["clickbait"] > 0, "Should detect clickbait patterns"
    print(f"  Detected {patterns['clickbait']} clickbait patterns")
    print("✓ test_pattern_detector_clickbait passed")


def test_pattern_detector_neutral_article():
    """Test pattern detector with neutral article"""
    detector = PatternDetector()
    text = """
    According to a study published in the Journal of Science, researchers found that 
    climate patterns are changing. However, the data also shows some regional variations. 
    Dr. Smith from the University stated that more research is needed. The analysis 
    included statistics from multiple sources.
    """
    patterns = detector.detect_patterns(text)
    
    # Neutral article should have low pattern scores
    assert patterns["sensational_phrases"] <= 1, "Should have few sensational phrases"
    assert patterns["conspiracy_framing"] == 0, "Should have no conspiracy framing"
    assert patterns["emotional_manipulation"] <= 1, "Should have minimal emotional manipulation"
    assert patterns["no_evidence"] < 0.5, "Should have evidence markers"
    
    print("✓ test_pattern_detector_neutral_article passed")


def test_pattern_detector_all_patterns():
    """Test pattern detector with text containing multiple patterns"""
    detector = PatternDetector()
    text = """
    SHOCKING REVELATION! Sources say this UNBELIEVABLE cover-up is absolutely terrifying!
    You won't believe what happened next. The mainstream media never tells you the truth.
    This is always happening and everyone knows it. Reports suggest this is devastating.
    """
    patterns = detector.detect_patterns(text)
    
    # Should detect multiple patterns
    assert patterns["sensational_phrases"] > 0
    assert patterns["vague_sources"] > 0
    assert patterns["conspiracy_framing"] > 0
    assert patterns["emotional_manipulation"] > 0
    assert patterns["extreme_adjectives"] > 0
    assert patterns["clickbait"] > 0
    
    # All values should be non-negative
    for key, value in patterns.items():
        assert value >= 0, f"Pattern {key} should be non-negative, got {value}"
    
    print("✓ test_pattern_detector_all_patterns passed")


if __name__ == "__main__":
    test_pattern_detector_empty_text()
    test_pattern_detector_sensational_phrases()
    test_pattern_detector_excessive_caps()
    test_pattern_detector_vague_sources()
    test_pattern_detector_conspiracy_framing()
    test_pattern_detector_emotional_manipulation()
    test_pattern_detector_one_sided()
    test_pattern_detector_no_evidence()
    test_pattern_detector_extreme_adjectives()
    test_pattern_detector_clickbait()
    test_pattern_detector_neutral_article()
    test_pattern_detector_all_patterns()
    
    print("\n✅ All pattern detector tests passed!")


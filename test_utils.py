"""
Unit tests for utility functions in utils.py
"""

import utils


def test_count_keywords():
    """Test keyword counting functionality"""
    text = "This is SHOCKING news! Absolutely SHOCKING and unbelievable."
    keywords = ["shocking", "unbelievable", "amazing"]
    
    count = utils.count_keywords(text, keywords)
    assert count == 3, f"Expected 3, got {count}"
    
    # Test empty inputs
    assert utils.count_keywords("", keywords) == 0
    assert utils.count_keywords(text, []) == 0
    assert utils.count_keywords("", []) == 0
    
    print("✓ test_count_keywords passed")


def test_count_phrases():
    """Test phrase counting functionality"""
    text = "Sources say that experts claim this is true. Sources say it again."
    phrases = ["sources say", "experts claim", "not present"]
    
    count = utils.count_phrases(text, phrases)
    assert count == 3, f"Expected 3, got {count}"
    
    # Test empty inputs
    assert utils.count_phrases("", phrases) == 0
    assert utils.count_phrases(text, []) == 0
    
    print("✓ test_count_phrases passed")


def test_split_into_sentences():
    """Test sentence splitting functionality"""
    text = "First sentence. Second sentence! Third sentence? Fourth sentence."
    sentences = utils.split_into_sentences(text)
    
    assert len(sentences) == 4, f"Expected 4 sentences, got {len(sentences)}"
    assert sentences[0] == "First sentence"
    assert sentences[1] == "Second sentence"
    
    # Test empty input
    assert utils.split_into_sentences("") == []
    
    # Test with newlines
    text_with_newlines = "Line one.\nLine two.\nLine three."
    sentences = utils.split_into_sentences(text_with_newlines)
    assert len(sentences) == 3
    
    print("✓ test_split_into_sentences passed")


def test_contains_vague_source():
    """Test vague source detection"""
    assert utils.contains_vague_source("Sources say this is true") == True
    assert utils.contains_vague_source("Experts claim this happened") == True
    assert utils.contains_vague_source("According to the study published in Nature") == False
    assert utils.contains_vague_source("") == False
    
    print("✓ test_contains_vague_source passed")


def test_contains_extreme_language():
    """Test extreme language detection"""
    assert utils.contains_extreme_language("This is absolutely shocking") == True
    assert utils.contains_extreme_language("Everyone always does this") == True
    assert utils.contains_extreme_language("This is a moderate statement") == False
    assert utils.contains_extreme_language("") == False
    
    print("✓ test_contains_extreme_language passed")


def test_contains_evidence_markers():
    """Test evidence marker detection"""
    assert utils.contains_evidence_markers("According to a study published in 2020") == True
    assert utils.contains_evidence_markers("The research shows that") == True
    assert utils.contains_evidence_markers("Statistics indicate 50 percent") == True
    assert utils.contains_evidence_markers("This is just an opinion") == False
    assert utils.contains_evidence_markers("") == False
    
    print("✓ test_contains_evidence_markers passed")


def test_contains_conspiracy_markers():
    """Test conspiracy marker detection"""
    assert utils.contains_conspiracy_markers("This is a cover-up by the government") == True
    assert utils.contains_conspiracy_markers("Wake up sheeple!") == True
    assert utils.contains_conspiracy_markers("The mainstream media won't tell you") == True
    assert utils.contains_conspiracy_markers("This is a normal news article") == False
    assert utils.contains_conspiracy_markers("") == False
    
    print("✓ test_contains_conspiracy_markers passed")


if __name__ == "__main__":
    test_count_keywords()
    test_count_phrases()
    test_split_into_sentences()
    test_contains_vague_source()
    test_contains_extreme_language()
    test_contains_evidence_markers()
    test_contains_conspiracy_markers()
    
    print("\n✅ All tests passed!")

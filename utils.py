"""
Utility functions for text processing and pattern detection in news credibility analysis.
"""

import re
from typing import List


def count_keywords(text: str, keywords: List[str]) -> int:
    """
    Count occurrences of keywords in text (case-insensitive).
    
    Args:
        text: The text to search in
        keywords: List of keywords to count
        
    Returns:
        Total count of all keyword occurrences
    """
    if not text or not keywords:
        return 0
    
    text_lower = text.lower()
    count = 0
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        count += text_lower.count(keyword_lower)
    
    return count


def count_phrases(text: str, phrases: List[str]) -> int:
    """
    Count occurrences of phrases in text (case-insensitive).
    
    Args:
        text: The text to search in
        phrases: List of phrases to count
        
    Returns:
        Total count of all phrase occurrences
    """
    if not text or not phrases:
        return 0
    
    text_lower = text.lower()
    count = 0
    
    for phrase in phrases:
        phrase_lower = phrase.lower()
        count += text_lower.count(phrase_lower)
    
    return count


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences using basic punctuation rules.
    
    Args:
        text: The text to split
        
    Returns:
        List of sentences
    """
    if not text:
        return []
    
    # Split on sentence-ending punctuation followed by whitespace or end of string
    # This regex handles periods, exclamation marks, and question marks
    sentences = re.split(r'[.!?]+\s+|\n+', text)
    
    # Filter out empty strings and strip whitespace
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences


def contains_vague_source(sentence: str) -> bool:
    """
    Detect if a sentence contains vague source references.
    
    Args:
        sentence: The sentence to check
        
    Returns:
        True if vague source references are detected, False otherwise
    """
    if not sentence:
        return False
    
    vague_source_patterns = [
        "sources say",
        "experts claim",
        "reports suggest",
        "allegedly",
        "rumored",
        "according to sources",
        "insiders say",
        "it is believed",
        "some say",
        "many believe"
    ]
    
    sentence_lower = sentence.lower()
    
    for pattern in vague_source_patterns:
        if pattern in sentence_lower:
            return True
    
    return False


def contains_extreme_language(sentence: str) -> bool:
    """
    Detect if a sentence contains extreme language or adjectives.
    
    Args:
        sentence: The sentence to check
        
    Returns:
        True if extreme language is detected, False otherwise
    """
    if not sentence:
        return False
    
    extreme_words = [
        "always",
        "never",
        "every",
        "all",
        "none",
        "completely",
        "totally",
        "absolutely",
        "definitely",
        "shocking",
        "unbelievable",
        "terrifying",
        "devastating",
        "horrifying",
        "disgusting",
        "appalling"
    ]
    
    sentence_lower = sentence.lower()
    
    # Use word boundaries to match whole words
    for word in extreme_words:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, sentence_lower):
            return True
    
    return False


def contains_evidence_markers(sentence: str) -> bool:
    """
    Detect if a sentence contains evidence markers (citations, data, research references).
    
    Args:
        sentence: The sentence to check
        
    Returns:
        True if evidence markers are detected, False otherwise
    """
    if not sentence:
        return False
    
    evidence_markers = [
        "study",
        "research",
        "data",
        "statistics",
        "percent",
        "according to",
        "published",
        "journal",
        "university",
        "professor",
        "dr.",
        "phd",
        "analysis",
        "survey",
        "report"
    ]
    
    sentence_lower = sentence.lower()
    
    for marker in evidence_markers:
        if marker in sentence_lower:
            return True
    
    return False


def contains_conspiracy_markers(sentence: str) -> bool:
    """
    Detect if a sentence contains conspiracy framing language.
    
    Args:
        sentence: The sentence to check
        
    Returns:
        True if conspiracy markers are detected, False otherwise
    """
    if not sentence:
        return False
    
    conspiracy_markers = [
        "cover-up",
        "cover up",
        "conspiracy",
        "they don't want you to know",
        "mainstream media",
        "wake up",
        "sheeple",
        "hidden truth",
        "secret agenda",
        "deep state",
        "false flag",
        "controlled by"
    ]
    
    sentence_lower = sentence.lower()
    
    for marker in conspiracy_markers:
        if marker in sentence_lower:
            return True
    
    return False

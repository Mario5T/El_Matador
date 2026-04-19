"""
Utility functions for text processing and pattern detection.

This module is the single source of truth for all text-level helpers used
across the credibility-analysis pipeline.  No other module should duplicate
these functions.
"""

import re
from typing import List


# ---------------------------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------------------------

def clean_text_for_model(text: str) -> str:
    """
    Normalise raw article text to match the preprocessing applied during training.

    Steps:
        1. Lowercase
        2. Strip HTML tags
        3. Remove non-alphabetic characters (keeps spaces)
        4. Collapse consecutive whitespace

    Args:
        text: Raw article text (may contain HTML, numbers, punctuation).

    Returns:
        Cleaned string suitable for TF-IDF vectorisation.
    """
    text = str(text).lower()
    text = re.sub(r"<[^>]+>", " ", text)        # strip HTML
    text = re.sub(r"[^a-z\s]", " ", text)        # letters only
    text = re.sub(r"\s+", " ", text).strip()      # collapse whitespace
    return text


# ---------------------------------------------------------------------------
# Keyword / phrase counters
# ---------------------------------------------------------------------------

def count_keywords(text: str, keywords: List[str]) -> int:
    """
    Count total occurrences of *keywords* in *text* (case-insensitive).

    Args:
        text: Text to search.
        keywords: Keywords to count (matched as substrings).

    Returns:
        Total count across all keywords.
    """
    if not text or not keywords:
        return 0
    text_lower = text.lower()
    return sum(text_lower.count(kw.lower()) for kw in keywords)


def count_phrases(text: str, phrases: List[str]) -> int:
    """
    Count total occurrences of multi-word *phrases* in *text* (case-insensitive).

    Args:
        text: Text to search.
        phrases: Phrases to count (matched as substrings).

    Returns:
        Total count across all phrases.
    """
    if not text or not phrases:
        return 0
    text_lower = text.lower()
    return sum(text_lower.count(ph.lower()) for ph in phrases)


# ---------------------------------------------------------------------------
# Sentence splitter
# ---------------------------------------------------------------------------

def split_into_sentences(text: str) -> List[str]:
    """
    Split *text* into sentences using punctuation heuristics.

    Args:
        text: Full article text.

    Returns:
        List of non-empty sentence strings.
    """
    if not text:
        return []
    parts = re.split(r"[.!?]+\s+|\n+", text)
    return [s.strip() for s in parts if s.strip()]


# ---------------------------------------------------------------------------
# Sentence-level detectors (used by ClaimHighlighter)
# ---------------------------------------------------------------------------

_VAGUE_SOURCE_PATTERNS: List[str] = [
    "sources say", "experts claim", "reports suggest", "allegedly",
    "rumored", "according to sources", "insiders say", "it is believed",
    "some say", "many believe",
]

_EXTREME_WORDS: List[str] = [
    "always", "never", "every", "all", "none", "completely", "totally",
    "absolutely", "definitely", "shocking", "unbelievable", "terrifying",
    "devastating", "horrifying", "disgusting", "appalling",
]

_EVIDENCE_MARKERS: List[str] = [
    "study", "research", "data", "statistics", "percent", "according to",
    "published", "journal", "university", "professor", "dr.", "phd",
    "analysis", "survey", "report",
]

_CONSPIRACY_MARKERS: List[str] = [
    "cover-up", "cover up", "conspiracy", "they don't want you to know",
    "mainstream media", "wake up", "sheeple", "hidden truth",
    "secret agenda", "deep state", "false flag", "controlled by",
]


def contains_vague_source(sentence: str) -> bool:
    """Return True if *sentence* contains a vague source reference."""
    if not sentence:
        return False
    sl = sentence.lower()
    return any(p in sl for p in _VAGUE_SOURCE_PATTERNS)


def contains_extreme_language(sentence: str) -> bool:
    """Return True if *sentence* contains extreme / sensational language."""
    if not sentence:
        return False
    sl = sentence.lower()
    return any(re.search(r"\b" + re.escape(w) + r"\b", sl) for w in _EXTREME_WORDS)


def contains_evidence_markers(sentence: str) -> bool:
    """Return True if *sentence* contains evidence-based markers."""
    if not sentence:
        return False
    sl = sentence.lower()
    return any(m in sl for m in _EVIDENCE_MARKERS)


def contains_conspiracy_markers(sentence: str) -> bool:
    """Return True if *sentence* contains conspiracy-framing language."""
    if not sentence:
        return False
    sl = sentence.lower()
    return any(m in sl for m in _CONSPIRACY_MARKERS)

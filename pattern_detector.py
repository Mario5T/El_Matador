"""
Pattern detection module for identifying linguistic patterns associated with misinformation.
"""

from typing import Dict
from utils import count_keywords, count_phrases


class PatternDetector:
    """
    Detects linguistic patterns associated with misinformation in news articles.
    """
    
    def __init__(self):
        """Initialize the PatternDetector with predefined pattern keywords and phrases."""
        # Sensational phrases keywords
        self.sensational_keywords = [
            "SHOCKING", "BREAKING", "UNBELIEVABLE", "EXPOSED",
            "REVEALED", "SECRET", "HIDDEN", "TRUTH", "BOMBSHELL",
            "EXPLOSIVE", "STUNNING", "INCREDIBLE"
        ]
        
        # Vague source patterns
        self.vague_source_patterns = [
            "sources say", "experts claim", "reports suggest",
            "allegedly", "rumored", "according to sources",
            "insiders say", "it is believed", "some say", "many believe"
        ]
        
        # Conspiracy framing keywords
        self.conspiracy_keywords = [
            "cover-up", "cover up", "conspiracy", "they don't want you to know",
            "mainstream media", "wake up", "sheeple", "hidden truth",
            "secret agenda", "deep state", "false flag", "controlled by"
        ]
        
        # Emotional manipulation keywords
        self.emotional_keywords = [
            "outrage", "terrifying", "devastating", "horrifying",
            "shocking", "disgusting", "appalling", "outrageous",
            "scandalous", "alarming", "disturbing"
        ]
        
        # Balance indicators (for detecting one-sided narratives)
        self.balance_indicators = [
            "however", "although", "on the other hand", "but",
            "despite", "nevertheless", "yet", "while", "whereas",
            "conversely", "alternatively"
        ]
        
        # Evidence indicators
        self.evidence_indicators = [
            "study", "research", "data", "statistics", "percent",
            "according to", "published", "journal", "university",
            "professor", "analysis", "survey", "report"
        ]
        
        # Extreme adjectives
        self.extreme_adjectives = [
            "always", "never", "every", "all", "none", "completely",
            "totally", "absolutely", "definitely", "entirely",
            "utterly", "wholly"
        ]
        
        # Clickbait patterns
        self.clickbait_patterns = [
            "you won't believe", "what happened next", "number",
            "will shock you", "doctors hate", "one weird trick",
            "this is why", "the reason why", "you need to see"
        ]
    
    def detect_patterns(self, text: str) -> Dict[str, float]:
        """
        Detect linguistic patterns associated with misinformation in the given text.
        
        Args:
            text: The article text to analyze
            
        Returns:
            Dictionary containing pattern detection results with the following keys:
            - sensational_phrases: Count of sensational keywords
            - excessive_caps: Ratio of excessively capitalized words
            - vague_sources: Count of vague source references
            - conspiracy_framing: Count of conspiracy keywords
            - emotional_manipulation: Count of emotional manipulation keywords
            - one_sided: Score indicating one-sided narrative (0.0-1.0)
            - no_evidence: Score indicating lack of evidence (0.0-1.0)
            - extreme_adjectives: Count of extreme adjectives
            - clickbait: Count of clickbait patterns
        """
        if not text:
            return {
                "sensational_phrases": 0,
                "excessive_caps": 0.0,
                "vague_sources": 0,
                "conspiracy_framing": 0,
                "emotional_manipulation": 0,
                "one_sided": 0.0,
                "no_evidence": 0.0,
                "extreme_adjectives": 0,
                "clickbait": 0
            }
        
        patterns = {}
        
        # Detect sensational phrases
        patterns["sensational_phrases"] = count_keywords(text, self.sensational_keywords)
        
        # Detect excessive capitalization
        words = text.split()
        if len(words) > 0:
            caps_words = [w for w in words if w.isupper() and len(w) > 2]
            patterns["excessive_caps"] = len(caps_words) / len(words)
        else:
            patterns["excessive_caps"] = 0.0
        
        # Detect vague source references
        patterns["vague_sources"] = count_phrases(text, self.vague_source_patterns)
        
        # Detect conspiracy framing
        patterns["conspiracy_framing"] = count_keywords(text, self.conspiracy_keywords)
        
        # Detect emotional manipulation
        patterns["emotional_manipulation"] = count_keywords(text, self.emotional_keywords)
        
        # Detect one-sided narrative (lack of counterpoints)
        balance_count = count_phrases(text, self.balance_indicators)
        patterns["one_sided"] = max(0.0, 1.0 - min(1.0, balance_count / 3.0))
        
        # Detect lack of evidence
        evidence_count = count_keywords(text, self.evidence_indicators)
        patterns["no_evidence"] = max(0.0, 1.0 - min(1.0, evidence_count / 5.0))
        
        # Detect extreme adjectives
        patterns["extreme_adjectives"] = count_keywords(text, self.extreme_adjectives)
        
        # Detect clickbait patterns
        patterns["clickbait"] = count_phrases(text, self.clickbait_patterns)
        
        return patterns


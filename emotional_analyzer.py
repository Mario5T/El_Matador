"""
Emotional tone analysis module for detecting emotional manipulation and sensationalism.
"""

from typing import Dict


class EmotionalAnalyzer:
    """
    Analyzes emotional tone and manipulation tactics in news articles.
    """
    
    def analyze_emotional_tone(self, patterns: Dict[str, float], text: str) -> str:
        """
        Analyze the emotional tone of the article based on detected patterns.
        
        This method classifies the emotional tone based on:
        - Emotional manipulation score
        - Sensational phrases count
        - Conspiracy framing presence
        
        Args:
            patterns: Dictionary containing pattern detection results from PatternDetector
            text: The article text (for potential future enhancements)
            
        Returns:
            A descriptive string indicating the dominant emotional tone detected
        """
        # Extract relevant pattern scores
        emotional_manipulation = patterns.get("emotional_manipulation", 0)
        sensational_phrases = patterns.get("sensational_phrases", 0)
        conspiracy_framing = patterns.get("conspiracy_framing", 0)
        
        # Classify tone based on pattern thresholds
        # Priority: emotional manipulation > sensational > conspiracy > moderate > neutral
        
        if emotional_manipulation > 3:
            return "Highly emotional and manipulative"
        elif sensational_phrases > 3:
            return "Sensationalized and attention-seeking"
        elif conspiracy_framing > 0:
            return "Conspiratorial and fear-inducing"
        elif emotional_manipulation > 0:
            return "Moderately emotional"
        else:
            return "Neutral and analytical"

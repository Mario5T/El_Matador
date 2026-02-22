"""
Suspicious claim identification for news credibility analysis.
"""

from typing import List
from utils import (
    split_into_sentences,
    contains_vague_source,
    contains_extreme_language,
    contains_evidence_markers,
    contains_conspiracy_markers
)


class ClaimHighlighter:
    """
    Identifies suspicious claims in news articles that require fact-checking.
    
    This component analyzes text to identify statements that lack evidence,
    cite vague sources, or make extraordinary assertions.
    """
    
    def identify_suspicious_claims(self, text: str) -> List[str]:
        """
        Identify claims requiring fact-checking based on suspicion score.
        
        Args:
            text: The article text to analyze
            
        Returns:
            List of up to 5 most suspicious claims (sentences)
        """
        if not text:
            return []
        
        claims = []
        sentences = split_into_sentences(text)
        
        for sentence in sentences:
            suspicion_score = 0
            
            # Check for vague sources (weight: 2)
            if contains_vague_source(sentence):
                suspicion_score += 2
            
            # Check for extreme language (weight: 1)
            if contains_extreme_language(sentence):
                suspicion_score += 1
            
            # Check for lack of evidence (weight: 1)
            if not contains_evidence_markers(sentence):
                suspicion_score += 1
            
            # Check for conspiracy markers (weight: 2)
            if contains_conspiracy_markers(sentence):
                suspicion_score += 2
            
            # Filter sentences with suspicion score >= 3
            if suspicion_score >= 3:
                claims.append(sentence.strip())
        
        # Return top 5 most suspicious claims
        return claims[:5]

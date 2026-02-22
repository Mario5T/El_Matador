# Design Document: News Credibility and Misinformation Analysis Assistant

## Overview

This design extends the existing Flask-based fake news detection application with comprehensive credibility assessment capabilities. The system analyzes news article text using linguistic pattern detection, assigns credibility classifications, and outputs structured JSON assessments. The implementation leverages the existing trained model and vectorizer while adding new analysis components for pattern detection, emotional tone analysis, and claim identification.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask Application                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Existing /predict endpoint (preserved)              │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  New /analyze endpoint                               │  │
│  │    ↓                                                  │  │
│  │  CredibilityAnalyzer                                 │  │
│  │    ├─→ ClassificationEngine                          │  │
│  │    ├─→ PatternDetector                               │  │
│  │    ├─→ SignalExtractor                               │  │
│  │    ├─→ EmotionalAnalyzer                             │  │
│  │    ├─→ ClaimHighlighter                              │  │
│  │    ├─→ RiskCalculator                                │  │
│  │    └─→ JSONFormatter                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Existing Model & Vectorizer (reused)               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

1. **CredibilityAnalyzer**: Orchestrates the analysis pipeline and coordinates all sub-components
2. **ClassificationEngine**: Assigns credibility labels (REAL, FAKE, MISLEADING, UNVERIFIED)
3. **PatternDetector**: Identifies linguistic patterns associated with misinformation
4. **SignalExtractor**: Extracts key indicators influencing credibility assessment
5. **EmotionalAnalyzer**: Detects emotional manipulation and sensationalism
6. **ClaimHighlighter**: Identifies suspicious claims requiring fact-checking
7. **RiskCalculator**: Determines risk level based on credibility score thresholds
8. **JSONFormatter**: Structures analysis results into specified JSON format

## Data Structures

### Input Format

```python
{
    "text": str  # News article text to analyze
}
```

### Output Format

```python
{
    "classification": str,           # REAL | FAKE | MISLEADING | UNVERIFIED
    "credibility_score": int,        # 0-100
    "risk_level": str,               # Low Risk | Medium Risk | High Risk
    "confidence": int,               # 0-100
    "analysis_summary": str,         # 2-4 sentence summary
    "key_indicators": list[str],     # List of key indicators
    "emotional_tone": str,           # Emotional tone description
    "suspicious_claims": list[str],  # List of suspicious claims
    "recommended_action": str,       # Action recommendation
    "explanation": str               # Detailed explanation
}
```

## Core Algorithms

### Algorithm 1: Credibility Classification

**Purpose**: Assign credibility label based on model prediction and pattern analysis

**Input**: 
- `text`: str (article text)
- `model_prediction`: int (0 or 1 from existing model)
- `model_confidence`: float (0.0-1.0)
- `detected_patterns`: dict (pattern detection results)

**Output**: 
- `classification`: str (REAL | FAKE | MISLEADING | UNVERIFIED)

**Logic**:
```
FUNCTION classify_credibility(text, model_prediction, model_confidence, detected_patterns):
    IF length(text) < 50:
        RETURN "UNVERIFIED"
    
    pattern_score = calculate_pattern_score(detected_patterns)
    
    IF model_prediction == 0 AND model_confidence > 0.75:
        IF pattern_score > 0.7:
            RETURN "FAKE"
        ELSE:
            RETURN "MISLEADING"
    
    IF model_prediction == 1 AND model_confidence > 0.75:
        IF pattern_score < 0.3:
            RETURN "REAL"
        ELSE:
            RETURN "MISLEADING"
    
    IF model_confidence < 0.5:
        RETURN "UNVERIFIED"
    
    IF pattern_score > 0.5:
        RETURN "MISLEADING"
    ELSE:
        RETURN "REAL"
```

**Correctness Properties**:
- Property 1: Classification is always one of {REAL, FAKE, MISLEADING, UNVERIFIED}
- Property 2: Insufficient text (< 50 chars) always returns UNVERIFIED
- Property 3: Classification considers both model prediction and pattern analysis

### Algorithm 2: Credibility Score Calculation

**Purpose**: Calculate numerical credibility score (0-100)

**Input**:
- `model_confidence`: float (0.0-1.0)
- `model_prediction`: int (0 or 1)
- `pattern_score`: float (0.0-1.0, where higher = more suspicious patterns)

**Output**:
- `credibility_score`: int (0-100)

**Logic**:
```
FUNCTION calculate_credibility_score(model_confidence, model_prediction, pattern_score):
    IF model_prediction == 1:  # Model says credible
        base_score = model_confidence * 100
    ELSE:  # Model says fake
        base_score = (1 - model_confidence) * 100
    
    # Adjust based on pattern detection
    pattern_penalty = pattern_score * 30
    adjusted_score = base_score - pattern_penalty
    
    # Clamp to valid range
    credibility_score = max(0, min(100, adjusted_score))
    
    RETURN round(credibility_score)
```

**Correctness Properties**:
- Property 4: Credibility score is always in range [0, 100]
- Property 5: Higher pattern_score reduces credibility_score
- Property 6: Model prediction of 1 (credible) increases base score

### Algorithm 3: Pattern Detection

**Purpose**: Detect linguistic patterns associated with misinformation

**Input**:
- `text`: str (article text)

**Output**:
- `patterns`: dict with pattern detection results

**Logic**:
```
FUNCTION detect_patterns(text):
    patterns = {
        "sensational_phrases": 0,
        "excessive_caps": 0,
        "vague_sources": 0,
        "conspiracy_framing": 0,
        "emotional_manipulation": 0,
        "one_sided": 0,
        "no_evidence": 0,
        "extreme_adjectives": 0,
        "clickbait": 0
    }
    
    # Sensational phrases
    sensational_keywords = ["SHOCKING", "BREAKING", "UNBELIEVABLE", "EXPOSED", 
                           "REVEALED", "SECRET", "HIDDEN", "TRUTH"]
    patterns["sensational_phrases"] = count_keywords(text, sensational_keywords)
    
    # Excessive capitalization
    words = text.split()
    caps_words = [w for w in words if w.isupper() and len(w) > 2]
    patterns["excessive_caps"] = len(caps_words) / max(1, len(words))
    
    # Vague sources
    vague_source_patterns = ["sources say", "experts claim", "reports suggest",
                            "allegedly", "rumored", "according to sources"]
    patterns["vague_sources"] = count_phrases(text, vague_source_patterns)
    
    # Conspiracy framing
    conspiracy_keywords = ["cover-up", "conspiracy", "they don't want you to know",
                          "mainstream media", "wake up", "sheeple"]
    patterns["conspiracy_framing"] = count_keywords(text, conspiracy_keywords)
    
    # Emotional manipulation
    emotional_keywords = ["outrage", "terrifying", "devastating", "horrifying",
                         "shocking", "disgusting", "appalling"]
    patterns["emotional_manipulation"] = count_keywords(text, emotional_keywords)
    
    # One-sided narrative (lack of counterpoints)
    balance_indicators = ["however", "although", "on the other hand", "but",
                         "despite", "nevertheless"]
    patterns["one_sided"] = 1.0 - min(1.0, count_phrases(text, balance_indicators) / 3)
    
    # No evidence (lack of specific data)
    evidence_indicators = ["study", "research", "data", "statistics", "percent",
                          "according to", "published"]
    patterns["no_evidence"] = 1.0 - min(1.0, count_keywords(text, evidence_indicators) / 5)
    
    # Extreme adjectives
    extreme_adjectives = ["always", "never", "every", "all", "none", "completely",
                         "totally", "absolutely", "definitely"]
    patterns["extreme_adjectives"] = count_keywords(text, extreme_adjectives)
    
    # Clickbait patterns
    clickbait_patterns = ["you won't believe", "what happened next", "number",
                         "will shock you", "doctors hate", "one weird trick"]
    patterns["clickbait"] = count_phrases(text, clickbait_patterns)
    
    RETURN patterns
```

**Correctness Properties**:
- Property 7: All pattern values are non-negative
- Property 8: Pattern detection is deterministic for same input
- Property 9: Empty text returns zero counts for all patterns

### Algorithm 4: Risk Level Determination

**Purpose**: Determine risk level based on credibility score

**Input**:
- `credibility_score`: int (0-100)

**Output**:
- `risk_level`: str (Low Risk | Medium Risk | High Risk)

**Logic**:
```
FUNCTION determine_risk_level(credibility_score):
    IF credibility_score >= 75:
        RETURN "Low Risk"
    ELSE IF credibility_score >= 40:
        RETURN "Medium Risk"
    ELSE:
        RETURN "High Risk"
```

**Correctness Properties**:
- Property 10: Risk level is always one of {Low Risk, Medium Risk, High Risk}
- Property 11: Score >= 75 always returns Low Risk
- Property 12: Score < 40 always returns High Risk
- Property 13: Score in [40, 74] always returns Medium Risk

### Algorithm 5: Key Indicator Extraction

**Purpose**: Extract the most significant indicators influencing assessment

**Input**:
- `patterns`: dict (pattern detection results)
- `text`: str (article text)

**Output**:
- `key_indicators`: list[str]

**Logic**:
```
FUNCTION extract_key_indicators(patterns, text):
    indicators = []
    
    IF patterns["sensational_phrases"] > 3:
        indicators.append("High use of sensational language")
    
    IF patterns["excessive_caps"] > 0.1:
        indicators.append("Excessive capitalization detected")
    
    IF patterns["vague_sources"] > 2:
        indicators.append("Multiple vague source references")
    
    IF patterns["conspiracy_framing"] > 0:
        indicators.append("Conspiracy framing language present")
    
    IF patterns["emotional_manipulation"] > 2:
        indicators.append("Emotional manipulation tactics detected")
    
    IF patterns["one_sided"] > 0.7:
        indicators.append("One-sided narrative without counterpoints")
    
    IF patterns["no_evidence"] > 0.7:
        indicators.append("Lack of verifiable evidence or data")
    
    IF patterns["extreme_adjectives"] > 5:
        indicators.append("Overuse of extreme adjectives")
    
    IF patterns["clickbait"] > 0:
        indicators.append("Clickbait patterns in text")
    
    IF length(indicators) == 0:
        indicators.append("Balanced language and structure")
        indicators.append("Appropriate use of sources")
    
    RETURN indicators
```

**Correctness Properties**:
- Property 14: Key indicators list is never empty
- Property 15: Each indicator corresponds to a detected pattern

### Algorithm 6: Emotional Tone Analysis

**Purpose**: Analyze emotional tone and manipulation tactics

**Input**:
- `patterns`: dict (pattern detection results)
- `text`: str (article text)

**Output**:
- `emotional_tone`: str

**Logic**:
```
FUNCTION analyze_emotional_tone(patterns, text):
    IF patterns["emotional_manipulation"] > 3:
        tone = "Highly emotional and manipulative"
    ELSE IF patterns["sensational_phrases"] > 3:
        tone = "Sensationalized and attention-seeking"
    ELSE IF patterns["conspiracy_framing"] > 0:
        tone = "Conspiratorial and fear-inducing"
    ELSE IF patterns["emotional_manipulation"] > 0:
        tone = "Moderately emotional"
    ELSE:
        tone = "Neutral and analytical"
    
    RETURN tone
```

**Correctness Properties**:
- Property 16: Emotional tone is always a non-empty string
- Property 17: Higher emotional manipulation scores result in more critical tone descriptions

### Algorithm 7: Suspicious Claim Identification

**Purpose**: Identify claims requiring fact-checking

**Input**:
- `text`: str (article text)

**Output**:
- `suspicious_claims`: list[str]

**Logic**:
```
FUNCTION identify_suspicious_claims(text):
    claims = []
    sentences = split_into_sentences(text)
    
    FOR EACH sentence IN sentences:
        suspicion_score = 0
        
        # Check for vague sources
        IF contains_vague_source(sentence):
            suspicion_score += 2
        
        # Check for extraordinary claims
        IF contains_extreme_language(sentence):
            suspicion_score += 1
        
        # Check for lack of evidence
        IF NOT contains_evidence_markers(sentence):
            suspicion_score += 1
        
        # Check for conspiracy language
        IF contains_conspiracy_markers(sentence):
            suspicion_score += 2
        
        IF suspicion_score >= 3:
            claims.append(sentence.strip())
    
    # Limit to top 5 most suspicious
    RETURN claims[:5]
```

**Correctness Properties**:
- Property 18: Suspicious claims list contains at most 5 items
- Property 19: Each claim is a sentence from the original text
- Property 20: Empty text returns empty claims list

### Algorithm 8: Confidence Score Calculation

**Purpose**: Calculate system confidence in its assessment

**Input**:
- `model_confidence`: float (0.0-1.0)
- `pattern_consistency`: float (0.0-1.0, how consistent patterns are)

**Output**:
- `confidence`: int (0-100)

**Logic**:
```
FUNCTION calculate_confidence(model_confidence, pattern_consistency):
    # Combine model confidence and pattern consistency
    combined_confidence = (model_confidence * 0.6) + (pattern_consistency * 0.4)
    
    confidence_score = combined_confidence * 100
    
    RETURN round(confidence_score)
```

**Correctness Properties**:
- Property 21: Confidence score is always in range [0, 100]
- Property 22: Higher model confidence increases overall confidence
- Property 23: Higher pattern consistency increases overall confidence

## Implementation Details

### File Structure

```
app.py                          # Main Flask application (existing, to be extended)
credibility_analyzer.py         # New: Main analyzer orchestration
pattern_detector.py             # New: Pattern detection logic
emotional_analyzer.py           # New: Emotional tone analysis
claim_highlighter.py            # New: Suspicious claim identification
utils.py                        # New: Helper functions
```

### Integration Points

1. **Existing Model Reuse**: The implementation will use the existing `best_model.joblib` and `tfidf_vectorizer.joblib` for base predictions
2. **New Endpoint**: Add `/analyze` endpoint to Flask app for comprehensive analysis
3. **Preserved Functionality**: Keep existing `/predict` endpoint unchanged
4. **Shared Preprocessing**: Use existing `clean_text()` function for consistency

### Error Handling

- Insufficient text (< 50 chars): Return UNVERIFIED classification
- Model not loaded: Return 503 error with appropriate message
- Invalid JSON input: Return 400 error with validation message
- Empty text field: Return 400 error

## Testing Strategy

### Unit Tests
- Test each algorithm independently with known inputs
- Verify output format compliance
- Test edge cases (empty text, very long text, special characters)

### Property-Based Tests
- Property 1-23: Verify all correctness properties hold for random inputs
- Test classification invariants
- Test score range constraints
- Test risk level thresholds

### Integration Tests
- Test full analysis pipeline with sample articles
- Verify JSON output format
- Test integration with existing Flask endpoints

## Performance Considerations

- Pattern detection uses simple string matching for speed
- Limit suspicious claims to top 5 to control output size
- Reuse existing model and vectorizer (no retraining needed)
- Text preprocessing uses existing optimized function

## Security Considerations

- Input validation: Check text length and format
- No external API calls: All analysis is local
- No data persistence: Stateless analysis
- Sanitize text input to prevent injection attacks

## Deployment Notes

- No changes to existing model files required
- New Python files added to project root
- No new dependencies beyond existing requirements
- Compatible with existing Flask deployment setup

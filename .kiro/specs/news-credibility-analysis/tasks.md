# Implementation Plan: News Credibility and Misinformation Analysis Assistant

## Overview

This implementation plan breaks down the News Credibility and Misinformation Analysis Assistant into discrete coding tasks. The system extends the existing Flask application with comprehensive credibility assessment capabilities, including pattern detection, emotional tone analysis, and structured JSON output. All implementation will be in Python, leveraging the existing trained model and vectorizer.

## Tasks

- [x] 1. Create utility functions module
  - Create `utils.py` file with helper functions for text processing
  - Implement `count_keywords(text, keywords)` function to count keyword occurrences
  - Implement `count_phrases(text, phrases)` function to count phrase occurrences
  - Implement `split_into_sentences(text)` function to split text into sentences
  - Implement `contains_vague_source(sentence)` function to detect vague source references
  - Implement `contains_extreme_language(sentence)` function to detect extreme language
  - Implement `contains_evidence_markers(sentence)` function to detect evidence markers
  - Implement `contains_conspiracy_markers(sentence)` function to detect conspiracy language
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 9.5_

- [ ]* 1.1 Write unit tests for utility functions
  - Test keyword and phrase counting with various inputs
  - Test sentence splitting with edge cases
  - Test detection functions with positive and negative examples
  - _Requirements: 6.1-6.9, 9.5_

- [x] 2. Implement pattern detection module
  - Create `pattern_detector.py` file
  - Implement `PatternDetector` class with `detect_patterns(text)` method
  - Detect sensational phrases using keyword matching
  - Detect excessive capitalization by analyzing word patterns
  - Detect vague source references using phrase patterns
  - Detect conspiracy framing language
  - Detect emotional manipulation keywords
  - Detect one-sided narratives by checking for balance indicators
  - Detect lack of evidence by checking for evidence markers
  - Detect extreme adjectives usage
  - Detect clickbait patterns
  - Return dictionary with all pattern detection results
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10_

- [ ]* 2.1 Write property test for pattern detection
  - **Property 7: All pattern values are non-negative**
  - **Property 8: Pattern detection is deterministic for same input**
  - **Property 9: Empty text returns zero counts for all patterns**
  - **Validates: Requirements 6.1-6.10**

- [ ]* 2.2 Write unit tests for pattern detector
  - Test each pattern type with known examples
  - Test with articles containing multiple patterns
  - Test with neutral articles
  - _Requirements: 6.1-6.10_

- [x] 3. Implement emotional tone analyzer
  - Create `emotional_analyzer.py` file
  - Implement `EmotionalAnalyzer` class with `analyze_emotional_tone(patterns, text)` method
  - Classify tone based on emotional manipulation score
  - Classify tone based on sensational phrases
  - Classify tone based on conspiracy framing
  - Return descriptive emotional tone string
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

- [ ]* 3.1 Write property test for emotional analyzer
  - **Property 16: Emotional tone is always a non-empty string**
  - **Property 17: Higher emotional manipulation scores result in more critical tone descriptions**
  - **Validates: Requirements 8.1-8.6**

- [ ]* 3.2 Write unit tests for emotional analyzer
  - Test tone classification with various pattern combinations
  - Test edge cases with zero patterns
  - _Requirements: 8.1-8.6_

- [x] 4. Implement suspicious claim highlighter
  - Create `claim_highlighter.py` file
  - Implement `ClaimHighlighter` class with `identify_suspicious_claims(text)` method
  - Split text into sentences
  - Calculate suspicion score for each sentence based on vague sources
  - Calculate suspicion score based on extreme language
  - Calculate suspicion score based on lack of evidence
  - Calculate suspicion score based on conspiracy markers
  - Filter sentences with suspicion score >= 3
  - Return top 5 most suspicious claims
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ]* 4.1 Write property test for claim highlighter
  - **Property 18: Suspicious claims list contains at most 5 items**
  - **Property 19: Each claim is a sentence from the original text**
  - **Property 20: Empty text returns empty claims list**
  - **Validates: Requirements 9.1-9.5**

- [ ]* 4.2 Write unit tests for claim highlighter
  - Test with text containing suspicious claims
  - Test with neutral text
  - Test with more than 5 suspicious claims
  - _Requirements: 9.1-9.5_

- [x] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Implement core credibility analyzer
  - Create `credibility_analyzer.py` file
  - Implement `CredibilityAnalyzer` class with initialization
  - Implement `calculate_pattern_score(patterns)` method to aggregate pattern results
  - Implement `classify_credibility(text, model_prediction, model_confidence, detected_patterns)` method
  - Handle insufficient text case (< 50 chars) returning UNVERIFIED
  - Implement classification logic combining model prediction and pattern analysis
  - Implement `calculate_credibility_score(model_confidence, model_prediction, pattern_score)` method
  - Calculate base score from model prediction and confidence
  - Apply pattern penalty to adjust score
  - Clamp score to [0, 100] range
  - _Requirements: 1.1, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ]* 6.1 Write property tests for classification
  - **Property 1: Classification is always one of {REAL, FAKE, MISLEADING, UNVERIFIED}**
  - **Property 2: Insufficient text (< 50 chars) always returns UNVERIFIED**
  - **Property 3: Classification considers both model prediction and pattern analysis**
  - **Validates: Requirements 1.5, 2.1-2.6**

- [ ]* 6.2 Write property tests for credibility scoring
  - **Property 4: Credibility score is always in range [0, 100]**
  - **Property 5: Higher pattern_score reduces credibility_score**
  - **Property 6: Model prediction of 1 (credible) increases base score**
  - **Validates: Requirements 3.1-3.5**

- [ ]* 6.3 Write unit tests for credibility analyzer core methods
  - Test classification with various model predictions and patterns
  - Test score calculation with edge cases
  - Test insufficient text handling
  - _Requirements: 1.1-1.5, 2.1-2.6, 3.1-3.5_

- [x] 7. Implement risk calculator and supporting methods
  - In `credibility_analyzer.py`, implement `determine_risk_level(credibility_score)` method
  - Return "Low Risk" for score >= 75
  - Return "Medium Risk" for score in [40, 74]
  - Return "High Risk" for score < 40
  - Implement `calculate_confidence(model_confidence, pattern_consistency)` method
  - Combine model confidence and pattern consistency with weighted average
  - Return confidence score in [0, 100] range
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ]* 7.1 Write property tests for risk calculator
  - **Property 10: Risk level is always one of {Low Risk, Medium Risk, High Risk}**
  - **Property 11: Score >= 75 always returns Low Risk**
  - **Property 12: Score < 40 always returns High Risk**
  - **Property 13: Score in [40, 74] always returns Medium Risk**
  - **Validates: Requirements 4.1-4.5**

- [ ]* 7.2 Write property tests for confidence calculation
  - **Property 21: Confidence score is always in range [0, 100]**
  - **Property 22: Higher model confidence increases overall confidence**
  - **Property 23: Higher pattern consistency increases overall confidence**
  - **Validates: Requirements 5.1-5.5**

- [ ]* 7.3 Write unit tests for risk calculator and confidence methods
  - Test risk level thresholds with boundary values
  - Test confidence calculation with various inputs
  - _Requirements: 4.1-4.5, 5.1-5.5_

- [x] 8. Implement key indicator extraction and text generation
  - In `credibility_analyzer.py`, implement `extract_key_indicators(patterns, text)` method
  - Generate indicator descriptions based on pattern thresholds
  - Ensure at least one indicator is always returned
  - Implement `generate_analysis_summary(classification, credibility_score, key_indicators)` method
  - Create 2-4 sentence summary referencing primary factors
  - Implement `generate_recommended_action(risk_level)` method based on risk level
  - Implement `generate_explanation(classification, credibility_score, patterns, indicators)` method
  - Create detailed explanation referencing specific patterns and findings
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 10.1, 10.2, 10.3, 10.4, 10.5, 11.1, 11.2, 11.3, 11.4, 11.5, 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ]* 8.1 Write property tests for key indicator extraction
  - **Property 14: Key indicators list is never empty**
  - **Property 15: Each indicator corresponds to a detected pattern**
  - **Validates: Requirements 7.1-7.5**

- [ ]* 8.2 Write unit tests for text generation methods
  - Test summary generation with various classifications
  - Test recommended action for each risk level
  - Test explanation generation with different pattern combinations
  - _Requirements: 7.1-7.5, 10.1-10.5, 11.1-11.5, 12.1-12.5_

- [x] 9. Implement main analysis orchestration method
  - In `credibility_analyzer.py`, implement `analyze(text, model, vectorizer)` method
  - Validate input text and handle insufficient text case
  - Use existing model and vectorizer for base prediction
  - Call pattern detector to get pattern analysis
  - Calculate pattern score and pattern consistency
  - Call classification engine to get classification
  - Calculate credibility score
  - Determine risk level
  - Calculate confidence score
  - Extract key indicators
  - Analyze emotional tone using EmotionalAnalyzer
  - Identify suspicious claims using ClaimHighlighter
  - Generate analysis summary
  - Generate recommended action
  - Generate detailed explanation
  - Return complete analysis dictionary
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ]* 9.1 Write integration tests for full analysis pipeline
  - Test with sample credible articles
  - Test with sample fake articles
  - Test with sample misleading articles
  - Test with insufficient text
  - Verify all output fields are present
  - _Requirements: 1.1-1.5, 13.1-13.5_

- [x] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 11. Implement JSON formatter and output validation
  - In `credibility_analyzer.py`, implement `format_json_output(analysis_result)` method
  - Ensure all required fields are present: classification, credibility_score, risk_level, confidence, analysis_summary, key_indicators, emotional_tone, suspicious_claims, recommended_action, explanation
  - Validate data types: strings for classification, risk_level, analysis_summary, emotional_tone, recommended_action, explanation
  - Validate data types: integers for credibility_score, confidence
  - Validate data types: arrays for key_indicators, suspicious_claims
  - Return valid JSON structure
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7_

- [ ]* 11.1 Write unit tests for JSON formatter
  - Test JSON structure compliance
  - Test data type validation
  - Test with various analysis results
  - Verify JSON can be parsed without errors
  - _Requirements: 14.1-14.7_

- [x] 12. Integrate with Flask application
  - In `app.py`, import CredibilityAnalyzer and related components
  - Create new `/analyze` POST endpoint
  - Accept JSON input with "text" field
  - Validate input and return 400 error for missing/empty text
  - Check if model is loaded, return 503 error if not
  - Call CredibilityAnalyzer.analyze() with text, model, and vectorizer
  - Return JSON response with analysis results
  - Preserve existing `/predict` endpoint functionality
  - Add error handling for analysis failures
  - _Requirements: 1.1, 1.2, 1.3, 15.1, 15.2, 15.3, 15.4, 15.5_

- [ ]* 12.1 Write integration tests for Flask endpoint
  - Test `/analyze` endpoint with valid input
  - Test with missing text field
  - Test with empty text
  - Test with model not loaded scenario
  - Verify existing `/predict` endpoint still works
  - _Requirements: 1.1-1.3, 15.1-15.5_

- [x] 13. Add input validation and security measures
  - In `app.py`, add text length validation (max 50,000 characters)
  - Sanitize input text to prevent injection attacks
  - Add rate limiting considerations (document in comments)
  - Add request logging for monitoring
  - Handle edge cases: special characters, unicode, very long text
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ]* 13.1 Write security tests
  - Test with very long text input
  - Test with special characters and unicode
  - Test with malicious input patterns
  - _Requirements: 13.1-13.5_

- [x] 14. Final integration and wiring
  - Verify all components are properly imported and connected
  - Test full pipeline from Flask endpoint to JSON output
  - Ensure existing model and vectorizer are correctly reused
  - Verify no breaking changes to existing functionality
  - Add inline documentation and docstrings to all new functions
  - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_

- [ ]* 14.1 Write end-to-end integration tests
  - Test complete workflow with real article examples
  - Verify JSON output format compliance
  - Test error handling paths
  - Verify performance with typical article lengths
  - _Requirements: 1.1-1.5, 14.1-14.7, 15.1-15.5_

- [x] 15. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- The implementation reuses the existing Flask app structure, model, and vectorizer
- All new code will be in Python, consistent with the existing codebase
- Pattern detection uses simple string matching for performance
- No external dependencies beyond existing requirements.txt

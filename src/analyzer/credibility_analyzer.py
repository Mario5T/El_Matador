"""
Core credibility-analysis orchestrator — refactored into src/analyzer/.

Changes vs. original credibility_analyzer.py
--------------------------------------------
* All imports come from the ``src.*`` packages (no sys.path hacks).
* The inner ``clean_text_for_model`` helper has been removed; it now
  lives canonically in ``src.utils.text_utils``.
* PatternDetector, EmotionalAnalyzer, and ClaimHighlighter are
  instantiated **once** in ``__init__`` (not on every ``analyze()`` call),
  avoiding repeated object construction.
* Full type hints throughout.
"""

from __future__ import annotations

from typing import Any, Dict, List

from src.utils import clean_text_for_model
from src.patterns import PatternDetector, EmotionalAnalyzer, ClaimHighlighter


class CredibilityAnalyzer:
    """
    Orchestrates the complete credibility-assessment pipeline.

    The analyzer combines:
    * An ML model prediction (TF-IDF + sklearn classifier)
    * Rule-based linguistic pattern detection
    * Emotional tone classification
    * Suspicious-claim extraction

    Sub-components are instantiated once in ``__init__`` for efficiency.
    """

    # ------------------------------------------------------------------
    # Scoring constants (centralised for easy tuning)
    # ------------------------------------------------------------------
    _MODEL_WEIGHT: float = 0.70
    _PATTERN_WEIGHT: float = 0.30

    _MODEL_CONFIDENCE_WEIGHT: float = 0.60
    _PATTERN_CONSISTENCY_WEIGHT: float = 0.40

    _FAKE_CONF_THRESHOLD: float = 0.75
    _REAL_CONF_THRESHOLD: float = 0.75
    _LOW_CONF_THRESHOLD: float = 0.50

    _FAKE_PATTERN_HIGH: float = 0.70
    _REAL_PATTERN_LOW: float = 0.30
    _MED_PATTERN_THRESHOLD: float = 0.50

    _HIGH_CREDIBILITY: int = 75
    _MED_CREDIBILITY: int = 40

    _MIN_TEXT_LENGTH: int = 50

    def __init__(self) -> None:
        """Initialise sub-components (created once per analyzer instance)."""
        self._pattern_detector = PatternDetector()
        self._emotional_analyzer = EmotionalAnalyzer()
        self._claim_highlighter = ClaimHighlighter()

    # ------------------------------------------------------------------
    # Pattern scoring
    # ------------------------------------------------------------------

    def calculate_pattern_score(self, patterns: Dict[str, float]) -> float:
        """
        Aggregate pattern-detection results into a single suspicion score.

        Args:
            patterns: Dict produced by ``PatternDetector.detect_patterns()``.

        Returns:
            Float in ``[0.0, 1.0]`` — higher means more suspicious.
        """
        sensational  = min(1.0, patterns.get("sensational_phrases", 0) / 5.0)
        excessive_caps = patterns.get("excessive_caps", 0.0)
        vague_sources  = min(1.0, patterns.get("vague_sources", 0) / 3.0)
        conspiracy     = min(1.0, patterns.get("conspiracy_framing", 0) / 2.0)
        emotional      = min(1.0, patterns.get("emotional_manipulation", 0) / 4.0)
        one_sided      = patterns.get("one_sided", 0.0)
        no_evidence    = patterns.get("no_evidence", 0.0)
        extreme_adj    = min(1.0, patterns.get("extreme_adjectives", 0) / 6.0)
        clickbait      = min(1.0, patterns.get("clickbait", 0) / 2.0)

        return (
            sensational   * 0.15 +
            excessive_caps * 0.10 +
            vague_sources  * 0.15 +
            conspiracy     * 0.15 +
            emotional      * 0.10 +
            one_sided      * 0.10 +
            no_evidence    * 0.10 +
            extreme_adj    * 0.10 +
            clickbait      * 0.05
        )

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def classify_credibility(
        self,
        text: str,
        model_prediction: int,
        model_confidence: float,
        detected_patterns: Dict[str, float],
    ) -> str:
        """
        Assign a credibility label based on model output and pattern score.

        Returns:
            One of ``"REAL"``, ``"FAKE"``, ``"MISLEADING"``, ``"UNVERIFIED"``.
        """
        if len(text) < self._MIN_TEXT_LENGTH:
            return "UNVERIFIED"

        pattern_score = self.calculate_pattern_score(detected_patterns)

        if model_prediction == 0 and model_confidence > self._FAKE_CONF_THRESHOLD:
            return "FAKE" if pattern_score > self._FAKE_PATTERN_HIGH else "MISLEADING"

        if model_prediction == 1 and model_confidence > self._REAL_CONF_THRESHOLD:
            return "REAL" if pattern_score < self._REAL_PATTERN_LOW else "MISLEADING"

        if model_confidence < self._LOW_CONF_THRESHOLD:
            return "UNVERIFIED"

        return "MISLEADING" if pattern_score > self._MED_PATTERN_THRESHOLD else "REAL"

    # ------------------------------------------------------------------
    # Scoring helpers
    # ------------------------------------------------------------------

    def calculate_credibility_score(
        self,
        model_confidence: float,
        model_prediction: int,
        pattern_score: float,
    ) -> int:
        """
        Compute a 0–100 credibility score (higher = more credible).

        Blend: 70 % model component + 30 % pattern component.
        """
        if model_prediction == 1:
            model_component = model_confidence * 100
        else:
            model_component = (1 - model_confidence) * 100

        pattern_component = (1 - pattern_score) * 100

        score = (
            model_component  * self._MODEL_WEIGHT +
            pattern_component * self._PATTERN_WEIGHT
        )
        return round(max(0, min(100, score)))

    def determine_risk_level(self, credibility_score: int) -> str:
        """Map credibility score to a risk label."""
        if credibility_score >= self._HIGH_CREDIBILITY:
            return "Low Risk"
        if credibility_score >= self._MED_CREDIBILITY:
            return "Medium Risk"
        return "High Risk"

    def calculate_confidence(
        self,
        model_confidence: float,
        pattern_consistency: float,
    ) -> int:
        """Combined system confidence: 60 % model + 40 % pattern consistency."""
        combined = (
            model_confidence    * self._MODEL_CONFIDENCE_WEIGHT +
            pattern_consistency * self._PATTERN_CONSISTENCY_WEIGHT
        )
        return round(combined * 100)

    # ------------------------------------------------------------------
    # Indicator / summary / explanation helpers
    # ------------------------------------------------------------------

    def extract_key_indicators(
        self, patterns: Dict[str, float], text: str  # noqa: ARG002
    ) -> List[str]:
        """Return human-readable descriptions of the most significant patterns."""
        indicators: List[str] = []

        checks = [
            (patterns.get("sensational_phrases", 0) > 3,      "High use of sensational language"),
            (patterns.get("excessive_caps", 0.0) > 0.1,       "Excessive capitalization detected"),
            (patterns.get("vague_sources", 0) > 2,            "Multiple vague source references"),
            (patterns.get("conspiracy_framing", 0) > 0,       "Conspiracy framing language present"),
            (patterns.get("emotional_manipulation", 0) > 2,   "Emotional manipulation tactics detected"),
            (patterns.get("one_sided", 0.0) > 0.7,            "One-sided narrative without counterpoints"),
            (patterns.get("no_evidence", 0.0) > 0.7,          "Lack of verifiable evidence or data"),
            (patterns.get("extreme_adjectives", 0) > 5,       "Overuse of extreme adjectives"),
            (patterns.get("clickbait", 0) > 0,                "Clickbait patterns in text"),
        ]

        for condition, label in checks:
            if condition:
                indicators.append(label)

        if not indicators:
            indicators = ["Balanced language and structure", "Appropriate use of sources"]

        return indicators

    def generate_analysis_summary(
        self,
        classification: str,
        credibility_score: int,
        key_indicators: List[str],
    ) -> str:
        """Generate a concise 2–4 sentence analysis summary."""
        intros = {
            "REAL":        f"This article appears credible with a credibility score of {credibility_score}/100. ",
            "FAKE":        f"This article shows strong indicators of misinformation with a credibility score of {credibility_score}/100. ",
            "MISLEADING":  f"This article contains misleading elements with a credibility score of {credibility_score}/100. ",
            "UNVERIFIED":  f"This article cannot be reliably assessed with a credibility score of {credibility_score}/100. ",
        }
        closings = {
            "REAL":       "The content demonstrates balanced reporting and appropriate sourcing.",
            "FAKE":       "Multiple red flags suggest this content should be treated with extreme skepticism.",
            "MISLEADING": "While some elements may be factual, the overall presentation raises concerns.",
            "UNVERIFIED": "Additional information would be needed for a more definitive assessment.",
        }

        summary = intros.get(classification, intros["UNVERIFIED"])

        primary = key_indicators[:3]
        if len(primary) == 1:
            summary += f"The primary factor is: {primary[0].lower()}. "
        elif len(primary) == 2:
            summary += f"Key factors include: {primary[0].lower()} and {primary[1].lower()}. "
        elif len(primary) >= 3:
            summary += (
                f"Key factors include: {primary[0].lower()}, "
                f"{primary[1].lower()}, and {primary[2].lower()}. "
            )

        summary += closings.get(classification, closings["UNVERIFIED"])
        return summary

    def generate_recommended_action(self, risk_level: str) -> str:
        """Return actionable guidance based on risk level."""
        actions = {
            "High Risk": (
                "Exercise extreme caution with this content. Verify claims through multiple "
                "independent and reputable sources before accepting or sharing. Consider this "
                "content potentially misleading or false."
            ),
            "Medium Risk": (
                "Approach this content with caution. Cross-reference key claims with other "
                "credible sources and look for additional evidence before drawing conclusions "
                "or sharing."
            ),
            "Low Risk": (
                "This content appears credible based on linguistic analysis. However, always "
                "maintain critical thinking and verify important claims through additional "
                "sources when making significant decisions."
            ),
        }
        return actions.get(risk_level, actions["Medium Risk"])

    def generate_explanation(
        self,
        classification: str,
        credibility_score: int,
        patterns: Dict[str, float],
        indicators: List[str],
    ) -> str:
        """Generate a detailed natural-language explanation of the assessment."""
        class_notes = {
            "REAL":       "linguistic patterns and content structure align with credible journalism.",
            "FAKE":       "strong linguistic patterns associated with misinformation and fabricated content.",
            "MISLEADING": "a mix of credible and suspicious elements, suggesting partial truth with potential distortion.",
            "UNVERIFIED": "insufficient information or ambiguous patterns that prevent a definitive assessment.",
        }
        explanation = (
            f"The article received a classification of '{classification}' with a credibility "
            f"score of {credibility_score}/100. "
            f"This classification indicates {class_notes.get(classification, '')} "
        )

        pattern_score = self.calculate_pattern_score(patterns)
        explanation += (
            f"The overall pattern analysis score is {pattern_score:.2f} "
            f"(higher values indicate more suspicious patterns). "
        )

        if indicators:
            joined = ", and ".join(
                [", ".join(indicators[:-1]), indicators[-1]]
                if len(indicators) > 1
                else indicators
            )
            explanation += f"Specific findings include: {joined.lower()}. "

        notable: List[str] = []
        if patterns.get("sensational_phrases", 0) > 3:
            notable.append(f"sensational language ({int(patterns['sensational_phrases'])} instances)")
        if patterns.get("vague_sources", 0) > 2:
            notable.append(f"vague source references ({int(patterns['vague_sources'])} instances)")
        if patterns.get("emotional_manipulation", 0) > 2:
            notable.append(f"emotional manipulation tactics ({int(patterns['emotional_manipulation'])} instances)")
        if patterns.get("conspiracy_framing", 0) > 0:
            notable.append(f"conspiracy framing language ({int(patterns['conspiracy_framing'])} instances)")

        if notable:
            explanation += "Notable patterns detected: " + ", ".join(notable) + ". "

        explanation += (
            "This assessment is based exclusively on linguistic and structural analysis of "
            "the provided text, without external fact-checking or knowledge injection."
        )
        return explanation

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def analyze(
        self, text: str, model: Any, vectorizer: Any
    ) -> Dict[str, Any]:
        """
        Run the full credibility-assessment pipeline on *text*.

        Args:
            text: News article text.
            model: Trained sklearn classifier.
            vectorizer: Fitted TF-IDF vectorizer.

        Returns:
            Dictionary with keys: classification, credibility_score, risk_level,
            confidence, analysis_summary, key_indicators, emotional_tone,
            suspicious_claims, recommended_action, explanation, model_prediction,
            pattern_score, patterns.
        """
        _empty_result = {
            "classification": "UNVERIFIED",
            "credibility_score": 0,
            "risk_level": "High Risk",
            "confidence": 0,
            "analysis_summary": "",
            "key_indicators": ["Insufficient input"],
            "emotional_tone": "N/A",
            "suspicious_claims": [],
            "recommended_action": "Please provide article text for analysis.",
            "explanation": "INSUFFICIENT INFORMATION",
            "model_prediction": 0,
            "pattern_score": 0.0,
            "patterns": {},
        }

        if not text or not isinstance(text, str):
            _empty_result["analysis_summary"] = "No text provided for analysis."
            return _empty_result

        if len(text.strip()) < self._MIN_TEXT_LENGTH:
            _empty_result["analysis_summary"] = (
                "The provided text is too short for reliable analysis."
            )
            _empty_result["key_indicators"] = ["Insufficient text length"]
            _empty_result["recommended_action"] = (
                "Please provide more substantial article text for analysis."
            )
            return _empty_result

        # -- ML inference --------------------------------------------------
        cleaned = clean_text_for_model(text)
        features = vectorizer.transform([cleaned])
        model_prediction = int(model.predict(features)[0])

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(features)[0]
            model_confidence = float(max(proba))
        elif hasattr(model, "decision_function"):
            decision = abs(float(model.decision_function(features)[0]))
            model_confidence = min(1.0, 0.5 + decision / 10.0)
        else:
            model_confidence = 0.5

        # -- Pattern analysis ----------------------------------------------
        detected_patterns = self._pattern_detector.detect_patterns(text)
        pattern_score = self.calculate_pattern_score(detected_patterns)

        # Pattern consistency (low variance = high consistency)
        norm_vals = [
            min(1.0, detected_patterns.get("sensational_phrases", 0) / 5.0),
            detected_patterns.get("excessive_caps", 0.0),
            min(1.0, detected_patterns.get("vague_sources", 0) / 3.0),
            min(1.0, detected_patterns.get("conspiracy_framing", 0) / 2.0),
            min(1.0, detected_patterns.get("emotional_manipulation", 0) / 4.0),
            detected_patterns.get("one_sided", 0.0),
            detected_patterns.get("no_evidence", 0.0),
            min(1.0, detected_patterns.get("extreme_adjectives", 0) / 6.0),
            min(1.0, detected_patterns.get("clickbait", 0) / 2.0),
        ]
        mean_val = sum(norm_vals) / len(norm_vals)
        variance = sum((v - mean_val) ** 2 for v in norm_vals) / len(norm_vals)
        pattern_consistency = 1.0 - min(1.0, variance * 2.0)

        # -- Combine -------------------------------------------------------
        classification   = self.classify_credibility(
            text, model_prediction, model_confidence, detected_patterns
        )
        credibility_score = self.calculate_credibility_score(
            model_confidence, model_prediction, pattern_score
        )
        risk_level    = self.determine_risk_level(credibility_score)
        confidence    = self.calculate_confidence(model_confidence, pattern_consistency)
        key_indicators = self.extract_key_indicators(detected_patterns, text)
        emotional_tone = self._emotional_analyzer.analyze_emotional_tone(
            detected_patterns, text
        )
        suspicious_claims = self._claim_highlighter.identify_suspicious_claims(text)
        analysis_summary  = self.generate_analysis_summary(
            classification, credibility_score, key_indicators
        )
        recommended_action = self.generate_recommended_action(risk_level)
        explanation = self.generate_explanation(
            classification, credibility_score, detected_patterns, key_indicators
        )

        return {
            "classification":    classification,
            "credibility_score": credibility_score,
            "risk_level":        risk_level,
            "confidence":        confidence,
            "analysis_summary":  analysis_summary,
            "key_indicators":    key_indicators,
            "emotional_tone":    emotional_tone,
            "suspicious_claims": suspicious_claims,
            "recommended_action": recommended_action,
            "explanation":       explanation,
            "model_prediction":  model_prediction,
            "pattern_score":     pattern_score,
            "patterns":          detected_patterns,
        }

    # ------------------------------------------------------------------
    # Output validation
    # ------------------------------------------------------------------

    def format_json_output(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and return a JSON-safe dict conforming to the output schema.

        Raises:
            ValueError: If required fields are missing or have the wrong type.
        """
        required: Dict[str, type] = {
            "classification":    str,
            "credibility_score": int,
            "risk_level":        str,
            "confidence":        int,
            "analysis_summary":  str,
            "key_indicators":    list,
            "emotional_tone":    str,
            "suspicious_claims": list,
            "recommended_action": str,
            "explanation":       str,
        }

        missing = [f for f in required if f not in analysis_result]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        formatted: Dict[str, Any] = {}
        for field, expected_type in required.items():
            value = analysis_result[field]
            if not isinstance(value, expected_type):
                raise ValueError(
                    f"Field '{field}' should be {expected_type.__name__}, "
                    f"got {type(value).__name__}."
                )

            if field == "classification" and value not in {
                "REAL", "FAKE", "MISLEADING", "UNVERIFIED"
            }:
                raise ValueError(f"Invalid classification: {value}")

            if field in ("credibility_score", "confidence") and not (0 <= value <= 100):
                raise ValueError(f"'{field}' must be in [0, 100], got {value}.")

            if field == "risk_level" and value not in {
                "Low Risk", "Medium Risk", "High Risk"
            }:
                raise ValueError(f"Invalid risk_level: {value}")

            if field in ("key_indicators", "suspicious_claims"):
                if not all(isinstance(i, str) for i in value):
                    raise ValueError(f"All items in '{field}' must be strings.")

            formatted[field] = value

        return formatted

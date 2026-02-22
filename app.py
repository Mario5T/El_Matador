"""
News Article Credibility Classifier — Flask Web Application
============================================================
Serves the trained model via a REST API and a polished dashboard UI.

Routes:
  GET  /         → Dashboard UI
  POST /predict  → Credibility prediction
  POST /analyze  → Comprehensive credibility analysis
  GET  /health   → Model status
"""

import os
import re
import html
import logging
from datetime import datetime

import joblib
from flask import Flask, jsonify, render_template, request
from credibility_analyzer import CredibilityAnalyzer

# ── App Setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)

# Configure logging for monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security configuration
MAX_TEXT_LENGTH = 50000  # Maximum characters allowed in input text

# Rate limiting considerations:
# For production deployment, consider implementing rate limiting using:
# - Flask-Limiter: Provides decorator-based rate limiting per IP/user
# - Redis-based rate limiting: For distributed systems
# - API Gateway rate limiting: For cloud deployments (AWS API Gateway, etc.)
# Recommended limits:
# - 10 requests per minute per IP for /analyze endpoint
# - 20 requests per minute per IP for /predict endpoint
# - Implement exponential backoff for repeated violations

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.joblib")
TFIDF_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib")

DISCLAIMER = (
    "This system provides probabilistic credibility classification based on "
    "learned textual patterns. It does NOT perform real-time fact verification "
    "and should NOT be considered authoritative fact-checking. Predictions "
    "reflect source-level labeling patterns, not granular factual truth."
)

# ── Load Model ───────────────────────────────────────────────────────────────
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(TFIDF_PATH)
    model_loaded = True
    print("✅  Model and vectorizer loaded successfully.")
except Exception as e:
    model = None
    vectorizer = None
    model_loaded = False
    print(f"⚠️  Could not load model: {e}")


# ── Helpers ──────────────────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    """Same preprocessing as training pipeline."""
    text = str(text).lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def sanitize_input(text: str) -> str:
    """
    Sanitize input text to prevent injection attacks.
    
    Security measures:
    - Escape HTML entities to prevent XSS attacks
    - Remove null bytes that could cause issues
    - Normalize unicode to prevent homograph attacks
    - Strip control characters except newlines and tabs
    
    Args:
        text: Raw input text
        
    Returns:
        Sanitized text safe for processing
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Normalize unicode to NFC form (canonical composition)
    # This prevents homograph attacks using visually similar characters
    try:
        import unicodedata
        text = unicodedata.normalize('NFC', text)
    except Exception:
        pass  # If normalization fails, continue with original text
    
    # Escape HTML entities to prevent XSS
    text = html.unescape(text)  # First unescape any existing entities
    text = html.escape(text, quote=False)  # Then escape to prevent injection
    
    # Remove control characters except newline, tab, and carriage return
    # Control characters can cause issues in processing and logging
    text = ''.join(char for char in text if char in '\n\r\t' or not (0 <= ord(char) < 32 or ord(char) == 127))
    
    return text


def validate_text_input(text: str) -> tuple[bool, str]:
    """
    Validate text input for security and processing requirements.
    
    Args:
        text: Input text to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is empty string
    """
    # Check if text is a string
    if not isinstance(text, str):
        return False, "Input must be a string"
    
    # Check for empty or whitespace-only text
    if not text or not text.strip():
        return False, "Text cannot be empty or whitespace only"
    
    # Check text length
    if len(text) > MAX_TEXT_LENGTH:
        return False, f"Text exceeds maximum length of {MAX_TEXT_LENGTH} characters (received {len(text)} characters)"
    
    # Check for suspicious patterns that might indicate injection attempts
    # Look for excessive repetition of special characters
    suspicious_patterns = [
        (r'[<>]{50,}', "Excessive HTML-like brackets detected"),
        (r'[\{\}]{50,}', "Excessive curly braces detected"),
        (r'[\[\]]{50,}', "Excessive square brackets detected"),
        (r'[;]{20,}', "Excessive semicolons detected"),
    ]
    
    for pattern, message in suspicious_patterns:
        if re.search(pattern, text):
            return False, f"Suspicious input pattern: {message}"
    
    return True, ""


# ── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    """Serve the dashboard UI."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict credibility of a news article.

    Expects JSON: { "text": "article content here" }
    Returns JSON: { "label", "label_text", "confidence", "disclaimer" }
    """
    # Log request
    logger.info(f"Received /predict request from {request.remote_addr}")
    
    if not model_loaded:
        logger.error("Model not loaded - cannot process prediction request")
        return jsonify({"error": "Model not loaded. Run train_model.py first."}), 503

    try:
        data = request.get_json(force=True)
    except Exception as e:
        logger.warning(f"Invalid JSON in request: {e}")
        return jsonify({"error": "Invalid JSON format"}), 400
    
    raw_text = data.get("text", "")
    
    # Validate input
    is_valid, error_msg = validate_text_input(raw_text)
    if not is_valid:
        logger.warning(f"Input validation failed: {error_msg}")
        return jsonify({"error": error_msg}), 400
    
    # Sanitize input
    try:
        sanitized_text = sanitize_input(raw_text)
    except ValueError as e:
        logger.warning(f"Input sanitization failed: {e}")
        return jsonify({"error": str(e)}), 400

    # Preprocess & predict
    cleaned = clean_text(sanitized_text)
    features = vectorizer.transform([cleaned])

    prediction = int(model.predict(features)[0])
    label_text = "Credible" if prediction == 1 else "Fake"

    # Confidence — use decision_function or predict_proba
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(features)[0]
        confidence = float(max(proba))
    elif hasattr(model, "decision_function"):
        decision = abs(float(model.decision_function(features)[0]))
        # Normalize decision function to 0.5–1.0 range
        confidence = min(1.0, 0.5 + decision / 10.0)
    else:
        confidence = None

    logger.info(f"Prediction completed: {label_text} (confidence: {confidence})")
    
    return jsonify(
        {
            "label": prediction,
            "label_text": label_text,
            "confidence": round(confidence, 4) if confidence else None,
            "disclaimer": DISCLAIMER,
        }
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Perform comprehensive credibility analysis on a news article.

    Expects JSON: { "text": "article content here" }
    Returns JSON with comprehensive analysis including:
        - classification: REAL, FAKE, MISLEADING, or UNVERIFIED
        - credibility_score: 0-100
        - risk_level: Low Risk, Medium Risk, or High Risk
        - confidence: 0-100
        - analysis_summary: Brief summary of the analysis
        - key_indicators: List of key factors influencing the assessment
        - emotional_tone: Description of emotional tone
        - suspicious_claims: List of claims requiring fact-checking
        - recommended_action: Actionable guidance based on risk level
        - explanation: Detailed explanation of the assessment
    """
    # Log request with timestamp
    logger.info(f"Received /analyze request from {request.remote_addr} at {datetime.now().isoformat()}")
    
    # Check if model is loaded
    if not model_loaded:
        logger.error("Model not loaded - cannot process analysis request")
        return jsonify({"error": "Model not loaded. Run train_model.py first."}), 503

    # Get and validate JSON input
    try:
        data = request.get_json(force=True)
    except Exception as e:
        logger.warning(f"Invalid JSON in request: {e}")
        return jsonify({"error": "Invalid JSON format"}), 400
    
    raw_text = data.get("text", "")

    # Validate input using security validation function
    is_valid, error_msg = validate_text_input(raw_text)
    if not is_valid:
        logger.warning(f"Input validation failed: {error_msg}")
        return jsonify({"error": error_msg}), 400

    # Sanitize input to prevent injection attacks
    try:
        sanitized_text = sanitize_input(raw_text)
    except ValueError as e:
        logger.warning(f"Input sanitization failed: {e}")
        return jsonify({"error": str(e)}), 400
    
    # Log text length for monitoring (helps detect abuse patterns)
    logger.info(f"Processing text of length {len(sanitized_text)} characters")

    try:
        # Initialize analyzer and perform analysis
        analyzer = CredibilityAnalyzer()
        analysis_result = analyzer.analyze(sanitized_text, model, vectorizer)

        # Format and validate JSON output
        formatted_output = analyzer.format_json_output(analysis_result)

        logger.info(f"Analysis completed successfully: classification={formatted_output.get('classification')}, "
                   f"credibility_score={formatted_output.get('credibility_score')}")
        
        return jsonify(formatted_output)

    except Exception as e:
        # Handle analysis failures with detailed logging
        logger.error(f"Analysis failed with exception: {type(e).__name__}: {str(e)}")
        return jsonify({
            "error": "Analysis failed",
            "details": str(e)
        }), 500


@app.route("/health")
def health():
    """Check model load status."""
    return jsonify({"model_loaded": model_loaded, "status": "ok" if model_loaded else "model_not_found"})


# ── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)

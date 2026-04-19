# El Matador — AI-Powered News Credibility Analyzer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E?logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green)

**El Matador** is an ML-powered news credibility analysis tool that helps users evaluate the trustworthiness of news articles. It combines a TF-IDF + scikit-learn classifier trained on 63,000+ labeled articles with a suite of rule-based linguistic pattern detectors to produce an interpretable credibility score.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Credibility Score (0–100)** | Blends ML model confidence (70%) with pattern analysis (30%) |
| **4-class classification** | `REAL`, `FAKE`, `MISLEADING`, `UNVERIFIED` |
| **9 pattern detectors** | Sensational language, excessive caps, vague sources, conspiracy framing, emotional manipulation, one-sidedness, lack of evidence, extreme adjectives, clickbait |
| **Emotional tone** | 5-level tone classification from *Neutral* to *Highly manipulative* |
| **Suspicious claims** | Up to 5 flagged sentences per article with fact-check guidance |
| **Streamlit UI** | Interactive two-column layout with full score breakdown |
| **CLI-compatible** | `analyze()` returns a JSON-serialisable dict for downstream integration |

---

## 🏗️ Project Structure

```
El_Matador/
├── src/                        # Refactored source packages
│   ├── analyzer/
│   │   └── credibility_analyzer.py  # Core orchestrator
│   ├── models/
│   │   └── model_loader.py          # Lazy singleton model loader
│   ├── patterns/
│   │   ├── pattern_detector.py      # 9-pattern linguistic detector
│   │   ├── emotional_analyzer.py    # Tone classifier
│   │   └── claim_highlighter.py     # Suspicious-claim extractor
│   └── utils/
│       └── text_utils.py            # Canonical text helpers
│
├── tests/                      # pytest test suite
│   ├── test_utils.py
│   ├── test_patterns.py
│   ├── test_claim_highlighter.py
│   └── test_analyzer.py
│
├── models/                     # Trained model artefacts (git-ignored)
│   ├── best_model.joblib
│   ├── tfidf_vectorizer.joblib
│   ├── metadata.txt
│   └── training_report.json
│
├── streamlit_app.py            # Streamlit UI entry point
├── train_model.py              # Model training script (with cross-validation)
├── pyproject.toml              # pytest config
├── requirements.txt
└── .gitignore
```

> **Note:** The legacy flat-file modules (`credibility_analyzer.py`, `pattern_detector.py`, etc.) remain in the root for backward compatibility. New development should target `src/`.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- `pip`

### 1 — Clone the repository

```bash
git clone https://github.com/Mario5T/El_Matador.git
cd El_Matador
```

### 2 — Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Download the dataset (for training only)

Download the **WELFake** dataset from Kaggle:

> [https://www.kaggle.com/datasets/saurabhshahane/fake-news-classification](https://www.kaggle.com/datasets/saurabhshahane/fake-news-classification)

Place the file at:
```
dataset/WELFake_Dataset.csv
```

> ⚠️ The CSV (~150 MB) is excluded from version control. You **only** need it to retrain the model.

### 5 — Train the model

```bash
python train_model.py
```

This will:
- Train Logistic Regression and Passive Aggressive classifiers
- Print full metrics (accuracy, precision, recall, F1, confusion matrix) for each
- Run 5-fold cross-validation on the best model
- Save artefacts to `models/`

Expected output (example):

```
[4/6] Training & evaluating models …

  ▸ Passive Aggressive  (trained in 1.8s)
    Accuracy  : 0.9667
    Precision : 0.9668
    Recall    : 0.9667
    F1 Score  : 0.9667

[5/6] Cross-validating best model (Passive Aggressive, k=5) …
    accuracy  : 0.9654 ± 0.0021
    precision : 0.9655 ± 0.0022
    recall    : 0.9654 ± 0.0021
    f1        : 0.9654 ± 0.0021
```

### 6 — Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

The app opens at **[http://localhost:8501](http://localhost:8501)**.

---

## 📥 Input / Output

### Input format

Paste the **plain text** of a news article (minimum 50 characters, maximum 50,000 characters).

**Example — credible article snippet:**
```
Scientists at Stanford University published a peer-reviewed study showing 
a new vaccine candidate was 89% effective in phase 3 trials involving 30,000 
participants. Dr. Jane Smith confirmed the results would be submitted to the FDA.
```

**Example — suspicious article snippet:**
```
SHOCKING: Government scientists EXPOSED! Sources say the deep state is 
covering up a massive false flag. Many believe this conspiracy, but the 
mainstream media doesn't want you to know the truth. Wake up, people!
```

### Output

The `analyze()` method returns a dictionary:

| Key | Type | Description |
|---|---|---|
| `classification` | `str` | `REAL`, `FAKE`, `MISLEADING`, or `UNVERIFIED` |
| `credibility_score` | `int` | 0–100; higher = more credible |
| `risk_level` | `str` | `Low Risk` (≥75), `Medium Risk` (40–74), `High Risk` (<40) |
| `confidence` | `int` | System confidence in its own assessment (0–100%) |
| `analysis_summary` | `str` | 2–4 sentence summary |
| `key_indicators` | `list[str]` | Top linguistic red flags detected |
| `emotional_tone` | `str` | Dominant tone from *Neutral* to *Highly emotional and manipulative* |
| `suspicious_claims` | `list[str]` | Up to 5 sentences flagged for fact-checking |
| `recommended_action` | `str` | Actionable user guidance |
| `explanation` | `str` | Detailed assessment explanation |
| `pattern_score` | `float` | Raw pattern suspicion score (0.0–1.0) |
| `patterns` | `dict` | All 9 pattern detector outputs |

---

## 🖥️ CLI Usage

```python
from src.models import ModelLoader
from src.analyzer import CredibilityAnalyzer

loader   = ModelLoader()
model, vectorizer = loader.load()   # cached after first call

analyzer = CredibilityAnalyzer()
result   = analyzer.analyze(article_text, model, vectorizer)

print(result["classification"])     # → "FAKE"
print(result["credibility_score"])  # → 18
```

---

## 🧪 Running Tests

```bash
pytest
```

Test suite covers:
- `test_utils.py`  — text preprocessing and sentence-level helpers
- `test_patterns.py` — PatternDetector outputs and edge cases
- `test_claim_highlighter.py` — suspicious-claim extraction
- `test_analyzer.py` — full pipeline with mocked ML model

---

## 📊 Model Performance

| Model | Accuracy | Precision | Recall | F1 (weighted) |
|---|---|---|---|---|
| Logistic Regression | ~94% | ~94% | ~94% | ~94% |
| Passive Aggressive ✅ | ~96.7% | ~96.7% | ~96.7% | **~96.7%** |

> Trained on WELFake dataset (~63,000 labelled articles, 80/20 split).  
> 5-fold cross-validation confirms generalisation (F1 std ≈ 0.002).

---

## 🚀 Deployment

### Streamlit Cloud (recommended)

1. Push to GitHub (model artefacts excluded — see below).
2. Connect repo to [share.streamlit.io](https://share.streamlit.io).
3. Set entry point: `streamlit_app.py`.
4. Add `models/best_model.joblib` and `models/tfidf_vectorizer.joblib` via **Streamlit Secrets** or a one-time download script in `streamlit_app.py`.

**Cold-start optimisation:** `@st.cache_resource` on `load_model()` ensures the model is loaded **once per session**, not on every rerun.

### Model caching note

Because `.joblib` files are excluded from git (they are ~2.5 MB total), you have two options for Streamlit Cloud:

- **Option A:** Upload artefacts to a private GCS/S3 bucket and download on cold start.
- **Option B:** Store them in [Streamlit Secrets / file-based secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) as base64-encoded blobs.

---

## 📋 Commit Strategy

Suggested branch / PR breakdown:

| Branch | Purpose |
|---|---|
| `feat/src-restructure` | Move modules into `src/` packages |
| `feat/model-pipeline` | Improved `train_model.py` with CV and JSON report |
| `feat/analyzer-refactor` | Singleton sub-components, constants, type hints |
| `feat/model-loader` | Lazy `ModelLoader` with `lru_cache` |
| `feat/tests` | Full pytest suite |
| `chore/gitignore` | Add `.DS_Store`, `models/*.joblib`, `dataset/` |
| `docs/readme` | This README |

---

## 🔮 Limitations

- **No real-time fact-checking** — analysis is purely linguistic/structural.
- **No knowledge injection** — the model has no live internet access.
- **Domain drift** — model trained on English news; performance may degrade on non-news text or other languages.
- **Satire blind spot** — satirical articles may score as MISLEADING due to sensational language patterns.

---

## 📄 License

MIT — see [LICENSE](LICENSE).

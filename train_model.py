"""
News Article Credibility Classifier — Training Pipeline
========================================================
Trains Logistic Regression & Passive Aggressive classifiers on the WELFake
dataset and serialises the best model + TF-IDF vectorizer to disk.

Improvements over v1
---------------------
* Cross-validation (StratifiedKFold, k=5) with averaged metrics
* Full sklearn classification_report (accuracy, precision, recall, F1)
* Confusion matrix logged to metadata
* Results written to models/training_report.json for CI/monitoring
* Single clean_text source of truth (imported from src.utils)

Labels:  1 = Credible / True   |   0 = Fake / Misinformation
"""

import json
import os
import sys
import time
import warnings
from typing import Dict, Any

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split

warnings.filterwarnings("ignore")

# Ensure src package is importable when run from repo root
sys.path.insert(0, os.path.dirname(__file__))
from src.utils import clean_text_for_model  # noqa: E402

# ── Configuration ────────────────────────────────────────────────────────────
DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset", "WELFake_Dataset.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
TFIDF_MAX_FEATURES = 50_000
TEST_SIZE = 0.20
RANDOM_STATE = 42
CV_FOLDS = 5

SCORING = {
    "accuracy":  "accuracy",
    "precision": "precision_weighted",
    "recall":    "recall_weighted",
    "f1":        "f1_weighted",
}


def _header(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print("=" * 60)


def _section(step: str, total: int, label: str) -> None:
    print(f"\n[{step}/{total}] {label}")


def evaluate_model(
    name: str,
    model: Any,
    X_train: Any,
    X_test: Any,
    y_train: Any,
    y_test: Any,
) -> Dict[str, Any]:
    """Train *model*, evaluate on held-out test set, return metrics dict."""
    t0 = time.time()
    model.fit(X_train, y_train)
    elapsed = time.time() - t0

    preds = model.predict(X_test)

    acc  = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, average="weighted", zero_division=0)
    rec  = recall_score(y_test, preds, average="weighted", zero_division=0)
    f1   = f1_score(y_test, preds, average="weighted", zero_division=0)
    cm   = confusion_matrix(y_test, preds).tolist()
    report = classification_report(
        y_test, preds, target_names=["Fake (0)", "Credible (1)"]
    )

    print(f"\n  ▸ {name}  (trained in {elapsed:.1f}s)")
    print(f"    Accuracy  : {acc:.4f}")
    print(f"    Precision : {prec:.4f}")
    print(f"    Recall    : {rec:.4f}")
    print(f"    F1 Score  : {f1:.4f}")
    print("    Confusion Matrix:")
    print(f"      {cm[0]}")
    print(f"      {cm[1]}")
    print("\n    Classification Report:")
    print(report)
    print("-" * 50)

    return {
        "name":      name,
        "accuracy":  acc,
        "precision": prec,
        "recall":    rec,
        "f1":        f1,
        "confusion_matrix": cm,
        "train_time_s": round(elapsed, 2),
    }


def cross_validate_model(
    name: str,
    model: Any,
    X: Any,
    y: Any,
    cv: int = CV_FOLDS,
) -> Dict[str, float]:
    """Run k-fold cross-validation and return averaged metrics."""
    print(f"\n  Cross-validating {name} (k={cv}) …")
    cv_results = cross_validate(
        model,
        X,
        y,
        cv=StratifiedKFold(n_splits=cv, shuffle=True, random_state=RANDOM_STATE),
        scoring=SCORING,
        n_jobs=-1,
        return_train_score=False,
    )

    summary: Dict[str, float] = {}
    for metric, key in [
        ("accuracy",  "test_accuracy"),
        ("precision", "test_precision"),
        ("recall",    "test_recall"),
        ("f1",        "test_f1"),
    ]:
        mean = np.mean(cv_results[key])
        std  = np.std(cv_results[key])
        summary[metric] = round(float(mean), 4)
        summary[f"{metric}_std"] = round(float(std), 4)
        print(f"    {metric:10s}: {mean:.4f} ± {std:.4f}")

    return summary


# ── Main ─────────────────────────────────────────────────────────────────────

_header("News Credibility Classifier — Training Pipeline")

# 1. Load & clean ─────────────────────────────────────────────────────────────
_section(1, 6, "Loading dataset …")
df = pd.read_csv(DATASET_PATH)
print(f"      Raw rows: {len(df):,}")

df.dropna(subset=["title", "text"], inplace=True)
df.drop_duplicates(subset=["title", "text"], inplace=True)
print(f"      After cleanup: {len(df):,}")

print("\n      Label distribution:")
for label, count in df["label"].value_counts().sort_index().items():
    tag = "Fake" if label == 0 else "Credible"
    print(f"        {label} ({tag}): {count:,}")

df["content"] = (df["title"].fillna("") + " " + df["text"].fillna("")).apply(
    clean_text_for_model
)

# 2. TF-IDF features ──────────────────────────────────────────────────────────
_section(2, 6, "Building TF-IDF features …")
tfidf = TfidfVectorizer(
    max_features=TFIDF_MAX_FEATURES,
    stop_words="english",
    ngram_range=(1, 2),
    sublinear_tf=True,
)

X = tfidf.fit_transform(df["content"])
y = df["label"]
print(f"      Feature matrix: {X.shape[0]:,} samples × {X.shape[1]:,} features")

# 3. Train / test split ───────────────────────────────────────────────────────
_section(3, 6, "Splitting data (80 / 20 stratified) …")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
)
print(f"      Train: {X_train.shape[0]:,}  |  Test: {X_test.shape[0]:,}")

# 4. Train & evaluate ─────────────────────────────────────────────────────────
_section(4, 6, "Training & evaluating models …")

candidates = {
    "Logistic Regression": LogisticRegression(
        C=1.0, max_iter=1000, solver="lbfgs", random_state=RANDOM_STATE, n_jobs=-1
    ),
    "Passive Aggressive": PassiveAggressiveClassifier(
        max_iter=50, random_state=RANDOM_STATE, n_jobs=-1
    ),
}

all_metrics: Dict[str, Dict] = {}
best_name, best_model, best_f1 = None, None, 0.0

for name, model in candidates.items():
    metrics = evaluate_model(name, model, X_train, X_test, y_train, y_test)
    all_metrics[name] = metrics
    if metrics["f1"] > best_f1:
        best_name, best_model, best_f1 = name, model, metrics["f1"]

# 5. Cross-validation ─────────────────────────────────────────────────────────
_section(5, 6, f"Cross-validating best model ({best_name}, k={CV_FOLDS}) …")

# Re-initialise the best model (cross_validate trains its own copies)
best_proto = candidates[best_name]
cv_metrics = cross_validate_model(best_name, best_proto, X, y, cv=CV_FOLDS)
print(f"\n  ✅  Best model: {best_name}  (holdout F1={best_f1:.4f})")

# 6. Serialise ────────────────────────────────────────────────────────────────
_section(6, 6, f"Saving model to {MODEL_DIR}/ …")
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.joblib"))
joblib.dump(tfidf,      os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib"))

# Plain-text metadata (backward-compatible)
with open(os.path.join(MODEL_DIR, "metadata.txt"), "w") as fh:
    fh.write(f"model_name: {best_name}\n")
    fh.write(f"f1_score: {best_f1:.4f}\n")
    fh.write(f"tfidf_max_features: {TFIDF_MAX_FEATURES}\n")
    fh.write(f"train_samples: {X_train.shape[0]}\n")
    fh.write(f"test_samples: {X_test.shape[0]}\n")

# Machine-readable training report (useful for CI assertions)
report: Dict[str, Any] = {
    "best_model": best_name,
    "holdout_metrics": all_metrics[best_name],
    "cross_validation": {
        "folds": CV_FOLDS,
        "metrics": cv_metrics,
    },
    "tfidf_max_features": TFIDF_MAX_FEATURES,
    "train_samples": int(X_train.shape[0]),
    "test_samples":  int(X_test.shape[0]),
    "all_models": all_metrics,
}
with open(os.path.join(MODEL_DIR, "training_report.json"), "w") as fh:
    json.dump(report, fh, indent=2)

print("\n✅  Training complete.")
print(f"   Model artefacts saved to  : {MODEL_DIR}/")
print(f"   Training report saved to  : {MODEL_DIR}/training_report.json\n")

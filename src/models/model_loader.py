"""
Lazy, singleton model loader for the trained scikit-learn pipeline.

Design decisions
----------------
* ``functools.lru_cache(maxsize=None)`` on the internal ``_load`` method
  guarantees the model and vectorizer are deserialised from disk exactly
  **once** per process — subsequent calls return the cached objects.
* The public ``ModelLoader`` class provides a clean interface and a
  ``reload()`` helper for testing / hot-swap scenarios.
* Supports both ``joblib`` (preferred) and ``pickle`` artefacts.
"""

import os
import functools
import pickle
from typing import Any, Tuple

import joblib


class ModelLoader:
    """
    Singleton-style loader for the trained model + TF-IDF vectorizer.

    Usage
    -----
    >>> loader = ModelLoader()
    >>> model, vectorizer = loader.load()
    """

    DEFAULT_MODEL_DIR = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "models",
    )

    def __init__(self, model_dir: str | None = None) -> None:
        self._model_dir = model_dir or self.DEFAULT_MODEL_DIR

    # ------------------------------------------------------------------
    # Internal cached loader (lru_cache on an instance method requires
    # the instance to be hashable; we work around this by caching a
    # module-level function and routing through it)
    # ------------------------------------------------------------------

    def load(self) -> Tuple[Any, Any]:
        """
        Return the (model, vectorizer) tuple, loading from disk on first call.

        Raises
        ------
        FileNotFoundError
            If model or vectorizer artefacts are missing.
        RuntimeError
            If the artefacts cannot be deserialised.
        """
        return _cached_load(self._model_dir)

    def reload(self) -> Tuple[Any, Any]:
        """Force a fresh load from disk (clears the cache)."""
        _cached_load.cache_clear()
        return self.load()


@functools.lru_cache(maxsize=None)
def _cached_load(model_dir: str) -> Tuple[Any, Any]:
    """Module-level cached function so the cache survives across instances."""
    model = _load_artefact(model_dir, "best_model")
    vectorizer = _load_artefact(model_dir, "tfidf_vectorizer")
    return model, vectorizer


def _load_artefact(model_dir: str, stem: str) -> Any:
    """
    Load a joblib or pickle artefact by *stem* name.

    Tries ``<stem>.joblib`` first, then ``<stem>.pkl``.
    """
    for ext, loader in [(".joblib", joblib.load), (".pkl", pickle.load)]:
        path = os.path.join(model_dir, stem + ext)
        if os.path.exists(path):
            try:
                if ext == ".pkl":
                    with open(path, "rb") as fh:
                        return loader(fh)
                return loader(path)
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to deserialise '{path}': {exc}"
                ) from exc

    raise FileNotFoundError(
        f"No artefact found for '{stem}' in '{model_dir}'. "
        "Run `python train_model.py` to generate the model files."
    )

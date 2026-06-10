from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

from .config import ARTIFACTS_ROOT, RUNTIME_ARTIFACTS_ROOT


def train_classifier(train_embeddings: np.ndarray, train_labels: np.ndarray) -> LogisticRegression:
    classifier = LogisticRegression(
        max_iter=4000,
        class_weight="balanced",
        solver="lbfgs",
    )
    classifier.fit(train_embeddings, train_labels)
    return classifier


def save_bundle(
    classifier: LogisticRegression,
    dataset_df: pd.DataFrame,
    embeddings: np.ndarray,
    output_dir: Path = ARTIFACTS_ROOT,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    bundle_path = output_dir / "style_classifier_bundle.joblib"
    joblib.dump(
        {
            "classifier": classifier,
            "dataset": dataset_df.to_dict(orient="records"),
            "embeddings": embeddings,
        },
        bundle_path,
    )
    return bundle_path


def load_bundle(bundle_path: Path | None = None) -> dict:
    path = bundle_path or ((RUNTIME_ARTIFACTS_ROOT if RUNTIME_ARTIFACTS_ROOT.exists() else ARTIFACTS_ROOT) / "style_classifier_bundle.joblib")
    return joblib.load(path)


def rank_similar_images(query_embedding: np.ndarray, reference_embeddings: np.ndarray, top_k: int = 6) -> list[int]:
    similarities = cosine_similarity(query_embedding[None, :], reference_embeddings)[0]
    ranked = np.argsort(similarities)[::-1]
    return ranked[:top_k].tolist()


def save_metrics(metrics: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2, ensure_ascii=False)

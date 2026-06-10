from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from style_inspiration_tool.config import ARTIFACTS_ROOT, REPORTS_ROOT, STYLE_LABELS
from style_inspiration_tool.training import save_metrics


def main() -> None:
    bundle = joblib.load(ARTIFACTS_ROOT / "style_classifier_bundle.joblib")
    split_df = pd.DataFrame(bundle["dataset"])
    embeddings = bundle["embeddings"]
    classifier = bundle["classifier"]

    test_mask = split_df["split"] == "test"
    test_df = split_df.loc[test_mask].reset_index(drop=True)
    test_embeddings = embeddings[test_mask.to_numpy()]
    predictions = classifier.predict(test_embeddings)
    probabilities = classifier.predict_proba(test_embeddings)

    accuracy = float(accuracy_score(test_df["label"], predictions))
    report = classification_report(test_df["label"], predictions, output_dict=True, zero_division=0)
    metrics = {
        "accuracy": accuracy,
        "classification_report": report,
    }
    save_metrics(metrics, REPORTS_ROOT / "metrics.json")

    test_df = test_df.assign(prediction=predictions, confidence=probabilities.max(axis=1))
    test_df.to_csv(REPORTS_ROOT / "test_predictions.csv", index=False)

    matrix = confusion_matrix(test_df["label"], predictions, labels=STYLE_LABELS)
    plt.figure(figsize=(6, 5))
    plt.imshow(matrix, cmap="Blues")
    plt.title("Style Classifier Confusion Matrix")
    plt.xticks(range(len(STYLE_LABELS)), STYLE_LABELS, rotation=45, ha="right")
    plt.yticks(range(len(STYLE_LABELS)), STYLE_LABELS)
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            plt.text(col, row, int(matrix[row, col]), ha="center", va="center")
    plt.tight_layout()
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    plt.savefig(REPORTS_ROOT / "confusion_matrix.png", dpi=200)
    plt.close()

    summary_lines = [
        "# Evaluation Summary",
        "",
        f"- Accuracy: {accuracy:.3f}",
        "",
        "## Notes",
        "",
        "- This is a small subjective starter dataset.",
        "- The confusion matrix should be used together with qualitative error analysis.",
        "- Misclassifications are part of the critical reflection, not just a failure to hide.",
    ]
    (REPORTS_ROOT / "evaluation_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print(f"Saved reports to: {REPORTS_ROOT}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse

import numpy as np

from style_inspiration_tool.clip_embedder import ClipEmbedder
from style_inspiration_tool.config import ARTIFACTS_ROOT, DEFAULT_RANDOM_STATE, SPLIT_CSV
from style_inspiration_tool.dataset import load_splits
from style_inspiration_tool.training import save_bundle, train_classifier


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a CLIP-embedding style classifier.")
    parser.add_argument("--seed", type=int, default=DEFAULT_RANDOM_STATE)
    args = parser.parse_args()

    split_df = load_splits(SPLIT_CSV)
    embedder = ClipEmbedder()
    embeddings = embedder.encode_paths(split_df["image_path"].tolist())
    train_mask = split_df["split"] == "train"
    classifier = train_classifier(embeddings[train_mask.to_numpy()], split_df.loc[train_mask, "label"].to_numpy())
    bundle_path = save_bundle(classifier, split_df, embeddings, output_dir=ARTIFACTS_ROOT)
    np.savez_compressed(ARTIFACTS_ROOT / "dataset_embeddings.npz", embeddings=embeddings)
    print(f"Saved model bundle: {bundle_path}")


if __name__ == "__main__":
    main()

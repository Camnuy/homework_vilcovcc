from __future__ import annotations

import argparse

import pandas as pd
from sklearn.model_selection import train_test_split

from style_inspiration_tool.config import DEFAULT_RANDOM_STATE, SPLIT_CSV
from style_inspiration_tool.dataset import scan_dataset


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare stratified train/val/test splits for the style dataset.")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--val-size", type=float, default=0.2, help="Fraction of the remaining train set to use for validation.")
    parser.add_argument("--seed", type=int, default=DEFAULT_RANDOM_STATE)
    args = parser.parse_args()

    dataset_df = scan_dataset()
    if dataset_df.empty:
        raise SystemExit("No dataset images found. Add images under data/style_dataset/images/<label>/ first.")

    train_val, test = train_test_split(
        dataset_df,
        test_size=args.test_size,
        stratify=dataset_df["label"],
        random_state=args.seed,
    )
    train, val = train_test_split(
        train_val,
        test_size=args.val_size,
        stratify=train_val["label"],
        random_state=args.seed,
    )

    train = train.assign(split="train")
    val = val.assign(split="val")
    test = test.assign(split="test")
    split_df = pd.concat(
        [
            train[["image_path", "image_name", "label", "split"]],
            val[["image_path", "image_name", "label", "split"]],
            test[["image_path", "image_name", "label", "split"]],
        ],
        ignore_index=True,
    )
    split_df.to_csv(SPLIT_CSV, index=False)
    print(f"Saved splits: {SPLIT_CSV}")
    print(split_df.groupby(['split', 'label']).size().unstack(fill_value=0))


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .config import IMAGE_ROOT, PROJECT_ROOT, SPLIT_CSV, STYLE_LABELS


def scan_dataset(image_root: Path = IMAGE_ROOT) -> pd.DataFrame:
    records: list[dict[str, str]] = []
    for label in STYLE_LABELS:
        class_dir = image_root / label
        if not class_dir.exists():
            continue
        for path in sorted(class_dir.glob("*")):
            if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
                continue
            records.append(
                {
                    "label": label,
                    "image_path": path.relative_to(PROJECT_ROOT).as_posix(),
                    "image_name": path.name,
                }
            )
    return pd.DataFrame.from_records(records)


def load_splits(split_csv: Path = SPLIT_CSV) -> pd.DataFrame:
    if not split_csv.exists():
        raise FileNotFoundError(f"Split file not found: {split_csv}")
    return pd.read_csv(split_csv)


def save_jsonl(records: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = Path(getattr(sys, "_MEIPASS", PROJECT_ROOT))
DATA_ROOT = PROJECT_ROOT / "data" / "style_dataset"
IMAGE_ROOT = DATA_ROOT / "images"
SPLIT_CSV = DATA_ROOT / "splits.csv"
MANIFEST_JSONL = DATA_ROOT / "source_manifest.jsonl"
ARTIFACTS_ROOT = PROJECT_ROOT / "artifacts"
REPORTS_ROOT = PROJECT_ROOT / "reports"
MODEL_ROOT = PROJECT_ROOT / "models" / "clip-vit-base-patch32"
RUNTIME_DATA_ROOT = RUNTIME_ROOT / "data" / "style_dataset"
RUNTIME_ARTIFACTS_ROOT = RUNTIME_ROOT / "artifacts"
RUNTIME_MODEL_ROOT = RUNTIME_ROOT / "models" / "clip-vit-base-patch32"

EMBEDDING_MODEL_ID = "openai/clip-vit-base-patch32"
DEFAULT_RANDOM_STATE = 42

STYLE_LABELS = ["neoclassical", "industrial", "organic", "minimal"]
STYLE_DESCRIPTIONS = {
    "neoclassical": "Ornate, historical, classical, painterly, and academically composed imagery.",
    "industrial": "Hard-edged machinery, steel, factory atmospheres, bridges, and engineered structures.",
    "organic": "Plant life, natural textures, flowing forms, botanical references, and soft irregular growth.",
    "minimal": "Sparse geometry, reduced forms, controlled palettes, and strong use of negative space.",
}

WIKIMEDIA_QUERIES = {
    "neoclassical": [
        "\"Jacques-Louis David\" painting",
        "\"Jean-Auguste-Dominique Ingres\" portrait",
        "\"Angelica Kauffman\" painting",
        "\"Antonio Canova\" sculpture",
        "\"neoclassical art\" painting",
    ],
    "industrial": [
        "factory machinery",
        "industrial interior",
        "steel structure",
        "power plant interior",
        "shipyard crane",
    ],
    "organic": [
        "botanical illustration",
        "leaf macro",
        "flower macro",
        "vine ornament",
        "floral pattern",
    ],
    "minimal": [
        "\"Kazimir Malevich\" black square",
        "\"Kazimir Malevich\" suprematism",
        "\"Ilya Chashnik\" suprematism",
        "\"El Lissitzky\" proun",
        "\"Donald Judd\" sculpture",
    ],
}


def resolve_project_path(path_like: str | Path) -> Path:
    path = Path(path_like)
    return path if path.is_absolute() else RUNTIME_ROOT / path

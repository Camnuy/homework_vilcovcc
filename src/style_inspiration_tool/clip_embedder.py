from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

from .config import EMBEDDING_MODEL_ID, MODEL_ROOT, RUNTIME_MODEL_ROOT, resolve_project_path


class ClipEmbedder:
    def __init__(self, model_id: str = EMBEDDING_MODEL_ID):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        model_source = str(RUNTIME_MODEL_ROOT if RUNTIME_MODEL_ROOT.exists() else MODEL_ROOT) if (RUNTIME_MODEL_ROOT.exists() or MODEL_ROOT.exists()) else model_id
        self.model = CLIPModel.from_pretrained(model_source).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_source)
        self.model.eval()

    def _encode_batch(self, images: list[Image.Image]) -> np.ndarray:
        inputs = self.processor(images=images, return_tensors="pt", padding=True).to(self.device)
        with torch.no_grad():
            features = self.model.get_image_features(**inputs)
            if hasattr(features, "image_embeds"):
                features = features.image_embeds
            elif hasattr(features, "pooler_output"):
                features = features.pooler_output
            features = torch.nn.functional.normalize(features, dim=-1)
        return features.cpu().numpy()

    def encode_paths(self, image_paths: list[str], batch_size: int = 8) -> np.ndarray:
        arrays: list[np.ndarray] = []
        for start in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[start : start + batch_size]
            images = [Image.open(resolve_project_path(path)).convert("RGB") for path in batch_paths]
            arrays.append(self._encode_batch(images))
        return np.concatenate(arrays, axis=0) if arrays else np.zeros((0, 512), dtype=np.float32)

    def encode_image(self, image: Image.Image) -> np.ndarray:
        return self._encode_batch([image.convert("RGB")])[0]

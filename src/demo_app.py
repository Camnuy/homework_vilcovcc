from __future__ import annotations

from pathlib import Path
import traceback

import gradio as gr
import numpy as np
import pandas as pd
from PIL import Image, ImageOps

from style_inspiration_tool.clip_embedder import ClipEmbedder
from style_inspiration_tool.config import STYLE_DESCRIPTIONS, resolve_project_path
from style_inspiration_tool.training import load_bundle, rank_similar_images


bundle = load_bundle()
dataset_df = pd.DataFrame(bundle["dataset"])
reference_embeddings = np.asarray(bundle["embeddings"])
classifier = bundle["classifier"]
embedder = ClipEmbedder()


def _prepare_image(image: Image.Image, max_size: int = 1536) -> Image.Image:
    prepared = ImageOps.exif_transpose(image).convert("RGB")
    prepared.thumbnail((max_size, max_size))
    return prepared


def predict_style(image: Image.Image):
    if image is None:
        return "Please upload an image.", None, None

    try:
        prepared_image = _prepare_image(image)
        embedding = embedder.encode_image(prepared_image)
        probability_vector = classifier.predict_proba(embedding[None, :])[0]
        label_scores = {label: float(score) for label, score in zip(classifier.classes_, probability_vector)}
        best_label = max(label_scores, key=label_scores.get)
        ranked_indices = rank_similar_images(embedding, reference_embeddings, top_k=6)
        gallery = []
        for index in ranked_indices:
            row = dataset_df.iloc[index]
            gallery.append((str(resolve_project_path(row["image_path"])), f'{row["label"]} | {Path(row["image_path"]).name}'))

        summary = (
            f"Predicted style: {best_label}\n\n"
            f"Creative note: {STYLE_DESCRIPTIONS.get(best_label, '')}"
        )
        score_table = pd.DataFrame(
            [{"style": label, "confidence": round(score, 4)} for label, score in sorted(label_scores.items(), key=lambda item: item[1], reverse=True)]
        )
        return summary, score_table, gallery
    except Exception as exc:
        traceback.print_exc()
        return f"Processing failed: {exc}", pd.DataFrame([{"error": str(exc)}]), []


with gr.Blocks(title="Visual Style Classification and Judgement Tool") as demo:
    gr.Markdown("# Visual Style Classification and Creative Judgement Analysis Tool")
    gr.Markdown(
        "Upload an image to predict its closest curated style label, inspect confidence scores, and review supportive reference matches."
    )
    with gr.Row():
        input_image = gr.Image(type="pil", label="Upload Image")
        with gr.Column():
            summary_box = gr.Textbox(label="Prediction Summary", lines=5)
            score_table = gr.Dataframe(label="Style Confidence Scores", interactive=False)
    gallery = gr.Gallery(label="Similar Reference Images", columns=3, height="auto")
    run_button = gr.Button("Analyze Image")
    run_button.click(predict_style, inputs=input_image, outputs=[summary_box, score_table, gallery])


if __name__ == "__main__":
    demo.launch(inbrowser=True, show_error=True)

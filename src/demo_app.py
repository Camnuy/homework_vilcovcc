from __future__ import annotations

import json
from pathlib import Path
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import numpy as np
import pandas as pd
from PIL import Image, ImageOps, ImageTk

from style_inspiration_tool.clip_embedder import ClipEmbedder
from style_inspiration_tool.config import REPORTS_ROOT, STYLE_DESCRIPTIONS, STYLE_LABELS, resolve_project_path
from style_inspiration_tool.training import load_bundle, rank_similar_images


BUNDLE = load_bundle()
DATASET_DF = pd.DataFrame(BUNDLE["dataset"])
REFERENCE_EMBEDDINGS = np.asarray(BUNDLE["embeddings"])
CLASSIFIER = BUNDLE["classifier"]
EMBEDDER = ClipEmbedder()

WINDOW_BG = "#f4f1ea"
PANEL_BG = "#fbf9f3"
BORDER = "#d8d2c4"
TEXT = "#2d2a26"
MUTED = "#6b655d"
ACCENT = "#335c67"


def _prepare_image(image: Image.Image, max_size: int = 1536) -> Image.Image:
    prepared = ImageOps.exif_transpose(image).convert("RGB")
    prepared.thumbnail((max_size, max_size))
    return prepared


def predict_style(image: Image.Image):
    prepared_image = _prepare_image(image)
    embedding = EMBEDDER.encode_image(prepared_image)
    probability_vector = CLASSIFIER.predict_proba(embedding[None, :])[0]
    label_scores = {label: float(score) for label, score in zip(CLASSIFIER.classes_, probability_vector)}
    best_label = max(label_scores, key=label_scores.get)
    best_score = label_scores[best_label]
    ranked_indices = rank_similar_images(embedding, REFERENCE_EMBEDDINGS, top_k=6)

    gallery = []
    for index in ranked_indices:
        row = DATASET_DF.iloc[index]
        caption = f'{row["label"]} | {Path(row["image_path"]).name}'
        gallery.append((resolve_project_path(row["image_path"]), caption))

    sorted_scores = sorted(label_scores.items(), key=lambda item: item[1], reverse=True)
    return best_label, best_score, sorted_scores, gallery


def load_evaluation_snapshot() -> tuple[float | None, list[tuple[str, float, float]], Path | None]:
    metrics_path = REPORTS_ROOT / "metrics.json"
    matrix_path = REPORTS_ROOT / "confusion_matrix.png"
    if not metrics_path.exists():
        return None, [], None

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    accuracy = float(metrics.get("accuracy", 0.0))
    report = metrics.get("classification_report", {})
    rows: list[tuple[str, float, float]] = []
    for label in STYLE_LABELS:
        class_metrics = report.get(label, {})
        rows.append(
            (
                label,
                float(class_metrics.get("precision", 0.0)),
                float(class_metrics.get("recall", 0.0)),
            )
        )
    return accuracy, rows, matrix_path if matrix_path.exists() else None


class ScrollableTab(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master, style="App.TFrame")
        self.canvas = tk.Canvas(self, bg=WINDOW_BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.body = ttk.Frame(self.canvas, style="App.TFrame")
        self.body.bind(
            "<Configure>",
            lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure(self.canvas_window, width=event.width),
        )
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _bind_mousewheel(self, _event: tk.Event) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, _event: tk.Event) -> None:
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event: tk.Event) -> None:
        if event.delta:
            self.canvas.yview_scroll(int(-event.delta / 120), "units")


class ReferenceGrid(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)
        self.canvas = tk.Canvas(self, bg=PANEL_BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self)
        self.inner.bind(
            "<Configure>",
            lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure(self.canvas_window, width=event.width),
        )
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self._photos: list[ImageTk.PhotoImage] = []

    def set_items(self, items: list[tuple[Path, str]]) -> None:
        for child in self.inner.winfo_children():
            child.destroy()
        self._photos.clear()

        for index, (path, caption) in enumerate(items):
            frame = ttk.Frame(self.inner, style="Card.TFrame", padding=8)
            row = index // 3
            col = index % 3
            frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            self.inner.grid_columnconfigure(col, weight=1)

            with Image.open(path) as image:
                preview = image.convert("RGB")
                preview.thumbnail((280, 210))
                photo = ImageTk.PhotoImage(preview)
                self._photos.append(photo)

            image_label = ttk.Label(frame, image=photo)
            image_label.pack(fill="both", expand=True)
            caption_label = ttk.Label(frame, text=caption, wraplength=280, justify="left", style="Muted.TLabel")
            caption_label.pack(anchor="w", pady=(8, 0))


class StyleClassifierDesktopApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Visual Style Classification and Creative Judgement Analysis Tool")
        self.root.geometry("1500x980")
        self.root.minsize(1280, 840)
        self.root.configure(bg=WINDOW_BG)

        self.current_image_path: Path | None = None
        self.current_pil_image: Image.Image | None = None
        self.input_photo: ImageTk.PhotoImage | None = None
        self.matrix_photo: ImageTk.PhotoImage | None = None

        self._build_styles()
        self._build_layout()
        self._populate_evaluation_tab()
        self._populate_category_tab()

    def _build_styles(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background=WINDOW_BG)
        style.configure("Card.TFrame", background=PANEL_BG, relief="solid", borderwidth=1)
        style.configure("Panel.TLabelframe", background=PANEL_BG, borderwidth=1)
        style.configure("Panel.TLabelframe.Label", background=PANEL_BG, foreground=TEXT, font=("Segoe UI", 11, "bold"))
        style.configure("Title.TLabel", background=WINDOW_BG, foreground=TEXT, font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", background=WINDOW_BG, foreground=MUTED, font=("Segoe UI", 11))
        style.configure("Body.TLabel", background=PANEL_BG, foreground=TEXT, font=("Segoe UI", 11))
        style.configure("Muted.TLabel", background=PANEL_BG, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("Metric.TLabel", background=PANEL_BG, foreground=ACCENT, font=("Segoe UI", 28, "bold"))
        style.configure("MetricSmall.TLabel", background=PANEL_BG, foreground=TEXT, font=("Segoe UI", 14, "bold"))
        style.configure("TNotebook", background=WINDOW_BG, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=(14, 8))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=28, font=("Consolas", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_layout(self) -> None:
        wrapper = ttk.Frame(self.root, style="App.TFrame", padding=18)
        wrapper.pack(fill="both", expand=True)

        ttk.Label(wrapper, text="Visual Style Classification and Creative Judgement Analysis Tool", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            wrapper,
            text="A local classification lab for testing subjective style labels, comparing confidence profiles, and examining supportive reference clusters.",
            style="Subtitle.TLabel",
            wraplength=1200,
        ).pack(anchor="w", pady=(6, 14))

        notebook = ttk.Notebook(wrapper)
        notebook.pack(fill="both", expand=True)

        self.lab_tab = ScrollableTab(notebook)
        self.eval_tab = ScrollableTab(notebook)
        self.guide_tab = ScrollableTab(notebook)

        notebook.add(self.lab_tab, text="Classification Lab")
        notebook.add(self.eval_tab, text="Evaluation Snapshot")
        notebook.add(self.guide_tab, text="Category Guide")

        self._build_lab_tab()

    def _build_lab_tab(self) -> None:
        top = ttk.Frame(self.lab_tab.body, style="App.TFrame", padding=10)
        top.pack(fill="x", expand=False)

        left = ttk.LabelFrame(top, text="Input Image", style="Panel.TLabelframe", padding=12)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.image_preview_label = ttk.Label(left, text="Choose an image to start classification.", style="Muted.TLabel", anchor="center")
        self.image_preview_label.pack(fill="both", expand=True, ipady=120)

        controls = ttk.Frame(left, style="Card.TFrame", padding=6)
        controls.pack(fill="x", pady=(10, 0))
        ttk.Button(controls, text="Choose Image", command=self.choose_image).pack(side="left")
        ttk.Button(controls, text="Analyze Style", command=self.analyze_current_image, style="Primary.TButton").pack(side="left", padx=8)
        ttk.Button(controls, text="Clear", command=self.clear_current_image).pack(side="left")

        right = ttk.Frame(top, style="App.TFrame")
        right.pack(side="left", fill="both", expand=True)

        prediction_frame = ttk.LabelFrame(right, text="Predicted Style", style="Panel.TLabelframe", padding=12)
        prediction_frame.pack(fill="x", expand=False, pady=(0, 10))

        self.predicted_style_var = tk.StringVar(value="Awaiting image")
        self.predicted_score_var = tk.StringVar(value="Confidence: --")
        self.predicted_note_var = tk.StringVar(value="Upload an image to generate a prediction and reference cluster.")

        ttk.Label(prediction_frame, textvariable=self.predicted_style_var, style="Metric.TLabel").pack(anchor="w")
        ttk.Label(prediction_frame, textvariable=self.predicted_score_var, style="MetricSmall.TLabel").pack(anchor="w", pady=(2, 8))
        ttk.Label(prediction_frame, textvariable=self.predicted_note_var, style="Body.TLabel", wraplength=520, justify="left").pack(anchor="w")

        scores_frame = ttk.LabelFrame(right, text="Probability Profile", style="Panel.TLabelframe", padding=12)
        scores_frame.pack(fill="both", expand=True)

        self.score_tree = ttk.Treeview(scores_frame, columns=("style", "confidence"), show="headings", height=6)
        self.score_tree.heading("style", text="Style")
        self.score_tree.heading("confidence", text="Confidence")
        self.score_tree.column("style", width=180, anchor="w")
        self.score_tree.column("confidence", width=120, anchor="center")
        self.score_tree.pack(fill="both", expand=True)
        self._reset_score_tree()

        refs_frame = ttk.LabelFrame(self.lab_tab.body, text="Reference Cluster", style="Panel.TLabelframe", padding=12)
        refs_frame.pack(fill="both", expand=True, pady=(12, 0))
        self.reference_grid = ReferenceGrid(refs_frame)
        self.reference_grid.pack(fill="both", expand=True)

    def _populate_evaluation_tab(self) -> None:
        accuracy, rows, matrix_path = load_evaluation_snapshot()

        card = ttk.Frame(self.eval_tab.body, style="Card.TFrame", padding=16)
        card.pack(fill="x", expand=False)

        if accuracy is None:
            ttk.Label(card, text="Evaluation outputs not found.", style="MetricSmall.TLabel").pack(anchor="w")
            ttk.Label(card, text="Run training and evaluation first to populate this tab.", style="Body.TLabel").pack(anchor="w", pady=(8, 0))
            return

        ttk.Label(card, text="Evaluation Snapshot", style="MetricSmall.TLabel").pack(anchor="w")
        ttk.Label(card, text=f"Accuracy {accuracy:.1%}", style="Metric.TLabel").pack(anchor="w", pady=(4, 8))
        ttk.Label(
            card,
            text="This small model is meant to support critical discussion. The class metrics help show where visual judgement is relatively stable and where it becomes ambiguous.",
            style="Body.TLabel",
            wraplength=1100,
            justify="left",
        ).pack(anchor="w")

        metrics_frame = ttk.LabelFrame(self.eval_tab.body, text="Per-Class Precision / Recall", style="Panel.TLabelframe", padding=12)
        metrics_frame.pack(fill="x", expand=False, pady=(12, 12))

        tree = ttk.Treeview(metrics_frame, columns=("label", "precision", "recall"), show="headings", height=4)
        tree.heading("label", text="Style")
        tree.heading("precision", text="Precision")
        tree.heading("recall", text="Recall")
        tree.column("label", width=220, anchor="w")
        tree.column("precision", width=120, anchor="center")
        tree.column("recall", width=120, anchor="center")
        tree.pack(fill="x", expand=True)
        for label, precision, recall in rows:
            tree.insert("", "end", values=(label, f"{precision:.2f}", f"{recall:.2f}"))

        matrix_frame = ttk.LabelFrame(self.eval_tab.body, text="Confusion Matrix", style="Panel.TLabelframe", padding=12)
        matrix_frame.pack(fill="both", expand=True)

        if matrix_path and matrix_path.exists():
            with Image.open(matrix_path) as matrix_image:
                preview = matrix_image.convert("RGB")
                preview.thumbnail((780, 560))
                self.matrix_photo = ImageTk.PhotoImage(preview)
            ttk.Label(matrix_frame, image=self.matrix_photo).pack(anchor="center")

    def _populate_category_tab(self) -> None:
        card = ttk.Frame(self.guide_tab.body, style="Card.TFrame", padding=16)
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="Category Guide", style="MetricSmall.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="These labels are intentionally subjective. The system is useful as a classification experiment, but not as a claim that visual judgement is objective or fixed.",
            style="Body.TLabel",
            wraplength=1100,
            justify="left",
        ).pack(anchor="w", pady=(6, 14))

        for label in STYLE_LABELS:
            section = ttk.Frame(card, style="Card.TFrame", padding=10)
            section.pack(fill="x", expand=False, pady=6)
            ttk.Label(section, text=label, style="MetricSmall.TLabel").pack(anchor="w")
            ttk.Label(section, text=STYLE_DESCRIPTIONS.get(label, ""), style="Body.TLabel", wraplength=1100, justify="left").pack(anchor="w", pady=(4, 0))

    def choose_image(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.webp *.bmp"),
                ("All files", "*.*"),
            ],
        )
        if not file_path:
            return

        try:
            with Image.open(file_path) as image:
                prepared = _prepare_image(image.copy(), max_size=900)
                preview = prepared.copy()
                preview.thumbnail((520, 380))
                self.input_photo = ImageTk.PhotoImage(preview)
                self.image_preview_label.configure(image=self.input_photo, text="")
                self.current_pil_image = prepared
                self.current_image_path = Path(file_path)
        except Exception as exc:
            messagebox.showerror("Failed to open image", str(exc))

    def clear_current_image(self) -> None:
        self.current_image_path = None
        self.current_pil_image = None
        self.input_photo = None
        self.image_preview_label.configure(image="", text="Choose an image to start classification.")
        self.predicted_style_var.set("Awaiting image")
        self.predicted_score_var.set("Confidence: --")
        self.predicted_note_var.set("Upload an image to generate a prediction and reference cluster.")
        self._reset_score_tree()
        self.reference_grid.set_items([])

    def analyze_current_image(self) -> None:
        if self.current_pil_image is None:
            messagebox.showinfo("No image selected", "Please choose an image before running classification.")
            return

        try:
            best_label, best_score, sorted_scores, gallery = predict_style(self.current_pil_image)
            self.predicted_style_var.set(best_label)
            self.predicted_score_var.set(f"Confidence: {best_score:.1%}")
            self.predicted_note_var.set(STYLE_DESCRIPTIONS.get(best_label, ""))
            self._fill_score_tree(sorted_scores)
            self.reference_grid.set_items(gallery)
        except Exception as exc:
            traceback.print_exc()
            messagebox.showerror("Classification failed", str(exc))

    def _reset_score_tree(self) -> None:
        for item in self.score_tree.get_children():
            self.score_tree.delete(item)
        for label in STYLE_LABELS:
            self.score_tree.insert("", "end", values=(label, "--"))

    def _fill_score_tree(self, sorted_scores: list[tuple[str, float]]) -> None:
        for item in self.score_tree.get_children():
            self.score_tree.delete(item)
        for label, score in sorted_scores:
            self.score_tree.insert("", "end", values=(label, f"{score:.4f}"))


def main() -> None:
    root = tk.Tk()
    app = StyleClassifierDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

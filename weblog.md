# Research and Implementation Weblog

> Draft note: this file is a starter weblog structure. Before submission, rewrite it in your own voice so it reflects the real process and your own thinking.

## 2026-06-01 - Initial topic selection

- Decided to build a visual style classification and inspiration analysis tool.
- Chose this topic because it clearly combines machine learning, creative practice, and critical reflection.
- The main attraction is that it can become a practical tool for artists and designers rather than just a classifier demo.

## 2026-06-02 - Clarifying the project question

- Narrowed the project to a smaller question: can a lightweight model help sort visual references into subjective style groups?
- Noted that style labels are subjective and culturally loaded.
- Planned to treat that subjectivity as a theme of the project instead of pretending the labels are objective.

## 2026-06-03 - Defining categories

- Started with four style categories: neoclassical, industrial, organic, and minimal.
- Chose these because they are visually distinct enough for a small prototype but still subjective enough to support reflection.
- Considered using more categories, but that felt too risky for the available time.

## 2026-06-04 - Dataset strategy

- Decided to build a small curated starter dataset rather than rely on a giant dataset.
- Focused on public-domain or open-license sources to keep the project ethically cleaner.
- Planned to document image provenance in a source manifest.

## 2026-06-05 - Model choice

- Chose CLIP embeddings plus a lightweight classifier rather than training a full image model from scratch.
- This felt appropriate for a course project because it allows method selection, evaluation, and critical discussion without needing heavy hardware.
- Also planned a nearest-neighbour retrieval feature to make the tool more useful to creators.

## 2026-06-06 - Building the training pipeline

- Set up scripts for dataset preparation, training, and evaluation.
- Decided to separate data preparation from model training so the path from code to output would stay clear.
- Planned to save confusion matrices and reports as evidence for the README and video.

## 2026-06-07 - Demo design

- Designed the demo around two outputs: a predicted style label and similar reference images.
- This keeps the system grounded in creative use rather than only academic metrics.
- The interface is meant to feel like a moodboard helper.

## 2026-06-08 - Expected limitations

- Reflected on how the classifier may confuse style with content.
- For example, plants may be predicted as organic because of subject matter rather than a deeper visual understanding.
- This is a central limitation to discuss in the final reflection.

## 2026-06-09 - Evaluation and failure cases

- Planned to examine confusion matrix results and collect misclassified images.
- Failure cases will be important because they reveal what visual shortcuts the model is using.
- This supports the course emphasis on process and critical analysis.

## 2026-06-10 - Final framing

- Framed the project as a creative support tool plus a critique of computational style labelling.
- The final project should show that machine learning can help organize inspiration, but it also reduces complex visual judgement into simplified categories.
- This tension is probably the most interesting part of the whole project.

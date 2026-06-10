# Visual Style Classification and Creative Judgement Analysis Tool

This GitHub version is a **code-and-documentation release**. The local working dataset, saved artifacts, runtime models, and packaged app bundles are intentionally not uploaded here.

This project is an EMI 2026 final-project prototype built as a **classification and critical-analysis system** for visual style labels.

This folder is intentionally different from `homework_nan`:

1. `homework_nan` focuses on retrieval, ranking, and reference-board building
2. `homework女` focuses on classification, confidence scores, confusion matrices, and error analysis

The core idea here is:

1. collect a small image dataset of self-defined visual style categories
2. extract image embeddings with CLIP
3. train a lightweight classifier on top of those embeddings
4. study how the model predicts subjective labels and where that judgement breaks down

The project is framed as a **creative classification experiment** rather than a reference-search tool. It asks how machine learning can help sort visual material, while also showing how subjective style labels can be simplified or misread by a model.

## Project Question

How can a small machine-learning system classify subjective visual style categories without pretending that aesthetic judgement is objective or fixed?

## Style Categories

The current version uses four curated categories:

1. `neoclassical`
2. `industrial`
3. `organic`
4. `minimal`

These categories are intentionally subjective. The project is designed to discuss that subjectivity rather than hide it.

## Current Starter Dataset

The local working version was built around a small starter dataset with 50 images:

1. `20` neoclassical references reused from open-access museum images
2. public-domain / open-license downloads for the other categories
3. project-generated moodboard supplements for sparse categories so the classifier can be trained and demonstrated

This hybrid dataset makes sense for the brief because the project is framed as a creative style-labelling experiment rather than a benchmark dataset paper.

## What Is In The Repo

```text
docs/                            assignment support notes
publication/                     client-facing overview and release notes
src/download_public_domain_style_dataset.py
src/prepare_style_dataset.py
src/train_style_classifier.py
src/evaluate_style_classifier.py
src/demo_app.py
src/style_inspiration_tool/      shared classification code
scripts/                         packaging and setup helpers
reports/                         evaluation summary files
weblog.md                        draft research and implementation weblog
```

Relevant extension note:

- `docs/reward_model_extension_zh.md` explains how the project could be extended with a reward-model-based ranking layer.

## Current Result Snapshot

After the first full training pass on the starter dataset:

1. held-out test accuracy: `0.80`
2. the strongest class is currently `neoclassical`
3. the weakest boundary is currently between `industrial` and `minimal`

That result is useful for the assignment because it gives the project both a working prototype and a clear limitation to discuss.

## How To Run

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

If you want to refresh the public-domain starter dataset:

```powershell
python src/download_public_domain_style_dataset.py
```

Prepare train/val/test splits:

```powershell
python src/prepare_style_dataset.py
```

Train the classifier:

```powershell
python src/train_style_classifier.py
```

Evaluate the classifier and generate figures:

```powershell
python src/evaluate_style_classifier.py
```

Run the classification demo:

```powershell
python src/demo_app.py
```

For this GitHub release, prepare the dataset locally and run training/evaluation steps before launching the demo.

## Machine Learning Focus

This project explicitly addresses the course requirements around:

1. data selection and preparation
2. method choice and system configuration
3. model training on top of pretrained embeddings
4. evaluation with accuracy, confusion matrix, and error cases
5. critical reflection on creative, cultural, and aesthetic implications

## Creative Practice Relevance

This project is intended as a tool for:

1. testing subjective style categories
2. comparing how the model separates visual groups
3. examining confidence scores and misclassifications
4. reflecting on how machine learning labels visual taste

## AI / Third-Party Disclosure

This repository contains code and structure created with AI assistance and uses third-party libraries and public-domain / open-license images. Before submission, the final student-facing README and weblog should be rewritten in the student's own words so they accurately describe their own process, decisions, and use of AI tools.

## Video And Weblog

The course requires:

1. a public repo
2. a public 3-5 minute demo video
3. a README
4. a weblog with dated entries

Draft project materials are included here:

1. `weblog.md`
2. `docs/video_plan.md`
3. `docs/submission_checklist.md`
4. `docs/assignment_alignment_zh.md`

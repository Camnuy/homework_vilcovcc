# Visual Style Classification and Creative Judgement Analysis Tool

Weblog link: [weblog.md](weblog.md)

Link to video: to be added after recording

## Introduction

This project explores a simple but difficult question: how can machine learning classify visual style categories without pretending that aesthetic judgement is fully objective? Instead of building a generic image classifier, I wanted to make a small creative-practice-oriented system that reveals both the usefulness and the limits of computational style labelling.

The final project is a local desktop application that accepts an input image, predicts the closest style label from a curated set of four categories, shows confidence scores across all categories, and displays visually related reference images from the local library. The aim is not to claim a final truth about style, but to create a working experiment that can be tested, evaluated, and discussed critically.

The current four labels are:

1. `neoclassical`
2. `industrial`
3. `organic`
4. `minimal`

These categories were chosen because they are visually distinct enough to support a small prototype, but still subjective enough to raise interesting questions about what the model is actually learning.

## Related Technical and/or Creative Work

The most important technical reference for this project is CLIP, a vision-language model that maps images and text into a shared embedding space (Radford et al., 2021). I used CLIP as a pretrained visual representation model so that I could focus on dataset design, classifier behaviour, evaluation, and interpretation rather than training a large image model from scratch.

On top of CLIP embeddings, I trained a lightweight Logistic Regression classifier using scikit-learn. This was a deliberate design choice. For a course project, a lightweight classifier makes the path from data to result easier to understand and explain, and it keeps the project realistic within limited compute resources.

Creatively, the project is also influenced by moodboard building, design-reference curation, and visual research workflows. In those contexts, categories such as "minimal" or "organic" are often useful in practice even though they remain culturally loaded and open to interpretation. That tension is central to the project.

## Summary of Design and Development Process

The development process moved through six main stages. First, I clarified the project question so it would not become a vague "AI art style" experiment. Second, I defined four style categories and built a small curated starter dataset from public-domain and open-license sources. Third, I wrote scripts for downloading images, preparing the dataset split, training the classifier, and evaluating it. Fourth, I used CLIP embeddings plus Logistic Regression to create a lightweight classification pipeline. Fifth, I added an interactive interface that shows both prediction scores and supportive reference matches. Finally, I revised the interface into a local desktop application so the final submission would be more stable and more distinct from a browser-based retrieval demo.

This process mattered because the project is not only about producing a number such as accuracy. It is also about making the machine-learning workflow inspectable: how the labels are defined, how the data is curated, what kinds of errors appear, and how interface design changes the way the model is interpreted by a user.

## Summary of Final Version

The final version is a local desktop application built with `tkinter`. It has three main areas:

1. `Classification Lab`
2. `Evaluation Snapshot`
3. `Category Guide`

In the main tab, the user chooses a local image and runs style analysis. The system then returns:

1. the predicted style label
2. a confidence score for the top result
3. a probability profile across all four categories
4. a small cluster of visually similar reference images

The second tab exposes the evaluation summary, including overall accuracy and the confusion matrix. The third tab explains the meaning of each label so that the app does not present them as natural or neutral categories.

At the current stage, the working local dataset used for evaluation contains `35` curated images:

1. `10` `neoclassical`
2. `10` `organic`
3. `9` `industrial`
4. `6` `minimal`

The final submitted version uses the currently available sourced images rather than synthetic filler images.

## Evaluation

I evaluated the current version with a held-out test split and a confusion matrix. On the local starter dataset used for the final run, the classifier achieved:

1. Accuracy: `0.857`

This result is promising for a very small prototype, but it should be interpreted carefully. The dataset is small, the labels are subjective, and the system is not solving an objective ground-truth task in the same way that a standard industrial image benchmark would.

The confusion matrix shows that the classifier is generally able to separate the four broad categories, but it also reveals an important ambiguity: one `industrial` test image was misclassified as `organic`. I think this is a useful result rather than an embarrassing one to hide. It suggests that the model may sometimes rely on local texture, material appearance, or colour patterns rather than a deeper understanding of how the category was intended conceptually.

The confidence values are also informative. In several cases they are not extremely high, which is consistent with the small size of the dataset and with the fact that these labels are interpretive rather than fixed.

## Reflection and Conclusion

I think the project works best when understood as a classification experiment and a critical design probe at the same time. It does demonstrate a functioning machine-learning pipeline: data collection, representation extraction, classifier training, evaluation, and interface design. But its more interesting contribution is that it exposes the instability of aesthetic labelling instead of hiding it.

The strongest part of the final version is its coherence. The dataset, model choice, evaluation method, and interface all support the same core question about computational style judgement. The weakest part is the size and scope of the dataset. With only thirty-five images, the system is inevitably shaped by curation decisions and cannot claim broad coverage.

If I continued the project, I would expand the dataset, improve the provenance records, collect more examples near category boundaries, and experiment with a small preference or reward layer for ranking reference matches more intelligently. Even in its current form, though, I think the project succeeds as a final assignment because it combines a working machine-learning artifact with a clear space for critical reflection.

## Repository Structure and Instructions for Running

### Repository structure

- `README.md`: final project overview and submission-facing documentation
- `weblog.md`: dated development log with iterative progress notes
- `weblog_assets/`: images embedded in the weblog entries
- `requirements.txt`: Python dependencies
- `run_demo.ps1`: simple launcher for the local desktop demo
- `src/demo_app.py`: main desktop application
- `src/download_public_domain_style_dataset.py`: downloads starter public-domain / open-license images
- `src/prepare_style_dataset.py`: builds the train/validation/test split metadata
- `src/train_style_classifier.py`: trains the style classifier on CLIP embeddings
- `src/evaluate_style_classifier.py`: evaluates the classifier and saves summary outputs
- `src/style_inspiration_tool/clip_embedder.py`: CLIP embedding wrapper
- `src/style_inspiration_tool/training.py`: bundle loading, classifier utilities, and reference ranking
- `src/style_inspiration_tool/config.py`: project paths, labels, and shared configuration
- `reports/`: saved evaluation outputs used in the write-up

Large local runtime assets such as cached model weights are prepared locally and may need to be regenerated after cloning the repository.

### Running the project

The project was developed and tested with Python 3.11 in Anaconda on Windows. A typical setup is:

```powershell
conda create -n emi_stylelab python=3.11
conda activate emi_stylelab
cd <your-local-repo-path>
python -m pip install -r requirements.txt
```

Download a starter dataset:

```powershell
python src/download_public_domain_style_dataset.py --per-query 20 --per-label 10 --max-per-query 2
```

Prepare the dataset split:

```powershell
python src/prepare_style_dataset.py
```

Train the classifier:

```powershell
python src/train_style_classifier.py
```

Evaluate the classifier:

```powershell
python src/evaluate_style_classifier.py
```

Launch the desktop app:

```powershell
python src/demo_app.py
```

The final app opens as a **local desktop window**, so no browser and no localhost port are required.

## Use of External Resources

### Statement on Use of AI Tools

AI tools were used during the development of this project for brainstorming, debugging, code revision support, packaging help, and drafting technical explanations. I used them as assistive tools rather than as the sole author of the project. The project direction, category definitions, testing decisions, and final repository contents were directed and reviewed by me.

### Use of Other Third-Party Resources

I used several third-party libraries and resources:

1. the pretrained CLIP model and Hugging Face `transformers` library for image embeddings
2. PyTorch as the model runtime
3. scikit-learn for the lightweight classifier
4. Pillow, NumPy, pandas, matplotlib, joblib, and requests for data processing and evaluation
5. Wikimedia Commons and other public-domain / open-license sources for the starter image set

I did not copy large external tutorial projects verbatim. The repository uses these libraries through their documented APIs and combines them into a project structure that is specific to this coursework brief.

## References

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M. and Duchesnay, E. (2011) *Scikit-learn: Machine learning in Python*. Journal of Machine Learning Research, 12, pp. 2825-2830.

Radford, A., Kim, J.W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G. and Sutskever, I. (2021) *Learning transferable visual models from natural language supervision*. Available at: https://arxiv.org/abs/2103.00020

Wikimedia Commons (2026) *Wikimedia Commons*. Available at: https://commons.wikimedia.org/

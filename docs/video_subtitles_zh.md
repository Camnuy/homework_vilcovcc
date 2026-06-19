# homework_vilcovcc 视频录制流程与字幕

## 启动方式

```powershell
conda activate homework2
cd d:\homework_yibai\_recovered\homework_vilcovcc
python src/demo_app.py
```

运行后会直接弹出本地桌面窗口，不需要浏览器。

## 建议录制顺序

1. 打开终端，展示激活环境和启动程序
2. 展示桌面程序首页和三个标签页
3. 选择第一张测试图片并点击 `Analyze Style`
4. 展示预测类别、概率表和参考图
5. 再换一张不同风格图片重复一次
6. 切换到 `Evaluation Snapshot` 展示 accuracy 和 confusion matrix
7. 切换到 `Category Guide` 展示四个类别说明
8. 回到主界面停留几秒结束

## 英文字幕稿

### Opening

```text
This project is a visual style classification and creative judgement analysis tool.
```

```text
It is designed as a local desktop application for testing subjective visual style labels.
```

### Launch

```text
I first activate the Python environment, enter the project folder, and launch the application locally.
```

```text
The program opens as a desktop interface rather than a browser-based demo.
```

### Interface

```text
The interface contains a classification lab, an evaluation snapshot, and a category guide.
```

### First example

```text
Here I choose a sample image and run style analysis.
```

```text
The system predicts the closest style label and shows a probability profile across all categories.
```

```text
The reference images below help explain why the prediction was made.
```

### Second example

```text
I then test another image from a different category to compare the classifier response.
```

### Evaluation

```text
The evaluation tab summarises model accuracy and shows a confusion matrix for the held-out test split.
```

### Category guide

```text
The category guide explains the meaning of each label and highlights that these labels remain subjective.
```

### Closing

```text
Overall, this project combines dataset preparation, CLIP embeddings, classifier training, evaluation, and a local desktop interface in one workflow.
```

```text
Its main value is not only classification accuracy, but also critical reflection on how machine learning simplifies visual judgement.
```

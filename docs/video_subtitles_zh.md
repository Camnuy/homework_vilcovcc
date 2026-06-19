# homework_vilcovcc 视频录制流程与字幕

这份文档按“**从项目文件夹开始录制**、**只用字幕不配音**”来写。  
建议总时长控制在 **3 到 5 分钟**，这一版按正常节奏录下来大约是 **3分20秒到4分30秒**。

## 一、推荐总流程

建议按下面顺序录：

1. 打开项目文件夹
2. 较详细展示仓库结构
3. 打开终端并启动程序
4. 展示桌面程序首页
5. 演示第一张图片分类
6. 演示第二张图片分类
7. 展示 `Evaluation Snapshot`
8. 展示 `Category Guide`
9. 回到主界面结束

---

## 二、具体录制步骤

### Step 1 - 从项目文件夹开始，进入 image 文件夹展示四个风格

画面操作：

1. 打开 `d:\homework_yibai\_recovered\homework_vilcovcc`
2. 先停留 3 到 4 秒，让老师看到这是本地项目文件夹
3. 然后慢一点往下看或移动一下鼠标，重点展示这些内容：
   - `README.md`
   - `weblog.md`
   - `requirements.txt`
   - `run_demo.ps1`
   - `src`
   - `data`
   - `reports`
   - `docs`
   - `publication`
   - `weblog_assets`
4. 接着进入 `data`
5. 再进入 `style_dataset`
6. 再进入 `images`
7. 停留展示四个风格文件夹：
   - `industrial`
   - `minimal`
   - `neoclassical`
   - `organic`
8. 可以在这里停 4 到 6 秒，让老师看清楚四个类别
9. 然后再回到项目根目录

建议时长：

- **35 到 45 秒**

这一段可以录得稍微完整一点，因为它能很直观地说明你有：

- 代码
- 数据
- 报告
- README
- weblog
- 视频辅助文档

对应字幕：

```text
This project is a visual style classification and creative judgement analysis tool.
```

```text
I begin from the local project folder, which contains the code, dataset, reports, README, weblog, and supporting documentation.
```

```text
This structure shows the full submission workflow, including implementation files, evaluation outputs, and reflective project materials.
```

```text
Inside the dataset image folder, the reference images are organised into four style categories: industrial, minimal, neoclassical, and organic.
```

```text
These four folders correspond to the curated visual labels used by the classifier.
```

---

### Step 2 - 在文件夹里打开终端并启动程序

画面操作：

1. 在项目目录中打开终端
2. 输入下面三行命令

```powershell
conda activate homework2
cd d:\homework_yibai\_recovered\homework_vilcovcc
python src/demo_app.py
```

3. 等程序弹出

建议时长：

- **15 到 20 秒**

对应字幕：

```text
I activate the Python environment, enter the project folder, and launch the application locally.
```

```text
The final version runs as a desktop application rather than a browser-based demo.
```

---

### Step 3 - 展示程序首页

画面操作：

1. 程序打开后先不要立刻操作
2. 停留几秒让老师看到标题和整体界面
3. 轻微切一下三个标签页：
   - `Classification Lab`
   - `Evaluation Snapshot`
   - `Category Guide`
4. 再回到 `Classification Lab`

建议时长：

- **12 到 18 秒**

对应字幕：

```text
The interface contains a classification lab, an evaluation snapshot, and a category guide.
```

```text
The tool is designed to test subjective visual style labels through a small local machine learning workflow.
```

---

### Step 4 - 演示第一张图片分类

画面操作：

1. 点击 `Choose Image`
2. 从本地选择第一张测试图
3. 点击 `Analyze Style`
4. 展示：
   - 预测类别
   - 置信度
   - 概率表
   - 下方参考图
5. 可以稍微往下滚一点，让老师看到参考图区域

建议第一张优先用：

- `neoclassical`

建议时长：

- **25 到 35 秒**

对应字幕：

```text
Here I choose a sample image and run style analysis.
```

```text
The system predicts the closest style label and shows a probability profile across all categories.
```

```text
The reference images below help explain why the prediction was made.
```

---

### Step 5 - 演示第二张不同风格图片

画面操作：

1. 再点一次 `Choose Image`
2. 换一张和上一张明显不同风格的图
3. 点击 `Analyze Style`
4. 展示第二次分类结果变化

建议第二张优先用：

- `industrial`
- 或 `organic`
- 或 `minimal`

建议时长：

- **25 到 35 秒**

对应字幕：

```text
I then test another image from a different category to compare the classifier response.
```

```text
This helps show that the model does not return the same judgement for every kind of visual input.
```

---

### Step 6 - 展示 Evaluation Snapshot

画面操作：

1. 点击 `Evaluation Snapshot`
2. 展示 `Accuracy`
3. 展示分类表格
4. 往下展示 `confusion matrix`
5. 停留几秒

建议时长：

- **20 到 30 秒**

对应字幕：

```text
The evaluation tab summarises model accuracy and shows a confusion matrix for the held-out test split.
```

```text
This part makes the project more than a demo, because it also presents measurable evaluation results.
```

---

### Step 7 - 展示 Category Guide

画面操作：

1. 点击 `Category Guide`
2. 慢一点往下滚动
3. 让老师看到四个类别的说明

建议时长：

- **18 到 25 秒**

对应字幕：

```text
The category guide explains the meaning of each label and shows that these categories are intentionally subjective.
```

```text
This project does not claim that visual judgement is fully objective or fixed.
```

---

### Step 8 - 回到主界面收尾

画面操作：

1. 回到 `Classification Lab`
2. 停在一个已经完成分类的结果页面
3. 保持 6 到 10 秒结束录制

建议时长：

- **10 到 15 秒**

对应字幕：

```text
Overall, this project combines dataset preparation, CLIP embeddings, classifier training, evaluation, and a local desktop interface in one workflow.
```

```text
Its main value is not only classification accuracy, but also critical reflection on how machine learning simplifies visual judgement.
```

---

## 三、推荐时间分配

如果你想稳定录进 `3-5 分钟`，可以按这个节奏：

1. 文件夹展示：`35-45秒`
2. 终端启动：`15-20秒`
3. 程序首页：`12-18秒`
4. 第一张图分类：`25-35秒`
5. 第二张图分类：`25-35秒`
6. Evaluation Snapshot：`20-30秒`
7. Category Guide：`18-25秒`
8. 结尾停留：`10-15秒`

总计大约：

- **3分30秒 到 4分45秒**

---

## 四、最稳的录制建议

为了录得更顺，建议你这样做：

1. 先提前把两张测试图放在桌面或固定文件夹里
2. 第一张用 `neoclassical`
3. 第二张用 `industrial` 或 `organic`
4. 每一步操作后停 2 秒，让字幕跟得上
5. 文件夹展示阶段可以多停留一点，这是最容易拉满时长又最自然的部分
6. 不要录 GitHub 页面，直接从本地文件夹开始
7. 结尾停在程序结果页，不要停在黑屏或终端

---

## 五、可以直接复制的完整字幕

按出现顺序整理如下：

```text
This project is a visual style classification and creative judgement analysis tool.
```

```text
I begin from the local project folder, which contains the code, dataset, reports, README, weblog, and supporting documentation.
```

```text
This structure shows the full submission workflow, including implementation files, evaluation outputs, and reflective project materials.
```

```text
Inside the dataset image folder, the reference images are organised into four style categories: industrial, minimal, neoclassical, and organic.
```

```text
These four folders correspond to the curated visual labels used by the classifier.
```

```text
I activate the Python environment, enter the project folder, and launch the application locally.
```

```text
The final version runs as a desktop application rather than a browser-based demo.
```

```text
The interface contains a classification lab, an evaluation snapshot, and a category guide.
```

```text
The tool is designed to test subjective visual style labels through a small local machine learning workflow.
```

```text
Here I choose a sample image and run style analysis.
```

```text
The system predicts the closest style label and shows a probability profile across all categories.
```

```text
The reference images below help explain why the prediction was made.
```

```text
I then test another image from a different category to compare the classifier response.
```

```text
This helps show that the model does not return the same judgement for every kind of visual input.
```

```text
The evaluation tab summarises model accuracy and shows a confusion matrix for the held-out test split.
```

```text
This part makes the project more than a demo, because it also presents measurable evaluation results.
```

```text
The category guide explains the meaning of each label and shows that these categories are intentionally subjective.
```

```text
This project does not claim that visual judgement is fully objective or fixed.
```

```text
Overall, this project combines dataset preparation, CLIP embeddings, classifier training, evaluation, and a local desktop interface in one workflow.
```

```text
Its main value is not only classification accuracy, but also critical reflection on how machine learning simplifies visual judgement.
```

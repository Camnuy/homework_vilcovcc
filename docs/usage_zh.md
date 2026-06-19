# 使用方式

## 运行环境

建议使用 Python 3.11。

先安装依赖：

```powershell
python -m pip install -r requirements.txt
```

## 正常运行步骤

1. 准备数据划分

```powershell
python src/prepare_style_dataset.py
```

2. 训练分类器

```powershell
python src/train_style_classifier.py
```

3. 评估模型

```powershell
python src/evaluate_style_classifier.py
```

4. 启动本地桌面程序

```powershell
python src/demo_app.py
```

运行后会直接弹出一个本地窗口，不需要打开浏览器，也不需要访问 `localhost`。

## 桌面程序使用方法

1. 点击 `Choose Image`
2. 选择一张本地图片
3. 点击 `Analyze Style`
4. 查看预测风格类别
5. 查看右侧 `Probability Profile`
6. 查看下方 `Reference Cluster`
7. 切换到 `Evaluation Snapshot` 查看 accuracy 和 confusion matrix
8. 切换到 `Category Guide` 查看四个标签的解释

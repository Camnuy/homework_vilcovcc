# 使用技术

这个项目当前使用的主要技术如下：

## 核心模型

1. `CLIP`
   - 用于提取图像语义特征 embedding

2. `Logistic Regression`
   - 用于在 CLIP embedding 之上完成轻量风格分类

## Python 库

1. `transformers`
2. `torch`
3. `scikit-learn`
4. `pandas`
5. `numpy`
6. `matplotlib`
7. `Pillow`
8. `joblib`
9. `tkinter`

## 系统结构

1. 数据层：自定义视觉风格分类数据集
2. 表征层：CLIP embedding
3. 分类层：轻量分类器
4. 评估层：accuracy / confusion matrix / error cases
5. 界面层：本地桌面界面 `tkinter`

## 输出形式

1. 训练好的分类 bundle
2. 评估报告
3. confusion matrix
4. 本地可交互桌面 demo

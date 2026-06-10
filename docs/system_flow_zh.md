# 整体流程逻辑

## 1. 数据准备

项目先建立一个小型自定义风格数据集，当前类别为：

1. `neoclassical`
2. `industrial`
3. `organic`
4. `minimal`

## 2. 特征提取

使用 CLIP 把所有图像转换成 embedding。

## 3. 风格分类

在 CLIP embedding 基础上训练轻量分类器，用于预测输入图像属于哪种风格类别。

## 4. 评估分析

系统输出：

1. accuracy
2. confusion matrix
3. test predictions

## 5. demo 展示

用户上传图片后，系统会：

1. 输出预测类别
2. 输出置信度
3. 返回相似参考图

这个返回参考图的功能是辅助性的，主线仍然是分类和判断分析。

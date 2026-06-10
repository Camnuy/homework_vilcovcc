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

4. 启动 demo

```powershell
python src/demo_app.py
```

## demo 使用方法

1. 上传一张图片
2. 点击 `Analyze Image`
3. 查看预测风格类别
4. 查看置信度表格
5. 查看辅助参考图

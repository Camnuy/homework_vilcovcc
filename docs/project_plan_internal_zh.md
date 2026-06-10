# EMI Final Project Plan

## 项目名称

**视觉风格分类与创意判断分析工具**  
Visual Style Classification and Creative Judgement Analysis Tool

## 一、项目定位

这个项目的定位不是纯技术分类器，而是一个**面向创作者的视觉判断分析工具**。

最终要讲清楚两层内容：

1. 机器学习如何把图像归入自定义风格类别
2. 机器学习如何把复杂的审美判断简化成有限标签，并因此产生误读

所以这项目必须同时有：

- 可运行的技术实现
- 创意实践场景
- 批判性反思

## 二、核心研究问题

建议统一成下面这个版本：

> How can a small machine-learning system classify subjective visual style categories without pretending that aesthetic judgement is objective or fixed?

中文可表述为：

> 一个小型机器学习系统是否能够把图像归入主观的视觉风格类别，同时又不把这种审美判断误装成客观、固定的分类标准？

## 三、作业目标

这个项目最后要完成的，不只是“模型能跑”，而是完整满足 EMI 大作业的交付要求。

目标拆成 5 个层次：

1. **技术层**  
   有完整代码流程：数据准备、训练、评估、demo

2. **项目层**  
   有明确问题、有方法选择、有结果分析

3. **展示层**  
   有 README、weblog、可录视频的演示界面

4. **批判层**  
   能讨论风格标签的主观性和模型误判

5. **实用层**  
   最终看起来像一个给创作者用的小工具，而不是孤立的 notebook

## 四、最终交付物

按照课程要求，最后应该包含这些内容：

1. GitHub repo
2. README
3. weblog
4. 训练与评估代码
5. 数据来源说明
6. 演示界面
7. 3-5 分钟视频
8. 至少 5 次以上 commit 记录

## 五、项目结构

当前项目建议按下面这条线讲：

### 1. 数据集

建立一个小型、可控的视觉风格数据集，先用 4 个主观但相对可区分的类别：

1. `neoclassical`
2. `industrial`
3. `organic`
4. `minimal`

这样做的好处：

- 类别数量不多，适合课程项目
- 足够有视觉差异，便于训练和展示
- 同时保留主观性，便于讨论“风格分类是否可靠”

### 2. 表征方式

使用预训练视觉模型提取图像 embedding，再训练轻量分类器。

当前主线可以统一写成：

- 使用 CLIP 提取图像特征
- 使用 Logistic Regression 做风格分类

这样合理，因为：

- 训练成本低
- 路径清楚
- 适合有限时间和硬件条件
- 结果容易解释

### 3. 工具输出

最终 demo 以分类分析为主，输出：

1. 风格预测类别
2. 预测置信度
3. 辅助性的相似参考图

这会让项目更像“创作判断实验”，而不只是“分类器作业”

## 六、完整技术路线

### Stage 1: Dataset building

1. 选定类别
2. 收集图片
3. 记录来源
4. 统一尺寸和基本清理
5. 生成 train / val / test split

### Stage 2: Representation learning

1. 加载预训练 CLIP
2. 提取所有图像 embedding
3. 保存 embedding 结果

### Stage 3: Classification

1. 使用 embedding 训练轻量分类器
2. 输出 accuracy、classification report、confusion matrix
3. 分析错误案例

### Stage 4: Supportive retrieval

1. 基于 embedding 做相似图像检索
2. 给每张输入图返回若干参考图
3. 辅助解释分类结果

### Stage 5: Demo

1. 做 Gradio 界面
2. 支持上传图片
3. 显示预测风格、置信度和参考图

## 七、项目最重要的叙事

这个作业最重要的不是“准确率越高越好”，而是要把叙事说顺。

推荐统一成下面这个逻辑：

1. 我想测试机器能不能处理主观的风格标签
2. 我先把视觉图像分成几个自定义风格类别
3. 我训练一个小模型判断输入图像更接近哪类风格
4. 我再观察它的置信度、错误和边界模糊区域
5. 我最后分析模型判断背后到底抓住了什么，以及它忽略了什么

## 八、需要重点写进 README / weblog 的内容

### README 要突出

1. 项目问题
2. 类别定义
3. 数据集来源
4. 模型选择
5. 结果截图
6. 怎么运行
7. 关键限制

### weblog 要突出

1. 为什么选这个题
2. 为什么选四个类别
3. 数据收集时遇到什么问题
4. 为什么选 CLIP + 轻量分类器
5. confusion matrix 说明了什么
6. 哪些图判错了
7. 风格标签为什么天然主观

## 九、批判性反思要点

这一块非常关键，最好提前准备。

建议主要写下面几个问题：

1. 风格到底是不是可以被稳定分类？
2. 模型是在识别“风格”，还是在识别“内容”和“颜色捷径”？
3. 如果模型把植物图都判成 `organic`，它到底理解了什么？
4. 机器学习是否会把复杂的审美经验压缩成粗糙标签？
5. 创作者会不会被模型输出反过来影响自己的判断？

## 十、reward model 的位置

如果要加上更“现在大模型时代”的扩展，可以把 reward model 定义成可选的第二阶段，而不是主线必需品。

推荐口径：

### V1（当前主线）

**分类 + 支持性相似图检索**

### V2（可选增强）

**分类 + 检索 + reward-based reranking**

也就是：

1. 先预测风格
2. 再找出一组候选参考图
3. 最后用 reward model 或多模态 judge 对候选结果重新排序

这样可以把系统升级成：

**Preference-aware inspiration tool**

但这块是加分项，不要让它拖慢主线交付。

## 十一、视频展示建议

3-5 分钟视频建议这样录：

1. 先介绍项目问题
2. 展示数据集结构
3. 简单展示训练和评估结果
4. 展示 confusion matrix
5. 打开 demo 上传几张图
6. 展示预测类别和参考图
7. 最后讲一两个错误案例和批判性反思

## 十二、当前最稳的完成标准

如果要把作业做得完整且风险可控，最低也要保证：

1. 数据集和来源说明完整
2. 训练脚本可跑
3. 评估脚本可跑
4. demo 可展示
5. README 完整
6. weblog 至少 10 条
7. 有视频提纲
8. 有一段明确的批判性反思

## 十三、最终一句话定位

可以把整个项目浓缩成下面这句话：

> This project develops a small machine-learning tool for classifying visual style references and retrieving similar inspiration images, while critically reflecting on how computational systems simplify subjective aesthetic judgement.

中文版本：

> 本项目开发了一个小型机器学习工具，用于对视觉风格参考图进行分类并返回相似灵感图像，同时批判性地反思计算系统如何将主观审美判断简化为可计算的标签。

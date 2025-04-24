## 项目一
### 统计决策方法的人脸识别系统设计与仿真

### 实验内容： 

基于人的脸部特征信息进行身份识别的一种生物识别技术。用摄像机或摄像头采集含有人脸的图像或视频流，利用所学过的统计决策方法模式识别知识，并自动在图像中检测和跟踪人脸，，进而实现人脸识别。

### 学习要求：
1. 利用所学模式识别知识对人脸识别模型进行建模；
2. 编程实现该模型，对其求解，并使用任意数据集对算法进行测试。

## 项目实现说明

### 项目结构

```
face_recognition_system/
│
├── data/                      # 数据集目录
│   ├── training/              # 训练数据，每个子文件夹代表一个人
│   └── testing/               # 测试数据，每个子文件夹代表一个人
│
├── models/                    # 存储训练好的模型
│
├── src/                       # 源代码
│   ├── face_detection.py      # 人脸检测模块
│   ├── feature_extraction.py  # 特征提取模块
│   ├── classifier.py          # 分类器实现
│   ├── utils.py               # 工具函数
│   ├── evaluation.py          # 评估模块
│   └── main.py                # 主程序
│
├── requirements.txt           # 项目依赖
└── README.md                  # 项目说明
```

### 系统流程

1. **数据准备**：将人脸图像数据按人物ID分类，放入data/training目录
2. **人脸检测**：使用Haar级联分类器或HOG+SVM方法检测图像中的人脸
3. **特征提取**：使用PCA、LBP或HOG方法提取人脸特征
4. **模型训练**：使用多种统计决策方法（LDA、QDA、朴素贝叶斯、KNN、SVM等）训练分类器
5. **模型评估**：通过混淆矩阵、准确率、ROC曲线等方式评估模型性能
6. **实时演示**：通过摄像头进行人脸识别实时演示

### 统计决策方法

本项目实现了多种统计决策方法：

1. **线性判别分析(LDA)**：寻找能最大化不同类别之间差异的投影方向
2. **二次判别分析(QDA)**：LDA的扩展，允许每个类别有不同的协方差矩阵
3. **贝叶斯决策**：基于贝叶斯定理，计算后验概率进行分类
4. **K近邻(KNN)**：基于最相似的K个样本的多数投票进行分类
5. **支持向量机(SVM)**：寻找能将不同类别样本分开的最优超平面
6. **随机森林**：集成多个决策树的结果进行分类

### 安装与使用

#### 环境配置

```bash
# 安装所需依赖
pip install -r requirements.txt
```

#### 数据准备

在data/training目录下，为每个人创建一个子文件夹，文件夹名为该人的ID或姓名。将该人的人脸图像放入对应文件夹。

#### 训练模型

```bash
# 使用默认参数训练模型
python src/main.py --mode train

# 指定参数训练模型
python src/main.py --mode train --data_dir ./data/training --feature pca --classifier lda
```

#### 测试模型

```bash
# 测试模型性能
python src/main.py --mode test --test_dir ./data/testing
```

#### 实时演示

```bash
# 启动摄像头进行实时人脸识别
python src/main.py --mode demo
```

### 参数说明

- `--mode`：运行模式，可选 train(训练)、test(测试)、demo(演示)
- `--data_dir`：训练数据目录
- `--test_dir`：测试数据目录
- `--model_path`：模型保存/加载路径
- `--detector`：人脸检测方法，可选 haar、hog
- `--feature`：特征提取方法，可选 pca、lbp、hog
- `--classifier`：分类器类型，可选 lda、qda、bayes、knn、svm、rf、bayesian
- `--pca_components`：PCA保留的主成分数量
- `--test_size`：测试集比例

### 数据集建议

您可以使用以下公开数据集进行测试：

1. [AT&T人脸数据库](https://git-disl.github.io/GTDLBench/datasets/att_face_dataset/)
2. [耶鲁人脸数据库](http://vision.ucsd.edu/content/yale-face-database)
3. [LFW人脸数据库](http://vis-www.cs.umass.edu/lfw/)

### 结果展示

系统会生成以下评估结果：

1. 混淆矩阵：显示分类器在各个类别上的性能
2. ROC曲线：评估分类器的辨别能力
3. 精确率-召回率曲线：评估分类器的查全率和查准率

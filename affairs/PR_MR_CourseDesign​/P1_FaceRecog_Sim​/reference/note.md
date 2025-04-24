## 4-24-01
完成了！我已经为你创建了一个基于统计决策方法的人脸识别系统。这个系统具有以下特点：
模块化设计：将系统分为人脸检测、特征提取、分类器和评估等模块，便于理解和扩展。
多种统计决策方法：实现了多种统计决策方法，包括：
线性判别分析(LDA)
二次判别分析(QDA)
贝叶斯决策
K近邻(KNN)
支持向量机(SVM)
随机森林
灵活的特征提取：支持多种特征提取方法：
主成分分析(PCA)
局部二值模式(LBP)
梯度方向直方图(HOG)
完整的评估系统：包含混淆矩阵、ROC曲线、精确率-召回率曲线等多种评估指标。
实时演示功能：支持通过摄像头进行实时人脸识别。
数据集准备工具：提供了下载和准备AT&T人脸数据集的工具。
使用步骤：
安装依赖：pip install -r requirements.txt
下载数据集：python download_dataset.py
训练模型：python src/main.py --mode train
测试模型：python src/main.py --mode test
实时演示：python src/main.py --mode demo
你可以根据需要调整特征提取方法和分类器类型，例如：
python src/main.py --mode train --feature lbp --classifier svm
这个系统实现了基于统计决策方法的人脸识别，满足了实验内容和学习要求。更详细的使用说明请参考项目的README.md文件。
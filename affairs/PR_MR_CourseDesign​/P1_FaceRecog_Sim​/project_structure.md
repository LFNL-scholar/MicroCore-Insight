# 人脸识别系统项目结构

```
face_recognition_system/
│
├── data/                      # 数据集目录
│   ├── training/              # 训练数据
│   └── testing/               # 测试数据
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
├── notebooks/                 # Jupyter笔记本（可选，用于实验和分析）
│
├── requirements.txt           # 项目依赖
└── README.md                  # 项目说明
``` 
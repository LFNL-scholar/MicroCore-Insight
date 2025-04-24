import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

def load_images_from_folder(folder, label=None):
    """
    从指定文件夹加载图像和标签
    
    参数:
        folder: 图像文件夹路径
        label: 该文件夹图像的标签（可选）
        
    返回:
        images: 图像列表
        labels: 标签列表
    """
    images = []
    labels = []
    
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path):
            try:
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转为灰度图
                    images.append(img)
                    if label is not None:
                        labels.append(label)
            except Exception as e:
                print(f"无法加载图像 {img_path}: {e}")
    
    return images, labels

def create_dataset(data_dir, test_size=0.2, random_state=42):
    """
    创建训练和测试数据集
    
    参数:
        data_dir: 数据目录，每个子文件夹对应一个类别
        test_size: 测试集比例
        random_state: 随机种子
        
    返回:
        X_train, X_test, y_train, y_test: 训练和测试数据集
    """
    X = []
    y = []
    
    # 遍历所有子文件夹
    for person_id, person_folder in enumerate(sorted(os.listdir(data_dir))):
        person_path = os.path.join(data_dir, person_folder)
        if os.path.isdir(person_path):
            person_images, _ = load_images_from_folder(person_path, label=person_id)
            X.extend(person_images)
            y.extend([person_id] * len(person_images))
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        np.array(X), np.array(y), test_size=test_size, random_state=random_state, stratify=y
    )
    
    return X_train, X_test, y_train, y_test

def plot_confusion_matrix(cm, classes, title='混淆矩阵', cmap=plt.cm.Blues):
    """
    绘制混淆矩阵
    
    参数:
        cm: 混淆矩阵
        classes: 类别名称
        title: 图标题
        cmap: 颜色映射
    """
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    
    fmt = 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
    
    plt.tight_layout()
    plt.ylabel('真实标签')
    plt.xlabel('预测标签')
    plt.show()

def resize_image(image, target_size=(100, 100)):
    """
    调整图像大小
    
    参数:
        image: 输入图像
        target_size: 目标大小 (width, height)
        
    返回:
        调整大小后的图像
    """
    return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA) 
import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import time
import argparse

# 导入自定义模块
from face_detection import FaceDetector
from feature_extraction import FeatureExtractor
from classifier import FaceClassifier, BayesianClassifier
from evaluation import evaluate_classifier, plot_evaluation_results
from utils import create_dataset, load_images_from_folder

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='人脸识别系统')
    
    parser.add_argument('--mode', type=str, default='train', choices=['train', 'test', 'demo'],
                      help='运行模式：train（训练模型）, test（测试模型）, demo（实时演示）')
    
    parser.add_argument('--data_dir', type=str, default='../data/training',
                      help='训练数据目录')
    
    parser.add_argument('--test_dir', type=str, default='../data/testing',
                      help='测试数据目录')
    
    parser.add_argument('--model_path', type=str, default='../models/face_model.pkl',
                      help='模型保存/加载路径')
    
    parser.add_argument('--detector', type=str, default='haar', choices=['haar', 'hog'],
                      help='人脸检测方法')
    
    parser.add_argument('--feature', type=str, default='pca', choices=['pca', 'lbp', 'hog'],
                      help='特征提取方法')
    
    parser.add_argument('--classifier', type=str, default='lda', 
                      choices=['lda', 'qda', 'bayes', 'knn', 'svm', 'rf', 'bayesian'],
                      help='分类器类型')
    
    parser.add_argument('--pca_components', type=int, default=50,
                      help='PCA保留的主成分数量')
    
    parser.add_argument('--test_size', type=float, default=0.2,
                      help='测试集比例（仅在使用train_test_split划分数据集时使用）')
    
    return parser.parse_args()

def train_model(args):
    """训练人脸识别模型"""
    print("开始训练模型...")
    
    # 加载训练数据
    print(f"从 {args.data_dir} 加载训练数据...")
    X_train, X_test, y_train, y_test = create_dataset(args.data_dir, test_size=args.test_size)
    
    # 初始化人脸检测器
    print(f"使用 {args.detector} 方法进行人脸检测...")
    detector = FaceDetector(method=args.detector)
    
    # 提取人脸区域
    print("提取人脸区域...")
    face_regions_train = []
    for img in X_train:
        faces, _ = detector.extract_face_regions(img)
        if faces:
            face_regions_train.append(faces[0])  # 假设每张图像只有一个人脸
        else:
            print("警告: 未检测到人脸，使用原始图像")
            face_regions_train.append(img)
    
    face_regions_test = []
    for img in X_test:
        faces, _ = detector.extract_face_regions(img)
        if faces:
            face_regions_test.append(faces[0])
        else:
            print("警告: 未检测到人脸，使用原始图像")
            face_regions_test.append(img)
    
    # 初始化特征提取器
    print(f"使用 {args.feature} 方法提取特征...")
    extractor = FeatureExtractor(method=args.feature, n_components=args.pca_components)
    
    # 提取特征
    print("提取人脸特征...")
    X_train_features = extractor.fit_transform(face_regions_train)
    X_test_features = extractor.transform(face_regions_test)
    
    # 初始化分类器
    if args.classifier == 'bayesian':
        # 使用自定义的贝叶斯分类器
        print("使用自定义贝叶斯分类器...")
        classifier = BayesianClassifier()
    else:
        # 使用sklearn分类器
        print(f"使用 {args.classifier} 分类器...")
        classifier = FaceClassifier(method=args.classifier)
    
    # 训练分类器
    print("训练分类器...")
    start_time = time.time()
    classifier.fit(X_train_features, y_train)
    training_time = time.time() - start_time
    print(f"训练完成，耗时 {training_time:.2f} 秒")
    
    # 评估分类器
    print("评估分类器性能...")
    train_accuracy = classifier.evaluate(X_train_features, y_train)
    test_accuracy = classifier.evaluate(X_test_features, y_test)
    
    print(f"训练集准确率: {train_accuracy:.4f}")
    print(f"测试集准确率: {test_accuracy:.4f}")
    
    # 保存模型
    print(f"保存模型到 {args.model_path}...")
    os.makedirs(os.path.dirname(args.model_path), exist_ok=True)
    
    # 创建保存的模型对象，包含所有需要的组件
    model_data = {
        'detector': detector,
        'extractor': extractor,
        'classifier': classifier,
        'args': args,
        'class_names': [str(i) for i in np.unique(y_train)]
    }
    
    import pickle
    with open(args.model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    # 详细评估并可视化结果
    evaluation_results = evaluate_classifier(classifier, X_test_features, y_test)
    plot_evaluation_results(evaluation_results)
    
    return model_data

def test_model(args):
    """测试现有的人脸识别模型"""
    print("开始测试模型...")
    
    # 加载模型
    print(f"从 {args.model_path} 加载模型...")
    import pickle
    try:
        with open(args.model_path, 'rb') as f:
            model_data = pickle.load(f)
            
        detector = model_data['detector']
        extractor = model_data['extractor']
        classifier = model_data['classifier']
        class_names = model_data.get('class_names', None)
        
    except (FileNotFoundError, pickle.UnpicklingError):
        print(f"错误: 无法加载模型文件 {args.model_path}")
        return
    
    # 加载测试数据
    print(f"从 {args.test_dir} 加载测试数据...")
    X_test = []
    y_test = []
    
    # 遍历测试目录中的所有子文件夹
    for person_id, person_folder in enumerate(sorted(os.listdir(args.test_dir))):
        person_path = os.path.join(args.test_dir, person_folder)
        if os.path.isdir(person_path):
            person_images, _ = load_images_from_folder(person_path, label=person_id)
            X_test.extend(person_images)
            y_test.extend([person_id] * len(person_images))
    
    if not X_test:
        print("错误: 未找到测试图像")
        return
    
    X_test = np.array(X_test)
    y_test = np.array(y_test)
    
    # 提取人脸区域
    print("提取人脸区域...")
    face_regions = []
    for img in X_test:
        faces, _ = detector.extract_face_regions(img)
        if faces:
            face_regions.append(faces[0])
        else:
            print("警告: 未检测到人脸，使用原始图像")
            face_regions.append(img)
    
    # 提取特征
    print("提取人脸特征...")
    X_test_features = extractor.transform(face_regions)
    
    # 评估分类器
    print("评估分类器性能...")
    evaluation_results = evaluate_classifier(classifier, X_test_features, y_test, class_names)
    plot_evaluation_results(evaluation_results, class_names)
    
    return evaluation_results

def run_demo(args):
    """运行实时演示"""
    print("启动人脸识别演示...")
    
    # 加载模型
    print(f"从 {args.model_path} 加载模型...")
    import pickle
    try:
        with open(args.model_path, 'rb') as f:
            model_data = pickle.load(f)
            
        detector = model_data['detector']
        extractor = model_data['extractor']
        classifier = model_data['classifier']
        class_names = model_data.get('class_names', None)
        
    except (FileNotFoundError, pickle.UnpicklingError):
        print(f"错误: 无法加载模型文件 {args.model_path}")
        return
    
    # 初始化摄像头
    print("初始化摄像头...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("错误: 无法打开摄像头")
        return
    
    print("按 'q' 键退出演示...")
    
    while True:
        # 读取一帧
        ret, frame = cap.read()
        
        if not ret:
            print("错误: 无法读取摄像头")
            break
        
        # 检测人脸
        face_regions, face_locations = detector.extract_face_regions(frame)
        
        # 在原始帧上绘制所有检测到的人脸
        frame_with_faces = detector.draw_faces(frame, face_locations)
        
        # 对每个检测到的人脸进行识别
        for i, face in enumerate(face_regions):
            # 提取特征
            face_features = extractor.transform([face])
            
            # 预测类别
            predicted_class = classifier.predict(face_features)[0]
            
            # 获取置信度（如果分类器支持）
            confidence = 0.0
            if hasattr(classifier, 'predict_proba'):
                try:
                    proba = classifier.predict_proba(face_features)[0]
                    confidence = proba[predicted_class]
                except:
                    pass
            
            # 获取类别名称
            if class_names and predicted_class < len(class_names):
                class_name = class_names[predicted_class]
            else:
                class_name = str(predicted_class)
            
            # 在图像上显示结果
            x, y, w, h = face_locations[i]
            cv2.putText(frame_with_faces, f"ID: {class_name}", (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            if confidence > 0:
                cv2.putText(frame_with_faces, f"Conf: {confidence:.2f}", (x, y + h + 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # 显示结果
        cv2.imshow('人脸识别演示', frame_with_faces)
        
        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

def main():
    # 解析命令行参数
    args = parse_args()
    
    # 根据运行模式执行相应的操作
    if args.mode == 'train':
        train_model(args)
    elif args.mode == 'test':
        test_model(args)
    elif args.mode == 'demo':
        run_demo(args)
    else:
        print(f"错误: 未知的运行模式 '{args.mode}'")

if __name__ == "__main__":
    main() 
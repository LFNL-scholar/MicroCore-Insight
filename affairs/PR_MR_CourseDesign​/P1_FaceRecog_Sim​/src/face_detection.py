import cv2
import numpy as np
import dlib

class FaceDetector:
    """人脸检测类，提供多种人脸检测方法"""
    
    def __init__(self, method='haar'):
        """
        初始化人脸检测器
        
        参数:
            method: 检测方法，可选 'haar'(Haar级联分类器) 或 'hog'(HOG特征+SVM)
        """
        self.method = method
        
        if method == 'haar':
            # 使用OpenCV的Haar级联分类器
            face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.detector = cv2.CascadeClassifier(face_cascade_path)
        elif method == 'hog':
            # 使用dlib的HOG特征+SVM检测器
            self.detector = dlib.get_frontal_face_detector()
        else:
            raise ValueError(f"不支持的检测方法: {method}，请选择 'haar' 或 'hog'")
    
    def detect_faces(self, image):
        """
        在图像中检测人脸
        
        参数:
            image: 输入图像 (OpenCV格式)
            
        返回:
            faces: 人脸区域列表，每个元素为 (x, y, w, h) 格式的矩形
        """
        # 确保图像为灰度图
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        if self.method == 'haar':
            # Haar级联分类器检测
            faces = self.detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            return faces  # 返回格式: [(x, y, w, h), ...]
            
        elif self.method == 'hog':
            # HOG+SVM检测
            dlib_faces = self.detector(gray, 1)
            # 转换为OpenCV格式 (x, y, w, h)
            faces = []
            for face in dlib_faces:
                x = face.left()
                y = face.top()
                w = face.right() - x
                h = face.bottom() - y
                faces.append((x, y, w, h))
            return faces
    
    def extract_face_regions(self, image, padding=0):
        """
        提取图像中的人脸区域
        
        参数:
            image: 输入图像
            padding: 人脸区域的额外填充（像素）
            
        返回:
            face_regions: 裁剪出的人脸图像列表
            face_locations: 人脸位置列表 [(x, y, w, h), ...]
        """
        face_locations = self.detect_faces(image)
        face_regions = []
        
        height, width = image.shape[:2]
        
        for (x, y, w, h) in face_locations:
            # 添加填充
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(width, x + w + padding)
            y2 = min(height, y + h + padding)
            
            # 裁剪人脸区域
            face_img = image[y1:y2, x1:x2]
            face_regions.append(face_img)
        
        return face_regions, face_locations
    
    def draw_faces(self, image, face_locations, color=(0, 255, 0), thickness=2):
        """
        在图像上绘制人脸边界框
        
        参数:
            image: 输入图像
            face_locations: 人脸位置列表 [(x, y, w, h), ...]
            color: 边界框颜色 (B, G, R)
            thickness: 边界框线条粗细
            
        返回:
            带有人脸边界框的图像
        """
        img_copy = image.copy()
        for (x, y, w, h) in face_locations:
            cv2.rectangle(img_copy, (x, y), (x + w, y + h), color, thickness)
        return img_copy 
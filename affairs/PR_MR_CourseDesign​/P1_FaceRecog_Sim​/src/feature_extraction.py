import cv2
import numpy as np
from sklearn.decomposition import PCA

class FeatureExtractor:
    """特征提取类，提供多种特征提取方法"""
    
    def __init__(self, method='pca', n_components=50):
        """
        初始化特征提取器
        
        参数:
            method: 特征提取方法，可选 'pca'、'lbp'(局部二值模式)或'hog'(梯度方向直方图)
            n_components: PCA保留的主成分数量
        """
        self.method = method
        self.n_components = n_components
        self.pca = None  # 如果使用PCA，将在训练时初始化
        
    def preprocess(self, images, target_size=(100, 100)):
        """
        预处理图像
        
        参数:
            images: 图像列表
            target_size: 目标大小
            
        返回:
            处理后的图像列表
        """
        processed_images = []
        for img in images:
            # 确保图像为灰度图
            if len(img.shape) == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 调整大小
            img = cv2.resize(img, target_size)
            
            # 直方图均衡化（增强对比度）
            img = cv2.equalizeHist(img)
            
            processed_images.append(img)
        
        return processed_images
    
    def extract_lbp_features(self, image):
        """
        提取局部二值模式(LBP)特征
        
        参数:
            image: 输入图像（灰度）
            
        返回:
            LBP特征直方图
        """
        radius = 1
        n_points = 8 * radius
        lbp = np.zeros_like(image)
        
        # 计算LBP
        for i in range(radius, image.shape[0] - radius):
            for j in range(radius, image.shape[1] - radius):
                center = image[i, j]
                binary_code = 0
                for k in range(n_points):
                    # 计算采样点坐标
                    angle = 2 * np.pi * k / n_points
                    x = i + radius * np.cos(angle)
                    y = j + radius * np.sin(angle)
                    
                    # 双线性插值
                    x1, y1 = int(np.floor(x)), int(np.floor(y))
                    x2, y2 = min(x1 + 1, image.shape[0] - 1), min(y1 + 1, image.shape[1] - 1)
                    
                    # 计算权重
                    tx, ty = x - x1, y - y1
                    
                    # 计算采样点的灰度值
                    value = (1 - tx) * (1 - ty) * image[x1, y1] + \
                            tx * (1 - ty) * image[x2, y1] + \
                            (1 - tx) * ty * image[x1, y2] + \
                            tx * ty * image[x2, y2]
                    
                    # 与中心点比较并构建二进制编码
                    if value >= center:
                        binary_code |= (1 << k)
                
                lbp[i, j] = binary_code
        
        # 计算LBP直方图
        histogram = np.histogram(lbp, bins=256, range=(0, 256))[0]
        
        # 归一化直方图
        if np.sum(histogram) != 0:
            histogram = histogram / np.sum(histogram)
            
        return histogram
    
    def extract_hog_features(self, image):
        """
        提取HOG特征
        
        参数:
            image: 输入图像（灰度）
            
        返回:
            HOG特征向量
        """
        # HOG参数
        win_size = (64, 64)
        block_size = (16, 16)
        block_stride = (8, 8)
        cell_size = (8, 8)
        nbins = 9
        
        # 确保图像大小符合HOG要求
        if image.shape[0] != win_size[0] or image.shape[1] != win_size[1]:
            image = cv2.resize(image, win_size)
        
        # 初始化HOG描述子
        hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
        
        # 计算HOG特征
        hog_features = hog.compute(image)
        
        return hog_features.flatten()
    
    def fit(self, images):
        """
        拟合特征提取器（用于PCA）
        
        参数:
            images: 训练图像列表
            
        返回:
            self
        """
        if self.method == 'pca':
            # 预处理图像
            processed_images = self.preprocess(images)
            
            # 将图像展平为向量
            X = np.array([img.flatten() for img in processed_images])
            
            # 拟合PCA
            self.pca = PCA(n_components=self.n_components)
            self.pca.fit(X)
            
        return self
    
    def transform(self, images):
        """
        提取特征
        
        参数:
            images: 图像列表
            
        返回:
            特征列表
        """
        # 预处理图像
        processed_images = self.preprocess(images)
        
        features = []
        for img in processed_images:
            if self.method == 'pca':
                # 检查PCA是否已经拟合
                if self.pca is None:
                    raise ValueError("在调用transform之前必须先调用fit方法")
                
                # 将图像展平并应用PCA
                img_vector = img.flatten().reshape(1, -1)
                feature = self.pca.transform(img_vector).flatten()
                
            elif self.method == 'lbp':
                # 提取LBP特征
                feature = self.extract_lbp_features(img)
                
            elif self.method == 'hog':
                # 提取HOG特征
                feature = self.extract_hog_features(img)
                
            else:
                raise ValueError(f"不支持的特征提取方法: {self.method}")
            
            features.append(feature)
        
        return np.array(features)
    
    def fit_transform(self, images):
        """
        拟合特征提取器并提取特征
        
        参数:
            images: 图像列表
            
        返回:
            特征列表
        """
        self.fit(images)
        return self.transform(images) 
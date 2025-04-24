import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class FaceClassifier:
    """人脸分类器类，提供多种统计决策方法"""
    
    def __init__(self, method='lda'):
        """
        初始化分类器
        
        参数:
            method: 分类方法，可选以下几种：
                'lda': 线性判别分析
                'qda': 二次判别分析
                'bayes': 朴素贝叶斯
                'knn': K近邻
                'svm': 支持向量机
                'rf': 随机森林
        """
        self.method = method
        self.model = None
        
        # 根据方法初始化相应的分类器
        if method == 'lda':
            self.model = LinearDiscriminantAnalysis()
        elif method == 'qda':
            self.model = QuadraticDiscriminantAnalysis()
        elif method == 'bayes':
            self.model = GaussianNB()
        elif method == 'knn':
            self.model = KNeighborsClassifier(n_neighbors=5)
        elif method == 'svm':
            self.model = SVC(kernel='rbf', probability=True)
        elif method == 'rf':
            self.model = RandomForestClassifier(n_estimators=100)
        else:
            raise ValueError(f"不支持的分类方法: {method}")
    
    def fit(self, X, y):
        """
        训练分类器
        
        参数:
            X: 特征矩阵，每行为一个样本的特征向量
            y: 类别标签
            
        返回:
            self
        """
        self.model.fit(X, y)
        return self
    
    def predict(self, X):
        """
        预测样本类别
        
        参数:
            X: 特征矩阵，每行为一个样本的特征向量
            
        返回:
            预测的类别标签
        """
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        预测样本属于各个类别的概率
        
        参数:
            X: 特征矩阵，每行为一个样本的特征向量
            
        返回:
            每个样本属于各个类别的概率
        """
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X)
        else:
            raise NotImplementedError(f"{self.method} 不支持概率预测")
    
    def evaluate(self, X, y):
        """
        评估分类器性能
        
        参数:
            X: 特征矩阵，每行为一个样本的特征向量
            y: 真实类别标签
            
        返回:
            准确率
        """
        y_pred = self.predict(X)
        accuracy = np.sum(y_pred == y) / len(y)
        return accuracy
    
    def save_model(self, model_path):
        """
        保存模型到文件
        
        参数:
            model_path: 模型保存路径
        """
        # 创建目录（如果不存在）
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # 保存模型
        joblib.dump(self.model, model_path)
    
    def load_model(self, model_path):
        """
        从文件加载模型
        
        参数:
            model_path: 模型文件路径
            
        返回:
            self
        """
        self.model = joblib.load(model_path)
        return self


class BayesianClassifier:
    """贝叶斯决策分类器"""
    
    def __init__(self):
        """初始化贝叶斯分类器"""
        self.classes = None  # 类别列表
        self.class_priors = None  # 先验概率 P(ω_i)
        self.class_means = None  # 类条件概率密度的均值
        self.class_covs = None  # 类条件概率密度的协方差矩阵
    
    def fit(self, X, y):
        """
        训练贝叶斯分类器
        
        参数:
            X: 特征矩阵，每行为一个样本的特征向量
            y: 类别标签
            
        返回:
            self
        """
        self.classes = np.unique(y)
        n_classes = len(self.classes)
        n_features = X.shape[1]
        
        # 初始化
        self.class_priors = np.zeros(n_classes)
        self.class_means = np.zeros((n_classes, n_features))
        self.class_covs = np.zeros((n_classes, n_features, n_features))
        
        # 计算先验概率和类条件概率密度参数
        n_samples = len(y)
        for i, cls in enumerate(self.classes):
            X_class = X[y == cls]
            n_class_samples = len(X_class)
            
            # 先验概率 P(ω_i)
            self.class_priors[i] = n_class_samples / n_samples
            
            # 类条件概率密度的均值
            self.class_means[i] = np.mean(X_class, axis=0)
            
            # 类条件概率密度的协方差矩阵
            self.class_covs[i] = np.cov(X_class, rowvar=False)
        
        return self
    
    def _multivariate_gaussian(self, x, mean, cov):
        """
        计算多元高斯分布概率密度
        
        参数:
            x: 单个样本的特征向量
            mean: 均值向量
            cov: 协方差矩阵
            
        返回:
            概率密度值
        """
        n = len(mean)
        det_cov = np.linalg.det(cov)
        if det_cov <= 0:
            # 处理奇异协方差矩阵
            cov = cov + np.eye(n) * 1e-6
            det_cov = np.linalg.det(cov)
            
        inv_cov = np.linalg.inv(cov)
        diff = x - mean
        
        # 计算多元高斯分布的概率密度
        exponent = -0.5 * np.dot(np.dot(diff, inv_cov), diff)
        coef = 1.0 / np.sqrt((2 * np.pi) ** n * det_cov)
        
        return coef * np.exp(exponent)
    
    def predict(self, X):
        """
        预测样本类别
        
        参数:
            X: 特征矩阵，每行为一个样本的特征向量
            
        返回:
            预测的类别标签
        """
        return np.array([self._predict_sample(x) for x in X])
    
    def _predict_sample(self, x):
        """
        预测单个样本的类别
        
        参数:
            x: 单个样本的特征向量
            
        返回:
            预测的类别标签
        """
        posteriors = []
        
        # 计算每个类别的后验概率
        for i, cls in enumerate(self.classes):
            # 类条件概率密度 p(x|ω_i)
            likelihood = self._multivariate_gaussian(x, self.class_means[i], self.class_covs[i])
            
            # 后验概率正比于 p(x|ω_i) * P(ω_i)
            posterior = likelihood * self.class_priors[i]
            posteriors.append(posterior)
        
        # 返回后验概率最大的类别
        return self.classes[np.argmax(posteriors)]
    
    def predict_proba(self, X):
        """
        预测样本属于各个类别的概率
        
        参数:
            X: 特征矩阵，每行为一个样本的特征向量
            
        返回:
            每个样本属于各个类别的概率
        """
        proba = np.zeros((X.shape[0], len(self.classes)))
        
        for i, x in enumerate(X):
            posteriors = []
            
            # 计算每个类别的后验概率
            for j, cls in enumerate(self.classes):
                # 类条件概率密度 p(x|ω_i)
                likelihood = self._multivariate_gaussian(x, self.class_means[j], self.class_covs[j])
                
                # 后验概率正比于 p(x|ω_i) * P(ω_i)
                posterior = likelihood * self.class_priors[j]
                posteriors.append(posterior)
            
            # 归一化后验概率
            posteriors = np.array(posteriors)
            sum_posteriors = np.sum(posteriors)
            
            if sum_posteriors > 0:
                proba[i] = posteriors / sum_posteriors
            else:
                # 处理极端情况
                proba[i] = self.class_priors
        
        return proba 
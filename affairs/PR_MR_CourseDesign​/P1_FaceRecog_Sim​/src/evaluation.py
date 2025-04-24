import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, auc
from utils import plot_confusion_matrix

def evaluate_classifier(classifier, X_test, y_test, class_names=None):
    """
    评估分类器性能
    
    参数:
        classifier: 分类器对象，必须实现predict方法
        X_test: 测试特征矩阵
        y_test: 测试标签
        class_names: 类别名称，如果为None则使用标签值
        
    返回:
        evaluation_results: 包含各种评估指标的字典
    """
    # 预测类别
    y_pred = classifier.predict(X_test)
    
    # 计算准确率
    accuracy = np.mean(y_pred == y_test)
    
    # 计算混淆矩阵
    cm = confusion_matrix(y_test, y_pred)
    
    # 如果未提供类别名称，则使用标签值
    if class_names is None:
        class_names = [str(i) for i in np.unique(y_test)]
    
    # 计算每个类别的精确率、召回率、F1分数等
    report = classification_report(y_test, y_pred, target_names=class_names, output_dict=True)
    
    # 组织评估结果
    evaluation_results = {
        'accuracy': accuracy,
        'confusion_matrix': cm,
        'classification_report': report
    }
    
    # 如果分类器支持predict_proba方法，则计算ROC曲线和AUC
    if hasattr(classifier, 'predict_proba'):
        try:
            y_proba = classifier.predict_proba(X_test)
            
            # 二分类情况
            if len(np.unique(y_test)) == 2:
                # 计算ROC曲线和AUC
                fpr, tpr, _ = roc_curve(y_test, y_proba[:, 1])
                roc_auc = auc(fpr, tpr)
                
                evaluation_results['roc'] = {
                    'fpr': fpr,
                    'tpr': tpr,
                    'auc': roc_auc
                }
                
                # 计算精确率-召回率曲线
                precision, recall, _ = precision_recall_curve(y_test, y_proba[:, 1])
                pr_auc = auc(recall, precision)
                
                evaluation_results['pr'] = {
                    'precision': precision,
                    'recall': recall,
                    'auc': pr_auc
                }
            
            # 多分类情况 - 计算每个类别的ROC和AUC
            else:
                roc_data = {}
                pr_data = {}
                
                for i, class_name in enumerate(class_names):
                    # 将问题转化为二分类：当前类别 vs 其他类别
                    y_bin = (y_test == i).astype(int)
                    
                    # 计算ROC曲线和AUC
                    fpr, tpr, _ = roc_curve(y_bin, y_proba[:, i])
                    roc_auc = auc(fpr, tpr)
                    
                    roc_data[class_name] = {
                        'fpr': fpr,
                        'tpr': tpr,
                        'auc': roc_auc
                    }
                    
                    # 计算精确率-召回率曲线
                    precision, recall, _ = precision_recall_curve(y_bin, y_proba[:, i])
                    pr_auc = auc(recall, precision)
                    
                    pr_data[class_name] = {
                        'precision': precision,
                        'recall': recall,
                        'auc': pr_auc
                    }
                
                evaluation_results['roc'] = roc_data
                evaluation_results['pr'] = pr_data
                
        except (ValueError, AttributeError) as e:
            print(f"计算ROC曲线时出错: {e}")
    
    return evaluation_results

def plot_evaluation_results(evaluation_results, class_names=None):
    """
    可视化评估结果
    
    参数:
        evaluation_results: evaluate_classifier返回的评估结果字典
        class_names: 类别名称，如果为None则使用标签值
    """
    # 绘制混淆矩阵
    cm = evaluation_results['confusion_matrix']
    if class_names is None:
        class_names = [str(i) for i in range(cm.shape[0])]
    
    plot_confusion_matrix(cm, class_names)
    
    # 计算并打印评估指标
    print("\n分类性能评估:")
    print(f"准确率: {evaluation_results['accuracy']:.4f}")
    
    report = evaluation_results['classification_report']
    print("\n分类报告:")
    for cls in class_names:
        print(f"类别 {cls}:")
        print(f"  精确率: {report[cls]['precision']:.4f}")
        print(f"  召回率: {report[cls]['recall']:.4f}")
        print(f"  F1分数: {report[cls]['f1-score']:.4f}")
        print(f"  支持数: {report[cls]['support']}")
    
    print(f"\n宏平均精确率: {report['macro avg']['precision']:.4f}")
    print(f"宏平均召回率: {report['macro avg']['recall']:.4f}")
    print(f"宏平均F1分数: {report['macro avg']['f1-score']:.4f}")
    
    print(f"\n加权平均精确率: {report['weighted avg']['precision']:.4f}")
    print(f"加权平均召回率: {report['weighted avg']['recall']:.4f}")
    print(f"加权平均F1分数: {report['weighted avg']['f1-score']:.4f}")
    
    # 如果有ROC曲线数据，则绘制ROC曲线
    if 'roc' in evaluation_results:
        roc_data = evaluation_results['roc']
        
        # 二分类情况
        if isinstance(roc_data, dict) and 'fpr' in roc_data:
            plt.figure(figsize=(10, 8))
            plt.plot(roc_data['fpr'], roc_data['tpr'], 
                    label=f'ROC曲线 (AUC = {roc_data["auc"]:.4f})')
            plt.plot([0, 1], [0, 1], 'k--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('假正例率')
            plt.ylabel('真正例率')
            plt.title('接收者操作特征曲线')
            plt.legend(loc="lower right")
            plt.show()
            
            # 绘制精确率-召回率曲线
            if 'pr' in evaluation_results:
                pr_data = evaluation_results['pr']
                plt.figure(figsize=(10, 8))
                plt.plot(pr_data['recall'], pr_data['precision'],
                        label=f'PR曲线 (AUC = {pr_data["auc"]:.4f})')
                plt.xlim([0.0, 1.0])
                plt.ylim([0.0, 1.05])
                plt.xlabel('召回率')
                plt.ylabel('精确率')
                plt.title('精确率-召回率曲线')
                plt.legend(loc="lower left")
                plt.show()
        
        # 多分类情况
        else:
            # 绘制ROC曲线
            plt.figure(figsize=(10, 8))
            for cls, data in roc_data.items():
                plt.plot(data['fpr'], data['tpr'], 
                        label=f'ROC曲线 {cls} (AUC = {data["auc"]:.4f})')
            
            plt.plot([0, 1], [0, 1], 'k--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('假正例率')
            plt.ylabel('真正例率')
            plt.title('接收者操作特征曲线 (每个类别 vs 其他)')
            plt.legend(loc="lower right")
            plt.show()
            
            # 绘制精确率-召回率曲线
            if 'pr' in evaluation_results:
                pr_data = evaluation_results['pr']
                plt.figure(figsize=(10, 8))
                for cls, data in pr_data.items():
                    plt.plot(data['recall'], data['precision'],
                            label=f'PR曲线 {cls} (AUC = {data["auc"]:.4f})')
                
                plt.xlim([0.0, 1.0])
                plt.ylim([0.0, 1.05])
                plt.xlabel('召回率')
                plt.ylabel('精确率')
                plt.title('精确率-召回率曲线 (每个类别 vs 其他)')
                plt.legend(loc="lower left")
                plt.show() 
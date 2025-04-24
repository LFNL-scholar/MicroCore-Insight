import os
import urllib.request
import zipfile
import shutil
import argparse
import sys

def download_att_faces(data_dir='data'):
    """
    下载并解压AT&T人脸数据集
    
    参数:
        data_dir: 数据目录
    """
    # 创建数据目录
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(os.path.join(data_dir, 'training'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, 'testing'), exist_ok=True)
    
    # AT&T数据集URL
    url = "https://git-disl.github.io/GTDLBench/datasets/att_face_dataset/att_faces.zip"
    zip_path = os.path.join(data_dir, 'att_faces.zip')
    extract_path = os.path.join(data_dir, 'att_faces')
    
    # 下载数据集
    print(f"正在下载AT&T人脸数据集...")
    try:
        urllib.request.urlretrieve(url, zip_path)
        print(f"下载完成，保存到 {zip_path}")
    except Exception as e:
        print(f"下载失败: {e}")
        return False
    
    # 解压数据集
    print(f"正在解压数据集...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        print(f"解压完成，保存到 {extract_path}")
    except Exception as e:
        print(f"解压失败: {e}")
        return False
    
    # 重命名文件夹
    att_path = os.path.join(data_dir, 'att_faces')
    if not os.path.exists(att_path):
        att_path = os.path.join(data_dir, 'ATT')  # 备选路径
        if not os.path.exists(att_path):
            print("无法找到解压后的数据集文件夹")
            return False
    
    # 分割数据集为训练集和测试集
    print("正在分割数据集为训练集和测试集...")
    s_path = os.path.join(att_path, 's')
    if os.path.exists(s_path):
        # 有些版本的AT&T数据集可能有一个额外的's'文件夹
        att_path = s_path
    
    # 遍历每个人的文件夹
    for person_folder in sorted(os.listdir(att_path)):
        person_path = os.path.join(att_path, person_folder)
        if os.path.isdir(person_path):
            # 创建训练和测试文件夹
            train_person_path = os.path.join(data_dir, 'training', person_folder)
            test_person_path = os.path.join(data_dir, 'testing', person_folder)
            os.makedirs(train_person_path, exist_ok=True)
            os.makedirs(test_person_path, exist_ok=True)
            
            # 获取所有图像文件
            image_files = sorted([f for f in os.listdir(person_path) if f.endswith(('.pgm', '.jpg', '.png'))])
            
            # 分割：前8张用于训练，后2张用于测试
            train_count = min(8, int(len(image_files) * 0.8))
            train_files = image_files[:train_count]
            test_files = image_files[train_count:]
            
            # 复制训练图像
            for f in train_files:
                src = os.path.join(person_path, f)
                dst = os.path.join(train_person_path, f)
                shutil.copy2(src, dst)
            
            # 复制测试图像
            for f in test_files:
                src = os.path.join(person_path, f)
                dst = os.path.join(test_person_path, f)
                shutil.copy2(src, dst)
    
    print(f"数据集准备完成。")
    print(f"训练数据位于: {os.path.join(data_dir, 'training')}")
    print(f"测试数据位于: {os.path.join(data_dir, 'testing')}")
    
    # 可选：删除临时文件
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    return True

def main():
    parser = argparse.ArgumentParser(description='下载并准备AT&T人脸数据集')
    parser.add_argument('--data_dir', type=str, default='data', help='数据目录')
    args = parser.parse_args()
    
    success = download_att_faces(args.data_dir)
    if success:
        print("数据集准备成功！")
        sys.exit(0)
    else:
        print("数据集准备失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 
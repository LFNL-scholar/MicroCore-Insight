import requests
import base64
import os
from datetime import datetime

def save_tts_audio(text, output_dir="output"):
    """
    调用TTS API并保存音频文件
    
    Args:
        text (str): 要转换为语音的文本
        output_dir (str): 输出目录，默认为'output'
    
    Returns:
        str: 生成的音频文件路径，如果失败则返回None
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # API endpoint
    url = "http://localhost:8007/api/tts"
    
    # 准备请求数据
    data = {
        "text": text,
        "voice": "zh_female_wanwanxiaohe_moon_bigtts"
    }
    
    try:
        # 发送请求到TTS API
        response = requests.post(url, json=data)
        response.raise_for_status()  # 检查请求是否成功
        
        # 获取响应数据
        result = response.json()
        
        if result["status"] == "success":
            # 解码base64音频数据
            audio_data = base64.b64decode(result["audio_data"])
            
            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tts_{timestamp}.mp3"
            filepath = os.path.join(output_dir, filename)
            
            # 保存音频文件
            with open(filepath, "wb") as f:
                f.write(audio_data)
            
            print(f"音频文件已保存: {filepath}")
            return filepath
                
        else:
            print(f"TTS转换失败: {result.get('message', '未知错误')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {str(e)}")
        return None
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None

if __name__ == "__main__":
    # 使用示例
    text = input("请输入要转换为语音的文本: ")
    output_path = save_tts_audio(text)
    
    if output_path:
        print(f"转换成功！文件保存在: {output_path}")
    else:
        print("转换失败！")

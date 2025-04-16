# VAD 检测 保留有人说话声音的部分，发送给ASR端点，获取识别到的文字
# 把文字发送给相应的服务端点

import sounddevice as sd
import numpy as np
import requests
import os
import time
from datetime import datetime
from scipy.io import wavfile
from scipy.io.wavfile import write as write_wav
import threading
import queue
from pydub import AudioSegment

# 录音参数配置
RATE = 16000  # 采样率
CHANNELS = 1  # 单声道
DTYPE = np.int16  # 采样格式
SILENCE_THRESHOLD = 0.03  # 静音阈值
MIN_AUDIO_LENGTH = 1.0  # 最短录音长度（秒）
MAX_AUDIO_LENGTH = 10.0  # 最长录音长度（秒）
SILENCE_DURATION = 1.0  # 停止录音的静音持续时间（秒）

def get_audio_level(data):
    """计算音频数据的音量级别"""
    return np.abs(data).mean()

def convert_to_mp3(wav_path):
    """
    将WAV文件转换为MP3格式
    """
    try:
        # 生成MP3文件路径
        mp3_path = wav_path.rsplit('.', 1)[0] + '.mp3'
        
        # 转换格式
        audio = AudioSegment.from_wav(wav_path)
        audio.export(mp3_path, format='mp3')
        
        # 删除原WAV文件
        os.remove(wav_path)
        
        return mp3_path
    except Exception as e:
        print(f"转换MP3格式失败: {str(e)}")
        return wav_path

def record_audio():
    """
    录制音频，自动检测语音开始和结束
    返回录音文件路径
    """
    # 创建输出目录
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成临时WAV文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    wav_path = os.path.join(output_dir, f"recording_{timestamp}.wav")
    
    # 用于存储音频数据的队列
    q = queue.Queue()
    
    # 录音回调函数
    def audio_callback(indata, frames, time, status):
        if status:
            print(f"录音状态: {status}")
        q.put(indata.copy())
    
    try:
        # 开始录音
        print("* 开始录音 (按Ctrl+C停止)...")
        
        frames = []  # 存储音频帧
        is_recording = False  # 是否正在录制有效语音
        silence_start = None  # 静音开始时间
        start_time = time.time()
        
        with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype=DTYPE, callback=audio_callback):
            while True:
                # 获取音频数据
                data = q.get()
                frames.append(data)
                
                # 计算音量级别
                level = get_audio_level(data)
                
                # 检测语音
                if level > SILENCE_THRESHOLD:
                    is_recording = True
                    silence_start = None
                elif is_recording:
                    # 开始记录静音时间
                    if silence_start is None:
                        silence_start = time.time()
                    # 检查静音持续时间
                    elif time.time() - silence_start >= SILENCE_DURATION:
                        break
                
                # 检查录音时长
                current_duration = time.time() - start_time
                if current_duration >= MAX_AUDIO_LENGTH:
                    break
                
                # 如果还没检测到语音且超过最短录音时间，继续等待
                if not is_recording and current_duration < MIN_AUDIO_LENGTH:
                    continue
        
        print("* 录音结束")
        
        # 如果没有检测到语音，返回 None
        if not is_recording:
            print("未检测到语音")
            return None
        
        # 合并音频数据并保存为WAV
        audio_data = np.concatenate(frames, axis=0)
        write_wav(wav_path, RATE, audio_data)
        
        # 转换为MP3格式
        print("* 正在转换为MP3格式...")
        mp3_path = convert_to_mp3(wav_path)
        
        return mp3_path
        
    except KeyboardInterrupt:
        print("\n* 录音被用户中断")
        return None
    except Exception as e:
        print(f"录音出错: {str(e)}")
        return None

def send_to_asr(audio_file_path):
    """
    将录音文件发送到 ASR 服务进行识别
    """
    if not audio_file_path or not os.path.exists(audio_file_path):
        return None
        
    url = "http://localhost:8007/api/asr"
    
    try:
        with open(audio_file_path, "rb") as f:
            files = {"audio_file": ("audio.mp3", f, "audio/mpeg")}
            response = requests.post(url, files=files)
            
        if response.status_code == 200:
            result = response.json()
            return result.get("text")
        else:
            print(f"ASR请求失败: {response.json().get('detail', '未知错误')}")
            return None
            
    except Exception as e:
        print(f"发送ASR请求时出错: {str(e)}")
        return None

def main():
    """
    主函数：录音并识别
    """
    print("\n录音程序使用说明：")
    print("1. 按回车开始录音")
    print("2. 说话时会自动开始录制")
    print("3. 停止说话后会自动结束录音")
    print("4. 也可以按 Ctrl+C 手动停止")
    print("5. 录音结束后会自动进行语音识别")
    
    try:
        while True:
            input("\n按回车开始新的录音...")
            audio_file = record_audio()
            
            if audio_file:
                print(f"录音文件已保存: {audio_file}")
                print("正在识别语音...")
                
                text = send_to_asr(audio_file)
                if text:
                    print(f"识别结果: {text}")
                else:
                    print("语音识别失败")
                    
                # 删除临时录音文件
                os.remove(audio_file)
            
            # 询问是否继续
            choice = input("\n是否继续录音？(y/n): ").lower()
            if choice != 'y':
                break
                
    except KeyboardInterrupt:
        print("\n程序已退出")

if __name__ == "__main__":
    main()

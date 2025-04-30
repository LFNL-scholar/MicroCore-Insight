import sys
from pathlib import Path
from typing import List, Optional
import asyncio

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
from config.logger import setup_logging
from app.volcano_asr import ASRProvider
from app.vad import create_instance as create_vad

class Connection:
    """连接对象，用于存储VAD检测相关的状态"""
    def __init__(self):
        self.client_audio_buffer = b""  # 音频缓冲区
        self.client_have_voice = False  # 是否检测到声音
        self.client_have_voice_last_time = 0  # 上次检测到声音的时间戳
        self.client_voice_stop = False  # 是否停止说话

class MainHandle:
    def __init__(self):
        """初始化"""
        self.logger = setup_logging().bind(tag=self.__class__.__name__)
        self.logger.info("初始化语音处理模块...")
        
        # 初始化ASR和VAD
        self.asr = ASRProvider()
        self.vad = create_vad()
        self.conn = Connection()
        
        # 存储有效的音频数据
        self.valid_audio_frames = []

    def process_audio(self, audio_frames: List[bytes]) -> Optional[str]:
        """处理录制的音频数据，应用VAD并进行ASR识别"""
        self.logger.info(f"开始处理 {len(audio_frames)} 个音频帧")
        
        # 重置状态
        self.conn = Connection()
        self.valid_audio_frames = []
        
        # 对每一帧进行VAD处理
        for frame in audio_frames:
            is_speech = self.vad.is_vad(self.conn, frame)
            if is_speech or self.conn.client_have_voice:
                self.valid_audio_frames.append(frame)
        
        # 如果没有检测到语音，返回None
        if not self.valid_audio_frames:
            self.logger.info("未检测到有效语音")
            return None
        
        # 异步执行ASR识别
        loop = asyncio.get_event_loop()
        if not loop.is_running():
            text = loop.run_until_complete(self.asr.speech_to_text(self.valid_audio_frames, "session_id"))
        else:
            # 如果已经在运行一个事件循环，创建一个新的
            text = asyncio.run(self.asr.speech_to_text(self.valid_audio_frames, "session_id"))
        
        self.logger.info(f"识别文本：{text}")
        return text
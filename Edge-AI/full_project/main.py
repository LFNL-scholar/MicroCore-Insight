import time
import sys
from app.audio_record import AudioRecorder
from app.handle import MainHandle
from config.logger import setup_logging

def main():
    logger = setup_logging().bind(tag="main")
    logger.info("程序启动")
    
    # 创建录音器并检查麦克风
    try:
        recorder = AudioRecorder()
        
        # 检查是否有麦克风，没有则直接退出
        if not recorder.has_microphone:
            logger.error("没有可用的麦克风设备")
            print("❌ 没有可用的麦克风设备，程序退出")
            sys.exit(0)
            
        # 初始化处理器
        handler = MainHandle()
        
        # 使用空格键控制录音
        print("按住空格键进行语音录制，录制完成后会自动识别并打印结果")
        print("按Ctrl+C退出程序")
        
        # 启动空格键监听线程
        monitor_thread = recorder.start_space_monitor()
        
        try:
            # 主循环
            while True:
                # 检查是否有录音数据
                if not recorder.is_recording and recorder.audio_frames:
                    # 获取录音数据进行处理
                    audio_data = recorder.audio_frames.copy()
                    recorder.audio_frames.clear()  # 清空缓冲区
                    
                    # 处理音频数据
                    try:
                        handler.process_audio(audio_data)
                    except Exception as e:
                        logger.error(f"处理音频数据失败: {e}")
                    
                time.sleep(0.1)  # 减少CPU使用率
                
        except KeyboardInterrupt:
            if recorder.is_recording:
                recorder.stop_recording()
            logger.info("程序退出")
            print("\n程序已退出")
            
    except Exception as e:
        logger.error(f"程序初始化失败: {e}")
        print(f"程序初始化失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
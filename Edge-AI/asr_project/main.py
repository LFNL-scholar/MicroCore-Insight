import time
from handle.audio_record import AudioRecorder

def main():
    # 创建录音器实例
    recorder = AudioRecorder()
    
    # 方式1：直接控制
    recorder.start_recording()
    time.sleep(5)  # 录制5秒
    audio_data = recorder.stop_recording()
    
    # 方式2：空格键控制
    if recorder.has_microphone:
        monitor_thread = recorder.start_space_monitor()
        try:
            while True:  # 主线程保持运行
                time.sleep(1)
        except KeyboardInterrupt:
            recorder.stop_recording()

if __name__ == "__main__":
    main()
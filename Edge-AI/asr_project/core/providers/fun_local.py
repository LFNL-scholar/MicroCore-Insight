import time
import io
import sys
import opuslib_next
from typing import Optional, Tuple, List
from config.logger import setup_logging

from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

TAG = __name__
logger = setup_logging()


class CaptureOutput:
    def __enter__(self):
        self._output = io.StringIO()
        self._original_stdout = sys.stdout
        sys.stdout = self._output

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self._original_stdout
        self.output = self._output.getvalue()
        self._output.close()

        if self.output:
            logger.bind(tag=TAG).success(f"ASR module initialized successfully | {self.output.strip()}")


class ASRProvider():
    def __init__(self):
        self.model_dir = "models/SenseVoiceSmall"
   
        with CaptureOutput():
            self.model = AutoModel(
                model=self.model_dir,
                vad_kwargs={"max_single_segment_time": 30000},
                disable_update=True,
                hub="hf"
                # device="cuda:0",  # 启用GPU加速
            )

    def decode_opus_to_pcm(self, opus_data: List[bytes]) -> bytes:
        """将Opus音频数据解码为PCM格式"""
        decoder = opuslib_next.Decoder(16000, 1)  # 16kHz, 单声道
        pcm_data = []

        for opus_packet in opus_data:
            try:
                pcm_frame = decoder.decode(opus_packet, 960)  # 960 samples = 60ms
                pcm_data.append(pcm_frame)
            except opuslib_next.OpusError as e:
                logger.bind(tag=TAG).error(f"Opus解码错误: {e}", exc_info=True)

        return b"".join(pcm_data)

    async def speech_to_text(self, opus_data: List[bytes], session_id: str) -> Tuple[Optional[str], Optional[str]]:
        """语音转文本主处理逻辑"""
        try:
            # 解码Opus为PCM
            start_time = time.time()
            pcm_data = self.decode_opus_to_pcm(opus_data)
            logger.bind(tag=TAG).debug(f"Opus解码耗时: {time.time() - start_time:.3f}s | 数据长度: {len(pcm_data)}字节")

            # 语音识别
            start_time = time.time()
            
            # 直接将PCM数据传递给模型
            result = self.model.generate(
                input=pcm_data,  # 直接传入PCM数据
                cache={},
                language="auto",
                use_itn=True,
                batch_size_s=60,
                data_type="sound"  # 指定输入类型为原始音频数据
            )
            
            text = rich_transcription_postprocess(result[0]["text"])
            logger.bind(tag=TAG).debug(f"语音识别耗时: {time.time() - start_time:.3f}s | 结果: {text}")

            return text

        except Exception as e:
            logger.bind(tag=TAG).error(f"语音识别失败: {e}", exc_info=True)
            return ""
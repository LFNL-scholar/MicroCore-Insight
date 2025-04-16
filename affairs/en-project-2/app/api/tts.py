from fastapi import HTTPException, APIRouter
from schemas.tts_request import TTSRequest
from services.tts_server import receive_tts_data
from datetime import datetime
import base64
import os

router = APIRouter()


@router.post("/api/tts")
async def receive_tts_request(tts_request: TTSRequest):
    """接收并存储设备信息"""
    text = tts_request.text
    try:
        audio_file_path = await receive_tts_data(text)
        
        # Read the audio file and encode it as base64
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        # Remove the temporary file after reading
        os.remove(audio_file_path)

        return {
            "status": "success",
            "message": "成功接收到TTS数据",
            "audio_data": audio_base64
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


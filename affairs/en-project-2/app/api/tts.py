from fastapi import HTTPException, APIRouter
from schemas.tts_request import TTSRequest
from services.tts_server import receive_tts_data
import base64
import os

router = APIRouter()

@router.post("/api/tts")
async def receive_tts_request(tts_request: TTSRequest):
    """语音合成接口"""
    text = tts_request.text
    voice = tts_request.voice

    if text == "":
        raise HTTPException(status_code=400, detail="文本不能为空")
    if len(text) > 100:
        raise HTTPException(status_code=400, detail="文本不能超过100个字符")
    
    try:
        audio_file_path = await receive_tts_data(text, voice)

        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        os.remove(audio_file_path)

        return {
            "status": "success",
            "message": "语音合成成功",
            "audio_data": audio_base64
        }
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


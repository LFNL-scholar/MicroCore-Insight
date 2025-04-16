from fastapi import HTTPException, APIRouter, UploadFile, File
from services.asr_server import recognize_speech

router = APIRouter()

@router.post("/api/asr")
async def receive_asr_request(audio_file: UploadFile = File(...)):
    """语音识别接口"""
    if not audio_file.filename.endswith('.mp3'):
        raise HTTPException(status_code=400, detail="只支持MP3格式的音频文件")
    
    try:
        audio_data = await audio_file.read()
        
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="音频文件为空")
        
        if len(audio_data) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="音频文件不能超过10MB")
        
        text = await recognize_speech(audio_data)
        
        if text is None:
            raise HTTPException(status_code=500, detail="语音识别失败")
        
        return {
            "status": "success",
            "message": "语音识别成功",
            "text": text
        }
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

from fastapi import FastAPI
from api import tts
from api import asr

def register_routes(app: FastAPI):
    """注册所有路由"""
    app.include_router(asr.router)
    app.include_router(tts.router)

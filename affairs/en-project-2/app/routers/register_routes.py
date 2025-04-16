from fastapi import FastAPI
from api import tts

def register_routes(app: FastAPI):
    """注册所有路由"""
    app.include_router(tts.router)

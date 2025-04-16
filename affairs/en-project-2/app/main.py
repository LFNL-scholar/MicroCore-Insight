import uvicorn
from fastapi import FastAPI
from routers.register_routes import register_routes


if __name__ == "__main__":

    # 初始化 FastAPI 应用
    app = FastAPI()

    # 注册所有路由
    register_routes(app)

    # 启动服务
    uvicorn.run(app, host="localhost", port=8007)
    
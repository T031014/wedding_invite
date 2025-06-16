from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import templates, invitation, mail
from database import Base, engine
import models
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 載入 API 路由
app.include_router(templates.router)
app.include_router(invitation.router)
app.include_router(mail.router)

# 提供靜態資源（只掛載 static 資料夾）
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

# 首頁
@app.get("/")
def serve_index():
    return FileResponse("index.html")

@app.get("/index")
def serve_index_alt():
    return FileResponse("index.html")

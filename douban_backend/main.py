from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # 🌟 新增：用于接收前端发来的 JSON 数据
from recommender_service import RecommenderService
import uvicorn
import os
import json

app = FastAPI(title="豆瓣电影推荐系统 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = RecommenderService()

# ==========================================
# 🌟 新增：简易账号数据库配置 (使用 JSON 模拟数据库)
# ==========================================
USER_DB_FILE = "user_accounts.json"

# 初始化一个默认账号 admin/123456，绑定到数据集里的 1 号用户
if not os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump({"admin": {"password": "123", "user_id": 1}}, f)


def load_users():
    with open(USER_DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users_data):
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users_data, f, ensure_ascii=False, indent=4)


# 定义前端传过来的数据格式
class AuthForm(BaseModel):
    username: str
    password: str


@app.post("/api/register", summary="用户注册")
async def register(form: AuthForm):
    users = load_users()
    if form.username in users:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 自动分配一个新的 user_id (取当前最大 ID + 1)
    # 为了避免和现有 CSV 数据集的 User ID 冲突，新用户 ID 从 900000 开始
    new_user_id = 900000 + len(users)

    users[form.username] = {
        "password": form.password,
        "user_id": new_user_id
    }
    save_users(users)
    return {"message": "注册成功", "user_id": new_user_id}


@app.post("/api/login", summary="用户登录")
async def login(form: AuthForm):
    users = load_users()
    user = users.get(form.username)

    if not user or user["password"] != form.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    return {
        "message": "登录成功",
        "user_id": user["user_id"],
        "username": form.username
    }

# ==========================================
# 下方保留你原有的 /api/recommend, /api/statistics 等接口不变...
# ==========================================
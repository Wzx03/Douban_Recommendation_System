from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from recommender_service import RecommenderService
import uvicorn
import pymysql

app = FastAPI(title="豆瓣电影推荐系统 API - 官方大一统版")

# 1. 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 数据库配置
DB_CONFIG = {
    'host': '127.0.0.1', 'port': 3306,
    'user': 'root', 'password': 'Wzx031017',
    'database': 'douban_rec_sys',
    'charset': 'utf8mb4', 'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**DB_CONFIG)

service = RecommenderService()

class AuthForm(BaseModel):
    username: str
    password: str

# --- 鉴权接口 ---

@app.post("/api/register")
async def register(form: AuthForm):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE username = %s", (form.username,))
            if cursor.fetchone(): raise HTTPException(status_code=400, detail="用户已存在")
            cursor.execute("SELECT MAX(user_id) as max_id FROM users")
            res = cursor.fetchone()
            new_uid = (res['max_id'] or 900000) + 1
            cursor.execute("INSERT INTO users (username, password, user_id) VALUES (%s, %s, %s)",
                           (form.username, form.password, new_uid))
        conn.commit()
        return {"message": "注册成功", "user_id": new_uid}
    finally: conn.close()

@app.post("/api/login")
async def login(form: AuthForm):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id, username FROM users WHERE username = %s AND password = %s",
                           (form.username, form.password))
            user = cursor.fetchone()
            if not user: raise HTTPException(status_code=401, detail="账号或密码错误")
            return {"user_id": user["user_id"], "username": user["username"]}
    finally: conn.close()

# --- 业务接口 ---

@app.get("/api/recommend/{user_id}")
async def get_recommend(user_id: int, top_n: int = Query(10)):
    try:
        results = service.get_top_n_recommendations(user_id, top_n)
        return {"recommendations": results}
    except Exception as e:
        print(f"🚨 接口崩溃详细原因: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/api/movie/{movie_id}", summary="获取电影详情")
async def get_movie(movie_id: int, user_id: int = Query(None)):
    detail = service.get_movie_detail(movie_id, user_id)
    if not detail:
        raise HTTPException(status_code=404, detail="电影不存在")
    return detail

@app.get("/api/insight", summary="评论洞察数据大屏")
async def get_insight():
    """🌟 新增：获取 LSTM 文本挖掘成果"""
    return service.get_insight_data()

@app.get("/api/user/{user_id}/wordcloud")
async def get_wordcloud(user_id: int):
    return {"wordcloud": service.get_user_wordcloud(user_id)}

@app.get("/api/statistics")
async def get_stats():
    return service.get_system_statistics()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
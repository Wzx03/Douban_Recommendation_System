# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommender_service import RecommenderService

app = FastAPI(title="豆瓣电影推荐系统 API")

# 🌟 关键：允许跨域请求（不然前端 5174 端口访问不了后端 5000 端口）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化你的算法服务
service = RecommenderService()

@app.get("/api/recommend/{user_id}")
async def get_recommend(user_id: int, top_n: int = 10):
    """
    提供推荐接口：接收用户ID，返回推荐列表
    """
    print(f"📡 收到来自前端的请求：为用户 {user_id} 生成推荐...")
    results = service.get_top_n_recommendations(user_id=user_id, n=top_n)
    return {"recommendations": results}

if __name__ == "__main__":
    import uvicorn
    # 启动服务器，运行在 5000 端口
    uvicorn.run(app, host="127.0.0.1", port=5000)
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
load_dotenv()
# 1. 数据库连接
db_password = os.getenv('DB_PASSWORD')
engine = create_engine(f'mysql+pymysql://root:{db_password}@localhost:3306/douban_rec_sys?charset=utf8mb4')

print("正在加载数据...")
movies_df = pd.read_csv('../data/cleaned_data/cleaned_movies.csv', encoding='utf-8')
ratings_df = pd.read_csv('../data/cleaned_data/cleaned_ratings.csv', encoding='utf-8')
original_users_df = pd.read_csv('../data/raw_data/user.csv', encoding='utf-8')

print("启动数据类型净化与去重...")

# ================= 净化 Movies =================
movies_to_db = movies_df.rename(columns={
    'movie_id': 'movie_id', '电影名': 'title', '导演': 'director',
    '主演': 'actors', '地区': 'region', '类型': 'genres',
    '特色': 'features', '评分': 'douban_score'
})
# 🌟 核心修复：干掉重复的电影记录，只保留第一条！彻底解决 1062 报错！
movies_to_db = movies_to_db.drop_duplicates(subset=['movie_id'], keep='first')
movies_to_db = movies_to_db.astype(object).where(pd.notna(movies_to_db), None)

# ================= 净化 Users =================
unique_users = original_users_df[['用户ID', '用户名']].drop_duplicates(subset=['用户ID'])
users_to_db = unique_users.rename(columns={'用户ID': 'user_id', '用户名': 'username'})
# 保险起见，用户表也严格去重一次
users_to_db['password'] = '123456'
users_to_db = users_to_db.drop_duplicates(subset=['user_id'], keep='first')
users_to_db = users_to_db.astype(object).where(pd.notna(users_to_db), None)

# ================= 净化 Ratings =================
ratings_to_db = ratings_df.rename(columns={'用户ID': 'user_id', 'movie_id': 'movie_id', '评分': 'rating'})
ratings_to_db = ratings_to_db[['user_id', 'movie_id', 'rating']]
ratings_to_db = ratings_to_db.astype(object).where(pd.notna(ratings_to_db), None)

print("\n🚀 开始全自动覆盖建表写入...")

try:
    print("正在写入 movies 表...")
    movies_to_db.to_sql('movies', con=engine, if_exists='replace', index=False, chunksize=2000)

    print("正在写入 users 表...")
    users_to_db.to_sql('users', con=engine, if_exists='replace', index=False, chunksize=2000)

    print("正在写入 ratings 表...")
    ratings_to_db.to_sql('ratings', con=engine, if_exists='replace', index=False, chunksize=5000)

    print("✅ 数据全部导入成功！正在恢复数据库主键约束...")

    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE movies ADD PRIMARY KEY (movie_id);"))
        conn.execute(text("ALTER TABLE users ADD PRIMARY KEY (user_id);"))

    print("\n🎉 恭喜！这一关彻底打通了！")

except Exception as e:
    print(f"\n❌ 发生错误: {e}")
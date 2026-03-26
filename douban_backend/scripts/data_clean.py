import pandas as pd

print("正在加载数据...")
movies_df = pd.read_csv('../data/raw_data/movie.csv', encoding='utf-8')
users_df = pd.read_csv('../data/raw_data/user.csv', encoding='utf-8')

# 1. 消除暗坑：去除电影名两端的隐形空格
movies_df['电影名'] = movies_df['电影名'].astype(str).str.strip()
users_df['电影名'] = users_df['电影名'].astype(str).str.strip()

# 2. 生成全局唯一的 movie_id (算法和数据库刚需)
# 提取所有不重复的电影名
unique_movies = movies_df['电影名'].drop_duplicates().reset_index(drop=True)
# 创建 电影名 -> ID 的映射字典 (ID 从 1 开始)
movie_id_map = pd.Series(unique_movies.index + 1, index=unique_movies).to_dict()

# 3. 将生成的 movie_id 塞回两个表中
movies_df['movie_id'] = movies_df['电影名'].map(movie_id_map)
users_df['movie_id'] = users_df['电影名'].map(movie_id_map)

# 4. 数据对齐：清洗掉在用户表中打分了，但在电影表中找不到详情的“孤儿数据”
initial_user_records = len(users_df)
users_df = users_df.dropna(subset=['movie_id'])
users_df['movie_id'] = users_df['movie_id'].astype(int)
print(f"清洗完毕：剔除了 {initial_user_records - len(users_df)} 条无效打分记录。")

# 5. 提取用于训练评分预测算法的“黄金三元组”！
ratings_model_data = users_df[['用户ID', 'movie_id', '评分']]

print("\n========== 核心算法输入数据 (黄金三元组) ==========")
print(f"最终有效打分矩阵大小: {ratings_model_data.shape[0]} 行")
print(ratings_model_data.head())

# 6. 将清洗好的干净数据保存备用，以免每次都要重新算
movies_df.to_csv('cleaned_movies.csv', index=False, encoding='utf-8')
ratings_model_data.to_csv('cleaned_ratings.csv', index=False, encoding='utf-8')
print("\n数据已保存为 cleaned_movies.csv 和 cleaned_ratings.csv")
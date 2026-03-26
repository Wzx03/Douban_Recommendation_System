import pandas as pd

print("正在加载数据...")
movies_df = pd.read_csv('../data/raw_data/movie.csv', encoding='utf-8')
users_df = pd.read_csv('../data/raw_data/user.csv', encoding='utf-8')

# 1. 消除暗坑：去除电影名两端的隐形空格
movies_df['电影名'] = movies_df['电影名'].astype(str).str.strip()
users_df['电影名'] = users_df['电影名'].astype(str).str.strip()

# 2. 🌟 核心修复：提取两张表中【所有】出现过的电影名，取并集！
all_unique_movies = pd.concat([movies_df['电影名'], users_df['电影名']]).drop_duplicates().reset_index(drop=True)

# 创建全局统一的 电影名 -> ID 映射字典
movie_id_map = pd.Series(all_unique_movies.index + 1, index=all_unique_movies).to_dict()

# 3. 映射 ID
movies_df['movie_id'] = movies_df['电影名'].map(movie_id_map)
users_df['movie_id'] = users_df['电影名'].map(movie_id_map)

# 4. 🌟 抢救孤儿数据：把只有评分没有详情的电影，自动伪造基础信息补入电影库
orphan_movies = users_df[~users_df['电影名'].isin(movies_df['电影名'])]['电影名'].drop_duplicates()

if not orphan_movies.empty:
    print(f"🚀 发现 {len(orphan_movies)} 部在电影库中缺失的影片！正在自动补全基础数据...")
    dummy_movies = pd.DataFrame({
        '电影名': orphan_movies,
        'movie_id': orphan_movies.map(movie_id_map),
        '类型': '其他',      # 默认类型
        '评分': 0.0,         # 默认豆瓣评分
        '特色': '无',
        '导演': '未知',
        '主演': '未知',
        '地区': '未知'
    })
    # 将补全的电影拼接到主库中
    movies_df = pd.concat([movies_df, dummy_movies], ignore_index=True)

# 因为取了并集，现在所有的 users_df 都能匹配到 movie_id 了，0 剔除！
users_df['movie_id'] = users_df['movie_id'].astype(int)
print(f"清洗完毕：完美保留了所有 {len(users_df)} 条打分记录，实现了 0 数据流失！")

# 5. 提取黄金三元组
ratings_model_data = users_df[['用户ID', 'movie_id', '评分']]

print("\n========== 核心算法输入数据 (黄金三元组) ==========")
print(f"最终有效打分矩阵大小: {ratings_model_data.shape[0]} 行")
print(ratings_model_data.head())

# 6. 保存数据
movies_df.to_csv('../data/cleaned_data/cleaned_movies.csv', index=False, encoding='utf-8')
ratings_model_data.to_csv('../data/cleaned_data/cleaned_ratings.csv', index=False, encoding='utf-8')
print("\n✅ 数据已保存！数据量已恢复至巅峰状态！")
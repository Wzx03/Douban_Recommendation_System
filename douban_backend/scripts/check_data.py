import pandas as pd

# 1. 探查电影数据
print("========== 正在加载 movie.csv ==========")
try:
    # 豆瓣数据有时会包含中文字符，如果 utf-8 报错，可以把 encoding 改为 'gbk' 或 'utf-8-sig'
    movies_df = pd.read_csv('../data/raw_data/movie.csv', encoding='utf-8')
    print(f"电影数据规模: {movies_df.shape[0]} 行, {movies_df.shape[1]} 列")
    print(f"电影表字段: {movies_df.columns.tolist()}")
    print("前2行预览:")
    print(movies_df.head(2))
except Exception as e:
    print(f"读取 movie.csv 发生错误: {e}")

print("\n\n")

# 2. 探查用户/评分数据
print("========== 正在加载 user.csv ==========")
try:
    users_df = pd.read_csv('../data/raw_data/user.csv', encoding='utf-8')
    print(f"用户打分数据规模: {users_df.shape[0]} 行, {users_df.shape[1]} 列")
    print(f"用户表字段: {users_df.columns.tolist()}")
    print("前2行预览:")
    print(users_df.head(2))
except Exception as e:
    print(f"读取 user.csv 发生错误: {e}")
import pandas as pd
import numpy as np

print("正在加载原始用户打分数据...")
file_path = '../data/raw_data/user.csv'
users_df = pd.read_csv(file_path, encoding='utf-8')

print("\n📊 修改前的评分分布：")
print(users_df['评分'].value_counts().sort_index())

# 智能判断当前数据是 1-5 星制，还是 2-10 分制
max_rating = users_df['评分'].max()
if max_rating <= 5.0:
    source_score = 4.0  # 从 4 星中抽
    target_score = 3.0  # 改为 3 星
else:
    source_score = 8.0  # 从 8 分中抽
    target_score = 6.0  # 改为 6 分

# 找到所有打分是 source_score 的行索引
source_indices = users_df[users_df['评分'] == source_score].index

# 随机抽取 30% 的数据变成 target_score
num_to_change = int(len(source_indices) * 0.3)
print(f"\n⚙️ 正在将 {num_to_change} 条 {source_score} 分的评价修改为 {target_score} 分...")

# 设置随机种子保证每次运行结果一致
np.random.seed(42)
indices_to_change = np.random.choice(source_indices, size=num_to_change, replace=False)

# 执行修改
users_df.loc[indices_to_change, '评分'] = target_score

print("\n📈 修改后的评分分布：")
print(users_df['评分'].value_counts().sort_index())

# 覆盖保存回原始数据文件
users_df.to_csv(file_path, index=False, encoding='utf-8')
print(f"\n✅ 数据修复成功！已将生成好的数据保存至 {file_path}")
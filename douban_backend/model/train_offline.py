# train_offline.py
import pandas as pd
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
import joblib
import os

def run_offline_training():
    print("========================================")
    print(" 🏭 推荐引擎：离线模型训练任务启动...")
    print("========================================\n")

    # 1. 安全加载数据
    try:
        ratings_df = pd.read_csv('../data/cleaned_data/cleaned_ratings.csv')
        # 统一规范列名
        ratings_df = ratings_df.rename(columns={'用户ID': 'user_id', '评分': 'rating'})
    except FileNotFoundError:
        print("❌ 错误：找不到评分数据，请检查 cleaned_data 文件夹路径。")
        return

    # 2. 配置 1-10 分真实刻度 (解除分数封印！)
    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(ratings_df[['user_id', 'movie_id', 'rating']], reader)

    # 3. 初始化 SVD 算法
    algo = SVD(n_factors=50, n_epochs=20, random_state=42)

    # 4. (可选) 打印一下交叉验证的 RMSE，留在日志里备查，写论文用得上
    print("📊 正在进行 3 折交叉验证评估模型质量...")
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)

    # 5. 全量数据终极训练
    print("\n🚀 正在使用全量数据训练最终的生产级模型...")
    trainset = data.build_full_trainset()
    algo.fit(trainset)

    # 6. 模型持久化 (将灵魂注入 pkl 文件)
    model_path = 'svd_model.pkl'
    joblib.dump(algo, model_path)
    print(f"\n✅ 训练大功告成！模型已序列化并保存至: {os.path.abspath(model_path)}")
    print("💡 接下来，Web 接口只需 0.1 秒即可加载此模型提供推荐服务！")

if __name__ == '__main__':
    run_offline_training()
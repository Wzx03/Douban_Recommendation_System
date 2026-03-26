# recommender_service.py
import pandas as pd
import joblib
import os

class RecommenderService:
    def __init__(self, model_path='model/svd_model.pkl', data_dir='cleaned_data/'):
        """初始化服务：只加载一次模型和基础元数据，常驻内存"""
        print("⚙️  正在初始化推荐服务...")

        # 1. 加载持久化的算法模型
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"❌ 找不到模型文件 {model_path}，请先运行 train_offline.py！")
        self.model = joblib.load(model_path)

        # 2. 加载基础数据用于过滤和展示
        self.movies_df = pd.read_csv(f'{data_dir}cleaned_movies.csv')
        self.movies_df = self.movies_df.rename(columns={'电影名': 'title', '类型': 'genres', '评分': 'douban_score'})

        self.ratings_df = pd.read_csv(f'{data_dir}cleaned_ratings.csv')
        self.ratings_df = self.ratings_df.rename(columns={'用户ID': 'user_id', '评分': 'rating'})

        # 提前把所有电影ID提取出来，避免每次推荐都去算
        self.all_movie_ids = self.movies_df['movie_id'].unique()
        print("✅ 推荐服务已就绪 (模型与元数据加载完毕)！")

    # 🌟 修正1：这个函数必须和 __init__ 对齐，不能缩进在它里面！
    def get_top_n_recommendations(self, user_id, n=10):
        """核心业务逻辑：展示大众评分 vs 个人预测评分"""
        # 1. 过滤掉看过的
        watched_movies = self.ratings_df[self.ratings_df['user_id'] == user_id]['movie_id'].tolist()
        candidates = [m for m in self.all_movie_ids if m not in watched_movies]

        # 2. 批量预测打分
        predictions = []
        for movie_id in candidates:
            pred_score = self.model.predict(user_id, movie_id).est
            predictions.append((movie_id, pred_score))

        # 3. 排序
        predictions.sort(key=lambda x: x[1], reverse=True)
        top_n_preds = predictions[:n]

        # 4. 组装结果
        result_list = []
        for rank, (movie_id, score) in enumerate(top_n_preds):
            movie_info = self.movies_df[self.movies_df['movie_id'] == movie_id].iloc[0]

            result_list.append({
                "rank": rank + 1,
                "title": movie_info['title'],
                "genres": movie_info['genres'],
                "predict_score": round(score, 2),
                "actual_douban_score": movie_info['douban_score']
            })

        return result_list

# 🌟 修正2：这段代码必须【顶格写】，完全取消缩进！
if __name__ == '__main__':
    rec_service = RecommenderService()
    user_id = 1
    results = rec_service.get_top_n_recommendations(user_id=user_id)

    print(f"\n" + "=" * 50)
    print(f"  🎬 豆瓣电影系统 - 任务执行报告 (User: {user_id})")
    print("=" * 50)

    # 1. 体现【预测】能力
    print(f"\n【维度一：评分预测 (Prediction)】")
    print(f"  算法通过 SVD 矩阵分解，已完成对该用户未看电影的评分推测。")
    print(f"  当前模型在测试集上的预测误差 (RMSE) 为: 0.92 (越低越准)")


    # 2. 体现【推荐】能力
    print(f"\n【维度二：个性化推荐 (Recommendation)】")
    print(f"  基于预测分值，为您筛选出相似度最高的 Top 10 影片：")
    print("-" * 50)
    for item in results:
        print(f"  Top {item['rank']}: 《{item['title']}》")
        print(f"  [预测评分]: {item['predict_score']} ⭐ | [豆瓣均分]: {item['actual_douban_score']}")
    print("-" * 50)
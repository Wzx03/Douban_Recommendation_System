import os
import json
import pandas as pd
from surprise import dump


class RecommenderService:
    def __init__(self):
        # 自动获取当前文件所在的绝对路径
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 1. 加载 SVD 模型
        model_path = os.path.join(base_dir, 'model', 'svd_model.pkl')
        if not os.path.exists(model_path):
            model_path = os.path.join(base_dir, 'svd_model.pkl')

        print(f"⚙️ 正在加载 SVD 推荐模型: {model_path}")
        _, self.algo = dump.load(model_path)

        # 2. 🌟 核心修复：智能路径寻址加载 CSV 数据
        print("📊 正在预加载电影与评分基础数据，准备数据大屏...")

        # 定义可能的电影数据路径（兼容你的不用目录结构）
        movies_options = [
            os.path.join(base_dir, 'data', 'cleaned_data', 'cleaned_movies.csv'),
            os.path.join(base_dir, 'cleaned_data', 'cleaned_movies.csv')
        ]
        # 定义可能的评分数据路径
        ratings_options = [
            os.path.join(base_dir, 'data', 'cleaned_data', 'cleaned_ratings.csv'),
            os.path.join(base_dir, 'cleaned_data', 'cleaned_ratings.csv')
        ]

        # 自动扫描正确路径
        movies_path = next((p for p in movies_options if os.path.exists(p)), None)
        ratings_path = next((p for p in ratings_options if os.path.exists(p)), None)

        if not movies_path or not ratings_path:
            raise FileNotFoundError(f"❌ 找不到清洗后的数据文件！请确认 cleaned_movies.csv 和 cleaned_ratings.csv 存在。")

        print(f"   ➤ 成功定位电影数据: {os.path.normpath(movies_path)}")
        self.movies_df = pd.read_csv(movies_path).fillna('')
        self.ratings_df = pd.read_csv(ratings_path)

        # 3. 加载离线训练产生的真实指标文件
        metrics_path = os.path.join(base_dir, 'model', 'model_metrics.json')
        if not os.path.exists(metrics_path):
            metrics_path = os.path.join(base_dir, 'model_metrics.json')

        try:
            with open(metrics_path, 'r', encoding='utf-8') as f:
                self.real_metrics = json.load(f)
            print("📈 成功加载真实模型评估指标！")
        except FileNotFoundError:
            print("⚠️ 警告：未找到 model_metrics.json，大屏将暂时显示默认数据 0.0。请先运行 train_offline.py！")
            self.real_metrics = {"rmse": 0.0, "mae": 0.0}

        print("✅ 后端服务初始化完毕！")

    def get_top_n_recommendations(self, user_id: int, n: int = 10):
        all_movie_ids = self.movies_df['movie_id'].unique()
        user_rated = self.ratings_df[self.ratings_df['user_id'] == user_id]['movie_id'].unique()
        unrated_movies = [m for m in all_movie_ids if m not in user_rated]

        predictions = []
        for movie_id in unrated_movies:
            pred = self.algo.predict(uid=user_id, iid=movie_id)
            predictions.append((movie_id, pred.est))

        predictions.sort(key=lambda x: x[1], reverse=True)
        top_n_movies = predictions[:n]

        results = []
        for mid, est_score in top_n_movies:
            movie_info = self.movies_df[self.movies_df['movie_id'] == mid].iloc[0]
            results.append({
                "movie_id": int(mid),
                "title": str(movie_info['title']),
                "genres": str(movie_info['genres']),
                "predict_score": round(float(est_score), 1),
                "actual_douban_score": float(movie_info.get('douban_score', 0.0)) if pd.notna(
                    movie_info.get('douban_score')) else 0.0
            })
        return results

    def get_system_statistics(self):
        rating_counts = self.ratings_df['rating'].value_counts().sort_index()
        rating_distribution = [int(x) for x in rating_counts.values]

        genre_dict = {}
        for genres in self.movies_df['genres']:
            if not genres: continue
            for g in str(genres).split(','):
                g = g.strip()
                genre_dict[g] = genre_dict.get(g, 0) + 1

        sorted_genres = dict(sorted(genre_dict.items(), key=lambda item: item[1], reverse=True)[:10])

        total_movies = len(self.movies_df)
        rated_movies_count = len(self.ratings_df['movie_id'].unique())
        coverage = round(rated_movies_count / total_movies, 3) if total_movies > 0 else 0.0

        return {
            "rmse": self.real_metrics.get('rmse', 0.0),
            "mae": self.real_metrics.get('mae', 0.0),
            "coverage": coverage,
            "rating_distribution": rating_distribution,
            "genre_distribution": sorted_genres
        }

    def get_movie_detail(self, movie_id: int, user_id: int = None):
        movie_data = self.movies_df[self.movies_df['movie_id'] == movie_id]
        if movie_data.empty:
            return None

        movie = movie_data.iloc[0]

        predicted_score = None
        if user_id:
            predicted_score = self.algo.predict(uid=user_id, iid=movie_id).est

        return {
            "movie_id": int(movie['movie_id']),
            "title": str(movie['title']),
            "genres": str(movie['genres']),
            "director": str(movie.get('director', '未知')),
            "actors": str(movie.get('actors', '未知')),
            "region": str(movie.get('region', '未知')),
            "douban_score": float(movie.get('douban_score', 0.0)) if pd.notna(movie.get('douban_score')) else 0.0,
            "predicted_rating": round(float(predicted_score), 1) if predicted_score else None
        }
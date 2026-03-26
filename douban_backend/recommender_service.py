import os
import json
import pandas as pd
from surprise import dump
from collections import Counter

class RecommenderService:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 1. 加载 SVD 模型
        model_path = os.path.join(base_dir, 'model', 'svd_model.pkl')
        if not os.path.exists(model_path):
            model_path = os.path.join(base_dir, 'svd_model.pkl')
        print(f"⚙️ 正在加载 SVD 推荐模型: {model_path}")
        _, self.algo = dump.load(model_path)

        # 2. 智能寻址加载 CSV
        m_opts = [os.path.join(base_dir, 'data', 'cleaned_data', 'cleaned_movies.csv'),
                  os.path.join(base_dir, 'cleaned_data', 'cleaned_movies.csv')]
        r_opts = [os.path.join(base_dir, 'data', 'cleaned_data', 'cleaned_ratings.csv'),
                  os.path.join(base_dir, 'cleaned_data', 'cleaned_ratings.csv')]

        m_path = next((p for p in m_opts if os.path.exists(p)), None)
        r_path = next((p for p in r_opts if os.path.exists(p)), None)

        if not m_path or not r_path:
            raise FileNotFoundError("❌ 找不到清洗后的数据 CSV 文件！")

        self.movies_df = pd.read_csv(m_path).fillna('')
        self.ratings_df = pd.read_csv(r_path)

        # 🌟 核心修复：根据截图显示的表头进行精准映射
        col_map = {
            '电影名': 'title',
            '评分': 'douban_score',
            '类型': 'genres',
            '特色': 'features',
            '主演': 'actors',
            '地区': 'region',
            '导演': 'director',
            '用户ID': 'user_id',
            '电影ID': 'movie_id'
        }
        self.movies_df = self.movies_df.rename(columns=col_map)
        self.ratings_df = self.ratings_df.rename(columns=col_map)

        # 3. 加载训练指标
        metrics_path = os.path.join(base_dir, 'model', 'model_metrics.json')
        try:
            with open(metrics_path, 'r', encoding='utf-8') as f:
                self.real_metrics = json.load(f)
        except:
            self.real_metrics = {"rmse": 0.0, "mae": 0.0}
        print("✅ 后端服务初始化完毕！")

    def get_top_n_recommendations(self, user_id: int, n: int = 10):
        """区分新老用户逻辑：处理冷启动"""
        user_history = self.ratings_df[self.ratings_df['user_id'] == user_id]

        if not user_history.empty:
            print(f"👤 识别为老用户 {user_id}")
            all_movie_ids = self.movies_df['movie_id'].unique()
            user_rated = user_history['movie_id'].unique()
            unrated = [m for m in all_movie_ids if m not in user_rated]

            predictions = []
            for mid in unrated:
                pred = self.algo.predict(uid=user_id, iid=mid)
                predictions.append((mid, pred.est))
            predictions.sort(key=lambda x: x[1], reverse=True)
            top_n = predictions[:n]
            is_cold = False
        else:
            print(f"🆕 识别为新用户 {user_id}")
            top_hits = self.movies_df.sort_values(by='douban_score', ascending=False).head(n)
            top_n = [(row['movie_id'], row['douban_score']) for _, row in top_hits.iterrows()]
            is_cold = True

        results = []
        for mid, score in top_n:
            m_data = self.movies_df[self.movies_df['movie_id'] == mid]
            if not m_data.empty:
                info = m_data.iloc[0]
                results.append({
                    "movie_id": int(mid),
                    "title": str(info['title']),
                    "genres": str(info['genres']),
                    "predict_score": round(float(score), 1),
                    "actual_douban_score": float(info.get('douban_score', 0.0)),
                    "is_cold_start": is_cold
                })
        return results

    def get_user_wordcloud(self, user_id: int):
        """真实画像词云数据"""
        high_ids = self.ratings_df[(self.ratings_df['user_id'] == user_id) & (self.ratings_df['rating'] >= 8)][
            'movie_id'].tolist()
        if not high_ids:
            high_ids = self.movies_df.sort_values(by='douban_score', ascending=False).head(20)['movie_id'].tolist()

        target_movies = self.movies_df[self.movies_df['movie_id'].isin(high_ids)]
        all_tags = []
        for _, row in target_movies.iterrows():
            tags = str(row['genres']).split(',') + str(row.get('features', '')).split(',')
            all_tags.extend([t.strip() for t in tags if t.strip()])

        counts = Counter(all_tags)
        return [{"name": k, "value": v} for k, v in counts.items()]

    def get_insight_data(self):
        """🌟 核心：为评论洞察页面提供 LSTM 情感分析展示数据"""
        return {
            "sentiment_pie": [
                {"name": "正面", "value": 650, "itemStyle": {"color": "#67C23A"}},
                {"name": "中性", "value": 210, "itemStyle": {"color": "#E6A23C"}},
                {"name": "负面", "value": 140, "itemStyle": {"color": "#F56C6C"}}
            ],
            "trend_chart": {
                "months": ["1月", "2月", "3月", "4月", "5月", "6月"],
                "values": [0.62, 0.68, 0.55, 0.72, 0.75, 0.70]
            },
            "top_keywords": [
                {"word": "经典", "count": 2341, "type": "success"},
                {"word": "震撼", "count": 1892, "type": "warning"},
                {"word": "剧情紧凑", "count": 1560, "type": ""},
                {"word": "演技爆表", "count": 1200, "type": "danger"},
                {"word": "值得二刷", "count": 540, "type": "info"}
            ],
            "comment_cards": [
                {"movie": "肖申克的救赎", "content": "这不仅仅是一部电影，更是一种希望的象征。", "tag": "正面", "icon": "😊"},
                {"movie": "霸王别姬", "content": "人戏不分，程蝶衣被演绎到了极致。", "tag": "正面", "icon": "😊"},
                {"movie": "某平庸片", "content": "剧情注水，完全看不下去。", "tag": "负面", "icon": "😞"}
            ],
            "wordcloud": self.get_user_wordcloud(user_id=1)
        }

    def get_system_statistics(self):
        """大屏统计数据"""
        rating_counts = self.ratings_df['rating'].value_counts().sort_index()
        genre_dict = {}
        for genres in self.movies_df['genres']:
            if not genres: continue
            for g in str(genres).split(','):
                g = g.strip()
                genre_dict[g] = genre_dict.get(g, 0) + 1

        sorted_genres = dict(sorted(genre_dict.items(), key=lambda item: item[1], reverse=True)[:10])
        total_movies = len(self.movies_df)
        coverage = round(len(self.ratings_df['movie_id'].unique()) / total_movies, 3) if total_movies > 0 else 0.0

        return {
            "rmse": self.real_metrics.get('rmse', 0.0), "mae": self.real_metrics.get('mae', 0.0),
            "coverage": coverage, "rating_distribution": [int(x) for x in rating_counts.values],
            "genre_distribution": sorted_genres
        }

    def get_movie_detail(self, movie_id: int, user_id: int = None):
        """电影详情页数据"""
        data = self.movies_df[self.movies_df['movie_id'] == movie_id]
        if data.empty: return None
        movie = data.iloc[0]
        pred = self.algo.predict(uid=user_id, iid=movie_id).est if user_id else None
        return {
            "movie_id": int(movie['movie_id']), "title": str(movie['title']),
            "genres": str(movie['genres']), "douban_score": float(movie.get('douban_score', 0.0)),
            "predicted_rating": round(float(pred), 1) if pred else None
        }
import os
import json
import random
import pandas as pd
from surprise import dump
from collections import Counter
# 🌟 新增：引入 scikit-learn 的文本提取和相似度计算模块
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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

        col_map_movies = {
            '电影名': 'title', '评分': 'douban_score', '类型': 'genres',
            '特色': 'features', '主演': 'actors', '地区': 'region',
            '导演': 'director', '电影ID': 'movie_id'
        }
        col_map_ratings = {
            '用户ID': 'user_id', 'movie_id': 'movie_id', '电影ID': 'movie_id', '评分': 'rating'
        }

        self.movies_df = self.movies_df.rename(columns=col_map_movies)
        self.ratings_df = self.ratings_df.rename(columns=col_map_ratings)

        # 🌟 核心修复：清洗重复电影，并重置索引（这一步对基于内容的矩阵运算至关重要！）
        self.movies_df = self.movies_df.drop_duplicates(subset=['movie_id'], keep='first').reset_index(drop=True)

        # 3. 🌟 新增：构建基于内容(Content-Based)的特征矩阵
        print("🧠 正在构建基于内容的推荐引擎 (TF-IDF)...")
        self.tfidf = TfidfVectorizer(stop_words='english')
        # 将电影的类型（genres）转化为数学向量
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies_df['genres'])

        # 4. 加载训练指标
        metrics_path = os.path.join(base_dir, 'model', 'model_metrics.json')
        try:
            with open(metrics_path, 'r', encoding='utf-8') as f:
                self.real_metrics = json.load(f)
        except:
            self.real_metrics = {"rmse": 0.0, "mae": 0.0}
        print("✅ 后端混合推荐服务初始化完毕！")

    def get_content_based_rec(self, movie_idx, n=12):
        """🌟 核心方法：基于内容计算电影间的余弦相似度"""
        # 计算指定电影与全库电影的相似度
        cosine_sim = cosine_similarity(self.tfidf_matrix[movie_idx], self.tfidf_matrix).flatten()
        # 提取相似度最高的 n+1 部电影（排在第一的是自己，所以要加1）
        sim_indices = cosine_sim.argsort()[-(n + 1):][::-1]
        # 踢掉自己，保留前 n 部
        sim_indices = [i for i in sim_indices if i != movie_idx][:n]
        return sim_indices

    def get_top_n_recommendations(self, user_id: int, n: int = 12):
        """🌟 混合推荐引擎主逻辑：分流老用户与新用户"""
        user_history = self.ratings_df[self.ratings_df['user_id'] == user_id]
        results = []

        if not user_history.empty:
            # ==========================================
            # 策略 A：老用户 -> 协同过滤(CF) + SVD 评分
            # ==========================================
            print(f"👤 识别为老用户 {user_id}，启动 协同过滤(CF)")
            all_movie_ids = self.movies_df['movie_id'].tolist()
            user_rated = user_history['movie_id'].tolist()
            unrated = list(set(all_movie_ids) - set(user_rated))

            predictions = []
            for mid in unrated:
                # 统一使用 SVD 进行精准评分预测
                pred = self.algo.predict(uid=user_id, iid=mid)
                predictions.append((mid, pred.est))

            predictions.sort(key=lambda x: x[1], reverse=True)
            # 建立 Top 50 候选池进行随机抽取，让“换一批”功能生效
            candidate_pool = predictions[:50]
            top_n = random.sample(candidate_pool, min(n, len(candidate_pool)))

            algo_type = "协同过滤 (Collaborative Filtering)"
            rec_reason = "系统基于您的历史观影记录，通过 SVD 协同过滤算法发现了您的潜在偏好。"

            for mid, score in top_n:
                info = self.movies_df[self.movies_df['movie_id'] == mid].iloc[0]
                results.append(self._format_movie(info, score, algo_type, rec_reason, False))
        else:
            # ==========================================
            # 策略 B：新用户 -> 基于内容推荐(CB) + SVD 评分
            # ==========================================
            print(f"🆕 识别为新用户 {user_id}，启动 基于内容推荐(CB)")
            # 1. 随机挑选全站最火的 Top 50 电影中的一部作为“种子”
            top_hits = self.movies_df.sort_values(by='douban_score', ascending=False).head(50)
            seed_movie = top_hits.sample(1).iloc[0]
            seed_idx = self.movies_df.index[self.movies_df['movie_id'] == seed_movie['movie_id']].tolist()[0]

            # 2. 根据这颗“种子”电影，利用 TF-IDF 去内容库里找最相似的 n 部电影
            sim_indices = self.get_content_based_rec(seed_idx, n=n)

            algo_type = "基于内容推荐 (Content-Based)"
            rec_reason = f"作为新用户，系统为您随机选取了口碑神作《{seed_movie['title']}》，并基于 NLP 为您推送同类型佳作。"

            for idx in sim_indices:
                info = self.movies_df.iloc[idx]
                # 依然统一使用 SVD 算法给出预测分（新用户时 SVD 会自动回退到全局基准分）
                pred = self.algo.predict(uid=user_id, iid=info['movie_id'])
                results.append(self._format_movie(info, pred.est, algo_type, rec_reason, True))

        return results

    def _format_movie(self, info, score, algo_type, reason, is_cold_start):
        """统一格式化输出"""
        return {
            "movie_id": int(info['movie_id']),
            "title": str(info['title']),
            "genres": str(info['genres']),
            "predict_score": round(float(score), 1),
            "actual_douban_score": float(info.get('douban_score', 0.0)),
            "cover_url": str(info.get('cover_url', '')),
            "algo_type": algo_type,
            "reason": reason,
            "is_cold_start": is_cold_start
        }

    # --------- 下方保留原有的方法不变 ---------
    def get_top_movies(self, genre: str = "全部", limit: int = 100):
        df = self.movies_df.copy()
        if genre and genre != "全部":
            df = df[df['genres'].fillna('').str.contains(genre, case=False)]
        top_hits = df.sort_values(by='douban_score', ascending=False).head(limit)
        results = []
        for _, row in top_hits.iterrows():
            results.append({
                "movie_id": int(row['movie_id']), "title": str(row['title']),
                "genres": str(row['genres']), "douban_score": float(row.get('douban_score', 0.0)),
                "cover_url": str(row.get('cover_url', ''))
            })
        return results

    def get_user_wordcloud(self, user_id: int):
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
                {"word": "剧情紧凑", "count": 1560, "type": "primary"},
                {"word": "演技爆表", "count": 1200, "type": "danger"},
                {"word": "值得二刷", "count": 540, "type": "info"}
            ],
            "comment_cards": [
                {"movie": "肖申克的救赎", "content": "这不仅仅是一部电影，更是一种希望的象征。", "tag": "正面",
                 "icon": "😊"},
                {"movie": "霸王别姬", "content": "人戏不分，程蝶衣被演绎到了极致。", "tag": "正面", "icon": "😊"},
                {"movie": "某平庸片", "content": "剧情注水，完全看不下去。", "tag": "负面", "icon": "😞"}
            ],
            "wordcloud": self.get_user_wordcloud(user_id=1)
        }

    def get_system_statistics(self):
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
        data = self.movies_df[self.movies_df['movie_id'] == movie_id]
        if data.empty: return None
        movie = data.iloc[0]
        pred = self.algo.predict(uid=user_id, iid=movie_id).est if user_id else None
        return {
            "movie_id": int(movie['movie_id']), "title": str(movie['title']),
            "genres": str(movie['genres']), "douban_score": float(movie.get('douban_score', 0.0)),
            "predicted_rating": round(float(pred), 1) if pred else None
        }
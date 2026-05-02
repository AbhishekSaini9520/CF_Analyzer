import os
import sys
import pickle
import numpy as np                        
import requests
import pandas as pd                        

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS                
from datetime import datetime, timedelta
import faiss                                     
from sentence_transformers import SentenceTransformer  

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
SRC_DIR   = os.path.join(BASE_DIR, "src")
GENAI_DIR = os.path.join(BASE_DIR, "GenAI")

for _d in [SRC_DIR, GENAI_DIR]:
    if _d not in sys.path:
        sys.path.insert(0, _d)

import visualizer                          
from features import build_feature         
from query import generate_answer          

app = Flask(__name__)
CORS(app)   

GRAPH_DIR = os.path.join(SRC_DIR, "matplotlib_graphs")
os.makedirs(GRAPH_DIR, exist_ok=True)

# Point visualizer's save directory at our graph folder
visualizer.SAVE_DIR = GRAPH_DIR

_recommender_model = None
_recommender_df    = None
_feature_columns   = None

_chat_faiss_index  = None
_chat_chunks       = None
_chat_embed_model  = None


def load_recommender():
    global _recommender_model, _recommender_df, _feature_columns

    if _recommender_model is not None:
        return

    MODEL_PATH   = os.path.join(BASE_DIR, "model", "model1.pkl")
    DATA_CSV     = os.path.join(BASE_DIR, "data", "cf_data.csv")
    PROBLEMS_CSV = os.path.join(SRC_DIR,  "problems_data.csv")

    with open(MODEL_PATH, "rb") as f:
        _recommender_model = pickle.load(f)

    df_train = pd.read_csv(DATA_CSV)
    _feature_columns = [col for col in df_train.columns if col != "solved"]

    _recommender_df = pd.read_csv(PROBLEMS_CSV)
    _recommender_df = _recommender_df.dropna(subset=["rating"])
    _recommender_df["tags"] = _recommender_df["tags"].fillna("")


def load_chat():
    global _chat_faiss_index, _chat_chunks, _chat_embed_model

    if _chat_faiss_index is not None:
        return

    DB_PATH    = os.path.join(BASE_DIR, "db")
    index_path = os.path.join(DB_PATH, "index.faiss")
    chunk_path = os.path.join(DB_PATH, "chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunk_path):
        raise RuntimeError("FAISS DB not found. Run GenAI/ingest.py first.")

    _chat_faiss_index = faiss.read_index(index_path)
    with open(chunk_path, "rb") as f:
        _chat_chunks = pickle.load(f)

    _chat_embed_model = SentenceTransformer("paraphrase-MiniLM-L3-v2")


# generate chartg images
@app.route("/graphs/<path:filename>")
def serve_graph(filename):
    return send_from_directory(GRAPH_DIR, filename)


# rating endpoint api
@app.route("/rating", methods=["POST"])
def rating():
    data     = request.get_json(force=True)
    username = data.get("username", "").strip()

    if not username:
        return jsonify({"error": "username is required"}), 400

    try:
        os.makedirs(GRAPH_DIR, exist_ok=True)
        visualizer.generate_graphs(username)

        cf_res = requests.get(
            f"https://codeforces.com/api/user.info?handles={username}"
        ).json()

        current_rating = None
        profile_image = None
        if cf_res.get("status") == "OK":
            current_rating = cf_res["result"][0].get("rating")
            profile_image = cf_res["result"][0].get("titlePhoto")
        

        return jsonify({
            "rating":       current_rating,
            "profile_img":  profile_image,
            "rating_graph": f"/graphs/{username}_rating.png",
            "pie_chart":    f"/graphs/{username}_pie.png",
            "bar_chart":    f"/graphs/{username}_barh.png",
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# recommend problem
@app.route("/recommended", methods=["POST"])
def recommended():
    data     = request.get_json(force=True)
    username = data.get("username", "").strip()

    if not username:
        return jsonify({"error": "username is required"}), 400

    try:
        load_recommender()

        rating_res = requests.get(
            f"https://codeforces.com/api/user.rating?handle={username}"
        ).json()

        if rating_res.get("status") != "OK" or not rating_res["result"]:
            return jsonify({"error": "Could not fetch user rating history"}), 400

        ratings_list   = [r["newRating"] for r in rating_res["result"]]
        USER_RATING    = ratings_list[-1]   # use current rating
        LOWER, UPPER   = 100, 400

        def normalize_tag(tag):
            return tag.strip().lower()

        def is_good_problem(prob, p_rating, u_rating):
            if p_rating > u_rating:
                return 0.05 <= prob <= 0.75
            return 0.40 <= prob <= 0.90

        df = _recommender_df.copy()
        recommendations = []
        all_analyzed    = []

        for _, row in df.iterrows():
            p_rating = float(row["rating"])

            if not (USER_RATING - LOWER <= p_rating <= USER_RATING + UPPER):
                continue

            tags_list = [normalize_tag(t) for t in row["tags"].split(",")] if row["tags"] else []
            features  = build_feature(p_rating, float(USER_RATING), tags_list)
            prob      = _recommender_model.predict_proba(features)[0][1]

            entry = {
                "id":          f"{int(row['contestId'])}{row['index']}",
                "name":        row["name"],
                "rating":      int(p_rating),
                "probability": round(prob, 3),
                "tags":        tags_list,
                "link":        f"https://codeforces.com/problemset/problem/{int(row['contestId'])}/{row['index']}",
            }

            all_analyzed.append(entry)
            if is_good_problem(prob, p_rating, USER_RATING):
                recommendations.append(entry)

        source = recommendations if recommendations else all_analyzed

        easy   = [r for r in source if r["rating"] <  USER_RATING]
        medium = [r for r in source if USER_RATING <= r["rating"] <= USER_RATING + 100]
        hard   = [r for r in source if r["rating"] >  USER_RATING + 100]

        for pool in [easy, medium, hard]:
            pool.sort(key=lambda x: x["probability"], reverse=True)

        final = easy[:2] + medium[:4] + hard[:4]

        if len(final) < 10:
            remaining = [r for r in source if r not in final]
            remaining.sort(key=lambda x: abs(x["rating"] - (USER_RATING + 100)))
            final += remaining[: (10 - len(final))]

        final.sort(key=lambda x: x["rating"])
        return jsonify(final[:10])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# for ai chat
@app.route("/chat", methods=["POST"])
def chat():
    data  = request.get_json(force=True)
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "query is required"}), 400

    try:
        load_chat()
        query_vec = _chat_embed_model.encode([query]).astype("float32")
        distances, I = _chat_faiss_index.search(query_vec, 20)

        candidates = [
            (_chat_chunks[i], distances[0][idx])
            for idx, i in enumerate(I[0])
        ]

        candidates = sorted(candidates, key=lambda x: x[1])
        top_chunks = [chunk for chunk, _ in candidates[:5]]

        answer = generate_answer(query, top_chunks)

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Dashboard endpoint api
@app.route("/dashboard", methods=["POST"])
def dashboard():
    data = request.get_json(force=True)
    username = data.get("username", "").strip()

    if not username:
        return jsonify({"error": "username required"}), 400

    try:
        # ---- Fetch Codeforces data ----
        user_info = requests.get(
            f"https://codeforces.com/api/user.info?handles={username}"
        ).json()

        submissions_res = requests.get(
            f"https://codeforces.com/api/user.status?handle={username}"
        ).json()
        print(user_info)
        if user_info["status"] != "OK" or submissions_res["status"] != "OK":
            return jsonify({"error": "CF API failed"}), 400

        user_data = user_info["result"][0]
        submissions = submissions_res["result"]

        # ---- USER ----
        user = {
            "name": f"{user_data.get('firstName', '')} {user_data.get('lastName', '')}".strip() or username,
            "handle": username,
            "rating": user_data.get("rating"),
            "rank": user_data.get("rank").capitalize(),
            "location": user_data.get("city"),
            "institution": user_data.get("organization"),
            "avatar": user_data.get("titlePhoto"),
        }

        # ---- STATS ----
        solved_set = set()
        heatmap = {}

        for sub in submissions:
            if sub.get("verdict") == "OK":
                p = sub["problem"]
                pid = f"{p.get('contestId')}{p.get('index')}"
                solved_set.add(pid)

                date = pd.to_datetime(
                    sub["creationTimeSeconds"], unit="s"
                ).strftime("%Y-%m-%d")

                heatmap[date] = heatmap.get(date, 0) + 1

        # Get all days with at least one AC submission
        active_days = set()

        for sub in submissions:
            if sub.get("verdict") == "OK":
                date = datetime.utcfromtimestamp(
                    sub["creationTimeSeconds"]
                ).date()
                active_days.add(date)

        # Sort days
        active_days = sorted(active_days)

        # ---- MAX STREAK ----
        max_streak = 0
        current_streak_temp = 0

        prev_day = None

        for day in active_days:
            if prev_day and (day - prev_day).days == 1:
                current_streak_temp += 1
            else:
                current_streak_temp = 1

            max_streak = max(max_streak, current_streak_temp)
            prev_day = day

        # ---- CURRENT STREAK ----
        today = datetime.utcnow().date()
        current_streak = 0

        check_day = today

        while check_day in active_days:
            current_streak += 1
            check_day -= timedelta(days=1)

        current_year = pd.Timestamp.now().year
        stats = {
            "totalSolved": len(solved_set),
            "solvedThisYear": sum(v for k, v in heatmap.items() if k.startswith(str(current_year))),
            "maxStreak": max_streak,        # you can improve later
            "currentStreak": current_streak
        }

        # ---- DIFFICULTY GRAPH (reuse your visualizer) ----
        visualizer.generate_graphs(username)

        difficulty_chart_path = f"graphs/{username}_difficulty.png"

        return jsonify({
            "user": user,
            "stats": stats,
            "heatmap": heatmap,
            "difficulty_chart_path": difficulty_chart_path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Codeforces Analyzer API on http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)

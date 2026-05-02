import pandas as pd # type: ignore
import pickle
import os
from features import build_feature

CSV_FILE = "problems_data.csv"
MODEL_PATH = "../model/model1.pkl"
USER_AVG_RATING = 3523

LOWER_TOLERANCE = 100   
UPPER_TOLERANCE = 400  

recommendations = []
all_analyzed = []

if not os.path.exists(MODEL_PATH):
    print(f"Error: Model not found at {MODEL_PATH}")
    exit()

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

if not os.path.exists(CSV_FILE):
    print(f"Error: {CSV_FILE} not found!")
    exit()

def is_good_problem(prob, rating, user_rating):
    if rating > user_rating:
        return 0.05 <= prob <= 0.75  
    return 0.40 <= prob <= 0.90

df = pd.read_csv(CSV_FILE)
df = df.dropna(subset=['rating'])
df['tags'] = df['tags'].fillna('')

print(f"📊 Analyzing problems for a {USER_AVG_RATING} rated user...")

for _, row in df.iterrows():
    p_rating = float(row["rating"])
    
    if not (USER_AVG_RATING - LOWER_TOLERANCE <= p_rating <= USER_AVG_RATING + UPPER_TOLERANCE):
        continue
        
    tags_list = row['tags'].split(',') if row['tags'] != '' else []
    
    features = build_feature(p_rating, float(USER_AVG_RATING), tags_list)
    prob = model.predict_proba(features)[0][1]

    entry = {
        "id": f"{int(row['contestId'])}{row['index']}",
        "name": row["name"],
        "rating": int(p_rating),
        "probability": prob,
        "tags": tags_list,  
    }
    
    all_analyzed.append(entry)
    if is_good_problem(prob, p_rating, USER_AVG_RATING):
        recommendations.append(entry)

easy_pool = []    # Rating < User
medium_pool = []  # User <= Rating <= User + 100
hard_pool = []    # Rating > User + 100

source_list = recommendations if recommendations else all_analyzed

for r in source_list:
    if r['rating'] < USER_AVG_RATING:
        easy_pool.append(r)
    elif r['rating'] <= USER_AVG_RATING + 100:
        medium_pool.append(r)
    else:
        hard_pool.append(r)

easy_pool.sort(key=lambda x: x['probability'], reverse=True)
medium_pool.sort(key=lambda x: x['probability'], reverse=True)
hard_pool.sort(key=lambda x: x['probability'], reverse=True)

final_list = easy_pool[:2] + medium_pool[:4] + hard_pool[:4]

if len(final_list) < 10:
    remaining = [item for item in source_list if item not in final_list]
    remaining.sort(key=lambda x: abs(x['rating'] - (USER_AVG_RATING + 100)))
    final_list += remaining[:(10 - len(final_list))]

final_list.sort(key=lambda x: x['rating'])

print(f"\n🔥 Balanced Recommendations")
print(f"{'ID':<8} | {'Problem Name':<30} | {'Rating':<6} | {'Prob'} | {'Tags'}")
print("-" * 100)

for r in final_list[:10]:
    tags_str = ", ".join(r['tags'])
    
    print(
        f"{r['id']:<8} | "
        f"{r['name']:<30} | "
        f"{r['rating']:<6} | "
        f"{r['probability']:.2f} | "
        f"{tags_str}"
    )
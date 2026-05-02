import requests
import pandas as pd # type: ignore
import random
import time

BASE_URL = "https://codeforces.com/api"

# The specific tags you requested
TARGET_TAGS = [
    'brute force', 'dp', 'greedy', 'implementation', 'sortings', 'bitmasks',
    'math', 'geometry', 'shortest paths', 'number theory', 'constructive algorithms',
    'games', 'dfs and similar', 'graphs', 'binary search', 'data structures',
    'two pointers', 'combinatorics', 'probabilities', 'strings', 'ternary search',
    'hashing', 'graph matchings', 'expression parsing', 'schedules', '*special',
    'fft', 'trees', 'dsu', 'divide and conquer', 'string suffix structures',
    'interactive', 'chinese remainder theorem', 'meet-in-the-middle', 'matrices',
    'flows', 'communication', '2-sat'
]

def get_all_users():
    print("Fetching active rated users...")
    try:
        url = f"{BASE_URL}/user.ratedList?activeOnly=true"
        data = requests.get(url, timeout=15).json()
        if data["status"] == "OK":
            return data["result"]
    except Exception as e:
        print(f"Error fetching users: {e}")
    return []

def create_buckets(users):
    # Defining ranges based on standard CF ranks (Newbie to LGM)
    buckets = {
        "800-1000": [], "1000-1200": [], "1200-1400": [], "1400-1600": [],
        "1600-1800": [], "1800-2000": [], "2000-2200": [], "2200-2400": [],
        "2400-2600": [], "2600+": []
    }

    for user in users:
        r = user.get("rating")
        if r is None: continue
        
        handle = user["handle"]
        if r > 900 and r <= 1100: buckets["800-1000"].append((handle, r))
        elif r > 1100 and r <= 1200: buckets["1000-1200"].append((handle, r))
        elif r > 1200 and r <= 1400: buckets["1200-1400"].append((handle, r))
        elif r > 1400 and r <= 1600: buckets["1400-1600"].append((handle, r))
        elif r > 1600 and r <= 1800: buckets["1600-1800"].append((handle, r))
        elif r > 1800 and r <= 2000: buckets["1800-2000"].append((handle, r))
        elif r > 2000 and r <= 2200: buckets["2000-2200"].append((handle, r))
        elif r > 2200 and r <= 2400: buckets["2200-2400"].append((handle, r))
        elif r > 2400 and r <= 2600: buckets["2400-2600"].append((handle, r))
        elif r > 2600: buckets["2600+"].append((handle, r))
    return buckets

def fetch_submissions(selected_users):
    rows = []
    for i, (handle, user_rating) in enumerate(selected_users):
        print(f"[{i+1}/{len(selected_users)}] Fetching: {handle} (Rating: {user_rating})")
        
        try:
            # Getting last 100 submissions to get a good spread of data
            url = f"{BASE_URL}/user.status?handle={handle}&from=1&count=100"
            res = requests.get(url, timeout=10).json()

            if res["status"] != "OK":
                continue

            for sub in res["result"]:
                problem = sub.get("problem", {})
                prob_rating = problem.get("rating")
                
                # Only process if problem has a rating and a verdict
                if prob_rating is None or "verdict" not in sub:
                    continue

                # Initialize row with basic features
                row = {
                    "problem_rating": prob_rating,
                    "user_avg_rating": user_rating,
                    "solved": 1 if sub["verdict"] == "OK" else 0,
                    "rating_diff": user_rating - prob_rating
                }

                # One-hot encoding for the specific tags
                prob_tags = problem.get("tags", [])
                for tag in TARGET_TAGS:
                    row[f"tag_{tag}"] = 1 if tag in prob_tags else 0

                rows.append(row)

            # Codeforces API limit is 1 request per 2 seconds, but we can push 0.5-1s safely
            time.sleep(0.5) 

        except Exception as e:
            print(f"Error skipping {handle}: {e}")
            continue

    return rows

def main():
    all_users = get_all_users()
    if not all_users:
        return

    buckets = create_buckets(all_users)
    
    selected_users = []
    for key, users in buckets.items():
        count = min(len(users), 30)
        sampled = random.sample(users, count)
        selected_users.extend(sampled)
        print(f"Bucket {key}: Selected {count} users")

    data_rows = fetch_submissions(selected_users)
    
    if data_rows:
        df = pd.DataFrame(data_rows)
        # Ensure column order matches your request
        base_cols = ["problem_rating", "user_avg_rating", "solved"]
        tag_cols = [f"tag_{t}" for t in TARGET_TAGS]
        final_cols = base_cols + tag_cols + ["rating_diff"]
        
        df = df[final_cols]
        df.to_csv("cf_data.csv", index=False)
        print(f"\nSuccess! Dataset saved with {len(df)} rows.")
    else:
        print("No data collected.")

if __name__ == "__main__":
    main()
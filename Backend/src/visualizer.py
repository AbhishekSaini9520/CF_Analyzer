import os
import requests
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib

# Force non-interactive backend for server-side use
matplotlib.use('Agg')

BASE_URL = "https://codeforces.com/api"
SAVE_DIR = "matplotlib_graphs"

# Exact Hex Codes as requested
RANK_COLORS = [
    (0, 1200, '#808080'),    # Newbie - Gray
    (1200, 1400, '#008000'), # Pupil - Green
    (1400, 1600, '#03A89E'), # Specialist - Cyan
    (1600, 1900, '#0000FF'), # Expert - Blue
    (1900, 2100, '#AA00AA'), # Candidate Master - Violet
    (2100, 2300, '#FFAC00'), # Master - Orange
    (2300, 2400, '#FF8C00'), # International Master - Orange
    (2400, 2600, "#F97171"), # Grandmaster - Red
    (2600, 3000, '#FF0000'), # International Grandmaster - Red
    (3000, 5000, "#A00202"), # Legendary Grandmaster - Dark Red
]

def get_user_data(handle):
    status_url = f"{BASE_URL}/user.status?handle={handle}"
    rating_url = f"{BASE_URL}/user.rating?handle={handle}"
    
    status_res = requests.get(status_url).json()
    rating_res = requests.get(rating_url).json()
    
    if status_res["status"] != "OK" or rating_res["status"] != "OK":
        raise Exception(f"Failed to fetch data for handle: {handle}")
        
    return status_res["result"], rating_res["result"]

def generate_graphs(handle):
    print(f"🚀 Generating graphs for handle: {handle}...")
    
    submissions, rating_history = get_user_data(handle)
    
    # DATA PROCESSING 
    solved_problems = []
    seen_problems = set()
    for sub in submissions:
        if sub["verdict"] == "OK":
            p = sub['problem']
            p_id = f"{p.get('contestId')}{p.get('index')}"
            if p_id not in seen_problems:
                solved_problems.append(p)
                seen_problems.add(p_id)

    all_tags = [tag for p in solved_problems for tag in p.get("tags", [])]
    tag_counts = pd.Series(all_tags).value_counts()

    #  1. PIE CHART 
    plt.figure(figsize=(10, 8))
    top_tags_pie = tag_counts.head(10)
    colors = plt.get_cmap('tab20').colors
    labels_with_counts = [f'{tag} ({count})' for tag, count in zip(top_tags_pie.index, top_tags_pie.values)]
    
    plt.pie(top_tags_pie, labels=labels_with_counts, autopct='%1.1f%%', 
            startangle=140, colors=colors, wedgeprops={'edgecolor': 'white'})
    
    plt.title(f"Top 10 Topics - {handle} (Total Solved: {len(seen_problems)})", pad=20, fontweight='bold')
    plt.savefig(os.path.join(SAVE_DIR, f"{handle}_pie.png"), bbox_inches='tight')
    plt.close()

    #  2. BARH GRAPH 
    plt.figure(figsize=(12, 8))
    ax = tag_counts.head(15).plot(kind='barh', color='#6fa8dc', edgecolor='navy')
    plt.gca().invert_yaxis()
    
    for i, v in enumerate(tag_counts.head(15)):
        ax.text(v + 0.5, i, f" {v}", color='black', fontweight='bold', va='center')

    plt.title(f"Topic-wise Proficiency - {handle}", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(SAVE_DIR, f"{handle}_barh.png"))
    plt.close()

    #  3. RATING GRAPH (SOLID HEX COLORS) 
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ratings = [r["newRating"] for r in rating_history]
    times = pd.to_datetime([r["ratingUpdateTimeSeconds"] for r in rating_history], unit='s')

    for low, high, color in RANK_COLORS:
        ax.axhspan(low, high, facecolor=color, alpha=0.8)

    # Plotting the line on top of the solid bands
    ax.plot(times, ratings, color='yellow', marker='o', markersize=5, 
            markerfacecolor='white', markeredgecolor='yellow', linewidth=1.5,)
    
    ax.set_title(f"Rating History: {handle}", fontsize=15, fontweight='bold', color='white' if ratings and ratings[-1] > 3000 else 'black')
    ax.grid(True, linestyle=':', alpha=0.3, color='white')
    
    if ratings:
        ax.set_ylim(max(0, min(ratings)-150), max(ratings)+250)
    else:
        ax.set_ylim(0, 3500)

    plt.savefig(os.path.join(SAVE_DIR, f"{handle}_rating.png"), bbox_inches='tight')
    plt.close()

    #  4. DIFFICULTY DISTRIBUTION 
    difficulty_counts = {}

    for p in solved_problems:
        rating = p.get("rating")
        if rating is None:
            continue

        # Bucket ratings (e.g., 800–1199 → 800)
        bucket = (rating // 400) * 400
        difficulty_counts[bucket] = difficulty_counts.get(bucket, 0) + 1

    # Sort by rating
    sorted_items = sorted(difficulty_counts.items())

    if sorted_items:
        ratings, counts = zip(*sorted_items)
    else:
        ratings, counts = [], []

    # Plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar([str(r) for r in ratings], counts, color="#cbd5e1", edgecolor="#94a3b8")

    # Labels
    plt.xlabel("Problem Rating", fontsize=12)
    plt.ylabel("Number of Problems Solved", fontsize=12)
    plt.title(f"Problem Difficulty Distribution - {handle}", fontweight="bold")

    # Add values on top
    for i, v in enumerate(counts):
        plt.text(i, v + 1, str(v), ha='center', fontsize=10)

    plt.tight_layout()

    # Save image
    plt.savefig(os.path.join(SAVE_DIR, f"{handle}_difficulty.png"))
    plt.close()
        
    print(f"Success! Graphs saved for {handle}.")

if __name__ == "__main__":
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        
    user_handle = input("Enter Codeforces Handle: ").strip()
    
    if user_handle:
        try:
            generate_graphs(user_handle)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Please provide a valid handle.")
import pandas as pd 
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../model/model1.pkl")
DATA_PATH = os.path.join(BASE_DIR, "../data/cf_data.csv")

with open(MODEL_PATH, "rb") as f:
    _model = pickle.load(f)

if hasattr(_model, "feature_names_in_"):
    FEATURE_COLUMNS = list(_model.feature_names_in_)
else:
    df_train = pd.read_csv(DATA_PATH)
    FEATURE_COLUMNS = [col for col in df_train.columns if col != "solved"]

def normalize_tag(tag):
    return tag.strip().lower()

def build_feature(problem_rating, user_avg_rating, problem_tags):
    problem_tags = [normalize_tag(t) for t in problem_tags]

    feature_dict = {}
    feature_dict["problem_rating"] = problem_rating
    feature_dict["user_avg_rating"] = user_avg_rating
    feature_dict["rating_diff"] = user_avg_rating - problem_rating

    for col in FEATURE_COLUMNS:
        if col.startswith("tag_"):
            tag_name = col.replace("tag_", "")
            feature_dict[col] = 1 if tag_name in problem_tags else 0

    return pd.DataFrame([feature_dict], columns=FEATURE_COLUMNS)
import pandas as pd # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.ensemble import RandomForestClassifier # type: ignore
import pickle

# 1. Load data
data = pd.read_csv("../data/cf_data.csv")

X = data.drop("solved", axis=1)
y = data["solved"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=25,
    min_samples_leaf=5,
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

# 3. Validation
importances = pd.Series(model.feature_importances_, index=X.columns)
print("\n📊 Top Important Features:")
print(importances.sort_values(ascending=False).head(5))

accuracy = model.score(X_test, y_test)
print(f"\nTraining Accuracy: {accuracy:.4f}")

with open("../model/model1.pkl", "wb") as f:
    pickle.dump(model, f)
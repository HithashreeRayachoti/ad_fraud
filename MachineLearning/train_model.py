import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


#Loading features and labels

features_df = pd.read_csv('ProcessedPhase1/train_features.csv')
labels_df = pd.read_csv('ProcessedPhase1/train_labels.csv')

df = pd.merge(features_df, labels_df, on='session_id')

X = df.drop(columns=["session_id", "label"])
y = df["label"]

# === Train-test split ===
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)

# === Train model ===
RandomClf = RandomForestClassifier(n_estimators=100, random_state=42)
RandomClf.fit(X_train, y_train)

# === Save the model ===
joblib.dump(RandomClf, "savedModels/random_forest_classifier.joblib")

# === Predictions & Evaluation ===
y_pred = RandomClf.predict(X_val)

print("\n=== Accuracy ===")
print(f"{accuracy_score(y_val, y_pred):.4f}")

print("\n=== Classification Report ===")
print(classification_report(y_val, y_pred))

# === Confusion Matrix ===
cm = confusion_matrix(y_val, y_pred)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Human", "Bot"], yticklabels=["Human", "Bot"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# === Feature Importances ===
importances = RandomClf.feature_importances_
indices = np.argsort(importances)[::-1]
feature_names = X.columns[indices]

plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(len(importances)), importances[indices], align="center")
plt.xticks(range(len(importances)), feature_names, rotation=90)
plt.tight_layout()
plt.show()



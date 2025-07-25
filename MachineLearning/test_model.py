import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# === Load test data ===
features_df = pd.read_csv('ProcessedPhase1/test_features.csv')
labels_df = pd.read_csv('ProcessedPhase1/test_labels.csv')

# === Merge by session_id (if applicable) ===
df = pd.merge(features_df, labels_df, on='session_id')

X_test = df.drop(columns=["session_id", "label"])
y_test = df["label"]

# === Load trained model ===
model = joblib.load("savedModels/random_forest_classifier.joblib")

# === Predict ===
y_pred = model.predict(X_test)

# === Evaluation ===
print("\n=== Accuracy ===")
print(f"{accuracy_score(y_test, y_pred):.4f}")

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred))

# === Confusion Matrix ===
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", xticklabels=["Human", "Bot"], yticklabels=["Human", "Bot"])
plt.title("Test Set Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

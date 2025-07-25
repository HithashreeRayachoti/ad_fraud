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


#=====xGBoost Classifier=====

from sklearn.preprocessing import LabelEncoder

# Encode string labels to integers
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Now split using the encoded labels
X_train, X_val, y_train, y_val = train_test_split(X, y_encoded, test_size=0.3, random_state=42)


from xgboost import XGBClassifier

# === Train XGBoost model ===
xgb_clf = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
xgb_clf.fit(X_train, y_train)

# === Save XGBoost model ===
joblib.dump(xgb_clf, "savedModels/xgboost_classifier.joblib")

# === Predictions & Evaluation for XGBoost ===
y_pred_xgb = xgb_clf.predict(X_val)

print("\n=== [XGBoost] Accuracy ===")
print(f"{accuracy_score(y_val, y_pred_xgb):.4f}")

print("\n=== [XGBoost] Classification Report ===")
print(classification_report(y_val, y_pred_xgb))

# === Confusion Matrix for XGBoost ===
cm_xgb = confusion_matrix(y_val, y_pred_xgb)
plt.figure(figsize=(6, 4))
sns.heatmap(cm_xgb, annot=True, fmt="d", cmap="Greens", xticklabels=["Human", "Bot"], yticklabels=["Human", "Bot"])
plt.title("Confusion Matrix (XGBoost)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()


#=====Gradient Boosting Classifier=====

from sklearn.ensemble import GradientBoostingClassifier

# Instantiate and train
gbm_clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gbm_clf.fit(X_train, y_train)
joblib.dump(gbm_clf, "savedModels/gradient_boosting_classifier.joblib")

y_pred = gbm_clf.predict(X_val)

# Evaluate
print("Accuracy GBM:", accuracy_score(y_val, y_pred))
print("Classification Report GBM:\n", classification_report(y_val, y_pred))
print("Confusion Matrix GBM:\n", confusion_matrix(y_val, y_pred))

importances = gbm_clf.feature_importances_
indices = np.argsort(importances)[::-1]
features = X.columns  # if X is a DataFrame

plt.figure(figsize=(10,6))
plt.title("Feature Importances")
plt.bar(range(len(importances)), importances[indices])
plt.xticks(range(len(importances)), [features[i] for i in indices], rotation=90)
plt.tight_layout()
plt.show()

from sklearn.metrics import roc_auc_score

y_proba = gbm_clf.predict_proba(X_val)[:,1]
print("ROC AUC Score:", roc_auc_score(y_val, y_proba))

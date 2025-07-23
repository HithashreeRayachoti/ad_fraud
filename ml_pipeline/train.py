# ml_pipeline/train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc # <-- 1. ADDED roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

print("Starting model training and visualization process...")

# --- Load Processed Data ---
PROCESSED_DATA_PATH = 'ml_pipeline/data/processed/'
FEATURES_FILE = os.path.join(PROCESSED_DATA_PATH, 'features.csv')

if not os.path.exists(FEATURES_FILE):
    print(f"Error: The file {FEATURES_FILE} was not found.")
    print("Please run 'process_data.py' first to generate the features.")
    exit()

final_df = pd.read_csv(FEATURES_FILE)

# --- 1. Define Features (X) and Target (y) ---
X = final_df.drop(columns=['session_id', 'is_bot'])
y = final_df['is_bot']

# --- 2. Split Data into Training and Testing Sets ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
print(f"Data split complete. Training set has {len(X_train)} samples.")
print(f"Testing set has {len(X_test)} samples.")


# --- VISUALIZATION 1: Feature Pair Plot ---
print("\nGenerating feature pair plot to visualize data separation...")
plot_df = X_train.copy()
plot_df['label'] = y_train.map({0: 'Human', 1: 'Bot'})

pair_plot = sns.pairplot(plot_df, hue='label', palette={'Human': 'blue', 'Bot': 'red'})
pair_plot.fig.suptitle("Feature Relationships by Class", y=1.02)
plt.show()


# --- Model Training ---
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced',
    n_jobs=-1
)

print("\nTraining Random Forest model...")
model.fit(X_train, y_train)


# --- Evaluation ---
print("\nEvaluating model on the test set...")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=['Human', 'Bot']))


# --- VISUALIZATION 2: Confusion Matrix ---
print("Generating confusion matrix...")
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Predicted Human', 'Predicted Bot'],
            yticklabels=['Actual Human', 'Actual Bot'])
plt.title('Confusion Matrix')
plt.show()


# --- (NEW) VISUALIZATION 3: ROC-AUC Curve ---
print("Generating ROC-AUC Curve...")
# Get the prediction probabilities for the 'Bot' class (the positive class)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Calculate the ROC curve points
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)

# Calculate the Area Under the Curve (AUC)
roc_auc = auc(fpr, tpr)

# Plot the ROC curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--') # Dashed line for random chance
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()


# --- VISUALIZATION 4: Feature Importance ---
print("Generating feature importance plot...")
importances = pd.Series(model.feature_importances_, index=X.columns)
sorted_importances = importances.sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=sorted_importances, y=sorted_importances.index)
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importance')
plt.tight_layout()
plt.show()


# --- Saving the Model ---
MODELS_PATH = 'models/'
os.makedirs(MODELS_PATH, exist_ok=True)
joblib.dump(model, os.path.join(MODELS_PATH, 'random_forest_model.pkl'))
print(f"\nModel trained and saved to: {os.path.join(MODELS_PATH, 'random_forest_model.pkl')}")
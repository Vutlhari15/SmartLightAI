
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the real dataset
df = pd.read_csv("street_light_fault_prediction_dataset.csv")


print("\n===== FAULT LABEL DEFINITIONS =====")
print(
    df.groupby("fault_type")[
        [
            "power_consumption (Watts)",
            "voltage_levels (Volts)",
            "current_fluctuations (Amperes)",
            "temperature (Celsius)"
        ]
    ].mean().round(2)
)

print("Dataset loaded successfully!")
print("Total records:", len(df))

# Select the input features
features = [
    "power_consumption (Watts)",
    "voltage_levels (Volts)",
    "current_fluctuations (Amperes)",
    "temperature (Celsius)",
    "current_fluctuations_env (Amperes)"
]

# Prepare inputs and target labels
X = df[features]
y = df["fault_type"]

# Convert environmental conditions into numbers
X = X.copy()
X["environmental_conditions"] = (
    df["environmental_conditions"]
    .astype("category")
    .cat.codes
)

# Include the encoded environmental feature
features.append("environmental_conditions")
X = X[features]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train the AI model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)

print("\n===== MODEL EVALUATION =====")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Accuracy:", round(accuracy_score(y_test, predictions) * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))
from sklearn.metrics import confusion_matrix

print("\n===== CONFUSION MATRIX =====")
print(confusion_matrix(y_test, predictions))

print("\n===== ACCURACY BY FAULT CLASS =====")
for label in sorted(y_test.unique()):
    mask = y_test == label
    correct = (predictions[mask] == y_test[mask]).sum()
    total = mask.sum()
    print(f"Class {label}: {correct}/{total} correct")

# Save the trained model and feature information
with open("smartlight_model.pkl", "wb") as file:
    pickle.dump(
        {"model": model, "features": features},
        file
    )

print("\nReal-dataset model saved as smartlight_model.pkl")

print("\n===== FEATURE IMPORTANCE =====")

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print(importance.to_string(index=False))


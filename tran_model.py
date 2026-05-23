import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset
data = pd.read_csv("dataset.csv")

# Sirf numeric columns lo
data = data.select_dtypes(include=['number'])

# Features
X = data.drop("web_traffic", axis=1)

# Labels
Y = data["web_traffic"]

# Split
X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)

model.fit(X_train, Y_train)

# Accuracy
accuracy = model.score(X_test, Y_test)

print("Accuracy:", accuracy)

# Save model
joblib.dump(model,"phishing_model.pkl")
print("model saved")

print("AI Model Saved Successfully")
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Create model directory if missing
os.makedirs('model', exist_ok=True)

# Updated training data - COVID-19 replaced with Pneumonia
SYMPTOMS = ["Fever", "Cough", "Headache", "Fatigue", "Nausea", "Shortness of breath"]
DISEASES = {
    "Common Cold": [1, 1, 0, 1, 0, 0],  # Fever, Cough, No Headache, Fatigue, No Nausea, No Short breath
    "Flu":        [1, 1, 1, 1, 1, 0],   # All symptoms except shortness of breath
    "Migraine":   [0, 0, 1, 1, 1, 0],   # No fever/cough
    "Pneumonia":  [1, 1, 0, 1, 0, 1]    # Replaces COVID-19 (same symptom pattern)
}

# Convert to DataFrame
df = pd.DataFrame.from_dict(DISEASES, orient='index', columns=SYMPTOMS)
df['Disease'] = df.index  # Add disease names as column

# Encode labels
le = LabelEncoder()
df['Disease_Encoded'] = le.fit_transform(df['Disease'])

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(df[SYMPTOMS], df['Disease_Encoded'])

# Save artifacts
joblib.dump(model, 'model/disease_predictor.joblib')
joblib.dump(le, 'model/label_encoder.joblib')
joblib.dump(SYMPTOMS, 'model/symptoms.joblib')  # For reference

# Verify
print("Model trained successfully with these classes:")
print(le.classes_)
print("\nSample prediction (Fever+Cough+Shortness of breath):")
print("Predicted:", le.inverse_transform(model.predict([[1, 1, 0, 1, 0, 1]]))[0])
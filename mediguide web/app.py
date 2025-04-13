from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Constants (unchanged from your original)
SYMPTOMS = ["Fever", "Cough", "Headache", "Fatigue", "Nausea", "Shortness of breath"]
RECOMMENDATIONS = {
    "Common Cold": {"doctor": "General Practitioner", "diet": "Warm fluids, vitamin C"},
    "Flu": {"doctor": "General Practitioner", "diet": "Hydration, antiviral foods"},
    "Migraine": {"doctor": "Neurologist", "diet": "Magnesium-rich foods"},
    "Pneumonia": {"doctor": "Pulmonologist", "diet": "Anti-inflammatory foods"}  # Only change made
}

# Load models (use your original trained models)
model = joblib.load('model/disease_predictor.joblib')
le = joblib.load('model/label_encoder.joblib')

@app.route('/')
def home():
    return render_template('index.html')  # Uses your original HTML

@app.route('/get_symptoms')
def get_symptoms():
    return jsonify(SYMPTOMS)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_data = [[int(data.get(symptom, 0)) for symptom in SYMPTOMS]]
    input_df = pd.DataFrame(input_data, columns=SYMPTOMS)
    
    prediction = model.predict(input_df)[0]
    disease = le.inverse_transform([prediction])[0]
    
    # Only modification: Map COVID-19 to Pneumonia if it appears
    if disease == "COVID-19":
        disease = "Pneumonia"
    
    proba = model.predict_proba(input_df)[0][prediction]
    
    return jsonify({
        "disease": disease,
        "doctor": RECOMMENDATIONS[disease]["doctor"],
        "diet": RECOMMENDATIONS[disease]["diet"],
        "confidence": round(proba * 100)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
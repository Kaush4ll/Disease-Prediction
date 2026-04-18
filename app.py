import pandas as pd
import random
import os
from flask import Flask, request, render_template
from sklearn.ensemble import RandomForestClassifier

# =============================
# 1. INIT APP
# =============================
app = Flask(__name__)

# =============================
# 2. SYMPTOMS LIST
# =============================
symptoms = [
    "fever","cough","fatigue","headache","nausea",
    "vomiting","diarrhea","body_pain",
    "sore_throat","runny_nose","chills","sweating",
    "abdominal_pain","chest_pain","shortness_of_breath",
    "dizziness","rash","loss_of_taste","loss_of_smell"
]

# =============================
# 3. DISEASE PATTERNS
# =============================
disease_patterns = {
    "Flu": ["fever","cough","fatigue","body_pain","chills"],
    "Cold": ["cough","runny_nose","sore_throat"],
    "COVID-19": ["fever","cough","fatigue","loss_of_taste","loss_of_smell"],
    "Food Poisoning": ["nausea","vomiting","diarrhea","abdominal_pain"],
    "Malaria": ["fever","chills","sweating","fatigue"],
    "Migraine": ["headache","nausea","dizziness"],
    "Bronchitis": ["cough","fatigue","chest_pain"],
    "Typhoid": ["fever","fatigue","abdominal_pain","headache"],
    "Pneumonia": ["fever","cough","chest_pain","shortness_of_breath"],
    "Dengue": ["fever","rash","headache","body_pain"],
    "Allergy": ["runny_nose","sore_throat","cough"],
    "Chikungunya": ["fever","body_pain","fatigue"],
    "Asthma": ["cough","shortness_of_breath","chest_pain"],
    "Gastroenteritis": ["nausea","vomiting","diarrhea"],
    "Hypertension": ["headache","dizziness"],
    "Depression": ["fatigue","dizziness"],
    "Anemia": ["fatigue","dizziness","headache"],
    "Hepatitis": ["fatigue","nausea","abdominal_pain"],
    "Tuberculosis": ["cough","fever","fatigue"],
    "Sinusitis": ["headache","runny_nose","sore_throat"],
    "Chickenpox": ["fever","rash","fatigue"],
    "Pancreatitis": ["abdominal_pain","nausea","vomiting"],
    "Stress": ["headache","fatigue"],
    "Measles": ["fever","rash","cough"],
    "Appendicitis": ["abdominal_pain","nausea"],
    "Vertigo": ["dizziness","headache"],
    "Whooping Cough": ["cough","fatigue"],
    "Hay Fever": ["runny_nose","cough"],
    "Leptospirosis": ["fever","body_pain","headache"],
    "Cholera": ["diarrhea","vomiting","fatigue"]
}

# =============================
# 4. DATASET GENERATION
# =============================
def generate_row(disease):
    row = [0] * len(symptoms)

    for sym in disease_patterns[disease]:
        if sym in symptoms:
            row[symptoms.index(sym)] = 1

    # small noise
    for i in range(len(row)):
        if random.random() < 0.1:
            row[i] = 1 - row[i]

    return row + [disease]


# Create dataset if not exists
if not os.path.exists("disease_dataset.csv"):
    rows = []
    for disease in disease_patterns:
        for _ in range(200):  # reduced for speed
            rows.append(generate_row(disease))

    df = pd.DataFrame(rows, columns=symptoms + ["prognosis"])
    df.to_csv("disease_dataset.csv", index=False)
else:
    df = pd.read_csv("disease_dataset.csv")

# =============================
# 5. TRAIN MODEL
# =============================
X = df[symptoms]
y = df["prognosis"]

model = RandomForestClassifier(n_estimators=200, max_depth=15)
model.fit(X, y)

# =============================
# 6. HELPER FUNCTIONS
# =============================
def get_reason(input_data):
    selected = [symptoms[i] for i, v in enumerate(input_data) if v == 1]
    return "Because of: " + ", ".join(selected[:5]) if selected else ""

def doctor_advice(top_predictions):
    top = top_predictions[0]
    if top["probability"] > 75:
        return f"High chance of {top['disease']}. Consult a doctor."
    elif top["probability"] > 50:
        return f"Possible {top['disease']}. Monitor symptoms."
    else:
        return "Low confidence. If symptoms persist, consult a doctor."

# =============================
# 7. ROUTE
# =============================
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        # Get input safely
        input_data = [1 if request.form.get(sym) == "on" else 0 for sym in symptoms]

        # 🚨 Prevent empty input
        if sum(input_data) == 0:
            return render_template("index.html", symptoms=symptoms, error="Please select at least one symptom")

        # Convert to DataFrame (fix warning)
        input_df = pd.DataFrame([input_data], columns=symptoms)

        probs = model.predict_proba(input_df)[0]
        classes = model.classes_

        # Top 3 predictions
        top_idx = probs.argsort()[-3:][::-1]

        top_predictions = []
        for i in top_idx:
            top_predictions.append({
                "disease": classes[i],
                "probability": round(probs[i]*100, 2)
            })

        reason = get_reason(input_data)
        advice = doctor_advice(top_predictions)

        return render_template(
            "index.html",
            symptoms=symptoms,
            predictions=top_predictions,
            reason=reason,
            advice=advice
        )

    return render_template("index.html", symptoms=symptoms)

# =============================
# 8. RUN
# =============================
if __name__ == "__main__":
    app.run(debug=True)
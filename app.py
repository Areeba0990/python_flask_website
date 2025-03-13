from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Define symptom-disease mapping with probabilities
disease_mapping = {
    "Influenza": ["fever", "cough", "body ache", "chills"],
    "Common Cold": ["runny nose", "sore throat", "cough", "headache"],
    "COVID-19": ["fever", "cough", "shortness of breath", "loss of taste"],
    "Malaria": ["fever", "chills", "sweating", "headache"]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    result = None

    if request.method == 'POST':
        symptoms = request.form.getlist('symptoms')  # Get selected symptoms

        if len(symptoms) != 4:  # Ensure exactly 4 symptoms are selected
            return render_template('detect.html', error="Please select exactly 4 symptoms.")

        disease_scores = {}

        # Calculate disease probability based on symptoms
        for disease, disease_symptoms in disease_mapping.items():
            match_count = sum(1 for symptom in symptoms if symptom in disease_symptoms)
            probability = (match_count / 4) * 100  # Convert to percentage
            if probability > 0:
                disease_scores[disease] = round(probability)  # Remove extra `%`

        # Sort diseases by highest probability
        sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)

        result = sorted_diseases

    return render_template('detect.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Define symptom-disease mapping with probabilities
disease_mapping = {
    "Influenza": ["fever", "cough", "body ache", "chills"],
    "Common Cold": ["runny nose", "sore throat", "cough", "headache"],
    "COVID-19": ["fever", "cough", "shortness of breath", "loss of taste"],
    "Malaria": ["fever", "chills", "sweating", "headache"]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    result = None

    if request.method == 'POST':
        symptoms = request.form.getlist('symptoms')  # Get selected symptoms

        if len(symptoms) != 4:  # Ensure exactly 4 symptoms are selected
            return render_template('detect.html', error="Please select exactly 4 symptoms.")

        disease_scores = {}

        # Calculate disease probability based on symptoms
        for disease, disease_symptoms in disease_mapping.items():
            match_count = sum(1 for symptom in symptoms if symptom in disease_symptoms)
            probability = (match_count / 4) * 100  # Convert to percentage
            if probability > 0:
                disease_scores[disease] = round(probability)  # Remove extra `%`

        # Sort diseases by highest probability
        sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)

        result = sorted_diseases

    return render_template('detect.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

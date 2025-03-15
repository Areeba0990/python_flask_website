from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "aSdF123!@#randomSECRETkey$$%"  # Secret key for flashing messages

# Database Configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the Database
db = SQLAlchemy(app)

# Define the Contact Model (Database Table)
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create database tables before the first request
with app.app_context():
    db.create_all()

# Home Page Route
@app.route('/')
def home():
    return render_template('index.html')

# Define symptom-disease mapping with probabilities
disease_mapping = {
    "Influenza": ["fever", "cough", "body ache", "chills"],
    "Common Cold": ["runny nose", "sore throat", "cough", "headache"],
    "COVID-19": ["fever", "cough", "shortness of breath", "loss of taste"],
    "Malaria": ["fever", "chills", "sweating", "headache"]
}

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

# Contact Page Route (Handles Form Submission)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Save form data to the database
        new_contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(new_contact)
        db.session.commit()

        flash("Message sent successfully!")  # Flash success message
        return redirect('/contact')  # Redirect to clear the form

    return render_template('contact.html')

# About Page Route
@app.route('/about')
def about():
    return render_template('about.html')

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)

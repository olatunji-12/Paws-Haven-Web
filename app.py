from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://petuser:petpassword@localhost/petadoption"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db = SQLAlchemy(app)

# Models
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    species = db.Column(db.String(64), nullable=False)
    breed = db.Column(db.String(64))
    age = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(256))

# Routes
@app.route('/')
def index():
    animals = Animal.query.all()
    return render_template('index.html', animals=animals)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if name and email and message:
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        
        flash('Please fill in all fields.', 'danger')
    return render_template('contact.html')

# Initialize database
with app.app_context():
    db.create_all()
    if not Animal.query.first():
        sample_animals = [
            Animal(
                name="Buddy",
                species="Dog",
                breed="Golden Retriever",
                age=3,
                description="Friendly and loves playing fetch.",
                image_url="https://www.rover.com/blog/wp-content/uploads/2021/06/denvers_golden_life-1024x1024.jpg"
            ),
            # Add more sample animals here
        ]
        for animal in sample_animals:
            db.session.add(animal)
        db.session.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
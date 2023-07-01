from flask import Flask
from remote_doctor.views import bp
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_login import LoginManager
from remote_doctor.models import Patient, Session




# Create a Flask application instance
app = Flask(__name__, static_url_path='/static', static_folder='static')
login_manager = LoginManager(app)
app.secret_key = 'd6c3734041b1310121d30aed96a5484b'


# Configure the login manager
login_manager = LoginManager()

# Define the user loader function
@login_manager.user_loader
def load_user(patient_id):
    # Implement the logic to load the patient object based on the patient ID
    # For example, you can retrieve the patient from the database
    session = Session()
    patient = session.query(Patient).get(int(patient_id))
    session.close()
    return patient

# Initialize the login manager
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://johnson:Ibelieve1!@localhost:3306/remote_doctor"

db = SQLAlchemy(app)


# Register the blueprint
app.register_blueprint(bp)


# Run the Flask application if executed directly
if __name__ == '__main__':
    app.run(debug=True)


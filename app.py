from flask import Flask
from remote_doctor.views import bp
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_login import LoginManager
from remote_doctor.models import Patient, Doctor, Session




# Create a Flask application instance
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.debug = True
login_manager = LoginManager(app)
app.secret_key = 'd6c3734041b1310121d30aed96a5484b'

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://johnson:Ibelieve1!@localhost:3306/remote_doctor"

# Initialize the SQLAlchemy database
db = SQLAlchemy(app)



# Initialize and configure the login manager
login_manager.init_app(app)
#login_manager.login_view = 'login'  # Specify the login view endpoint

# Define the user loader function
@login_manager.user_loader
def load_patient(patient_id):
    print(f"Loading patient with ID: {patient_id}")
    # Implement the logic to load the patient object based on the patient ID
    # For example, you can retrieve the patient from the database
    session = Session()
    patient = session.get(Patient, int(patient_id))

    print(f"Loaded patient: {patient}")
    session.close()
    return patient

# Define the user loader function for Doctors
@login_manager.user_loader
def load_doctor(doctor_id):
    # Implement the logic to load the doctor object based on the doctor ID
    # For example, you can retrieve the doctor from the database
    session = Session()
    doctor = session.get(Doctor, int(doctor_id))

    session.close()
    return doctor


# Register the blueprint
app.register_blueprint(bp)


# Run the Flask application if executed directly
if __name__ == '__main__':
    app.run(debug=True)


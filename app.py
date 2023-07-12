from flask import Flask
from remote_doctor.views import bp
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_login import LoginManager
from remote_doctor.models import Patient, Doctor, User, Session


# Create a Flask application instance
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.debug = True
login_manager = LoginManager(app)
app.secret_key = 'd6c3734041b1310121d30aed96a5484b'

# Register the blueprint
app.register_blueprint(bp)


# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://johnson:Ibelieve1!@localhost:3306/remote_doctor"

# Initialize the SQLAlchemy database
db = SQLAlchemy(app)



# Initialize and configure the login manager
login_manager.init_app(app)
#login_manager.login_view = 'login'  # Specify the login view endpoint

@login_manager.user_loader
def load_user(user_id):
    session = Session()

    # Retrieve the user based on the user ID
    user = session.query(User).get(int(user_id))

    if user is not None:
        # Check the role of the user
        if user.role == 'patient':
            # User is a patient
            patient = session.query(Patient).filter_by(id=user.id).first()
            session.close()
            return patient
        elif user.role == 'doctor':
            # User is a doctor
            doctor = session.query(Doctor).filter_by(id=user.id).first()
            session.close()
            return doctor

    session.close()
    return None  # User not found or unrecognized role


# Run the Flask application if executed directly
if __name__ == '__main__':
    app.run(debug=True)


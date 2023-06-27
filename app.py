from flask import Flask
from remote_doctor.views import bp
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_login import LoginManager




# Create a Flask application instance
app = Flask(__name__)
login_manager = LoginManager(app)
app.secret_key = 'd6c3734041b1310121d30aed96a5484b'


# Configure the login manager
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # Retrieve the user object from the database based on the user ID
    user = User.query.get(int(user_id))

    # Return the user object if found, or None if not found
    return user

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://johnson:Ibelieve1!@localhost:3306/remote_doctor"

db = SQLAlchemy(app)

@app.route('/index.html')
def index():
    return render_template('index.html')

# Register the blueprint
app.register_blueprint(bp)


# Define routes and views
@app.route('/')
def home():
    return render_template('webpage.html')


# Run the Flask application if executed directly
if __name__ == '__main__':
    app.run(debug=True)


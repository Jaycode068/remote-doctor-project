from flask import Blueprint, jsonify, request, render_template, url_for, redirect
import model.models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user, current_user, login_required


engine = create_engine("mysql+mysqlconnector://johnson:Ibelieve1!@localhost:3306/remote_doctor")
Session = sessionmaker(bind=engine)

bp = Blueprint('remote_doctor', __name__)


# Registration route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Validate the form data
        # Check if the username is already taken
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        if user:
            error = 'Username already exists'
            return render_template('register.html', error=error)

        # Check for password complexity (e.g., minimum length, special characters, etc.)
        if len(password) < 8:
            error = 'Password must be at least 8 characters long'
            return render_template('register.html', error=error)

        # Create a new User object
        user = User(username=username, password=password, email=email)

        # Save the user record to the database
        session.add(user)
        session.commit()
        
        try:
            # Save the user record to the database
            session.add(user)
            session.commit()
        except Exception as e:
            error = 'An error occurred during registration. Please try again later.'
            return render_template('register.html', error=error)       

        # Redirect the user to a success page or login page
        return redirect(url_for('remote_doctor.login'))

    # If it's a GET request, render the registration form
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Implement the logic to authenticate the user
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)  # Login the user
            return redirect(url_for('remote_doctor.get_doctors'))

    return render_template('login.html')

@bp.route('/logout')
@login_required  # Protect the logout route as well
def logout():
    logout_user()  # Logout the user
    return redirect(url_for('remote_doctor.login'))

@bp.route('/doctors', methods=['GET'])
def get_doctors():
    session = Session()
    doctors = session.query(Doctor).all()
    session.close()    
    return jsonify([doctor.to_dict() for doctor in doctors])

@bp.route('/doctors', methods=['POST'])
def create_doctor():
    session = Session()
    data = request.json
    doctor = Doctor(**data)
    session.add(doctor)
    session.commit()
    session.close()
    return jsonify(doctor.to_dict()), 201

@bp.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    session = Session()
    doctor = session.query(Doctor).get(doctor_id)
    session.close()
    if doctor is None:
        return jsonify({'error': 'Doctor not found'}), 404
    return jsonify(doctor.to_dict())


@bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    session = Session()
    data = request.json
    doctor = session.query(Doctor).get(doctor_id)
    if doctor is None:
        session.close()
        return jsonify({'error': 'Doctor not found'}), 404
    doctor.name = data.get('name', doctor.name)
    doctor.specialty = data.get('specialty', doctor.specialty)
    # Update other attributes as needed
    session.commit()
    session.close()
    return jsonify(doctor.to_dict())

@bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    session = Session()
    doctor = session.query(Doctor).get(doctor_id)
    if doctor is None:
        session.close()
        return jsonify({'error': 'Doctor not found'}), 404
    session.delete(doctor)
    session.commit()
    session.close()
    return '', 204


#Defining end-points to perform CRUD for patients

@bp.route('/patients', methods=['GET'])
def get_patients():
    session = Session()
    patients = session.query(Patient).all()
    session.close()
    return jsonify([patient.to_dict() for patient in patients])

@bp.route('/patients', methods=['POST'])
def create_patient():
    session = Session()
    data = request.json
    patient = Patient(**data)
    session.add(patient)
    session.commit()
    session.close()
    return jsonify(patient.to_dict()), 201

@bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    session = Session()
    patient = session.query(Patient).get(patient_id)
    session.close()
    if patient is None:
        return jsonify({'error': 'Patient not found'}), 404
    return jsonify(patient.to_dict())

@bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    session = Session()
    data = request.json
    patient = session.query(Patient).get(patient_id)
    if patient is None:
        session.close()
        return jsonify({'error': 'Patient not found'}), 404
    patient.name = data.get('name', patient.name)
    patient.age = data.get('age', patient.age)
    # Update other attributes as needed
    session.commit()
    session.close()
    return jsonify(patient.to_dict())

@bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    session = Session()
    patient = session.query(Patient).get(patient_id)
    if patient is None:
        session.close()
        return jsonify({'error': 'Patient not found'}), 404
    session.delete(patient)
    session.commit()
    session.close()
    return '', 204

#Defining end-points to perform CRUD for appointments

@bp.route('/appointments', methods=['GET'])
def get_appointments():
    session = Session()
    appointments = session.query(Appointment).all()
    session.close()
    return jsonify([appointment.to_dict() for appointment in appointments])

@bp.route('/appointments', methods=['POST'])
def create_appointment():
    session = Session()
    data = request.json
    appointment = Appointment(**data)
    session.add(appointment)
    session.commit()
    session.close()
    return jsonify(appointment.to_dict()), 201

@bp.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    session = Session()
    appointment = session.query(Appointment).get(appointment_id)
    session.close()
    if appointment is None:
        return jsonify({'error': 'Appointment not found'}), 404
    return jsonify(appointment.to_dict())

@bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    session = Session()
    data = request.json
    appointment = session.query(Appointment).get(appointment_id)
    if appointment is None:
        session.close()
        return jsonify({'error': 'Appointment not found'}), 404
    appointment.doctor_id = data.get('doctor_id', appointment.doctor_id)
    appointment.patient_id = data.get('patient_id', appointment.patient_id)
    appointment.datetime = data.get('datetime', appointment.datetime)
    # Update other attributes as needed
    session.commit()
    session.close()
    return jsonify(appointment.to_dict())

@bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    session = Session()
    appointment = session.query(Appointment).get(appointment_id)
    if appointment is None:
        session.close()
        return jsonify({'error': 'Appointment not found'}), 404
    session.delete(appointment)
    session.commit()
    session.close()
    return '', 204

#Defining end-points to perform CRUD for medical records

@bp.route('/medical_records', methods=['GET'])
def get_medical_records():
    session = Session()
    medical_records = session.query(MedicalRecord).all()
    session.close()
    return jsonify([medical_record.to_dict() for medical_record in medical_records])

@bp.route('/medical_records', methods=['POST'])
def create_medical_record():
    session = Session()
    data = request.json
    medical_record = MedicalRecord(**data)
    session.add(medical_record)
    session.commit()
    session.close()
    return jsonify(medical_record.to_dict()), 201

@bp.route('/medical_records/<int:medical_record_id>', methods=['GET'])
def get_medical_record(medical_record_id):
    session = Session()
    medical_record = session.query(MedicalRecord).get(medical_record_id)
    session.close()
    if medical_record is None:
        return jsonify({'error': 'Medical record not found'}), 404
    return jsonify(medical_record.to_dict())

@bp.route('/medical_records/<int:medical_record_id>', methods=['PUT'])
def update_medical_record(medical_record_id):
    session = Session()
    data = request.json
    medical_record = session.query(MedicalRecord).get(medical_record_id)
    if medical_record is None:
        session.close()
        return jsonify({'error': 'Medical record not found'}), 404
    medical_record.patient_id = data.get('patient_id', medical_record.patient_id)
    medical_record.appointment_id = data.get('appointment_id', medical_record.appointment_id)
    medical_record.diagnosis = data.get('diagnosis', medical_record.diagnosis)
    # Update other attributes as needed
    session.commit()
    session.close()
    return jsonify(medical_record.to_dict())

@bp.route('/medical_records/<int:medical_record_id>', methods=['DELETE'])
def delete_medical_record(medical_record_id):
    session = Session()
    medical_record = session.query(MedicalRecord).get(medical_record_id)
    if medical_record is None:
        session.close()
        return jsonify({'error': 'Medical record not found'}), 404
    session.delete(medical_record)
    session.commit()
    session.close()
    return '', 204





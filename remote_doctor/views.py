from flask import Blueprint, jsonify, request, render_template, url_for, redirect, flash
from remote_doctor.models import Doctor, Patient, Appointment, MedicalRecord, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
from flask import abort


engine = create_engine("mysql+mysqlconnector://johnson:Ibelieve1!@localhost:3306/remote_doctor")
Session = sessionmaker(bind=engine)

bp = Blueprint('remote_doctor', __name__)

@bp.route('/')
def landing_page():
    return render_template('webpage.html')


@bp.route('/main')
@login_required  # Require login to access the main page
def main():
    # Add the logic to retrieve data for the main page and render the template
    return render_template('main.html')


@bp.route('/register/patient', methods=['GET', 'POST'])
def register_patient():
    if request.method == 'POST':
        # Get the form data from the request
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        # Create a new Patient instance with the form data
        patient = Patient(name=name, age=age, gender=gender, email=email,
                          phone=phone, address=address, username=username, password=password)

        # Create a session
        session = Session()

        try:
            # Add the patient to the session
            session.add(patient)
            # Commit the changes to the database
            session.commit()
            # Close the session
            session.close()

            # Flash a success message to the user
            flash('Patient registration successful!', 'success')
            return redirect(url_for('remote_doctor.login'))

        except Exception as e:
            # Handle any exceptions that occurred during the registration process
            # Rollback the session to revert any changes
            session.rollback()
            # Close the session
            session.close()

            # Flash an error message to the user or handle the exception in a desired way
            flash('An error occurred during patient registration. Please try again later.', 'error')

    return render_template('register_patient.html')


@bp.route('/register/doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        # Get the form data from the request
        name = request.form['name']
        specialty = request.form['specialty']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        # Create a new Doctor instance with the form data
        doctor = Doctor(id=id, name=name, specialty=specialty, email=email,
                        phone=phone, address=address, username=username, password=password)

        # Create a session
        session = Session()

        try:
            # Add the doctor to the session
            session.add(doctor)
            # Commit the changes to the database
            session.commit()
            # Close the session
            session.close()

            # Flash a success message to the user
            flash('Doctor registration successful!', 'success')
            return redirect(url_for('remote_doctor.login'))

        except Exception as e:
            # Handle any exceptions that occurred during the registration process
            # Rollback the session to revert any changes
            session.rollback()
            # Close the session
            session.close()

            # Flash an error message to the user or handle the exception in a desired way
            flash('An error occurred during doctor registration. Please try again later.', 'error')

    return render_template('register_doctor.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Implement the logic to authenticate the patient
        patient = Patient.get_by_username(username)
        if patient and patient.password == password:
            login_user(patient)  # Login the patient
            return redirect(url_for('remote_doctor.main'))

        # Invalid credentials or unsuccessful login attempt
        flash('Invalid username or password', 'error')
        return redirect(url_for('remote_doctor.login'))

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('remote_doctor.login'))

# Define a decorator to restrict access based on user roles
def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            # Check if the user is authenticated
            if not current_user.is_authenticated:
                return redirect(url_for('remote_doctor.login'))

            # Check if the user has the required role
            if current_user.role != role:
                # Return an access denied page or template
                return render_template('access_denied.html')

            # User has the required role, proceed with the view function
            return view_func(*args, **kwargs)

        return wrapper

    return decorator

# Apply the role_required decorator to restricted routes

@bp.route('/doctor/dashboard')
@login_required
@role_required('doctor')  # Restrict access to users with the 'doctor' role
def doctor_dashboard():
    # Code to display the doctor dashboard
    return render_template('doctor_dashboard.html')

@bp.route('/patient/profile')
@login_required
@role_required('patient')  # Restrict access to users with the 'patient' role
def patient_profile():
    # Code to display the patient profile
    return render_template('patient_profile.html')

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

@bp.route('/patient', methods=['GET'])
@login_required
def get_current_patient():
    return jsonify(username=current_user.username)


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





from flask import Blueprint, jsonify, request, render_template, url_for, redirect, flash
from remote_doctor.models import Doctor, Patient, Appointment, MedicalRecord, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
from flask import abort


# from werkzeug.security import check_password_hash



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

@bp.route('/doctors')
@login_required  # Require login to access the doctors dashboard page
def doctors():
    # Add the logic to retrieve data for doctors page and render the template
    return render_template('doctor_dashboard.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
    
        # Create a new session
        session = Session()
    
        if role == 'patient':
            # Additional fields for patient registration
            age = request.form['age']
            gender = request.form['gender']
    
            # Create a new Patient object
            patient = Patient(name=name, email=email, phone=phone, address=address, username=username, password=password, age=age, gender=gender)
    
            # Add the patient to the session
            session.add(patient)
    
        elif role == 'doctor':
            # Additional fields for doctor registration
            specialty = request.form['specialty']
    
            # Create a new Doctor object
            doctor = Doctor(name=name, email=email, phone=phone, address=address, username=username, password=password, specialty=specialty)
    
            # Add the doctor to the session
            session.add(doctor)
    
        # Create a new User object
        user = User(name=name, email=email, phone=phone, address=address, username=username, password=password, role=role)
    
        # Add the user to the session
        session.add(user)
    
        # Commit the changes to the database
        session.commit()
        session.close()
    
        return redirect(url_for('remote_doctor.login'))

    return render_template('register.html')

# Login route
@bp.route('/login', methods=['GET', 'POST'])
def login():

    session = Session()

    if current_user.is_authenticated:
        # User is already logged in, redirect to home page or appropriate route
        if current_user.role == 'patient':
            return redirect(url_for('remote_doctor.main'))
        elif current_user.role == 'doctor':
            return redirect(url_for('remote_doctor.doctors'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Find the user by username in the User table
        user = session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            # User found and password is correct
            # Log in the user
            login_user(user)

            # Redirect to the appropriate page based on the user's role
            if user.role == 'patient':
                return redirect(url_for('remote_doctor.main'))
            elif user.role == 'doctor':
                # Call the handle_doctor_login function with the logged-in doctor's username
                handle_doctor_login(user.username)

                return redirect(url_for('remote_doctor.doctors'))

        # Login failed, show an error message
        error_message = 'Invalid username or password'
        return render_template('login.html', error_message=error_message)

    # GET request, render the login form
    return render_template('login.html')    

@bp.route('/logout')
@login_required
def logout():
    # Call the handle_doctor_logout function with the logged-out doctor's username
    handle_doctor_logout(current_user.username)
    
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('remote_doctor.login'))

# Initialize the online_status dictionary
online_status = {}

@bp.route('/doctors-json')
def get_doctors_json():
    session = Session()
    doctors = session.query(Doctor).all()
    session.close()

    serialized_doctors = []
    for doctor in doctors:
        serialized_doctors.append({
            'id': doctor.id,
            'name': doctor.name,
            'specialty': doctor.specialty,
            'email': doctor.email,
            'phone': doctor.phone,
            'address': doctor.address
        })

    return jsonify({
        'doctors': serialized_doctors,
        'online_status': online_status
    })

# Whenever a doctor logs in
def handle_doctor_login(doctor_username):
    global online_status  # Add this line to access the global online_status dictionary
    online_status[doctor_username] = True

# Whenever a doctor logs out or disconnects
def handle_doctor_logout(doctor_username):
    global online_status  # Add this line to access the global online_status dictionary
    online_status[doctor_username] = False


@bp.route('/doctor', methods=['GET'], endpoint='doctor')
def get_doctors():
    session = Session()
    doctors = session.query(Doctor).all()
    session.close()

    logged_in_username = current_user.username if current_user else None
    return render_template('doctors.html', doctors=doctors, online_status=online_status, logged_in_username=logged_in_username)

@bp.route('/doctor_username', methods=['GET'])
@login_required
def get_current_doctor():
    return jsonify(username=current_user.username)

@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    session = Session()
    data = request.form

    # Retrieve the current user
    
    current_user = session.query(User).filter_by(username=current_user.username).first()
    print('Current User:', current_user)  # Print the current user for debugging purposes
    if not current_user:
        return jsonify(error='User not found'), 404

    # Update the user's profile with the form data
    current_user.name = data.get('name')
    current_user.email = data.get('email')
    current_user.phone = data.get('phone')
    current_user.address = data.get('address')

    try:
        session.commit()
        session.close()
        print('Profile updated successfully')
        return jsonify(message='Profile updated successfully')
    except Exception as e:
        session.rollback()
        session.close()
        print('Error updating profile:', e)
        return jsonify(error=str(e)), 500





"""
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
"""

#Defining end-points to perform CRUD for patients


@bp.route('/patient_username', methods=['GET'])
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

@bp.route('/profile', methods=['GET'])
@login_required  # Add a decorator to ensure the user is logged in
def get_profile():
    
    logged_in_patient = current_user

    # Create a dictionary with the profile details excluding the patient ID
    profile_details = {
        'name': logged_in_patient.name,
        'age': logged_in_patient.age,
        'gender': logged_in_patient.gender,
        'email': logged_in_patient.email,
        'phone': logged_in_patient.phone,
        'address': logged_in_patient.address,
        'username': logged_in_patient.username
    }

    return jsonify(profile_details)


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
    if request.headers['Content-Type'] == 'application/json':
        session = Session()
        data = request.json
        patient_id = data['patient_id']
        doctor_id = data['doctor_id']
        
        

        patient = session.query(Patient).get(patient_id)
        doctor = session.query(Doctor).get(doctor_id)
        
        if not patient or not doctor:
            session.close()
            return jsonify({'error': 'Invalid patient or doctor ID'}), 400
        
        appointment = Appointment(patient=patient, doctor=doctor, date=data['date'], notes=data['notes'])
        session.add(appointment)
        session.commit()
        
        appointment_data = appointment.to_dict()

        session.close()
        
        return jsonify(appointment_data), 201
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415

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
@login_required  # Assuming you have a login decorator to protect this route
def get_medical_records():
    patient_id = current_user.id
    session = Session()
    medical_records = session.query(MedicalRecord).options(joinedload(MedicalRecord.doctor)).filter_by(patient_id=patient_id).all()
    session.close()
    return jsonify([medical_record.to_dict() for medical_record in medical_records])


@bp.route('/medical_records', methods=['POST'])
def create_medical_record():
    session = Session()
    data = request.json

    # Extract the patient username from the form data
    patient_username = data.get('patient')
    print(f"Patient username: {patient_username}")

    # Find the patient with the given username
    patient = session.query(Patient).filter_by(username=patient_username).first()
    if not patient:
        print("Patient not found")
        return jsonify(error='Patient not found'), 404

    # Create the new MedicalRecord object
    medical_record = MedicalRecord(
        patient=patient,
        doctor=current_user,  # Assuming you have the current user stored in current_user variable
        diagnosis=data.get('diagnosis'),
        prescription=data.get('prescription')
    )

    session.add(medical_record)
    session.commit()

    # Refresh the medical_record object to ensure it is associated with the session
    session.refresh(medical_record)

    session.close()

    print("Medical record saved:", medical_record.to_dict())
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





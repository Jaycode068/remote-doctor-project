import pytest
from flask import url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .app import app
from remote_doctor.models import Doctor, Patient, Appointment, MedicalRecord, User


@pytest.fixture
def client() -> FlaskClient:
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register(client):
    # Simulate a POST request with form data
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testuser@example.com'
    })
    assert response.status_code == 302  # Check if the response is a redirect
    assert response.headers['Location'] == 'http://localhost/login'  # Check the redirect location

    # Verify that the user was created in the database (you may need to adapt this code to your specific database setup)
    with app.app_context():
        session = Session()
        user = session.query(User).filter_by(username='testuser').first()
        assert user is not None
        assert user.username == 'testuser'
        assert user.email == 'testuser@example.com'

def test_login(client):
    # Create a test user in the database (you may need to adapt this code to your specific database setup)
    with app.app_context():
        session = Session()
        user = User(username='testuser', password='testpassword', email='testuser@example.com')
        session.add(user)
        session.commit()

    # Simulate a POST request with login credentials
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 302  # Check if the response is a redirect
    assert response.headers['Location'] == 'http://localhost/doctor/dashboard'  # Check the redirect location

    # Verify that the user is authenticated and logged in
    with client.session_transaction() as session:
        assert 'user_id' in session
        assert session['user_id'] == 1  # Assuming the user ID is 1

    # Simulate a GET request to the dashboard page
    response = client.get('/doctor/dashboard')
    assert response.status_code == 200  # Check if the response is successful
    assert b'Doctor Dashboard' in response.data  # Check if the expected content is present in the response body

def test_doctor_dashboard(client):
    # Simulate a GET request to the doctor dashboard page
    response = client.get('/doctor/dashboard')
    assert response.status_code == 302  # Check if the response is a redirect
    assert response.headers['Location'] == 'http://localhost/login'  # Check the redirect location

    # Create a test user with 'doctor' role in the database (you may need to adapt this code to your specific database setup)
    with app.app_context():
        session = Session()
        user = User(username='testuser', password='testpassword', email='testuser@example.com', role='doctor')
        session.add(user)
        session.commit()

    # Log in the test user
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })

    # Simulate a GET request to the doctor dashboard page again
    response = client.get('/doctor/dashboard')
    assert response.status_code == 200  # Check if the response is successful
    assert b'Doctor Dashboard' in response.data  # Check if the expected content is present in the response body

def test_patient_profile(client):
    # Simulate a GET request to the patient profile page
    response = client.get('/patient/profile')
    assert response.status_code == 302  # Check if the response is a redirect
    assert response.headers['Location'] == 'http://localhost/login'  # Check the redirect location

    # Create a test user with 'patient' role in the database (you may need to adapt this code to your specific database setup)
    with app.app_context():
        session = Session()
        user = User(username='testuser', password='testpassword', email='testuser@example.com', role='patient')
        session.add(user)
        session.commit()

    # Log in the test user
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })

    # Simulate a GET request to the patient profile page again
    response = client.get('/patient/profile')
    assert response.status_code == 200  # Check if the response is successful
    assert b'Patient Profile' in response.data  # Check if the expected content is present in the response body

def test_get_doctors(client):
    # Simulate a GET request to the /doctors route
    response = client.get('/doctors')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == []  # Check if the response contains an empty list

    # Create a test doctor in the database (you may need to adapt this code to your specific database setup)
    with app.app_context():
        session = Session()
        doctor = Doctor(name='John Doe', specialty='Cardiology')
        session.add(doctor)
        session.commit()

    # Simulate another GET request to the /doctors route
    response = client.get('/doctors')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == [{'id': 1, 'name': 'John Doe', 'specialty': 'Cardiology'}]  # Check if the response contains the created doctor

def test_create_doctor(client):
    # Simulate a POST request to the /doctors route
    response = client.post('/doctors', json={'name': 'Jane Smith', 'specialty': 'Dermatology'})
    assert response.status_code == 201  # Check if the response is successful
    assert response.json == {'id': 1, 'name': 'Jane Smith', 'specialty': 'Dermatology'}  # Check if the response contains the created doctor

def test_get_doctor(client):
    # Simulate a GET request to the /doctors/<doctor_id> route
    response = client.get('/doctors/1')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == {'id': 1, 'name': 'John Doe', 'specialty': 'Cardiology'}  # Check if the response contains the doctor with ID 1

def test_update_doctor(client):
    # Simulate a PUT request to the /doctors/<doctor_id> route
    response = client.put('/doctors/1', json={'specialty': 'Neurology'})
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == {'id': 1, 'name': 'John Doe', 'specialty': 'Neurology'}  # Check if the response contains the updated doctor

def test_delete_doctor(client):
    # Simulate a DELETE request to the /doctors/<doctor_id> route
    response = client.delete('/doctors/1')
    assert response.status_code == 204  # Check if the response is successful

    # Simulate a GET request to the /doctors/<doctor_id> route after deletion
    response = client.get('/doctors/1')
    assert response.status_code == 404  # Check if the response is not found
    assert response.json == {'error': 'Doctor not found'}  # Check if the error message is returned

def test_get_patients(client):
    # Simulate a GET request to the /patients route
    response = client.get('/patients')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == []  # Check if the response contains an empty list

    # Create a test patient in the database (you may need to adapt this code to your specific database setup)
    with app.app_context():
        session = Session()
        patient = Patient(name='John Doe', age=30)
        session.add(patient)
        session.commit()

    # Simulate another GET request to the /patients route
    response = client.get('/patients')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == [{'id': 1, 'name': 'John Doe', 'age': 30}]  # Check if the response contains the created patient

def test_create_patient(client):
    # Simulate a POST request to the /patients route
    response = client.post('/patients', json={'name': 'Jane Smith', 'age': 25})
    assert response.status_code == 201  # Check if the response is successful
    assert response.json == {'id': 1, 'name': 'Jane Smith', 'age': 25}  # Check if the response contains the created patient

def test_get_patient(client):
    # Simulate a GET request to the /patients/<patient_id> route
    response = client.get('/patients/1')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == {'id': 1, 'name': 'John Doe', 'age': 30}  # Check if the response contains the patient with ID 1

def test_update_patient(client):
    # Simulate a PUT request to the /patients/<patient_id> route
    response = client.put('/patients/1', json={'age': 35})
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == {'id': 1, 'name': 'John Doe', 'age': 35}  # Check if the response contains the updated patient

def test_delete_patient(client):
    # Simulate a DELETE request to the /patients/<patient_id> route
    response = client.delete('/patients/1')
    assert response.status_code == 204  # Check if the response is successful

    # Simulate a GET request to the /patients/<patient_id> route after deletion
    response = client.get('/patients/1')
    assert response.status_code == 404  # Check if the response is not found
    assert response.json == {'error': 'Patient not found'}  # Check if the error message is returned


def test_get_appointments(client):
    # Simulate a GET request to the /appointments route
    response = client.get('/appointments')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == []  # Check if the response contains an empty list

    # Create a test appointment in the database (you may need to adapt this code to your specific database setup)
    with app.app_context():
        session = Session()
        appointment = Appointment(doctor_id=1, patient_id=1, datetime=datetime.datetime.now())
        session.add(appointment)
        session.commit()

    # Simulate another GET request to the /appointments route
    response = client.get('/appointments')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == [{'id': 1, 'doctor_id': 1, 'patient_id': 1, 'datetime': '...'}]  # Check if the response contains the created appointment

def test_create_appointment(client):
    # Simulate a POST request to the /appointments route
    appointment_data = {'doctor_id': 1, 'patient_id': 1, 'datetime': '...'}
    response = client.post('/appointments', json=appointment_data)
    assert response.status_code == 201  # Check if the response is successful
    assert response.json == {'id': 1, 'doctor_id': 1, 'patient_id': 1, 'datetime': '...'}  # Check if the response contains the created appointment

def test_get_appointment(client):
    # Simulate a GET request to the /appointments/<appointment_id> route
    response = client.get('/appointments/1')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == {'id': 1, 'doctor_id': 1, 'patient_id': 1, 'datetime': '...'}  # Check if the response contains the appointment with ID 1

def test_update_appointment(client):
    # Simulate a PUT request to the /appointments/<appointment_id> route
    appointment_data = {'patient_id': 2, 'datetime': '...'}
    response = client.put('/appointments/1', json=appointment_data)
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == {'id': 1, 'doctor_id': 1, 'patient_id': 2, 'datetime': '...'}  # Check if the response contains the updated appointment

def test_delete_appointment(client):
    # Simulate a DELETE request to the /appointments/<appointment_id> route
    response = client.delete('/appointments/1')
    assert response.status_code == 204  # Check if the response is successful

    # Simulate a GET request to the /appointments/<appointment_id> route after deletion
    response = client.get('/appointments/1')
    assert response.status_code == 404  # Check if the response is not found
    assert response.json == {'error': 'Appointment not found'}  # Check if the error message is returned

def test_get_medical_records(client):
    # Simulate a GET request to the /medical_records route
    response = client.get('/medical_records')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == []  # Check if the response contains an empty list

    # Create a test medical record in the database (you may need to adapt this code to your specific database setup)
    with app.app_context():
        session = Session()
        medical_record = MedicalRecord(patient_id=1, appointment_id=1, diagnosis='...')
        session.add(medical_record)
        session.commit()

    # Simulate another GET request to the /medical_records route
    response = client.get('/medical_records')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == [{'id': 1, 'patient_id': 1, 'appointment_id': 1, 'diagnosis': '...'}]  # Check if the response contains the created medical record

def test_create_medical_record(client):
    # Simulate a POST request to the /medical_records route
    medical_record_data = {'patient_id': 1, 'appointment_id': 1, 'diagnosis': '...'}
    response = client.post('/medical_records', json=medical_record_data)
    assert response.status_code == 201  # Check if the response is successful
    assert response.json == {'id': 1, 'patient_id': 1, 'appointment_id': 1, 'diagnosis': '...'}  # Check if the response contains the created medical record

def test_get_medical_record(client):
    # Simulate a GET request to the /medical_records/<medical_record_id> route
    response = client.get('/medical_records/1')
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == {'id': 1, 'patient_id': 1, 'appointment_id': 1, 'diagnosis': '...'}  # Check if the response contains the medical record with ID 1

def test_update_medical_record(client):
    # Simulate a PUT request to the /medical_records/<medical_record_id> route
    medical_record_data = {'appointment_id': 2, 'diagnosis': '...'}
    response = client.put('/medical_records/1', json=medical_record_data)
    assert response.status_code == 200  # Check if the response is successful
    assert response.json == {'id': 1, 'patient_id': 1, 'appointment_id': 2, 'diagnosis': '...'}  # Check if the response contains the updated medical record

def test_delete_medical_record(client):
    # Simulate a DELETE request to the /medical_records/<medical_record_id> route
    response = client.delete('/medical_records/1')
    assert response.status_code == 204  # Check if the response is successful

    # Simulate a GET request to the /medical_records/<medical_record_id> route after deletion
    response = client.get('/medical_records/1')
    assert response.status_code == 404  # Check if the response is not found
    assert response.json == {'error': 'Medical record not found'}  # Check if the error message is returned


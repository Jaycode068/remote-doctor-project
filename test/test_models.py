import pytest
from flask import url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..app import app
from remote_doctor.models import Doctor, Patient, Appointment, MedicalRecord, User

# Create the engine and session
engine = create_engine("mysql+mysqlconnector://johnson:Ibelieve1!@localhost:3306/remote_doctor")

# Create a test session
Session = sessionmaker(bind=engine)

# Define the User model test class
class UserModelTest(unittest.TestCase):
    def setUp(self):
        # Create all tables in the test database
        User.metadata.create_all(engine)

        # Create a session for testing
        self.session = Session()

    def tearDown(self):
        # Rollback any changes and close the session
        self.session.rollback()
        self.session.close()

        # Drop all tables in the test database
        User.metadata.drop_all(engine)

    def test_user_creation(self):
        # Create a new user
        user = User(username='testuser', password='testpassword', email='test@example.com')

        # Add the user to the session and commit the changes
        self.session.add(user)
        self.session.commit()

        # Retrieve the user from the session
        retrieved_user = self.session.query(User).filter_by(username='testuser').first()

        # Assert that the retrieved user matches the created user
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertEqual(retrieved_user.password, 'testpassword')
        self.assertEqual(retrieved_user.email, 'test@example.com')

    def test_user_authentication(self):
        # Create a new user
        user = User(username='testuser', password='testpassword', email='test@example.com')

        # Add the user to the session and commit the changes
        self.session.add(user)
        self.session.commit()

        # Retrieve the user from the session
        retrieved_user = self.session.query(User).filter_by(username='testuser').first()

        # Assert that the user is authenticated
        self.assertTrue(retrieved_user.is_authenticated)

    def test_user_role(self):
        # Create a new user with a role
        user = User(username='testuser', password='testpassword', email='test@example.com', role='admin')

        # Add the user to the session and commit the changes
        self.session.add(user)
        self.session.commit()

        # Retrieve the user from the session
        retrieved_user = self.session.query(User).filter_by(username='testuser').first()

        # Assert that the user role matches the assigned role
        self.assertEqual(retrieved_user.role, 'admin')

def test_doctor_to_dict(self):
    # Create a new doctor
    doctor = Doctor(
        id=1,
        name='John Smith',
        specialty='Cardiology',
        email='john@example.com',
        phone='1234567890',
        address='123 Main St',
        rating=4.5
    )

    # Convert the doctor to a dictionary
    doctor_dict = doctor.to_dict()

    # Assert that the dictionary contains the correct keys and values
    self.assertEqual(doctor_dict['id'], 1)
    self.assertEqual(doctor_dict['name'], 'John Smith')
    self.assertEqual(doctor_dict['specialty'], 'Cardiology')
    self.assertEqual(doctor_dict['email'], 'john@example.com')
    self.assertEqual(doctor_dict['phone'], '1234567890')
    self.assertEqual(doctor_dict['address'], '123 Main St')
    self.assertEqual(doctor_dict['rating'], 4.5)

def test_patient_to_dict(self):
    # Create a new patient
    patient = Patient(
        id=1,
        name='Jane Doe',
        age=30,
        gender='Female',
        email='jane@example.com',
        phone='1234567890',
        address='456 Main St',
    )

    # Convert the patient to a dictionary
    patient_dict = patient.to_dict()

    # Assert that the dictionary contains the correct keys and values
    self.assertEqual(patient_dict['id'], 1)
    self.assertEqual(patient_dict['name'], 'Jane Doe')
    self.assertEqual(patient_dict['age'], 30)
    self.assertEqual(patient_dict['gender'], 'Female')
    self.assertEqual(patient_dict['email'], 'jane@example.com')
    self.assertEqual(patient_dict['phone'], '1234567890')
    self.assertEqual(patient_dict['address'], '456 Main St')

def test_appointment_to_dict(self):
    # Create a new patient
    patient = Patient(
        id=1,
        name='Jane Doe',
        age=30,
        gender='Female',
        email='jane@example.com',
        phone='1234567890',
        address='456 Main St',
    )

    # Create a new doctor
    doctor = Doctor(
        id=1,
        name='Dr. John Smith',
        specialty='Cardiology',
        email='john@example.com',
        phone='9876543210',
        address='123 Park Ave',
        rating=4.5,
    )

    # Create a new appointment
    appointment = Appointment(
        id=1,
        patient_id=patient.id,
        doctor_id=doctor.id,
        date='2023-05-30',
    )

    # Convert the appointment to a dictionary
    appointment_dict = appointment.to_dict()

    # Assert that the dictionary contains the correct keys and values
    self.assertEqual(appointment_dict['id'], 1)
    self.assertEqual(appointment_dict['patient_id'], patient.id)
    self.assertEqual(appointment_dict['doctor_id'], doctor.id)
    self.assertEqual(appointment_dict['date'], '2023-05-30')

def test_medical_record_to_dict(self):
    # Create a new patient
    patient = Patient(
        id=1,
        name='Jane Doe',
        age=30,
        gender='Female',
        email='jane@example.com',
        phone='1234567890',
        address='456 Main St',
    )

    # Create a new doctor
    doctor = Doctor(
        id=1,
        name='Dr. John Smith',
        specialty='Cardiology',
        email='john@example.com',
        phone='9876543210',
        address='123 Park Ave',
        rating=4.5,
    )

    # Create a new medical record
    medical_record = MedicalRecord(
        id=1,
        patient_id=patient.id,
        doctor_id=doctor.id,
        diagnosis='Hypertension',
        prescription='Take medication X',
    )

    # Convert the medical record to a dictionary
    medical_record_dict = medical_record.to_dict()

    # Assert that the dictionary contains the correct keys and values
    self.assertEqual(medical_record_dict['id'], 1)
    self.assertEqual(medical_record_dict['patient_id'], patient.id)
    self.assertEqual(medical_record_dict['doctor_id'], doctor.id)
    self.assertEqual(medical_record_dict['diagnosis'], 'Hypertension')
    self.assertEqual(medical_record_dict['prescription'], 'Take medication X')


if __name__ == '__main__':
    unittest.main()

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from flask_login import UserMixin
#from werkzeug.security import generate_password_hash, check_password_hash



# Create the engine and session
engine = create_engine("mysql+mysqlconnector://johnson:Ibelieve1!@localhost:3306/remote_doctor")
Session = sessionmaker(bind=engine)

# Create the base class for models
Base = declarative_base()



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(100))
    username = Column(String(50))
    password = Column(String(100))
    role = Column(String(20))

    def is_authenticated(self):
        # Implement the logic to determine if the user is authenticated
        return True  # or False based on your criteria

    def get_id(self):
        return str(self.id)

    def is_active(self):
        # Implement the logic to determine if the user is active
        return True  # or False based on your criteria

    @classmethod
    def get_by_username(cls, username):
        session = Session()
        user = session.query(cls).filter_by(username=username).first()
        session.close()
        return user
    
    def check_password(self, password):
        # You might need to adjust this based on how passwords are stored and checked in your system
        return self.password == password

    def __init__(self, name, email, phone, address, username, password, role):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, role={self.role})"


class Doctor(User):
    __tablename__ = 'doctors'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    specialty = Column(String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'username': self.username,
            'role': 'doctor'
        }
    def __init__(self, name, email, phone, address, username, password, specialty):
        super().__init__(name, email, phone, address, username, password, 'doctor')
        self.specialty = specialty
    
    def __repr__(self):
        return f"Doctor(id={self.id}, name={self.name}, specialty={self.specialty})"


class Patient(User):
    __tablename__ = 'patients'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    age = Column(Integer)
    gender = Column(String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'username': self.username,
            'role': 'patient'
        }
    
    def __init__(self, name, email, phone, address, username, password, age, gender):
        super().__init__(name, email, phone, address, username, password, 'patient')
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f"Patient(id={self.id}, name={self.name}, age={self.age}, gender={self.gender})"


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient', backref='appointments')
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    doctor = relationship('Doctor')
    date = Column(String(20))
    notes = Column(String(200)) 

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date': self.date,
            'notes': self.notes
        }

    def __init__(self, patient_id, doctor_id, date, notes):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.notes = notes

    def __repr__(self):
        return f"Appointment(id={self.id}, patient={self.patient}, doctor={self.doctor}, date={self.date}, notes={self.notes})"


class MedicalRecord(Base):
    __tablename__ = 'medical_records'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient', backref='medical_records')
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    doctor = relationship('Doctor')
    diagnosis = Column(String(100))
    prescription = Column(String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
        }

    def __init__(self, patient, doctor, diagnosis, prescription):
        self.patient = patient
        self.doctor = doctor
        self.diagnosis = diagnosis
        self.prescription = prescription

    def __repr__(self):
        return f"MedicalRecord(id={self.id}, patient={self.patient}, doctor={self.doctor}, " \
               f"diagnosis={self.diagnosis}, prescription={self.prescription})"




if __name__ == '__main__':
    # Create the table in the database

	Base.metadata.create_all(engine)

    # Define other columns and relationships



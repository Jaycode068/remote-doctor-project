from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from flask_login import UserMixin


# Create the engine and session
engine = create_engine("mysql+mysqlconnector://johnson:Ibelieve1!@localhost:3306/remote_doctor")
Session = sessionmaker(bind=engine)

# Create the base class for models
Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True  # Assuming all users are authenticated

    @property
    def is_active(self):
        return True  # Assuming all users are active

    @property
    def is_anonymous(self):
        return False

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    specialty = Column(String(50))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(100))
    rating = Column(Float)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'rating': self.rating
        }

    def __init__(self, id, name, speciality, email, phone, address, rating):
        self.id = id
        self.name = name
        self.speciality = speciality
        self.email = email
        self.phone = phone
        self.address = address
        self.rating = rating

    def __repr__(self):
        return (
            f"Doctor(id={self.id}, name={self.name}, specialty={self.specialty}, "
            f"email={self.email}, phone={self.phone}, address={self.address}, rating={self.rating})"
        )


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    gender = Column(String(20))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(100))


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
	    'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
        }


    def __init__(self, name, age, gender, email, phone, address):
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.phone = phone
        self.address = address

    def __repr__(self):
        return f"Patient(id={self.id}, name={self.name}, age={self.age}, gender={self.gender}, email={self.email}, phone={self.phone}, address={self.address})"


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient', backref='appointments')
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    doctor = relationship('Doctor')
    date = Column(String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date': self.date,
        }

    def __init__(self, patient, doctor, date):
        self.patient = patient
        self.doctor = doctor
        self.date = date

    def __repr__(self):
        return f"Appointment(id={self.id}, patient={self.patient}, doctor={self.doctor}, date={self.date})"


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



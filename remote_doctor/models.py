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


class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    specialty = Column(String(50))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(100))
    username = Column(String(50))
    password = Column(String(100))

    def is_authenticated(self):
        # Implement the logic to determine if the doctor is authenticated
        return True  # or False based on your criteria

    def get_id(self):
        return str(self.id)

    def is_active(self):
        # Implement the logic to determine if the doctor is active
        return True  # or False based on your criteria    

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'username': self.username
        }

    @staticmethod
    def get_by_username(username):
        return Session().query(Doctor).filter_by(username=username).first()

    def check_password(self, password):
        # You might need to adjust this based on how passwords are stored and checked in your system
        return self.password == password
  
    def __init__(self, name, specialty, email, phone, address, username, password):
        self.name = name
        self.specialty = specialty
        self.email = email
        self.phone = phone
        self.address = address
        self.username = username
        self.password = password

    def __repr__(self):
        return (
            f"Doctor(id={self.id}, name={self.name}, specialty={self.specialty}, "
            f"email={self.email}, phone={self.phone}, address={self.address})"
        )


# ...

class Patient(Base, UserMixin):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    gender = Column(String(20))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(100))
    username = Column(String(50))
    password = Column(String(100))

    def is_authenticated(self):
        # Implement the logic to determine if the patient is authenticated
        return True  # or False based on your criteria

    def get_id(self):
        return str(self.id)
   
    def is_active(self):
        # Implement the logic to determine if the patient is active
        return True  # or False based on your criteria

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'username': self.username
        }

    @staticmethod
    def get_by_username(username):
        session = Session()
        patient = session.query(Patient).filter_by(username=username).first()
        session.close()
        return patient
    
    def check_password(self, password):
        # You might need to adjust this based on how passwords are stored and checked in your system
        return self.password == password
    
    def __init__(self, name, age, gender, email, phone, address, username, password):
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.phone = phone
        self.address = address
        self.username = username
        self.password = password
        
    def __repr__(self):
        return (
            f"Patient(id={self.id}, name={self.name}, age={self.age}, "
            f"gender={self.gender}, email={self.email}, phone={self.phone}, "
            f"address={self.address})"
        )



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
            'notes': self.note
        }

    def __init__(self, patient, doctor, date):
        self.patient = patient
        self.doctor = doctor
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



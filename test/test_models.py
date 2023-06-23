import pytest
from flask import url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from remote_doctor.models import Doctor, Patient, Appointment, MedicalRecord, User



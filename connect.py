from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, TIMESTAMP, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an engine and base class for ORM mappings
engine = create_engine('sqlite:///hospital_data.db')
Base = declarative_base()
metadata = MetaData()

# Define the Patients table model
class Patient(Base):
    __tablename__ = 'Patients'
    
    ID = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)

# Create the Patients table
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

def create_patient_table(patient_id):
    """
    Creates a real-time health data table for a specific patient.
    The table is named dynamically based on the patient ID (e.g., Patient_1234).
    """
    table_name = f"Patient_{patient_id}"
    
    # Define a dynamic table for the patient's real-time health data
    patient_table = Table(
        table_name, metadata,
        Column('reading_id', Integer, primary_key=True, autoincrement=True),
        Column('timestamp', TIMESTAMP, default=datetime.utcnow),
        Column('oxymeter', Float),
        Column('temperature', Float),
        Column('pressure', Float),
        Column('heart_rate', Float),
        extend_existing=True
    )
    # Create the patient's table in the database
    metadata.create_all(engine, tables=[patient_table])

# Example usage to add a new patient
def add_new_patient(patient_id, first_name, surname, date_of_birth):
    """
    Adds a new patient to the Patients table and creates a corresponding real-time data table.
    """
    # Add the patient to the Patients table
    new_patient = Patient(ID=patient_id, first_name=first_name, surname=surname, date_of_birth=date_of_birth)
    session.add(new_patient)
    session.commit()
    
    # Create a real-time data table for the new patient
    create_patient_table(patient_id)

# Function to insert real-time data for a patient
def insert_real_time_data(patient_id, oxymeter, temperature, pressure, heart_rate):
    """
    Inserts a new set of real-time readings into the patient's table.
    """
    table_name = f"Patient_{patient_id}"
    patient_table = Table(table_name, metadata, autoload_with=engine)
    
    # Insert real-time data for the patient
    ins = patient_table.insert().values(
        oxymeter=oxymeter,
        temperature=temperature,
        pressure=pressure,
        heart_rate=heart_rate
    )
    with engine.connect() as connection:
        connection.execute(ins)

# Close the session when done
def close_connection():
    session.close()

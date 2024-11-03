import sqlite3
from datetime import datetime

# Connect to the SQLite database 
conn = sqlite3.connect('hospital_data.db')
cursor = conn.cursor()

# Create the main Patients table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Patients (
        ID INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        surname TEXT NOT NULL,
        date_of_birth DATE NOT NULL
    )
''')
conn.commit()

def create_patient_table(patient_id):
    """
    Table for storing real-time health data for a specific patient.
    The table is named based on the patient ID (e.g., Patient_1234).
    """
    table_name = f"Patient_{patient_id}"
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            oxymeter REAL,
            temperature REAL,
            pressure REAL,
            heart_rate REAL
        )
    ''')
    conn.commit()

# Example usage
def add_new_patient(patient_id, first_name, surname, date_of_birth):
    """
    Adds a new patient to the Patients table and creates a corresponding real-time data table.
    """
    # Add the patient to the Patients table
    cursor.execute('''
        INSERT INTO Patients (ID, first_name, surname, date_of_birth)
        VALUES (?, ?, ?, ?)
    ''', (patient_id, first_name, surname, date_of_birth))
    conn.commit()
    
    # Create a real-time data table for the new patient
    create_patient_table(patient_id)

# Adding a new patient
# add_new_patient(1234, 'John', 'Doe', '1980-05-15')

# Function to insert real-time data for a patient
def insert_real_time_data(patient_id, oxymeter, temperature, pressure, heart_rate):
    """
    Inserts a new set of real-time readings into the patient's table.
    """
    table_name = f"Patient_{patient_id}"
    cursor.execute(f'''
        INSERT INTO {table_name} (oxymeter, temperature, pressure, heart_rate)
        VALUES (?, ?, ?, ?)
    ''', (oxymeter, temperature, pressure, heart_rate))
    conn.commit()

# Close the connection when done
def close_connection():
    conn.close()


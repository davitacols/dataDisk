"""
Generate mock patient dataset with 1000 records for testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Sample data
first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Barbara',
               'David', 'Elizabeth', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen',
               'Christopher', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra',
               'Donald', 'Ashley', 'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
              'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson']

diagnoses = ['Diabetes Type 2', 'Hypertension', 'Asthma', 'COPD', 'Coronary Artery Disease', 'Heart Failure',
             'Chronic Kidney Disease', 'Depression', 'Anxiety Disorder', 'Osteoarthritis', 'Rheumatoid Arthritis',
             'Hyperlipidemia', 'Obesity', 'Sleep Apnea', 'Atrial Fibrillation', 'Stroke', 'Cancer', 'Pneumonia',
             'UTI', 'Cellulitis', 'GERD', 'Migraine', 'Back Pain', 'Osteoporosis', 'Hypothyroidism']

cities = ['Boston', 'New York', 'Chicago', 'Los Angeles', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio',
          'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte',
          'San Francisco', 'Indianapolis', 'Seattle', 'Denver']

states = ['MA', 'NY', 'IL', 'CA', 'TX', 'AZ', 'PA', 'FL', 'OH', 'NC', 'WA', 'CO']

# Generate 1000 patient records
data = []

for i in range(1000):
    patient_id = f'P{str(i+1).zfill(4)}'
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    # Generate SSN
    ssn = f'{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}'
    
    # Generate DOB (ages 18-95)
    age = random.randint(18, 95)
    dob = datetime.now() - timedelta(days=age*365 + random.randint(0, 365))
    
    # Generate phone
    phone = f'555-{random.randint(100, 999)}-{random.randint(1000, 9999)}'
    
    # Generate email
    email = f'{first_name.lower()}.{last_name.lower()}{random.randint(1, 99)}@email.com'
    
    # Address
    street = f'{random.randint(100, 9999)} {random.choice(["Main", "Oak", "Maple", "Pine", "Elm", "Cedar"])} {random.choice(["St", "Ave", "Rd", "Blvd", "Dr"])}'
    city = random.choice(cities)
    state = random.choice(states)
    zip_code = f'{random.randint(10000, 99999)}'
    
    # Medical Record Number
    mrn = f'MRN{random.randint(100000, 999999)}'
    
    # Clinical data
    diagnosis = random.choice(diagnoses)
    visit_date = datetime.now() - timedelta(days=random.randint(0, 365))
    
    # Vital signs
    systolic = random.randint(90, 180)
    diastolic = random.randint(60, 110)
    blood_pressure = f'{systolic}/{diastolic}'
    
    heart_rate = random.randint(60, 100)
    temperature = round(random.uniform(97.0, 99.5), 1)
    weight_kg = round(random.uniform(50, 120), 1)
    height_cm = random.randint(150, 195)
    
    # Lab values
    glucose = random.randint(70, 200)
    cholesterol = random.randint(150, 300)
    
    data.append({
        'patient_id': patient_id,
        'first_name': first_name,
        'last_name': last_name,
        'ssn': ssn,
        'dob': dob.strftime('%Y-%m-%d'),
        'age': age,
        'phone': phone,
        'email': email,
        'street': street,
        'city': city,
        'state': state,
        'zip': zip_code,
        'mrn': mrn,
        'diagnosis': diagnosis,
        'visit_date': visit_date.strftime('%Y-%m-%d'),
        'blood_pressure': blood_pressure,
        'heart_rate': heart_rate,
        'temperature_f': temperature,
        'weight_kg': weight_kg,
        'height_cm': height_cm,
        'glucose_mg_dl': glucose,
        'cholesterol_mg_dl': cholesterol
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('mock_patient_data_1000.csv', index=False)

print(f"Generated {len(df)} patient records")
print(f"Saved to: mock_patient_data_1000.csv")
print(f"\nColumns: {len(df.columns)}")
print(f"PHI columns: first_name, last_name, ssn, dob, phone, email, street, city, zip, mrn")
print(f"Clinical columns: diagnosis, visit_date, blood_pressure, heart_rate, temperature_f, weight_kg, height_cm, glucose_mg_dl, cholesterol_mg_dl")
print(f"\nSample record:")
print(df.head(1).to_string())

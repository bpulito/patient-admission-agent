# Assisted by watsonx Code Assistant

import requests
import datetime
import json

# Flask server details
BASE_URL = "http://localhost:3000"

patient_id = "test_patient_123"

# Check bed availability
reservation_response = requests.get(
    f"{BASE_URL}/reservation/{patient_id}"
)

if reservation_response.status_code == 200:
    reservations = reservation_response.json().get('reservations', [])
    if len(reservations) > 0:
        print(f"Reservations for patient_id: {patient_id}: {reservations}")
    else:
        print("No reservations found.")
else:
    print("Failed to check availability:", reservation_response.text)

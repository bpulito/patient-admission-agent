# Assisted by watsonx Code Assistant

import requests
import datetime
import json

# Flask server details
BASE_URL = "http://localhost:3000"

# Patient details for reservation
patient_id = "test_patient_123"
first_name = "Test"
last_name = "User"

# Reservation details
start_date = datetime.date.today()  # Start reservation from today
length_of_stay = 4  # Reservation for 4 days

# Make a reservation
reservation_data = {
    'patient_id': patient_id,
    'first_name': first_name,
    'last_name': last_name,
    'start_date': start_date.isoformat(),
    'length_of_stay': length_of_stay
}

reserve_response = requests.post(
    f"{BASE_URL}/reservation",
    json=reservation_data
)

if reserve_response.status_code == 201:
    print("Reservation successful.")

    # Query to check if reservation exists
    check_reservation_response = requests.get(
        f"{BASE_URL}/check_availability",
        params={
            'start_date': start_date,
            'length_of_stay': length_of_stay
        }
    )

    if check_reservation_response.status_code == 200:
        bed_id = check_reservation_response.json().get('bed_id')
        if bed_id:
            print(f"Reservation for patient {patient_id} exists. bed_id is {bed_id}")
        else:
            print("Unexpected: No bed_id returned even though the reservation was successful.")
    else:
        print("Failed to check reservation status.")
else:
    print(f"Failed to make reservation: {reserve_response.text}")

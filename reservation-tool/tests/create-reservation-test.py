import requests
import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
TOOL_APIKEY = os.getenv('RESERVATION_TOOL_APIKEY')

# Flask server details
#BASE_URL = "http://localhost:4000"
BASE_URL = "https://reservation-system.13i6qeudn7sc.us-east.codeengine.appdomain.cloud"

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

# create the APIKEY header to use with the HTTP request.
headers = {
    'apikey': TOOL_APIKEY
}

reserve_response = requests.post(
    f"{BASE_URL}/reservation",
    headers=headers,
    json=reservation_data
)

if reserve_response.status_code == 201:
    print("Reservation successful.")

    # Query to check if reservation exists
    get_reservation_response = requests.get(
        f"{BASE_URL}/reservation/{patient_id}",
        headers=headers
    )

    if get_reservation_response.status_code == 200:
        reservations = get_reservation_response.json().get('reservations')

        if len(reservations) > 0:
            print(f"Reservation for patient {patient_id} exists.")
        else:
            print("Unexpected: No reservation docs found after successful creation of a reservation.")
    else:
        print("Failed to check reservation status.")
else:
    print(f"Failed to make reservation: {reserve_response.text}")

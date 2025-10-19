import requests
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
TOOL_BEARER_TOKEN = os.getenv('RESERVATION_TOOL_BEARER_TOKEN')

# Flask server details
#BASE_URL = "http://localhost:4000"
BASE_URL = "https://reservation-system.13i6qeudn7sc.us-east.codeengine.appdomain.cloud"

patient_id = "test_patient_123"

# create the APIKEY header to use with the HTTP request.
headers = {
    'Authorization': 'Bearer ' + TOOL_BEARER_TOKEN
}

# Check bed availability
reservation_response = requests.get(
    f"{BASE_URL}/reservation/{patient_id}",
    headers=headers
)

if reservation_response.status_code == 200:
    reservations = reservation_response.json().get('reservations', [])
    if len(reservations) > 0:
        print(f"Reservations for patient_id: {patient_id}: {reservations}")
    else:
        print("No reservations found.")
else:
    print("Failed to check availability:", reservation_response.text)

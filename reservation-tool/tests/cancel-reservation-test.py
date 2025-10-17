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

# create the APIKEY header to use with the HTTP request.
headers = {
    'apikey': TOOL_APIKEY
}

cancel_response = requests.delete(
    f"{BASE_URL}/reservation/{patient_id}",
    headers=headers
)

if cancel_response.status_code == 200:
    print("Cancel successful.")
else:
    print(f"Failed to cancel: {cancel_response.text}")

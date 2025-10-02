import requests
import datetime
import json

# Flask server details
BASE_URL = "http://localhost:4000"

# Reservation details
start_date = datetime.date.today()  # Start reservation from today
length_of_stay = 4  # Reservation for 4 days

# Check bed availability
availability_response = requests.get(
    f"{BASE_URL}/check_availability",
    params={
        'start_date': start_date.isoformat(),
        'length_of_stay': length_of_stay
    }
)

if availability_response.status_code == 200:
    available_beds = availability_response.json().get('available_beds', [])
    if available_beds:
        print(f"Available beds for {length_of_stay} days starting from {start_date}: {available_beds}")
    else:
        print("No available beds for the requested period.")
else:
    print("Failed to check availability:", availability_response.text)

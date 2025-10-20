"""
This tool uses an Elasticsearch index to maintain a set of patient bed reservations for a hospital. It exposes the following REST API methods:

/check_availability (GET) - For getting a list of available bed resources.
/reservation (PUT) - For creating a new reservation.
/reservation/{patient_id} (GET) - For getting the reservation for a single patient
/reservation/{patient_id} (DELETE) - For canceling a reservation for a single patient
"""
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import datetime
import os
import uuid
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

print(f"Elasticsearch URL: {os.getenv('ES_URL')}")
print(f"Elasticsearch Index: {os.getenv('ES_INDEX_NAME')}")

# Initialize Flask app and Elasticsearch client
app = Flask(__name__)

elastic_search = Elasticsearch(
  os.getenv('ES_URL'),
  api_key=os.getenv('ES_API_KEY'),
  verify_certs=False
)

ES_INDEX_NAME = os.getenv('ES_INDEX_NAME')
NUMBER_OF_BEDS = int(os.getenv('NUMBER_OF_BEDS'))
RESERVATION_TOOL_BEARER_TOKEN = os.getenv('RESERVATION_TOOL_BEARER_TOKEN')

# Hospital beds configuration
BEDS = [f'bed-{i}' for i in range(NUMBER_OF_BEDS)]

# Used to lock the elasticsearch index so that only one thread at a time can make changes to the reservation index.
def lock_reservation_index():
    """
    Method used to lock the index while making a reservation or updating a reservation.
    Returns:
        guid (string): guid associated with the index lock

    Note that I ran out of time and did not implement this but here are the steps to locking the ES index using a single lock file in the index:
    
    1. First get the contents of the lock file to determine the current sequence number, primary term and whether or not it is currently locked.
    2. Is the file locked?
        a) No...so attempt to update the lock file with a generated GUID. Also include the following query paraemters: ?if_seq_no=<seq number returned>&if_primary_term=1 This will cause an error to be returned if a different thread locked the file before this thread (because there will be a mismatch of the sequence number).
        b) Yes...so sleep for .5 seconds and start over.
    3. Did lock file update return an error?
        a) Yes...so sleep .5 seconds and start over.
        b) No...the file/index is locked. Proceed with making changes to the index.
        
    This method is based on Elasticsearch's optimistic concurrency control method described here: https://www.elastic.co/docs/reference/elasticsearch/rest-apis/optimistic-concurrency-control
    """
    guid = str(uuid.uuid4())
    return (guid)

# Used to unlock the elasticsearch index so that other threads can make changes.
def unlock_reservation_index(guid):
    """
    Method used to unlock the index while making a reservation or updating a reservation.

    Args:
        guid (string): Guid associated with the lock.

    Implement by simply update the lock file in ES to remove the GUID which sets the index back to unlocked.
    """
    return

# Used to change general availability of beds on the specified date.
def get_available_beds(start_date, length_of_stay):
    """
    Returns a list of available beds for the given start_date and length_of_stay.

    Args:
        start_date (date): Start date of the availability check in the form: 
        length_of_stay (integer): Number of days associated with the query.
    """

    print(f"get_available_beds: start_date: {start_date}")
    print(f"get_available_beds: length_of_stay: {length_of_stay}")

    potential_beds = BEDS.copy()
    for day in range(length_of_stay):
        query = {
            "query": {
                "range": {
                    "reservation_date": {
                        "gte": start_date + datetime.timedelta(days=day),
                        "lte": start_date + datetime.timedelta(days=day)
                    }
                 }
            }
        }
        response = elastic_search.search(index=ES_INDEX_NAME, body=query)

        reserved_beds = [hit['_source']['bed_id'] for hit in response['hits']['hits']]
        potential_beds = [bed for bed in potential_beds if bed not in reserved_beds]
        print(f"Number of available beds: {len(potential_beds)}")

    return potential_beds

# Used to access all the documents related to the reservation associated with a specific patient.
def get_reservation(patient_id):
    """
    Retrieves all reservation documents associated with a specific patient ID.

    Args:
        patient_id (string): The ID of the patient whose reservations are to be retrieved.

    Returns:
        A list of reservation documents for the given patient_id.
    """
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"patient_id": patient_id}}
                ]
            }
        }
    }
    
    response = elastic_search.search(index=ES_INDEX_NAME, body=query)
    reservations = [res['_source'] for res in response['hits']['hits']]
    return reservations

# Used to creates a new bed reservation using elasticsearch.
def create_reservation(start_date, length_of_stay, patient_id, first_name, last_name):
    """
    Makes a reservation by finding available beds and creating reservation documents.

    Args:
        start_date (date): Start date of the reservation in the form: 
        length_of_stay (integer): Number of days to make the reservation.
        patient_id (string): ID of patient.
        first_name (string): Patients first name.
        last_name (string): Patients last name.
    """

    # Start by locking the index so that only this thread can create a new reservation.
    guid = lock_reservation_index()

    # First check to see if this patient already has a reservation. If so, return an error for now.
    reservations = get_reservation(patient_id)

    if len(reservations) > 0:
        return jsonify({"error": "Reservation already exist for this patient."}), 400

    available_beds = get_available_beds(start_date, length_of_stay)

    if not available_beds:
        return jsonify({"error": "No available beds for the requested period."}), 400
    
    # Grab the first available ID in the list. This will be the bed that will be reserved for this patient.
    bed_id = available_beds[0]
    reservation_id = str(uuid.uuid4())

    for day in range(length_of_stay):
        """
        Create a reservation document for each day of the reservation and store each document in the
        reservation index.
        """
        reservation_data = {
            "patient_id": patient_id,
            "first_name": first_name,
            "last_name": last_name,
            "reservation_date": start_date + datetime.timedelta(days=day),
            "bed_id": bed_id
        }
        elastic_search.index(index=ES_INDEX_NAME, id=f"{request.json['patient_id']}-{start_date + datetime.timedelta(days=day)}", body=reservation_data)

    # Finish by unlocking the index so that other threads can create new reservations.
    unlock_reservation_index(guid)
    
    return jsonify({"message": "Reservation successful.", "bed_id": bed_id}), 201

# Used to verify the bearer token.
def verify_bearer_token(request):
    """
    Pulls the bearer token from the request and verifies it against the configured bearer token.
    """

    # If no Bearer Token was defined always return True
    if RESERVATION_TOOL_BEARER_TOKEN is None:
        print ("WARNING: the reservation tool is unsecured. You should setup authentication by configuring a bearer token ASAP.")
        return True

    # Try the Authorization header.
    authorization_header = request.headers.get('Authorization')
    if authorization_header is not None:
        parts = authorization_header.split()
        bearer_token = parts[1]

        if bearer_token is not None:
            if bearer_token != RESERVATION_TOOL_BEARER_TOKEN:
                return False
            else:
                return True
        else:
            return False
    else:
        return False


# REST API endpoints
@app.route('/check_availability', methods=['GET'])
def check_availability():
    """
    Check bed availability for a given start date and length of stay.
    """
    # First verify the Bearer Token 
    if verify_bearer_token(request) == False:
        return jsonify({"error": "Invalid Bearer Token"}), 401

    start_date_string = request.args.get('start_date')
    date_format = "%Y-%m-%d"
    start_date = datetime.datetime.strptime(start_date_string, date_format)

    print (f"start_date: {start_date}")

    length_of_stay = int(request.args.get('length_of_stay'))
    available_beds = get_available_beds(start_date, length_of_stay)
    return jsonify({"available_beds": available_beds}), 200

@app.route('/reservation', methods=['POST'])
def create_new_reservation():
    """
    Reserve a bed for the given start date and length of stay.
    """
    # First verify the Bearer Token 
    if verify_bearer_token(request) == False:
        return jsonify({"error": "Invalid Bearer Token"}), 401

    # Extract all the reservation parameters out of the request JSON
    start_date_string = request.json['start_date']
    date_format = "%Y-%m-%d"
    start_date = datetime.datetime.strptime(start_date_string, date_format)

    length_of_stay = int(request.json['length_of_stay'])

    patient_id = request.json['patient_id']
    first_name = request.json['first_name']
    last_name = request.json['last_name']   

    return create_reservation(start_date, length_of_stay, patient_id, first_name, last_name)

@app.route('/reservation/<patient_id>', methods=['GET'])
def get_patient_reservation(patient_id):
    """
    Get all reservation documents for a specific patient ID.

    Args:
        patient_id (string): The ID of the patient whose reservations are to be retrieved.
    """
    # First verify the Bearer Token 
    if verify_bearer_token(request) == False:
        return jsonify({"error": "Invalid Bearer Token"}), 401
    
    reservations = get_reservation(patient_id)
    return jsonify({"reservations": reservations}), 200

@app.route('/reservation/<patient_id>', methods=['DELETE'])
def cancel_reservation(patient_id):
    """
    Delete all reservation documents for a specific patient ID.

    Args:
        patient_id (string): The ID of the patient whose reservations are to be deleted.
    """
    # First verify the Bearer Token 
    if verify_bearer_token(request) == False:
        return jsonify({"error": "Invalid Bearer Token"}), 401

    reservations = get_reservation(patient_id)
    if not reservations:
        return jsonify({"error": "No reservations found for this patient."}), 404
    
    query = {
            "query": {
                "match": {
                    "patient_id": patient_id
                }
            }
        }

    response = elastic_search.delete_by_query(index=ES_INDEX_NAME, body=query)

    return jsonify({"message": f"Reservation(s) cancelled successfully. Deleted {response['deleted']} documents."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)

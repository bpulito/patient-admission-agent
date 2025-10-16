"""
This is a very simple function stub that returns two static patient profiles/records. It is designed to always return a valid record if an 8 digit patient ID and a properly formated date of birth are passed in the query.

This code can run as is as a serverless function in IBM cloud Code Engine.
"""
import os
import json

from datetime import datetime

DEBUG = True

def print_debug(text, data=None):
    if DEBUG:
        print(f'----------- {text} -----------')
        if data is not None:
            print(json.dumps(data, indent=4))
            
def verify_patient_id(n):
    if isinstance(n, int):
        return 10000000 <= n <= 99999999
    elif isinstance(n, str) and n.isdigit() and len(n) == 8:
        return 10000000 <= int(n) <= 99999999
    else:
        return False
           
def validate_dob(dob_string):
    try:
        datetime.strptime(dob_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def main(message):
    request = message
    
    print_debug ("Message object:", message)
    
    if 'patient_id' not in request or 'patient_DOB' not in request:
        return {
            "headers": {
                "Content-Type": "application/json",
            },
            "statusCode": 400,
            "body": {"error": "patient ID or patient date if birth not found"}
        }
    elif verify_patient_id(request['patient_id']) != True:
        return {
            "headers": {
                "Content-Type": "application/json",
            },
            "statusCode": 400,
            "body": {"error": "Invalid patient ID. Patient IDs should be an eight digit number."}
        }
    elif validate_dob(request['patient_DOB']) != True:
        return {
            "headers": {
                "Content-Type": "application/json",
            },
            "statusCode": 400,
            "body": {"error": "Invalid date of birth"}
        }

    response = {}
    '''
    This is where the patient profiles are returned. Note that the DOB passed in is always return as the DOB contained in the profile.
    '''
    if ('patient_id' in request and request['patient_id'] == '12345678'):
        response['patient_id'] = 12345678
        response['first_name'] = "Jim"
        response['last_name'] = "Briggs"
        response['date_of_birth'] = request['patient_DOB']
    else:
        response['patient_id'] = request['patient_id']
        response['first_name'] = "Jane"
        response['last_name'] = "Smith"
        response['date_of_birth'] = request['patient_DOB']
    
    print_debug ("Response object:", response)

    return {
        "headers": {
            "Content-Type": "application/json",
        },
        "statusCode": 200,
        "body": response
    }

# patient-profile-tool
This tool is a very simple python stub that serves up two patient profiles. The stub returns one profile for patient ID 12345678 and the other profile for any patient ID provided.

This is designed to run as a serverless function. I used IBM Code Engine to run the stub but any service than can host code and expose it on the public internet wil do. To read more about IBM Cloud Engine functions go [here](https://cloud.ibm.com/docs/codeengine?topic=codeengine-fun-work).

## Contents

- patient-profile-function.py: Python script to copy and paste into an IBM cloud function.
- patient-profile-tool-open-api.json: Open API script used to access this function. 

## Setup
After deploying the servless function be sure to update the OpenAPI script with the appropriate service URL.
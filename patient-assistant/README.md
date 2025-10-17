# patient-assistant
This directory contains the export of the patient-admission assistant. This JSON file can be uploaded into a watsonx Orchestrate Assistant Builder assistant and contains the complete definition of the assistant. watsonx Orchestrate Assistant Builder is a Conversational AI tool for creating AI assistants that are built on top of a classifier.

## Setup Instructions

Note that these instructions assume you have already created the two services that back this assistant. The instructions for setting up the two services can be found here:

- [reservation-tool](../reservation-tool)
- [patient-profile-tool](../patient-profile-tool)

Here are the instructions:

1. Go into the watonsx Orchestrate Assistant Builder. You can read more about the watosnx Orchestrate Assistant Builder [here](https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=building-ai-assistants).

2. Create a new Assistant.

3. Create the reservation tool extension. Here is the associated [reservation-tool OpenAPI script](../reservation-tool/reservation-tool-open-api.json). Note that you will need the APIKEY for this tool that was setup in the .env file for the tool service.

4. Create the patient profile tool extension. Here is the associated [patient-profile-tool OpenAPI script](../patient-profile-tool/patient-profile-tool-open-api.json). Any APIKEY will be used for this stub.

5. Import the Patient-Admissions-Assistant-action.json file to load the assistant.


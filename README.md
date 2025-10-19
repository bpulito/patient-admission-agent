# patient-admission-agent
This repo contains all the code needed to deploy a patient admissions/bed reservation management agent. The reservation system is built on an Elasticsearch index. Each reservation document represents a reservation for a single bed, for a single day, for a single patient. A reservation can span multiple days. For example, a single reservation that spans 4 days will result in 4 documents (JSON objects) stored in the index. The reservation system is fronted by a reservation-tool that is built in python. There is also a stubbed out python script that represents a patient record store. It serves up two static patient records. The assumption is that a separate process, not implemented in this repo, would be responsible for registering the patients records. The python stub is only used to verify that the patient exist.

This project contains the following two implementations of a patient admissions assistant and agent:

- **patient-assistant**: This assistant is built on a traditional Conversation AI plaform (watsonx Orchestrate Assistant Builder) which relies on a classifier and the two REST based services described above (reservation-tool and a patient-profile-tool). It provides fairly deterministic responses based on the following four intents: admit a patient, check availbility, check a reservation or cancel a reservation. This assistant can be accessed via webchat or via a phone number.

- **patient-agent**: This agent is built on a modern LangGrpah like platform (watsonx Orchestrate Agent Builder) which relies on an LLM (llama-3-2-90b-vision-instruct) and the two tools described above (reservation-tool and a patient-profile-tool). Note that the watsonx Orchestrate's agent builder spilts up the reservation tool into 4 different tools, one for each REST method in the tool. Because all orchestration is managed by an LLM, the responses from this agent are less deterministic but it is more flexible in the types of interactions it can handle.

Note that the two tools are integrated into the assistant and agent via OpenAPI scripts also included in this repo.

## Setup
There are a number of steps required to setup each of these assistants/agents. The following links point to README files that explain each aspect of the setup:

- [reservation-tool setup](./reservation-tool/README.md)
- [patient-profile-tool setup](./patient-profile-tool/README.md)
- [patient-assistant setup](./patient-assistant/README.md)
- [patient-agent setup](./patient-agent/README.md)

## Try the Patient Assistant

There are two ways to test the patient assistant:

I used the pre-built webchat client as a front-end digital channel to demonstrate the assistant:

- WebChat Demo: Click on the following [link](https://web-chat.global.assistant.watson.appdomain.cloud/preview.html?backgroundImageURL=https%3A%2F%2Fus-south.watson-orchestrate.cloud.ibm.com%2Fmfe_assistants%2Fpublic%2Fimages%2Fupx-4dd6daea-0f5d-4e88-91e3-fb58fc0290e6%3A%3A200d35c1-8665-46bb-9bd7-0c75586f256c&integrationID=cdcb6e0a-4b3e-4573-b8aa-3d3227390539&region=wxo-us-south&serviceInstanceID=4dd6daea-0f5d-4e88-91e3-fb58fc0290e6) and follow the script.

I used a Twilio SIP trunk to connect to a provisioned phone channel on the assistant:
- Voice Demo: Call **1-339-329-9194** and follow the script.

### Sample Script
Feel free to veer off from this script but this will help you get started working with the patient assistant. 

1. User: "I want to admit a patient."
2. Assistant: "What is your patient ID."
3. User: "The patient ID is 12345678."
4. Assistant: "What is the patient's date of birth?"
5. User: "The date of birth June 4, 1999 (any date will work)"
6. Assistant: "What is the start date of the reservation?"
7. User: "Two weeks from tomorrow."
8. Assistant: "What is the length of stay?"
9: User: "4 days"
10. Assistant: "Reservation was successful! Jim Briggs's reservation is for bed-1."

Note that if a reservation already exist you may get an error. If this happens you can say:

11. User: "I need to cancel that reservation."
12. Assistant: "To confirm, you wish to create a reservation for Jim Briggs who's patient ID is 12345678?"
13. User: "yes"
14. Assistant: "Patient reservation was successfully deleted. What else can I help you with?"

You can also test slot filling by saying something like:
1. User: "I need to admit patient 12345678. The patient's date of birth is June 4, 1999."

## Try the Patient Agent

The patient agent can be accessed from the following [webpage](./patient-agent/patient-agent-homepage.html).

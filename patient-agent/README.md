# patient-agent
This directory contains various files related to the patient admission agent that was created on watsonx Orchestrate. The agent is a combination of:

- The same tools used by the patient-assistant.
- A set of prompts used to define the behavior of the agent.
- An AI generated policy documented that is used for a RAG based search by the agent.

Here is a list of the included files and their role:

- **wxo-scripts** - These are various scripts that are used to run the watsonx Orchestrate ADK. These were used to interact with a WxO SaaS environment.
- **patient-agent.yaml** - This YAML file holds the complete definition of the patient-agent including all the related prompts.
- **patient-agent-homepage.html** - This HTML page loads up the patient admission agent demo.
- **Hospital Patient Admission Policy.pdf** - An AI generated policy document used as the basis for a RAG search in the assistant.
- **patient-agent-test-cases.csv** - Sample .csv file that contains a list of test cases that can be uploaded into watsonx Orchestrate.
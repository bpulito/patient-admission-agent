# wxo-scripts
These are various shell script used to setup all the agent related resources in the cloud (agent yaml that includes the prompts, tools, etc.) . They work with the watsonx Orchestrate Agent Developer Kit, which is a set of development tools for building out pro-code agents. Go [here](https://developer.watson-orchestrate.ibm.com/) to read more about the watsonx Orchestrate ADK.

This is the list of files and their purpose:

- **activate-ibm-cloud-env.sh**: used to active the SaaS environment where the agent resources are uploaded.
- **create-ibm-cloud-env.sh**: used to create the remote SaaS environment.
- **export-patient-agent.sh**: used to export the agent yaml from cloud. This is helpful for archiving when changes are made in the cloud agent builder.
- **import_tools.sh**: used to upload the tool OpenAPI scripts to the SaaS environment.

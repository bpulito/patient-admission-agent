# reservation-tool
This tool uses an Elasticsearch index to maintain a set of patient bed reservations for a hospital. It exposes the following REST API methods:

- /check_availability (GET) - For getting a list of available bed resources.
- /reservation (PUT) - For creating a new reservation.
- /reservation/{patient_id} (GET) - For getting the reservation for a single patient
- /reservation/{patient_id} (DELETE) - For canceling a reservation for a single patient

## Setup
1. The reservation-tool requires a **.env** file in the root tool directory. You can copy the .env-example to .env to get started. The .env will need to include the following variables:

| Variable Name | Details |
|---------------|---------|
| ES_INDEX_NAME | Elasticesearch index to be used in the scripts. |
| ES_API_KEY | The is your Elasticsearch API key. This is typically generated from a Kibana instance connected to your Elasticsearch DB. |
| ES_URL | Elastic search URL. If using IBM Cloud Databases, you can find this URL on the overview page (see the HTTPS tab). Note that the URL should include the username and password for your instance. |
| NUMBER_OF_BEDS | Number of bed resources that can be reserved. |
| RESERVATION_TOOL_BEARER_TOKEN | Bearer Token needed to access the reservation tool. |

2. Next create the Elasticsearch reservation index by running the **es-create-index.sh** script under./elastic-scripts.

### Test locally
You can run the reservation tool on your local machine by using pythin to start the reservation-tool script:
> python ./src/reservation-tool.py

### Run using Docker
To build and run docker image of reservation system, make sure you have docker installed and run these commands from the reservation-tool directory:
| Command | Details |
|---------|---------|
| docker build -t reservation-system . | Build the docker image |
| docker run -p 4000:4000 --name reservation-system reservation-system:latest | Startup the docker container on Intel hardware |

When running the docker image locally you may need to cleanup older containers and images at times. Use these commands to cleanup your environment:
| Command | Details |
|---------|---------|
| docker ps -a | Get list of containers and IDs |
| docker stop <container id> | Stop container |
| docker rm -f <container id> | Force remove container | 
| docker images | Get all images and IDs |
| docker rmi <image id> | Remove an image |

### Pushing docker image to Code Engine
To access the reservation tool from cloud you can use IBM code engine to run your docker image. These commands describe how to upload the reservation-tool docker image to the IBM cloud registr. 

| Command | Details |
|---------|---------|
| ibmcloud login --sso | Login to IBM cloud |
| ibmcloud cr login | Login to the IBM cloud container registry |
| docker tag reservation-system:latest us.icr.io/agent-demos/reservation-system:latest | First tag the image |
| docker push us.icr.io/agent-demos/reservation-system:latest | Now push the image to the IBM cloud registry |

At this point you will need to create an IBM Code Engine service to pull in the reservation-tool image and startup the container. To learn more about how to deploy apps in IBM Code Engine go [here](https://cloud.ibm.com/docs/codeengine?topic=codeengine-deploy-app&interface=ui).

**Note: All environment variables are still pulled from the .env file installed on the local Docker image. The proper way to do that is to put the environment variables into a docker-compose file and startup the container from compose.**

## Tool Limitations

1. A single patiant ID can only create one reservation within the solution. A patient's previous reservation must be deleted before a new one can be created.
2. Similar to a hotel room, the checkout date for the patient is not included in the reservation.

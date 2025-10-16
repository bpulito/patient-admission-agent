# reservation-tool
This tool uses an Elasticsearch index to maintain a set of patient bed reservations for a hospital.

## Setup
1. The reservation-tool requires an **.env** file in the root tool directory. You can copy the .env-example to .env to get started. The .env will need to include the following variables:

| Variable Name | Details |
|---------------|---------|
| ES_INDEX_NAME | Elasticesearch index to be used in the scripts. |
| ES_API_KEY | The is your Elasticsearch API key. This is typically generated from a Kibana instance connected to your Elasticsearch DB. |
| ES_URL | Elastic search URL. If using IBM Cloud Databases, you can find this URL on the overview page (see the HTTPS tab). Note that the URL should include the username and password for your instance. |
| NUMBER_OF_BEDS | Number of bed resources that can be reserved. |
| RESERVATION_TOOL_APIKEY | APIKEY needed to access the reservation tool. |

2. Next create the Elasticsearch reservation index by running the **es-create-index.sh** script under./elastic-scripts.

### Run python script locally
> python ./src/reservation-tool.py

### Run using Docker
To build and run docker image of reservation system, make sure you have docker installed and run these commands from the reservation-tool directory:
| Command | Details |
|---------|---------|
| docker build -t reservation-system . | Build the docker image |
| docker run -p 4000:4000 --name reservation-system reservation-system:latest | Startup the docker container on Intel hardware |

Cleanup commands:
| Command | Details |
|---------|---------|
| docker ps -a | Get list of containers and IDs |
| docker stop <container id> | Stop container |
| docker rm -f <container id> | Force remove container | 
| docker images | Get all images and IDs |
| docker rmi <image id> | Remove an image |

### Pushing docker image to Code Engine
| Command | Details |
|---------|---------|
| ibmcloud login --sso | Login to IBM cloud |
| ibmcloud cr login | Login to the IBM cloud container registry |
| docker tag reservation-system:latest us.icr.io/agent-demos/reservation-system:latest | First tag the image |
| docker push us.icr.io/agent-demos/reservation-system:latest | Now push the image to the IBM cloud registry |

**Note: All environment variables are still pulled from the .env file installed on the local Docker image. The proper way to do that is to put the environment variables into a docker-compose file and startup the container from compose.**

## Tool Limitations

1. A single patiant ID can only create one reservation within the solution. A patient's previous reservation must be deleted before a new one can be created.
2. Similar to a hotel room, the checkout date for the patient is not included in the reservation.

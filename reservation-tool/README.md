# reservation-tool
This tool uses an Elasticsearch index to maintain a set of patient bed reservations for a hospital.

## Setup
1. First create the Elasticsearch reservation index by running the **es-create-index.sh** script under./tests/elastic-scripts. The README.md in that directory explains how to setup the script.

2. The reservation-tool requires an **.env** file in the root tool directory. The .env will need to include the following variables:

| Variable Name | Details |
|---------------|---------|
| ES_INDEX_NAME | Elasticesearch index to be used in the scripts. |
| ES_API_KEY | The is your Elasticsearch API key. This is typically generated from Kibana |
| ES_URL | Elastic search URL. If using IBM Cloud Databases, you can find this URL on the overview page (see the HTTPS tab). Note that the URL should include the username and password for your instance. |
| NUMBER_OF_BEDS | Number of bed resources that can be reserved. |

## Tool Limitations

1. A single patiant ID can only create 1 reservation within the solution. A patient's previous reservation must be deleted before a new one can be created.
2. Similar to a hotel room, the checkout date for the patient is not included in the reservation.

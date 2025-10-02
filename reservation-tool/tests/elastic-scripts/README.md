# Elasticsearch Scripts
This directory holds a number of scripts that can be used to interact with a configured Elasticsearch index. 

## Setup
To run these scripts you will need to create a **.env** file in the directory that holds the scripts. The .env will need to include the following variables:

| Variable Name | Details |
|---------------|---------|
| INDEX_NAME | Elasticesearch index to be used in the scripts. |
| API_KEY | The is your Elasticsearch API key. This is typically generated from Kibana |
| ES_URL | Elastic search URL. If using IBM Cloud Databases, you can find this URL on the overview page (see the HTTPS tab). Note that the URL should include the username and password for your instance. |

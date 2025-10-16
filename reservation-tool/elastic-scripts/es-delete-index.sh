source ../.env
curl -k -X DELETE "${ES_URL}/${ES_INDEX_NAME}" \
    -H "Authorization: ApiKey "${ES_API_KEY}"" 

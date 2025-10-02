source ./.env
curl -k -X GET "${ES_URL}/${ES_INDEX_NAME}/_search" \
    -H "Authorization: ApiKey "${ES_API_KEY}"" \
    -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
        "must": [
            {"match": {"patient_id": "test_patient_123"}}
        ]
      }
  }
}
'

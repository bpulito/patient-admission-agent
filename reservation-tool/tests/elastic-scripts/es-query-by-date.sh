source ./.env
curl -k -X GET "${ES_URL}/${ES_INDEX_NAME}/_search" \
    -H "Authorization: ApiKey "${ES_API_KEY}"" \
    -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "reservation_date": {
        "gte": "2025-10-01",
        "lte": "2025-10-01"
      }
    }
  }
}
'

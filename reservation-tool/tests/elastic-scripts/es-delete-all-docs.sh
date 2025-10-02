source ../../.env
curl -k -X POST "${ES_URL}/${ES_INDEX_NAME}/_delete_by_query?pretty" \
    -H "Authorization: ApiKey "${ES_API_KEY}"" \
    -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  }
}
'

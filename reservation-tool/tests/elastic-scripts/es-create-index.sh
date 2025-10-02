source ./.env
curl -k -X PUT "${ES_URL}/${ES_INDEX_NAME}" \
    -H "Authorization: ApiKey "${ES_API_KEY}"" \
    -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "sort.field": "reservation_date", 
      "sort.order": "desc"  
    }
  },
  "mappings": {
    "properties": {
      "patient_id": {
        "type": "keyword"
      },
      "reservation_date": {
        "type": "date",
        "format": "strict_date_optional_time_nanos"
      },
      "first_name": {
        "type": "keyword"
      },
      "last_name": {
        "type": "keyword"
      },
      "bed_id": {
        "type": "keyword"
      }
    }
  }
}
'

curl -X 'POST' \
  'http://127.0.0.1:8080/api/settings/set_block_period' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "block_period": "2024-11-01"
}'

curl -X 'PUT' \
  'http://127.0.0.1:8080/api/api/nomenclature' \
  -H 'accept: text/html' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Творог",
  "full_name": "",
  "group_id": "",
  "range_id": ""
}'

curl -X 'PATCH' \
  'http://127.0.0.1:8080/api/api/nomenclature' \
  -H 'accept: text/html' \
  -H 'Content-Type: application/json' \
  -d '{
  "unique_code": "",
  "name": "",
  "full_name": "",
  "group_id": "",
  "range_id": ""
}'
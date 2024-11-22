curl -X 'POST' \
  'http://127.0.0.1:8080/api/get/transactions' \
  -H 'accept: text/html' \
  -H 'Content-Type: application/json' \
  -d '{
  "warehouse": {
    "name": "",
    "unique_code": "",
    "type": 2
  },
  "nomenclature": {
    "name": "Петр",
    "unique_code": "",
    "type": 2
  }
}'

curl -X 'GET' \
  'http://127.0.0.1:8080/api/api/report/osv?start_date=2024-05-05&end_date=2024-10-10&warehouse=BEST%20WAREHOUSE' \
  -H 'accept: application/json'

curl -X 'POST' \
  'http://127.0.0.1:8080/api/filter/range' \
  -H 'accept: text/html' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Гр",
  "unique_code": "",
  "type": 2
}'
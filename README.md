# Portfolio enrichment

Download 
Gathers data from EQS portfolio (+ divestments)


## Prerequisites
* python 3
* google account (and access to motherbrain-external-test bucket)

### Download proprietary data
``` shell
mkdir reference-data
gsutil cp gs://motherbrain-external-test/interview-test-org.json.gz  reference-data/
gsutil cp gs://motherbrain-external-test/interview-test-funding.json.gz reference-data/
```

### Run the process
```shell
pip install -r requirements.txt
python 
dt=$(date "+%Y-%m-%d")

python src/fetch_portfolio_data.py
python src/combine_sources.py --divestments output/divestments/$dt/output.json --portfolio output/portfolio/$dt/output.json  --organisation reference-data/interview-test-org.json.gz --funding reference-data/interview-test-funding.json.gz 

```


## Schemas

### "enriched" output

```json
[
  "_id",
  "city",
  "company_details",
  "company_name",
  "company_uuid",
  "country",
  "country_code",
  "date",
  "description",
  "employee_count",
  "entryDate",
  "exitDate",
  "founded_on",
  "fund",
  "funding_rounds",
  "funding_total_usd",
  "fundings",
  "homepage_url",
  "last_funding_on",
  "normalized_company_name",
  "path",
  "promotedSdg",
  "sdg",
  "sector",
  "short_description",
  "source_url",
  "title",
  "topic"
]
```

## Org data

```json
{
  "$schema": "http://json-schema.org/schema#",
  "type": "object",
  "properties": {
    "uuid": {
      "type": "string"
    },
    "company_name": {
      "type": "string"
    },
    "homepage_url": {
      "type": "string"
    },
    "country_code": {
      "type": "string"
    },
    "city": {
      "type": "string"
    },
    "founded_on": {
      "type": "string"
    },
    "short_description": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "funding_rounds": {
      "type": "string"
    },
    "funding_total_usd": {
      "type": "string"
    },
    "employee_count": {
      "type": "string"
    },
    "last_funding_on": {
      "type": "string"
    }
  },
  "required": [
    "city",
    "company_name",
    "country_code",
    "employee_count",
    "funding_rounds",
    "funding_total_usd",
    "homepage_url",
    "short_description",
    "uuid"
  ]
}

```

## funding data

```json
{
  "$schema": "http://json-schema.org/schema#",
  "type": "object",
  "properties": {
    "funding_round_uuid": {
      "type": "string"
    },
    "company_uuid": {
      "type": "string"
    },
    "company_name": {
      "type": "string"
    },
    "investment_type": {
      "type": "string"
    },
    "announced_on": {
      "type": "string"
    },
    "raised_amount_usd": {
      "type": "string"
    },
    "investor_names": {
      "type": "string"
    },
    "investor_count": {
      "type": "string"
    }
  },
  "required": [
    "announced_on",
    "company_name",
    "company_uuid",
    "funding_round_uuid",
    "investment_type",
    "investor_names"
  ]
}
```

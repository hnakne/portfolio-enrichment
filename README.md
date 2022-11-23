# tbd

## figure out schemas
``` shell
gsutil cp gs://motherbrain-external-test/interview-test-org.json.gz  reference-data/
gsutil cp gs://motherbrain-external-test/interview-test-funding.json.gz reference-data/
```

interview-test-org.json
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

funding
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

# Thailand Address Data

This repository contains data for Thailand address. The data is in JSON format.

## Data Structure

The data is structured as follows:

```json
{
  "province": {
    "name": "Province Name",
    "district": {
      "name": "District Name",
      "subdistrict": {
        "name": "Subdistrict Name",
        "zipcode": "Zip Code"
      }
    }
  }
}
```

## Query Data

You can query by zipcode using the following URL:

url: `/thai/api/address`

request:

````json
{
  "zipcode": "10200"
}

response:

```json
[
    {
        "id": 100101,
        "zipcode": "10200",
        "name": "พระบรมมหาราชวัง",
        "district": "เขตพระนคร",
        "province": "กรุงเทพมหานคร",
        "district_id": 1001,
        "province_id": 1
    },
    {
        "id": 100102,
        "zipcode": "10200",
        "name": "วังบูรพาภิรมย์",
        "district": "เขตพระนคร",
        "province": "กรุงเทพมหานคร",
        "district_id": 1001,
        "province_id": 1
    },
    ...
]
````

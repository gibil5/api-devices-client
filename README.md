# api-devices-client

[![Version](https://img.shields.io/badge/version-0.0.1-blue)](https://img.shields.io/badge/version-0.0.1-blue)
[![Maintainability](https://api.codeclimate.com/v1/badges/9ed5d6f56b4db526ecbb/maintainability)](https://codeclimate.com/repos/5f5a99eb03b2c5018b011671/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9ed5d6f56b4db526ecbb/test_coverage)](https://codeclimate.com/repos/5f5a99eb03b2c5018b011671/test_coverage)
[![Team](https://img.shields.io/badge/team-ite-orange)](https://img.shields.io/badge/team-ite-orange)

This client is meant to be used to query `api-devices` REST endpoints.

&nbsp;
## Installation


Add this to you python requirements:

    serverless-dd-forwarder==0.0.3

> The instalation and setup will be explained with the datadog 11 version.
> You should have the `datadog-lambda==2.13.0` previously defined

This package is stored in Gemfury. You'll need to add the gemfury index to 
your python requirements file. For that you can add: 

    --extra-index-url https://repo.fury.io/${FURY_AUTH}/electric/

The `FURY_AUTH` variable can be taken from [here](https://manage.fury.io/manage/electric/tokens/shared)

> You may need to add the PyPI index as a fallback
> 
> `--extra-index-url https://pypi.org/simple/`

&nbsp;
## Usage

```python
from devices.v2.client import DevicesV2API
from devices.v2.query import FilterByOperator

url = "https://devices-staging.electric.ai/staging"


customer_id = "a7e7c92f-46d7-4d69-9536-1fba38008962"
token = "your_auth0_token"
limit = 50
filters = {"gatekeeper": True}
filter_by_operator = "OR"

result = DevicesV2API(url=url, auth_token=token) \
    .get_devices(customer_id=customer_id) \
    .limit(limit=limit) \
    .after(after="") \
    .filter_by(**filters) \
    .filter_by_operator(operator=FilterByOperator.OR) \
    .all()
```


&nbsp;
## Development


### Setup 

You just have to Run:

    make init

> After the command is run, activate your virtual environment running
>
> `source venv/bin/activate` [linux]
> `.\venv\Scripts\activate.bat` [windows]


&nbsp;
### Test & Coverage

For running the tests:

    make test

For checking coverage:

    make coverage

&nbsp;
### Build

Run:

    make build

This will output a `gz` in the `/dist/` folder. Inside that folder
you'll find a file called `api-devices-client-{VERSION}.tar.gz`. This is the artifact that
we upload to gemfury



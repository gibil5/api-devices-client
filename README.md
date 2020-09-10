# api-devices-client

[![Version](https://img.shields.io/badge/version-0.0.1-blue)](https://img.shields.io/badge/version-0.0.1-blue)
[![CircleCI](https://circleci.com/gh/ElectricAI/api-devices-client.svg?style=svg&circle-token=6b1b7d4e6fe9e1758e8c1f10f6170ddf66341176)](https://circleci.com/gh/ElectricAI/api-devices-client)
[![Maintainability](https://api.codeclimate.com/v1/badges/9ed5d6f56b4db526ecbb/maintainability)](https://codeclimate.com/repos/5f5a99eb03b2c5018b011671/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9ed5d6f56b4db526ecbb/test_coverage)](https://codeclimate.com/repos/5f5a99eb03b2c5018b011671/test_coverage)
[![Team](https://img.shields.io/badge/team-ite-orange)](https://img.shields.io/badge/team-ite-orange)

This client is meant to be used to query `api-devices` REST endpoints.

&nbsp;
## Installation


Add this to you python requirements:

    api-devices-client==0.0.1


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
## Environments

| Stage      | Link                                                            |
| ---------- | --------------------------------------------------------------- |
| dev        | <https://qqsvee9xz7.execute-api.us-east-1.amazonaws.com/dev>        |
| staging    | <https://devices-staging.electric.ai/staging>    |
| production | <https://devices-prod.electric.ai/production> |




&nbsp;
## Development


### Pre requisites

- Install [Make](https://www.gnu.org/software/make)
- Obtain your [Gemfury Token](https://manage.fury.io/manage/electric/tokens/shared) (aka `FURY_AUTH`)

### Set your Gemfury token as an environment variable

For this step you must have already obtained your Gemfury token. Then create a new environment variable called `FURY_AUTH` and assign your Gemfury token to it so it will be available when running scripts from the terminal.

For this you have two options:

- Add it for your current terminal session (this must be repeated every time you want to use this variable):

  - *Linux/macOS*:

        export FURY_AUTH=<your_gemfury_token>

- Add the variable to your environment variables and restart your terminal (this won't require you to set it again):

  - *Linux/macOS*:

        Add `export FURY_AUTH=<your_gemfury_token>` to your `.bashrc`/`.zshrc` file.


### Initialize your development environment

Just run:

    make init


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

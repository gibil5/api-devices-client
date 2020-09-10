# api-devices-client

This client is meant to be used to query `api-devices` REST endpoints.
Import this library from Gemfury


Client usage example:

```python
from devices.client import DevicesAPI
from devices.query import Order, FilterByOperator


with DevicesAPI(url=DEVICES_URL, auth_token=AUTH_TOKEN) as api:
    response = api.get_devices(customer_id=CUSTOMER_ID) \
        .filter_by(healthy=True, filevault=False) \
        .filter_by_operator(FilterByOperator.OR) \
        .order_by(Order.ASCENDING, "os_version") \
        .all()
```

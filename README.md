### Datacube Economic Indexes - Microservice

This service will serve you an object containing all* economic products Product IDs and it's corresponding Datacube Indexes.

*New economic product might not be served since their format is not supported. 

## Supported Requests
#### Get list of all supported economic products (Product IDs) with corresponding Datacube Indexes.
##### GET /
Note that datacube index version in not implemented correctly yet.

Header:
```
{
    "authenticationToken": "..."
}
```

Example Response:
```
{
    "results": {
        "SK_AGR_CON_SAI_IN_D": [
            {
                "algorithm": "weighted_index_value_12d",
                "aoi_label": "in",
                "source": "rolling_activity_index_value_12d_sar_change_c_m2_construction",
                "version": "254"
            },
            {
                "algorithm": "weighted_index_value_24d",
                "aoi_label": "in",
                "source": "rolling_activity_index_value_24d_sar_change_c_m2_construction",
                "version": "254"
            },
            {
                "algorithm": "weighted_index_value_30d",
                "aoi_label": "in",
                "source": "rolling_activity_index_value_30d_sar_change_c_m2_construction",
                "version": "254"
            },
            ...
        ],
        "SK_AGR_MAN_SAI_GB_D": [...],
        "SK_AGR_MAN_SAI_IN_D": [...],
        ...
    },
    "status": "success"
}
```
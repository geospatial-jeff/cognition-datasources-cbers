[![CircleCI](https://circleci.com/gh/geospatial-jeff/cognition-datasources-cbers.svg?style=svg)](https://circleci.com/gh/geospatial-jeff/cognition-datasources-cbers)

## CBERS

| Parameter | Status |
| ----------| ------ |
| Spatial | :heavy_check_mark: |
| Temporal | :heavy_check_mark: |
| Properties | :heavy_check_mark: |
| **kwargs | [limit, subdatasets] |

* The `subdatasets` kwarg allows querying by sensor (mux, awfi, pan5m, and pan10m).

##### Properties
| Property | Type | Example |
|--------------------------|-------|-------------|
| eo:gsd | float | 20.0 |
| eo:epsg | int | 32614 |
| eo:platform | str | 'CBERS' |
| eo:sun_azimuth | float | 154.88 |
| eo:sun_elevation | float | 28.26 |
| eo:off_nadir | float | 0.004 |
| cbers:data_type | str | 'L2' |
| cbers:path | int | 229 |
| cbers:row | int | '48 |
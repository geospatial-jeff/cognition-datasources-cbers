import json
import requests
import copy

from datasources.stac.query import STACQuery
from datasources.sources.base import Datasource

class CBERS(Datasource):
    stac_compliant = True
    tags = ['EO', 'Satellite', 'Raster']

    def __init__(self, manifest):
        super().__init__(manifest)
        self.endpoint = 'https://earth-search.aws.element84.com/stac/search'

    def mux_configuration(self):
        return [
            {"name": "B5",
             "common_name": "blue",
             "gsd": 20,
             "center_wavelength": 0.485,
             "full_width_half_max": 0.035},
            {"name": "B6",
             "common_name": "green",
             "gsd": 20,
             "center_wavelength": 0.555,
             "full_width_half_max": 0.045},
            {"name": "B7",
             "common_name": "red",
             "gsd": 20,
             "center_wavelength": 0.66,
             "full_width_half_max": 0.03},
            {"name": "B8",
             "common_name": "nir",
             "gsd": 20,
             "center_wavelength": 0.83,
             "full_width_half_max": 0.06}
        ]

    def awfi_configuration(self):
        return [
            {"name": "B13",
             "common_name": "blue",
             "gsd": 20,
             "center_wavelength": 0.485,
             "full_width_half_max": 0.035},
            {"name": "B14",
             "common_name": "green",
             "gsd": 20,
             "center_wavelength": 0.555,
             "full_width_half_max": 0.045},
            {"name": "B15",
             "common_name": "red",
             "gsd": 20,
             "center_wavelength": 0.66,
             "full_width_half_max": 0.03},
            {"name": "B16",
             "common_name": "nir",
             "gsd": 20,
             "center_wavelength": 0.83,
             "full_width_half_max": 0.06}
        ]

    def pan10m_configuration(self):
        return [
            {"name": "B2",
             "common_name": "blue",
             "gsd": 10,
             "center_wavelength": 0.485,
             "full_width_half_max": 0.035},
            {"name": "B3",
             "common_name": "green",
             "gsd": 10,
             "center_wavelength": 0.555,
             "full_width_half_max": 0.045},
            {"name": "B4",
             "common_name": "red",
             "gsd": 10,
             "center_wavelength": 0.66,
             "full_width_half_max": 0.03}
        ]

    def pan5m_configuration(self):
        return [
            {"name": "B1",
             "common_name": "pan",
             "gsd": 5,
             "center_wavelength": 0.62,
             "full_width_half_max": 0.11}
        ]

    def search(self, spatial, temporal=None, properties=None, limit=10, **kwargs):
        stac_query = STACQuery(spatial, temporal)

        query_body = {
            'query': {},
            'intersects': stac_query.spatial,
            'limit': limit
        }

        if temporal:
            query_body.update({'time': "/".join([x.strftime("%Y-%m-%dT%H:%M:%S.%fZ") for x in stac_query.temporal])})

        if properties:
            for (k,v) in properties.items():
                query_body['query'].update({k:v})

        # If no subdatasets, query them all.
        if 'subdatasets' not in kwargs:
            kwargs.update({'subdatasets': ['mux', 'awfi', 'pan5m', 'pan10m']})

        for subdataset in kwargs['subdatasets']:
            copied = copy.deepcopy(query_body)
            copied['query'].update({
                'collection': {
                    'eq': f'cbers4-{subdataset}'
                }
            })
            self.manifest.searches.append([self, copied])

    def execute(self, query):
        headers = {
            "ContentType": "application/json",
            "Accept": "application/geo+json"
        }
        r = requests.post(self.endpoint, data=json.dumps(query), headers=headers)
        response = r.json()

        # Add band information
        for feat in response['features']:
            feat['properties'].update({
                'eo:bands': getattr(self, f'{feat["properties"]["collection"].split("-")[-1]}_configuration')()
            })

        return response
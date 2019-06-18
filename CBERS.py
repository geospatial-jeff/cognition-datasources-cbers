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
        return r.json()
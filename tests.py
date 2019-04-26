from datasources import tests
from shapely.geometry import Polygon

from CBERS import CBERS

class CBERSTestCases(tests.BaseTestCases):

    def _setUp(self):

        self.datasource = CBERS
        self.spatial = {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -102.74414062499999,
              47.18971246448421
            ],
            [
              -102.23876953125,
              47.18971246448421
            ],
            [
              -102.23876953125,
              47.517200697839414
            ],
            [
              -102.74414062499999,
              47.517200697839414
            ],
            [
              -102.74414062499999,
              47.18971246448421
            ]
          ]
        ]
      }
        self.temporal = ("2016-01-01", "2016-12-31")
        self.properties = {'eo:instrument': {'eq': 'PAN10M'}}
        self.limit = 1
        self.spatial_mode = 'extent'


    def test_limit(self):
        # Overwriting default limit test
        # Limit doesn't work with structure of underlying API
        pass


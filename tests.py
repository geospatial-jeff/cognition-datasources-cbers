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
                              -64.951171875,
                              -7.520426889868663
                            ],
                            [
                              -64.5172119140625,
                              -7.520426889868663
                            ],
                            [
                              -64.5172119140625,
                              -7.144498849647323
                            ],
                            [
                              -64.951171875,
                              -7.144498849647323
                            ],
                            [
                              -64.951171875,
                              -7.520426889868663
                            ]
                          ]
                        ]
                      }
        self.temporal = ("2016-01-01", "2016-12-31")
        self.properties = {'eo:instrument': {'eq': 'PAN10M'}}
        self.limit = 20

    def test_spatial_search(self):
        # Overwriting default spatial test (testing with item bbox rather than item geometry)
        self.manifest.flush()
        self.manifest['CBERS'].search(self.spatial)
        response = self.manifest.execute()
        self.assertEqual(list(response), ['CBERS'])

        # Confirming that each output feature intersects the input
        for feat in response['CBERS']['features']:
            asset_geom = Polygon([[feat['bbox'][0], feat['bbox'][3]],
                                  [feat['bbox'][2], feat['bbox'][3]],
                                  [feat['bbox'][2], feat['bbox'][1]],
                                  [feat['bbox'][0], feat['bbox'][1]],
                                  [feat['bbox'][0], feat['bbox'][3]]])

            self.assertEqual(asset_geom.intersects(self.spatial_geom), True)

    def test_limit(self):
        # Overwriting default limit test
        # Limit doesn't work with structure of underlying API
        pass


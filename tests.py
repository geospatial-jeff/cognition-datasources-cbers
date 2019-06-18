from datasources import tests

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
        self.properties = {'eo:sun_azimuth': {'gt': '169'}}
        self.limit = 5
        self.spatial_mode = 'extent'


    def test_subdatasets(self):
        self.manifest.flush()
        self.manifest[self.name].search(self.spatial, properties=self.properties, subdatasets=['mux'])
        response = self.manifest.execute()

        for feat in response[self.name]['features']:
            self.assertTrue(self.check_properties(feat['properties']['collection'], 'cbers-mux'))


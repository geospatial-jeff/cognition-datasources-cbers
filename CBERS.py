import json
import requests
import copy

import boto3

from datasources.stac.query import STACQuery
from datasources.sources.base import Datasource

s3 = boto3.client('s3')


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
        print(r.json())
        return r.json()

#
# class CBERS(Datasource):
#
#     stac_compliant = False
#     tags = ['EO', 'Satellite', 'Raster']
#
#     @staticmethod
#     def asset_path(item, band):
#         fname = f"CBERS_{item['version']}_{item['sensor']}_{item['acquisition_date']}_{item['path']}_{item['row']}_{item['processing_level']}_BAND{band}.tif"
#         return os.path.join('s3://', 'cbers-pds', item['key'], fname)
#
#     @staticmethod
#     def metadata_path(item, band):
#         fname = f"CBERS_{item['version']}_{item['sensor']}_{item['acquisition_date']}_{item['path']}_{item['row']}_{item['processing_level']}_BAND{band}.xml"
#         return os.path.join('s3://', 'cbers-meta-pds', item['key'], fname)
#
#     def __init__(self, manifest):
#         super().__init__(manifest)
#
#     def mux_configuration(self, item):
#         bands = [
#             {"name": "B5",
#              "common_name": "blue",
#              "gsd": 20,
#              "center_wavelength": 0.485,
#              "full_width_half_max": 0.035},
#             {"name": "B6",
#              "common_name": "green",
#              "gsd": 20,
#              "center_wavelength": 0.555,
#              "full_width_half_max": 0.045},
#             {"name": "B7",
#              "common_name": "red",
#              "gsd": 20,
#              "center_wavelength": 0.66,
#              "full_width_half_max": 0.03},
#             {"name": "B8",
#              "common_name": "nir",
#              "gsd": 20,
#              "center_wavelength": 0.83,
#              "full_width_half_max": 0.06}
#         ]
#
#         assets = {
#             "B5": {
#                 "href": self.asset_path(item, 5),
#                 "title": "Band 5 (Blue)",
#                 "eo:bands": [0]
#             },
#             "B5_meta": {
#                 "href": self.metadata_path(item, 5),
#                 "title": "Band 5 Metadata",
#                 "eo:bands": [0]
#             },
#             "B6": {
#                 "href": self.asset_path(item, 6),
#                 "title": "Band 6 (Green)",
#                 "eo:bands": [1]
#             },
#             "B6_meta": {
#                 "href": self.metadata_path(item, 6),
#                 "title": "Band 6 Metadata",
#                 "eo:bands": [1]
#             },
#             "B7": {
#                 "href": self.asset_path(item, 7),
#                 "title": "Band 7 (Red)",
#                 "eo:bands": [2]
#             },
#             "B7_meta": {
#                 "href": self.metadata_path(item, 7),
#                 "title": "Band 7 Metadata",
#                 "eo:bands": [2]
#             },
#             "B8": {
#                 "href": self.asset_path(item, 8),
#                 "title": "Band 8 (NIR)",
#                 "eo:bands": [3]
#             },
#             "B8_meta": {
#                 "href": self.metadata_path(item, 8),
#                 "title": "Band 8 Metadata",
#                 "eo:bands": [3]
#             },
#             "thumbnail": {
#                 "href": item['thumbURL'],
#                 "title": "Thumbnail"
#             },
#             "browseurl": {
#                 "href": item['browseURL'],
#                 "title": "BrowseURL"
#             }
#         }
#         return [bands, assets]
#
#     def awfi_configuration(self, item):
#         bands = [
#             {"name": "B13",
#              "common_name": "blue",
#              "gsd": 20,
#              "center_wavelength": 0.485,
#              "full_width_half_max": 0.035},
#             {"name": "B14",
#              "common_name": "green",
#              "gsd": 20,
#              "center_wavelength": 0.555,
#              "full_width_half_max": 0.045},
#             {"name": "B15",
#              "common_name": "red",
#              "gsd": 20,
#              "center_wavelength": 0.66,
#              "full_width_half_max": 0.03},
#             {"name": "B16",
#              "common_name": "nir",
#              "gsd": 20,
#              "center_wavelength": 0.83,
#              "full_width_half_max": 0.06}
#         ]
#
#         assets = {
#             "B13": {
#                 "href": self.asset_path(item, 13),
#                 "title": "Band 13 (Blue)",
#                 "eo:bands": [0]
#             },
#             "B13_meta": {
#                 "href": self.metadata_path(item, 13),
#                 "title": "Band 13 Metadata",
#                 "eo:bands": [0]
#             },
#             "B14": {
#                 "href": self.asset_path(item, 14),
#                 "title": "Band 14 (Green)",
#                 "eo:bands": [1]
#             },
#             "B14_meta": {
#                 "href": self.metadata_path(item, 14),
#                 "title": "Band 14 Metadata",
#                 "eo:bands": [1]
#             },
#             "B15": {
#                 "href": self.asset_path(item, 15),
#                 "title": "Band 15 (Red)",
#                 "eo:bands": [2]
#             },
#             "B15_meta": {
#                 "href": self.metadata_path(item, 15),
#                 "title": "Band 15 Metadata",
#                 "eo:bands": [2]
#             },
#             "B16": {
#                 "href": self.asset_path(item, 16),
#                 "title": "Band 16 (NIR)",
#                 "eo:bands": [3]
#             },
#             "B16_meta": {
#                 "href": self.metadata_path(item, 16),
#                 "title": "Band 16 Metadata",
#                 "eo:bands": [3]
#             },
#             "thumbnail": {
#                 "href": item['thumbURL'],
#                 "title": "Thumbnail"
#             },
#             "browseurl": {
#                 "href": item['browseURL'],
#                 "title": "BrowseURL"
#             }
#         }
#         return [bands, assets]
#
#     def pan10m_configuration(self, item):
#         bands = [
#             {"name": "B2",
#              "common_name": "blue",
#              "gsd": 10,
#              "center_wavelength": 0.485,
#              "full_width_half_max": 0.035},
#             {"name": "B3",
#              "common_name": "green",
#              "gsd": 10,
#              "center_wavelength": 0.555,
#              "full_width_half_max": 0.045},
#             {"name": "B4",
#              "common_name": "red",
#              "gsd": 10,
#              "center_wavelength": 0.66,
#              "full_width_half_max": 0.03}
#         ]
#
#         assets = {
#             "B2": {
#                 "href": self.asset_path(item, 2),
#                 "title": "Band 2 (Blue)",
#                 "eo:bands": [0]
#             },
#             "B2_meta": {
#                 "href": self.metadata_path(item, 2),
#                 "title": "Band 2 Metadata",
#                 "eo:bands": [0]
#             },
#             "B3": {
#                 "href": self.asset_path(item, 3),
#                 "title": "Band 3 (Green)",
#                 "eo:bands": [1]
#             },
#             "B3_meta": {
#                 "href": self.metadata_path(item, 3),
#                 "title": "Band 3 Metadata",
#                 "eo:bands": [1]
#             },
#             "B4": {
#                 "href": self.asset_path(item, 4),
#                 "title": "Band 4 (Red)",
#                 "eo:bands": [2]
#             },
#             "B4_meta": {
#                 "href": self.metadata_path(item, 4),
#                 "title": "Band 4 Metadata",
#                 "eo:bands": [2]
#             },
#             "thumbnail": {
#                 "href": item['thumbURL'],
#                 "title": "Thumbnail"
#             },
#             "browseurl": {
#                 "href": item['browseURL'],
#                 "title": "BrowseURL"
#             }
#         }
#         return [bands, assets]
#
#     def pan5m_configuration(self, item):
#         bands = [
#             {"name": "B1",
#              "common_name": "pan",
#              "gsd": 5,
#              "center_wavelength": 0.62,
#              "full_width_half_max": 0.11}
#         ]
#
#         assets = {
#             "B1": {
#                 "href": self.asset_path(item, 1),
#                 "title": "Band 1 (Panchromatic)",
#                 "eo:bands": [0]
#             },
#             "B1_meta": {
#                 "href": self.metadata_path(item, 1),
#                 "title": "Band 1 (Panchromatic)",
#                 "eo:bands": [0]
#             },
#             "thumbnail": {
#                 "href": item['thumbURL'],
#                 "title": "Thumbnail"
#             },
#             "browseurl": {
#                 "href": item['browseURL'],
#                 "title": "BrowseURL"
#             }
#         }
#         return [bands, assets]
#
#
#
#     def search(self, spatial, temporal=None, properties=None, limit=10, **kwargs):
#         from db import Database
#
#         stac_query = STACQuery(spatial, temporal, properties)
#
#         with Database.load(read_only=True, deployed=True) as db:
#             path_rows = db.spatial_query({"type": "Feature", "geometry": stac_query.spatial})
#
#         searches = 0
#         for candidate in path_rows:
#             query_body = {
#                 'path': candidate['PATH'],
#                 'row': candidate['ROW'],
#             }
#
#             if temporal:
#                 query_body.update({"temporal": stac_query.temporal})
#
#             if properties:
#                 query_body.update({"properties": stac_query})
#                 if "eo:instrument" in list(properties):
#                     query_body.update({"sensor": properties["eo:instrument"]})
#
#             if searches < limit:
#                 self.manifest.searches.append([self, query_body])
#                 searches+=1
#
#     def execute(self, query):
#         valid_list = []
#         sensor = query['sensor']['eq'] if 'sensor' in list(query) else 'MUX'
#         cbers_meta = cbers(query['path'], query['row'], sensor)
#
#         for idx, item in enumerate(cbers_meta):
#             approx_acquisition_date = f"{item['acquisition_date'][0:4]}-{item['acquisition_date'][4:6]}-{item['acquisition_date'][6:8]}"
#
#             if "temporal" in list(query):
#                 acquisition_date_time = datetime.strptime(approx_acquisition_date, "%Y-%m-%d")
#                 if not query['temporal'][0] < acquisition_date_time < query['temporal'][1]:
#                     continue
#
#             # Creating a STAC Item
#             stac_item = {
#                 "id": item['scene_id'],
#                 "type": "Feature",
#                 "geometry": {
#                     "type": "Polygon"
#                 },
#                 "properties": {
#                     "eo:platform": item['satellite'],
#                     "eo:instrument": item['sensor'],
#                     "legacy:path": item['path'],
#                     "legacy:row": item['row'],
#                     "legacy:processing_level": item['processing_level']
#                 },
#                 "assets": {
#                     "key": {
#                         "href": item['key'],
#                         "title": "Image Data (all bands)"
#                     },
#                     "thumbnail": {
#                         "href": item['thumbURL'],
#                         "title": "Thumbnail"
#                     },
#                     "browseurl": {
#                         "href": item['browseURL'],
#                         "title": "BrowseURL"
#                     }
#                 }
#             }
#
#             # Handling bands and assets for different sensors
#             bands, assets = getattr(self, item['sensor'].lower() + '_configuration')(item)
#             stac_item['properties'].update({'bands': bands})
#             stac_item.update({'assets': assets})
#
#             # Reading metadata
#             meta_key = [x for x in list(assets) if 'meta' in x][0]
#             md_key = '/'.join(assets[meta_key]['href'].split('//')[1].split('/')[1:])
#             md_obj = s3.get_object(Bucket="cbers-pds", Key=md_key, RequestPayer="requester")
#             metadata = md_obj['Body'].read().decode('utf-8')
#
#             # Stripping namespace
#             it = ET.iterparse(StringIO(metadata))
#             for _, el in it:
#                 if '}' in el.tag:
#                     el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
#             root = it.root
#
#             # Parsing metadata and appending to STAC item where appropriate
#             for image in root.findall('image'):
#                 for child in image:
#                     if child.tag == 'boundingBox' or child.tag == 'imageData':
#                         ul = [float(child[0].find('longitude').text), float(child[0].find('latitude').text)]
#                         ur = [float(child[1].find('longitude').text), float(child[1].find('latitude').text)]
#                         lr = [float(child[2].find('longitude').text), float(child[2].find('latitude').text)]
#                         ll = [float(child[3].find('longitude').text), float(child[3].find('latitude').text)]
#
#                         xmin = min(ul[0], ll[0])
#                         xmax = max(lr[0], ur[0])
#                         ymin = min(lr[1], ll[1])
#                         ymax = min(ul[1], ur[1])
#
#                         if child.tag == 'boundingBox':
#                             bbox = [xmin, ymin, xmax, ymax]
#                             stac_item.update({'bbox': bbox})
#                         elif child.tag == 'imageData':
#                             coordinates = [[ul, ur, lr, ll, ul]]
#                             stac_item['geometry'].update({'coordinates': coordinates})
#
#                     elif child.tag == 'timeStamp':
#                         stac_item['properties'].update({'datetime': child.find('center').text+'Z'})
#
#                     elif child.tag == 'verticalPixelSize':
#                         vertical_gsd = float(child.text)
#                     elif child.tag == 'horizontalPixelSize':
#                         horizontal_gsd = float(child.text)
#
#                     elif child.tag == 'sunPosition':
#                         stac_item['properties'].update({'eo:sun_elevation': float(child[0].text)})
#                         stac_item['properties'].update({'eo:sun_azimuth': float(child[1].text)})
#
#             # Update GSD
#             stac_item['properties'].update({'eo:gsd': (vertical_gsd + horizontal_gsd) / 2})
#
#             # Find EPSG of WGS84 UTM zone from centroid of bbox
#             centroid = [(stac_item['bbox'][1] + stac_item['bbox'][3]) / 2, (stac_item['bbox'][0] + stac_item['bbox'][2]) / 2]
#             utm_zone = utm.from_latlon(*centroid)
#             epsg = '32' + '5' + str(utm_zone[2]) if centroid[0] < 0 else '32' + '6' + str(utm_zone[2])
#             stac_item['properties'].update({'eo:epsg': int(epsg)})
#
#             if "properties" in list(query):
#                 if not query['properties'].check_properties(stac_item['properties']):
#                     continue
#
#             # Validate STAC item
#             STACItem.load(stac_item)
#
#             valid_list.append(stac_item)
#
#         return valid_list
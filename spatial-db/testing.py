import json

with open('cbers_reference.geojson', 'r') as infile:
    data = json.load(infile)
    out_data = {
        'type': 'FeatureCollection',
        'features': []
    }
    for idx, feat in enumerate(data['features']):
        feat['properties'].update({'id': idx})

        xvals = [x[0] for x in feat['geometry']['coordinates'][0]]
        yvals = [y[1] for y in feat['geometry']['coordinates'][0]]

        if max(xvals) < 180 and max(yvals) < 90 and min(xvals) > -180 and min(yvals) > -90:
            out_data['features'].append(feat)

    with open('cbers_reference_id.geojson', 'w') as outfile:
        json.dump(out_data, outfile)
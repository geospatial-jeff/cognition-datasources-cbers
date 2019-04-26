from datasources import Manifest

def CBERS(event, context):
    manifest = Manifest()
    manifest['CBERS'].search(**event)
    response = manifest.execute()
    return response



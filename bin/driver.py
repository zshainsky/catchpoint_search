# import the module
import time
import catchpoint
import frame

# overview: driver file -- define your catchpoint credentials;  -- a dictionary.

class CPDrive(object):

    def __init__(
            self
    ):
        self.credentials = None

    def retrieve_rd_wrapper(self):
        creds = {
            'client_id': 'F0-C-jSLj1VFDNy',
            'client_secret': '5a3663bd-e664-4af8-a6a3-d128ddb210f9',
            'refresh_token': 'None',
            'api_URIs': [
                {'token_uri': {
                    'hostname_prefix': 'ioqa.',
                    'path_template_arg1': 'HawkUI/',
                    'path_template_arg2': 'token/'
                }},
                {'endpoint_uri': {
                    'path_template_arg2': 'v1/nodes/'
                }}
            ]
        }

        creds_original = {
            'client_id': 'RY-Rc-jRiqNSLy7u',
            'client_secret': 'bbdab1dd-f0a4-4555-b8ed-4835a7b03c74',
            'refresh_token': 'None',
            'api_URIs': [
                {'token_uri': {
                    'hostname_prefix': 'io.',
                    'path_template_arg1': 'ui/',
                    'path_template_arg2': 'token/'
                }},
                {'endpoint_uri': {
                    'path_template_arg2': 'v1/performance/raw?tests=76386,81093'
                }}
            ]
        }

        creds = creds_original
        # force URIs developed to have the same beginning path
        creds['api_URIs'][1]['endpoint_uri']['hostname_prefix'] = creds['api_URIs'][0]['token_uri']['hostname_prefix']
        creds['api_URIs'][1]['endpoint_uri']['path_template_arg1'] = creds['api_URIs'][0]['token_uri']['path_template_arg1']

        raw_data = catchpoint.Catchpoint().raw(creds)
        mapped = frame.search(raw_data)
        return mapped


    
# for testing purposes only below:
# def getEvent(result):
#     event = {'_time': time.time(),  # {'start': str(result['_time']['start']), 'end': str(result['_time']['end'])},
#              'synthetic_metrics': result['synthetic_metrics'], 'host_Ip': str(result['host_Ip']),
#              'breakdown_2': {'id': str(result['breakdown_2']['id']), 'name': str(result['breakdown_2']['name'])},
#              'breakdown_1': {'id': str(result['breakdown_1']['id']), 'name': str(result['breakdown_1']['name'])},
#              'dimension': {'id': str(result['dimension']['id']), 'name': str(result['dimension']['name'])}}
#     return event
#
# rd = CPDrive().retrieve_rd_wrapper()
# for result in rd:
#     print getEvent(result)
#     print key
#     print
#     for element in key:
#         # if element['synthetic_metrics']:
#         #     pass
#         # print element['synthetic_metrics']
#         print element



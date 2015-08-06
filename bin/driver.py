# import the module
import time
import catchpoint
import frame
import json

# overview: driver file -- define your catchpoint credentials;  -- a dictionary.

class CPDrive(object):

    def __init__(
            self
    ):
        self.credentials = None

    # def retrieve_rd_wrapper(self):
    def retrieve_rd_wrapper(self, consumer_key, consumer_secret, test_id):
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
            'client_id': consumer_key, #'RY-Rc-jRiqNSLy7u',
            'client_secret': consumer_secret, #'bbdab1dd-f0a4-4555-b8ed-4835a7b03c74',
            'refresh_token': 'None',
            'api_URIs': [
                {'token_uri': {
                    'hostname_prefix': 'io.',
                    'path_template_arg1': 'ui/',
                    'path_template_arg2': 'token/'
                }},
                {'endpoint_uri': {
                    'path_template_arg2': '{0}/performance/raw?tests={1}' .format('v1', test_id) #76386,81093' 
                }}
            ]
        }

        creds = creds_original
        # force URIs developed to have the same beginning path
        creds['api_URIs'][1]['endpoint_uri']['hostname_prefix'] = creds['api_URIs'][0]['token_uri']['hostname_prefix']
        creds['api_URIs'][1]['endpoint_uri']['path_template_arg1'] = creds['api_URIs'][0]['token_uri']['path_template_arg1']

        raw_data = catchpoint.Catchpoint().raw(creds)
        mapped = frame.search(raw_data)  # unabridged, raw information
        return mapped

# for testing purposes only below:

# content = CPDrive().retrieve_rd_wrapper('RY-Rc-jSl18UYU23', '59d65360-9248-410e-a697-28e62b70054e', 81093)
# for index in content["detail"]:
#     metric = content["detail"][index]
#     # print metric
#     element = {'start': content['start'], 'end': content['end'], 'timezone': content['timezone'],
#            'breakdown_1': metric['breakdown_1'], 'breakdown_2': metric['breakdown_2'], 'dimension': metric['dimension'],
#            'host_Ip': metric['host_Ip'], 'synthetic_metric': metric['synthetic_metrics'] }
#     print '\n\n{0}: \n'.format(index), json.dumps(element, sort_keys=True, indent=4, separators=(',', ': '))

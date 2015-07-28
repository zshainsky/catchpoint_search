import sys
import base64
import json
import requests  # overview: importing the request module #note:install modules: C:\Python34\python setup.py install
# import requests_oauthlib
# from requests_oauthlib import OAuth2
# import ssl
# C:\Python34\py.exe
# https://pypi.python.org/pypi/requests-oauthlib
# from requests_oauthlib import OAuth2Session

class CatchpointError(Exception):
    pass


class Catchpoint(object):
    def __init__(
            self

    ):
        """
        Basic init method.

        """

        self.verbose = False
        self.token_uri = None
        self.endpoint_uri = None

        self.content_type = "application/json"
        self._auth = False
        self._token = None

    def _console_logger(self, msg, describe):
        """
        :param msg: "logs description and prim./user-defined objects (as json) to console"
        :return: void
        """
        # if type(msg).__name__ is 'dict':
        if describe is "":
            relay = "default: ".ljust(35)
        else:
            relay = describe.ljust(35)

        print("console log: ", relay, msg)

    def _debug(self, msg):
        """
        Debug output. Set self.verbose to True to enable.
        """
        if self.verbose:
            sys.stderr.write(msg + '\n')

    def _connection_error(self, e):
        msg = "Unable to reach {0}: {1}".format(self.host, e)
        sys.exit(msg)

    def _authorize(self, creds):
        """
        Request an auth token.

        - creds: dict with client_id and client_secret
        """

        self._debug("Creating auth url...")
        uri = self.token_uri

        payload = {
            'refresh_token': creds['refresh_token'],
            'grant_type': 'client_credentials',  # 'refresh_token',
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret']
        }

        # make request
        self._debug("Making auth request...")
        try:
            r = requests.post(str(uri), data=payload)
        except requests.exceptions.ConnectionError as e:
            self._connection_error(e)

        self._debug("URL: " + r.url)
        data = r.json()  # overview: return value is key/value pair json, accessible through array indexing

        self._token = data['access_token']  # ok! data is sent an access token
        self._debug(self._token)
        self._auth = True

    def _make_request(self, uri, params=None, data=None):
        """
        Make a request with an auth token.

        - uri: URI for the new Request object.
        - params: (optional) dict or bytes to be sent in the query string for the Request.
        - data: (optional) dict, bytes, or file-like object to send in the body of the Request.
        """
        self._debug("Making request...")
        headers = {
            'Accept': self.content_type,
            'Authorization': "Bearer " + base64.b64encode(

                self._token.encode('ascii')

            ).decode("utf-8")
        }

        try:
            r = requests.get(uri, headers=headers, params=params, data=data, verify=True)
            if r.status_code != 200:  # if not ok,  throw

                raise CatchpointError(r.content)
        except requests.ConnectionError as e:
            self._connection_error(e)

        self._debug("URL: (119) " + r.url)
        try:
            r_data = r.json()
        except TypeError as e:
            return e
        # print r_data
        return r_data

    def _expired_token_check(self, data):
        """
        Determine whether the token is expired. While this check could
        technically be performed before each request, it's easier to offload
        retry logic onto the script using this class to avoid too many
        req/min.

        - data: The json data returned from the API call.
        """
        if "Message" in data:
            if data['Message'].find("Expired token") != -1:
                self._debug("Token was expired and has been cleared, try again...")
                self._token = None
                self._auth = False

    def _develop_URIs(self, creds):
        """
            overview: provides an abstraction layer over uri construction.
            constructs URLs from the endpoint fragments in the correct format
            for the underlying calls to the REST API.
            structure: https://{0}catchpoint.com/{1}api/{ [options: select an endpoint] }
            @args:
            {0} = hostname_prefix

            path_template = "{1}api/{options}"
            {1} =  insert a valid string BEFORE 'api/' to access valid endpoint | empty string
            [options] = insert a valid string AFTER 'api/' to access valid endpoint | CANNOT be the empty string.
        """
        """ overview: build token uri: path construction: {0}api/{1} """
        path_template = "{0}api/{1}"
        path_arg1 = creds['api_URIs'][0]['token_uri']['path_template_arg1']
        path_arg2 = creds['api_URIs'][0]['token_uri']['path_template_arg2']
        token_path = path_template.format(path_arg1, path_arg2)

        hostname_prefix = creds['api_URIs'][0]['token_uri']['hostname_prefix']
        host = "https://{0}catchpoint.com/".format(hostname_prefix)
        self.token_uri = "{0}{1}".format(host, token_path)

        """ overview: build api endpoint uri: path construction too. """
        path_arg1 = creds['api_URIs'][1]['endpoint_uri']['path_template_arg1']
        path_arg2 = creds['api_URIs'][1]['endpoint_uri']['path_template_arg2']
        api_endpoint_path = path_template.format(path_arg1, path_arg2)
        self.endpoint_uri = "{0}{1}".format(host, api_endpoint_path)

    def raw(self, creds):
        """
        Retrieve raw performance chart data.
        """

        self._develop_URIs(creds)
        if not self._auth:
            self._authorize(creds)

        return self._make_request(self.endpoint_uri)

import sys
from splunklib.modularinput import *
import splunk.clilib.cli_common as cli_common
# import logging, time, httplib2
from catchpoint import *
from driver import *
import json


class MIClass(Script):
    # overview: writing errors to a log file to ensure that debugging
    # code doesn't interfere with Splunk's operations.
    # /Applications/Splunk/bin/splunk

    def setup_logging(self):
        pass

    def get_scheme(self):
        scheme = Scheme("Catchpoint Modular Input")

        scheme.description = "Stream specified test metrics into Splunk from Catchpoint"
        scheme.use_external_validation = True
        scheme.use_single_instance = True

        test_arg = Argument(
            name="test_id",
            description="The test ID(s)",
            # validation = "",
            data_type=Argument.data_type_number,
            required_on_edit=True,
            required_on_create=True
        )

        scheme.add_argument(test_arg)
        return scheme

    # overview: check against lamba -- the empty string, review more eloquent solutions later
    def validate_input(self, validation_definition):
        test_id = validation_definition.parameters["test_id"]

        if not test_id:
            raise ValueError("All fields must have a value")

    def stream_events(self, inputs, ew):
        # http = httplib2.Http('.cache')
        # overview @ .cache param -- https://github.com/jcgregorio/httplib2/#usage
        # The 'content' is the content retrieved from the URL
        # The 'resp' contains all the response headers
        # A 'source type' determines how Splunk Enterprise
        # formats the data during the indexing process.

        event_data = Event()
        event_data.index = "catchpoint"
        # event_data.sourcetype="json"
        #	index='catchpoint',  # assuming container element which holds all events.
        #	sourcetype='json'

        # Create driver class object
        cp_object = CPDrive()

        # Get data from the catchpoint configuration file at stanza [catchpoint_account]. This is configured in the setup ui: http://localhost:8000/en-US/manager/catchpoint_search/apps/local/catchpoint_search/setup?action=edit
        setup_input = cli_common.getConfStanza("catchpoint", "catchpoint_account")
        consumer_key = setup_input['client_key']
        consumer_secret = setup_input['client_secret']
        # Here we should be able to get the access_token that was set on the setup page. IS THIS NECESSARY??
        # access_token = setup_input['access_token']

        # Testing:
        # event_data.data = cp_object.retrieve_rd_wrapper('RY-Rc-jSl18UYU23', '59d65360-9248-410e-a697-28e62b70054e', 81093)
        # consider writing driver retrieve interface to accept variant key / secret / tests. -- update: done.

        for input_name, input_item in inputs.inputs.iteritems():
            test_id = input_item['test_id']

            event_data.stanza = input_name
            content = cp_object.retrieve_rd_wrapper(consumer_key, consumer_secret, test_id)
            # Must convert the Python Dictionary to a String for splunk to write to stdout and ingest data
            # json.dumps(content["detail"])
            for index in content["detail"]:
                metric = content["detail"][index]
                element = {'start': content['start'], 'end': content['end'], 'timezone': content['timezone'],
                           'breakdown_1': metric['breakdown_1'], 'breakdown_2': metric['breakdown_2'], 'dimension': metric['dimension'],
                           'host_Ip': metric['host_Ip'], 'synthetic_metric': metric['synthetic_metric'] }
                event_data.data = json.dumps(element, sort_keys=True)

                # Testing:
                # print event_data.data
                ew.write_event(event_data)

                # consider writing driver retrieve interface to accept variant key / secret / tests. -- update: done.
	# overview: writing errors to a log file to ensure that debugging
	# code doesn't interfere with Splunk's operations.
	# /Applications/Splunk/bin/splunk

	def setup_logging(self):
		pass

	def get_scheme(self):
		scheme = Scheme("Catchpoint Modular Input")

		scheme.description = "Stream specified test metrics into Splunk from Catchpoint"
		scheme.use_external_validation = True
		scheme.use_single_instance = True

		test_arg = Argument(
			name="test_id",
			description="The test ID(s)",
			# validation = "",
			data_type=Argument.data_type_number,
			required_on_edit=True,
			required_on_create=True
		)

		scheme.add_argument(test_arg)
		return scheme

	# overview: check against lamba -- the empty string, review more eloquent solutions later
	def validate_input(self, validation_definition):
		test_id = validation_definition.parameters["test_id"]

		if not test_id:
			raise ValueError("All fields must have a value")

	def stream_events(self, inputs, ew):
		# http = httplib2.Http('.cache')
		# overview @ .cache param -- https://github.com/jcgregorio/httplib2/#usage
		# The 'content' is the content retrieved from the URL
		# The 'resp' contains all the response headers
		# A 'source type' determines how Splunk Enterprise
		# formats the data during the indexing process.

		event_data = Event()
		event_data.index = "catchpoint"
		# event_data.sourcetype="json"
		#	index='catchpoint',  # assuming container element which holds all events.
		#	sourcetype='json'
		


		# Create driver class object
		cp_object = CPDrive()

		# Get data from the catchpoint configuration file at stanza [catchpoint_account]. This is configured in the setup ui: http://localhost:8000/en-US/manager/catchpoint_search/apps/local/catchpoint_search/setup?action=edit
		setup_input = cli_common.getConfStanza("catchpoint", "catchpoint_account")
		consumer_key = setup_input['client_id']
		consumer_secret = setup_input['client_secret']
		# Here we should be able to get the access_token that was set on the setup page. IS THIS NECESSARY??
		# access_token = setup_input['access_token']

		# Testing:
		# event_data.data = cp_object.retrieve_rd_wrapper('RY-Rc-jSl18UYU23', '59d65360-9248-410e-a697-28e62b70054e', 81093)
		# consider writing driver retrieve interface to accept variant key / secret / tests. -- update: done.

		for input_name, input_item in inputs.inputs.iteritems():
			test_id = input_item['test_id']

			event_data.stanza = input_name
			content = cp_object.retrieve_rd_wrapper(consumer_key, consumer_secret, test_id)
			# Must convert the Python Dictionary to a String for splunk to write to stdout and ingest data
			event_data.data = json.dumps(content)

			# Testing:
			# print event_data.data
			ew.write_event(event_data)

		# consider writing driver retrieve interface to accept variant key / secret / tests. -- update: done.

if __name__ == "__main__":
    sys.exit(MIClass().run(sys.argv))

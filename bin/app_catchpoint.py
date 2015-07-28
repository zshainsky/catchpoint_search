import sys
from splunklib.modularinput import *
# import logging, time, httplib2
from catchpoint import *
from driver import *

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

		# overview: defining 'arguments' below -- text fields which drive functionality
		consumer_key_arg = Argument(
			name="consumer_key",
			description="Receives client ID here.",
			# validation = "",
			data_type=Argument.data_type_string,
			required_on_edit=True,
			required_on_create=True
		)

		consumer_secret_arg = Argument(
			name="consumer_secret",
			description="Receives client secret here.",
			# validation = "",
			data_type=Argument.data_type_string,
			required_on_edit=True,
			required_on_create=True
		)

		test_arg = Argument(
			name="test_id",
			description="The test ID(s)",
			# validation = "",
			data_type=Argument.data_type_number,
			required_on_edit=True,
			required_on_create=True
		)

		scheme.add_argument(consumer_key_arg)
		scheme.add_argument(consumer_secret_arg)
		scheme.add_argument(test_arg)
		return scheme

	# overview: check against lamba -- the empty string, review more eloquent solutions later
	def validate_input(self, validation_definition):
		consumer_key = validation_definition.parameters["consumer_key"]
		consumer_secret = validation_definition.parameters["consumer_secret"]
		test_id = validation_definition.parameters["test_id"]

		if not consumer_key or not consumer_secret or not test_id:
			raise ValueError("All fields must have a value")

	def stream_events(self, inputs, ew):
		# http = httplib2.Http('.cache')
		# overview @ .cache param -- https://github.com/jcgregorio/httplib2/#usage
		# The 'content' is the content retrieved from the URL
		# The 'resp' contains all the response headers
		# A 'source type' determines how Splunk Enterprise
		# formats the data during the indexing process.

		event_data = Event(
			index='catchpoint',  # assuming container element which holds all events.
			sourcetype='json'
		)

		cp_object = CPDrive()
		event_data.data = cp_object.retrieve_rd_wrapper('RY-Rc-jSl18UYU23', '59d65360-9248-410e-a697-28e62b70054e', 81093)
		print event_data.data
		# consider writing driver retrieve interface to accept variant key / secret / tests. -- update: done.

		for input_name, input_item in inputs.inputs.iteritems():
			consumer_key = input_item['consumer_key']
			consumer_secret = input_item['consumer_secret']
			test_id = input_item['test_id']

			cp_object = CPDrive()

			event_data.stanza = input_name
			# event_data.data = cp_object.retrieve_rd_wrapper(consumer_key, consumer_secret, test_id)
			ew.write_event(event_data)

		# consider writing driver retrieve interface to accept variant key / secret / tests. -- update: done.

if __name__ == "__main__":
	sys.exit(MIClass().run(sys.argv))

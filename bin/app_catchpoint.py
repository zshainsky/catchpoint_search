import sys
from splunklib.modularinput import *
import logging, time, httplib2 
from catchpoint import *
from driver import *

class MIClass(Script):
	
	''' overview: writing errors to a log file to ensure that debugging 
	code doesn't interfere with Splunk's operations. 
	'''
	def setup_logging():
		pass
		
	def get_scheme(self):
		scheme = Scheme("Catchpoint/Splunk Modular Input")
		
		scheme.description = "Stream specified test metrics into Splunk from Catchpoint"
		scheme.use_external_validation = True
		scheme.use_single_instance = True
		
		# overview: defining 'arguments' below -- text fields which drive functionailty
		consumer_key_arg = Argument(
			name = "consumer_key",
			description = "Recieves client ID here.",
			# validation = "",
			data_type=Argument.data_type_string,
			required_on_edit=True,
			require_on_create=True
		)
		
		consumer_secret_arg = Argument(
			name= "consumer_secret",
			description = "Recieves client secret here."
			# validation = "",
			data_type = Argument.data_type_string,
			required_on_edit = True,
			require_on_create = True
		)
		
		test_arg = Argument(
			name = "test_id",
			description = "The test ID(s)",
			# validation = "",
			data_type = Argument.data_type_number,
			required_on_edit = True,
			require_on_create = True
		)
		

	# overview: check against lamba -- the empty string, review more eloquent solutions later 
	def validate_input(self, validation_definiton):
		consumer_key = validation_definiton.parameters["consumer_key"]
		consumer_secret = validation_definiton.parameters["consumer_secret"]
		test_id = validation_definiton.parameters["test_id"]
		
		if not consumer_key or not consumer_secret or not test_id:
			raise ValueError("All fields must have a value")
			
	def stream_events(self, inputs, ew):
		http = httplib2.Http('.cache')
		# overview @ .cache param -- https://github.com/jcgregorio/httplib2/#usage
		# The 'content' is the content retrieved from the URL
		# The 'resp' contains all the response headers
		# A 'source type' determines how Splunk Enterprise 
		# formats the data during the indexing process.

		event_data= Event(
			index = 'catchpoint', # assuming container element which holds all events.
			sourceType = 'json'
		)
		
		for input_name, input_item in inputs.inputs.iteritems():
			consumer_key = input_item['consumer_key']
			consumer_secret = input_item['consumer_secret']
			test_id = input_item['test_id']
			
			# consider writing driver retrieve interface to accept variant key / secret / tests.
			
			
			

			
		
		
		
		
		
		
		
		
				

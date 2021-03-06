#print "Starting Catchpoint_setup.py Script"
import splunk.admin as admin
import splunk.entity as en

import splunk
import sys, os
import os.path as op
import logging, logging.handlers
sys.path.append(op.join(op.dirname(op.abspath(__file__)), ""))
from catchpoint import *
from driver import *
import json
# import your required python modules

'''
Copyright (C) 2005 - 2010 Splunk Inc. All Rights Reserved.
Description:  This skeleton python script handles the parameters in the configuration page.

      handleList method: lists configurable parameters in the configuration page
      corresponds to handleractions = list in restmap.conf

      handleEdit method: controls the parameters and saves the values 
      corresponds to handleractions = edit in restmap.conf

'''
def setup_logger(fileName):
  logger = logging.getLogger('splunk.%s' % fileName)
  SPLUNK_HOME = os.environ['SPLUNK_HOME']

  LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
  LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
  LOGGING_STANZA_NAME = 'python'
  LOGGING_FILE_NAME = fileName
  BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
  LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
  splunk_log_handler = logging.handlers.RotatingFileHandler(os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a')
  splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
  logger.addHandler(splunk_log_handler)
  splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
  return logger
logger = setup_logger("catchpoint_setup.log")
logger.info("*******************************")

class ConfigApp(admin.MConfigHandler):
  catchpoint_args = ("url", "client_id", "client_secret", "access_token")
  cp = catchpoint.Catchpoint()
  
  '''
  Changes argument format from how it is received from the web form to match the expexted creds format from: catchpoint.py _authorize(self, creds)
  '''
  def changeArgsFormat(self, args):
    logger.info("Changing Args...")
    logger.info(args)
    tempArgs = {}
    for arg in self.catchpoint_args:
      if arg == "access_token":
        tempArgs["refresh_token"] = ""
        logger.info("refresh Token=")
        logger.info(tempArgs["refresh_token"])
      else:
        tempArgs[arg] = args[arg][0]
        logger.info("Other Args: ")
        logger.info(arg)
        logger.info(tempArgs[arg])

    tempArgs['api_URIs'] = [
                {'token_uri': {
                    'hostname_prefix': 'io.',
                    'path_template_arg1': 'ui/',
                    'path_template_arg2': 'token/'
                }},
                {'endpoint_uri': {
                    'path_template_arg1': '',
                    'path_template_arg2': ''
                }}
                ]

    logger.info(tempArgs)
    return tempArgs
  
  '''
  Get Access_token from form input
  '''
  def requestToken(self, args):
    # Create Driver and Catchpoint class objects
    catchpoint = Catchpoint()
    cp_object = CPDrive()

    # Change args to proper format
    creds = self.changeArgsFormat(args)
    logger.info("Authorizing...")
    # Sets _token variable in Catchpoint() class
    catchpoint._develop_URIs(creds)
    catchpoint._authorize(creds)
    logger.info("Authoization complete: New Authtoken Generated. Token=")
    logger.info(catchpoint._token)
    return catchpoint._token

  '''
  Set up supported arguments
  '''
  def setup(self):
    if self.requestedAction == admin.ACTION_EDIT:
      logger.info("Setup admin.action_edit")
      for arg in self.catchpoint_args:
        #print arg
        self.supportedArgs.addOptArg(arg)
    else:
      logger.info("Setup admin.action_list")
        
  '''
  Read the initial values of the parameters from the custom file
      myappsetup.conf, and write them to the setup screen. 

  If the app has never been set up,
      uses .../<appname>/default/myappsetup.conf. 

  If app has been set up, looks at 
      .../local/myappsetup.conf first, then looks at 
  .../default/myappsetup.conf only if there is no value for a field in
      .../local/myappsetup.conf

  For boolean fields, may need to switch the true/false setting.

  For text fields, if the conf file says None, set to the empty string.
  '''

  def handleList(self, confInfo):
    confDict = self.readConf("catchpoint")
    if None != confDict:
      for stanza, settings in confDict.items():
        for key, val in settings.items():
          if key in self.catchpoint_args:
            if val is None:
              val = ''
            confInfo[stanza].append(key, val)
      # Reset access_token to "". This never allows access_token to be set. Keep disabled.
      # confInfo["catchpoint_account"].append("access_token","")

          
  '''
  After user clicks Save on setup screen, take updated parameters,
  normalize them, and save them somewhere
  '''
  def handleEdit(self, confInfo):
    logger.info("Editing...")
    name = self.callerArgs.id
    args = self.callerArgs.data
    # String type expected. Will throw error if None type is found
    for arg in self.catchpoint_args:
      if args.get(arg, None) and args[arg][0] is None:
        args[arg][0] = ""

    # Request Token and store it in "access_token" config variable
    returnedToken = self.requestToken(args)    

    # TESTING: 
    # returnedToken = "temporary_token"
    
    if returnedToken:
      logger.info("returned token.......")
      args["access_token"][0] = returnedToken
    
    logger.info("access_token=")
    logger.info(args["access_token"][0])
    '''
    Since we are using a conf file to store parameters, 
write them to the [setupentity] stanza
    in <appname>/local/myappsetup.conf  
    '''
    
    self.writeConf('catchpoint', 'catchpoint_account', self.callerArgs.data)
      
# initialize the handler
admin.init(ConfigApp, admin.CONTEXT_NONE)
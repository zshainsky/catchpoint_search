#!/usr/bin/env python

# | catchpoint term=""

import os, sys, time, requests, oauth2, json, urllib
import driver

from splunklib.searchcommands import \
  dispatch, GeneratingCommand, Configuration, Option, validators


@Configuration()
class CPCommand(GeneratingCommand):
  term = Option(require=False)


  def generate(self):

    rd = driver.CPDrive().retrieve_rd_wrapper()


    for key in rd:
        result = key 
        yield self.getEvent(result)

  def getEvent(self, result):
    event = {'_time': time.time(),  # {'start': str(result['_time']['start']), 'end': str(result['_time']['end'])},
             # time metrics,
             'synthetic_metrics': result['synthetic_metrics'], 'host_Ip': str(result['host_Ip']),
             'breakdown_2': {'id': int(str(result['breakdown_2']['id'])), 'name': str(result['breakdown_2']['name'])},
             'breakdown_1': {'id': int(str(result['breakdown_1']['id'])), 'name': str(result['breakdown_1']['name'])},
             'dimension': {'id': int(str(result['dimension']['id'])), 'name': str(result['dimension']['name'])}}
    return event

dispatch(CPCommand, sys.argv, sys.stdin, sys.stdout, __name__)

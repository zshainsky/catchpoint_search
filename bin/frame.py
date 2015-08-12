'''
    Author: Catchpoint Systems, All Rights Reserved.
    Raw Data Mapping Algorithm and Implementation for Splunk-Catchpoint Integration
'''
'''
@param x:
    represents one of the five keys being sent into the function for evaluation.
@param data:
    represents the data structure (a dictionary) containing values
@elements:
    elements = ['synthetic_metrics', 'host_Ip', 'breakdown_2', 'breakdown_1', 'dimension']
overview:
    this function can be considered as the driver for performing the mapping of values
    contained within the 'detail' index.
'''
def init_map(data, LENGTH, blueprint, values_list, elements):
    an_item = {}

    '''
    overview: for each key (otherwise known as variable x), create a new key/value pair within the dictionary named 'an_item'
    through the process of case matching. if match is found, index into the value_collection at element x
    and return. The return value will become the 'value' field within the new key/value pair structure we are constructing.

    ### notes ###
    an_item: a mapped dictionary which resides under the parent key -- 'detail'
    an_item[x] = ...: adds a new key/value pair into the dictionary 'an_item'
    '''
    for x in elements:
        an_item[x] = case_match_metrics(x, data, LENGTH, blueprint, values_list)
    return an_item

'''
@param LENGTH:
    represents the length of value_collection dictionary indexed at 'synthetic_metric' --
    hence, LENGTH can be described as the length of the synthetic_metric array
    note: value_collection is simply a large array filled entirely of values. more pointedly, 
    value_collection contains all the values to be mapped. it is extracted from the following structure.
    {
    start : ..
    end : ..
    timezone : ..
    detail : {
            fields : blueprint located here.
            items : value_collection located here.
        }
    }

@param blueprint:
    represents a dictionary of 'key/value pairs' -- otherwise known as a dictionary of dictionaries.
    we use blueprint to index into 'synthetic_metrics' dictionary.
    blueprint['synthetic_metrics'] represents the place-holding structure (dictionary) we will use as a scaffold to build our
    desired mapping with the values held in the value_collection dictionary
    indexing in once more to the 'name' field , we use the value of blueprint['synthetic_metrics']['name'] to represent the keys
    of the synthetic_metrics dictionary within the brand new data structure we are constructing.
@param value_collection_AT_synthetic_metrics_INDEX:
    note: value_collection is an array of dictionaries, all containing the values to be mapped for the parent key 'detail'. 
    value_collection['at some arbitrary array index']['synthetic_metrics'] fetches a singular synthetic_metrics array holding 
    only synthetic_metrics values produced from making a get request to the Catchpoint API tests endpoint. 
Logic: If we iterate through the 'value_collection_AT_synthetic_metrics_INDEX' array while, at the same time, iterating through the blueprint structure at the desired indices, we are able to perform dynamic mappings across all synthetic_metrics values.
'''
def map_synthetic(LENGTH, blueprint, value_collection_AT_synthetic_metrics_INDEX):
    synthetic_metrics_structure = [] # push new elements to dictionary.
    for index in range(LENGTH):  # length of synth. field array
        key = blueprint[index]['name']
        value = str(value_collection_AT_synthetic_metrics_INDEX[index])
        synthetic_metrics_structure.append({str(key): value})  #
    return synthetic_metrics_structure


''' 
@param x: 
    represents one of the three keys being sent into the function for evaluation.
@param data:
    represents the data structure (a dictionary) containing values
Logic: If we were to index into the data structure, 'data' at 'x' (data[x]),
the information fetched can then be set as the value field of a 'key/value pair' which sits within 
the new data structure we are building.
'''
def case_match_main(x, data):
    return {
        'start': str(data[x]),
        'end': str(data[x]),
        'timezone': data[x]
    }.get(x, None)

''' 
@param x: 
    represents one of the five keys being sent into the function for evaluation.
@param data:
    represents the data structure (a dictionary) containing values
@other parameters: 
    see map_synthetic function above for more information.
Logic: If we were to index into the data structure, 'data' at 'x' (data[x]),
the information fetched can then be set as a value field of 'key/value' object within a brand new data structure.

returns JSON, an array or a string value.
'''
def case_match_metrics(x, data, LENGTH, blueprint, values_list):
    return {
        'synthetic_metrics': map_synthetic(LENGTH, blueprint, values_list),
        'host_Ip': data[x],
        'breakdown_2': data[x],
        'breakdown_1': data[x],
        'dimension': data[x]
    }.get(x, None)

'''
overview: sifts through the 'detail' construct, returns it's member elements when matches are made, and feeds these
values into a more manageable, compact dictionary
'''
def case_match_detail_elements(x, structure, structure_key):
    return {
        'fields': {'value_collection_blueprint': structure[structure_key][x]},

        'items': {'value_collection': structure[structure_key][x],
                  'how_many_items_in_items_array': len(structure[structure_key][x])}

    }.get(x, None)

# overview: maps raw data values into a key/value structure
# -- the function walks through the raw data (data structure) and executes a mapping
# of fields specified by the raw data 
# -- returns an array of dictionaries containing mapped metrics 
def search(structure):
    dictionary = {}
    details = {}
    simple_metrics = {}

    if structure is not None:
        # overview: the algorithm begins by searching through the four main keys of the structure:
        # 'start', 'end', 'timezone' and 'details'
        for structure_key in structure:

            ''' overview: case match against the first three main fields '''
            simple_metrics[structure_key] = case_match_main(structure_key, structure)

            if structure_key == 'detail':

                for child_structure in structure[structure_key]:

                    '''
                    overview: populate the dictionary object with a blueprint object, the count of key fields
                    for the blueprint object and the values to populate the blueprint object with.

                    Logic: To determine if case 'child_structure' is in 'detail', match against all keys in function --
                    return value field of matched. If no match found, return the None object. Do while there exist
                    remaining children of detail to iterate through.

                    Debugging note: length of items in items array computed by --
                    len(structure[structure_key][child_structure])
                    '''
                    dictionary[child_structure] = case_match_detail_elements(child_structure, structure, structure_key)

                _item_count = dictionary['items']['how_many_items_in_items_array']
                _blueprint = dictionary['fields']['value_collection_blueprint']
                value_collection = dictionary['items']['value_collection']
                if _item_count and _blueprint and value_collection:

                    for i in range(_item_count):
                        # print "_item_count: ", _item_count
                        index = "details_{0}".format(i)
                        details[index] = init_map(value_collection[i],
                                                  len(value_collection[i]['synthetic_metrics']),
                                                  _blueprint['synthetic_metrics'],
                                                  value_collection[i]['synthetic_metrics'],
                                                  value_collection[i].keys())

    simple_metrics["detail"] = details
    return simple_metrics

# testing purposes.
def raw_data_testing_purposes():
     return {u'start': u'2015-08-08T02:01:48.6949806Z', u'end': u'2015-08-08T02:16:48.6949806Z', u'detail': {u'fields': {u'synthetic_metrics': [{u'index': 0, u'name': u'DNS (ms)'}, {u'index': 1, u'name': u'Connect (ms)'}, {u'index': 2, u'name': u'SSL (ms)'}, {u'index': 3, u'name': u'Send (ms)'}, {u'index': 4, u'name': u'Wait (ms)'}, {u'index': 5, u'name': u'Time To First Byte (ms)'}, {u'index': 6, u'name': u'Load (ms)'}, {u'index': 7, u'name': u'Response (ms)'}, {u'index': 8, u'name': u'Redirect (ms)'}, {u'index': 9, u'name': u'Server Response (ms)'}, {u'index': 10, u'name': u'File Size'}, {u'index': 11, u'name': u'Downloaded Bytes'}, {u'index': 12, u'name': u'Total Downloaded Bytes'}, {u'index': 13, u'name': u'Throughput'}, {u'index': 14, u'name': u'DOM Load (ms)'}, {u'index': 15, u'name': u'Content Load (ms)'}, {u'index': 16, u'name': u'Document Complete (ms)'}, {u'index': 17, u'name': u'Webpage Response (ms)'}, {u'index': 18, u'name': u'Speed Index'}, {u'index': 19, u'name': u'Wire Time (ms)'}, {u'index': 20, u'name': u'Client Time (ms)'}, {u'index': 21, u'name': u'Render Start (ms)'}, {u'index': 22, u'name': u'Time to Title (ms)'}, {u'index': 23, u'name': u'Webpage Throughput'}, {u'index': 24, u'name': u'# Connections'}, {u'index': 25, u'name': u'# Hosts'}, {u'index': 26, u'name': u'# Zones'}, {u'index': 27, u'name': u'# Items (Total)'}, {u'index': 28, u'name': u'# Redirect'}, {u'index': 29, u'name': u'# Html'}, {u'index': 30, u'name': u'Html Bytes'}, {u'index': 31, u'name': u'# Image'}, {u'index': 32, u'name': u'Image Bytes'}, {u'index': 33, u'name': u'# Script'}, {u'index': 34, u'name': u'Script Bytes'}, {u'index': 35, u'name': u'# Css'}, {u'index': 36, u'name': u'Css Bytes'}, {u'index': 37, u'name': u'# Flash'}, {u'index': 38, u'name': u'Flash Bytes'}, {u'index': 39, u'name': u'# Xml'}, {u'index': 40, u'name': u'Xml Bytes'}, {u'index': 41, u'name': u'# Media'}, {u'index': 42, u'name': u'Media Bytes'}, {u'index': 43, u'name': u'# Font'}, {u'index': 44, u'name': u'Font Bytes'}, {u'index': 45, u'name': u'# Other'}, {u'index': 46, u'name': u'Other Bytes'}, {u'index': 47, u'name': u'% Ping Packet Loss'}, {u'index': 48, u'name': u'Ping Round Trip (ms)'}, {u'index': 49, u'name': u'% Availability'}, {u'index': 50, u'name': u'% Content Availability'}, {u'index': 51, u'name': u'Apdex'}, {u'index': 52, u'name': u'% Satisfied'}, {u'index': 53, u'name': u'% Tolerating'}, {u'index': 54, u'name': u'% Frustrated'}, {u'index': 55, u'name': u'% Not Frustrated'}, {u'index': 56, u'name': u'# Runs'}, {u'index': 57, u'name': u'Page Speed Score'}, {u'index': 58, u'name': u'# JS Errors per Page'}, {u'index': 59, u'name': u'# Content Load Errors'}, {u'index': 60, u'name': u'# Tests with JS Errors'}, {u'index': 61, u'name': u'# DNS Failures'}, {u'index': 62, u'name': u'# Connection Failures'}, {u'index': 63, u'name': u'# SSL Failures'}, {u'index': 64, u'name': u'# Response Failures'}, {u'index': 65, u'name': u'# Timeout Failures'}, {u'index': 66, u'name': u'# Test Errors'}], u'host_Ip': True, u'breakdown_2': {u'id': 2, u'name': u'Node'}, u'breakdown_1': {u'id': 1, u'name': u'Test'}, u'error': True, u'dimension': {u'id': 0, u'name': u'Time'}}, u'items': [{u'host_Ip': u'206.190.36.45', u'synthetic_metrics': [78.0, 75.0, 127.0, 0.0, 128.0, 408.0, 11.0, 419.0, 149.0, 341.0, 2958.0, 4607.0, 4607.0, 33.14388656616211, None, 102.0, None, 419.0, None, 419.0, 0.0, None, None, 10.995226860046387, 2.0, 2.0, None, 2.0, 1.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 100.0, 100.0, 1.0, 100.0, 0.0, 0.0, 100.0, 1.0, None, None, 0.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635745961110000000, u'name': u'2015-08-08T02:01:51Z'}, u'breakdown_1': {u'id': 81093, u'name': u'Yahoo Test'}, u'breakdown_2': {u'id': 257, u'name': u'Los Angeles - TWTC'}}, {u'host_Ip': u'206.190.36.105', u'synthetic_metrics': [643.0, 88.0, 101.0, 0.0, 151.0, 983.0, 10.0, 993.0, 528.0, 350.0, 2958.0, 4608.0, 4608.0, 28.621118545532227, None, 124.0, None, 993.0, None, 993.0, 0.0, None, None, 4.640483379364014, 2.0, 2.0, None, 2.0, 1.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 100.0, 100.0, 0.5, 0.0, 100.0, 0.0, 100.0, 1.0, None, None, 0.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635745962400000000, u'name': u'2015-08-08T02:04:00Z'}, u'breakdown_1': {u'id': 81093, u'name': u'Yahoo Test'}, u'breakdown_2': {u'id': 28, u'name': u'San Francisco - VZN'}}, {u'host_Ip': u'2001:4998:58:c02::a9', u'synthetic_metrics': [30.0, 56.0, 88.0, 0.0, 116.0, 290.0, 10.0, 300.0, 98.0, 270.0, 2959.0, 4609.0, 4609.0, 36.57936477661133, None, 90.0, None, 300.0, None, 300.0, 0.0, None, None, 15.363333702087402, 2.0, 2.0, None, 2.0, 1.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 100.0, 100.0, 1.0, 100.0, 0.0, 0.0, 100.0, 1.0, None, None, 0.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635745963420000000, u'name': u'2015-08-08T02:05:42Z'}, u'breakdown_1': {u'id': 81093, u'name': u'Yahoo Test'}, u'breakdown_2': {u'id': 171, u'name': u'Chicago - Level3 IPv6'}}, {u'host_Ip': u'98.139.180.149', u'synthetic_metrics': [9.0, 35.0, 65.0, 0.0, 97.0, 206.0, 11.0, 217.0, 44.0, 208.0, 2958.0, 4608.0, 4608.0, 42.66666793823242, None, 89.0, None, 217.0, None, 217.0, 0.0, None, None, 21.235023498535156, 2.0, 2.0, None, 2.0, 1.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 100.0, 100.0, 1.0, 100.0, 0.0, 0.0, 100.0, 1.0, None, None, 0.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635745964720000000, u'name': u'2015-08-08T02:07:52Z'}, u'breakdown_1': {u'id': 81093, u'name': u'Yahoo Test'}, u'breakdown_2': {u'id': 134, u'name': u'Washington, DC - Zayo'}}, {u'host_Ip': u'98.139.183.24', u'synthetic_metrics': [17.0, 27.0, 50.0, 0.0, 89.0, 183.0, 10.0, 193.0, 40.0, 176.0, 2959.0, 4609.0, 4609.0, 46.55555725097656, None, 82.0, None, 193.0, None, 193.0, 0.0, None, None, 23.880828857421875, 2.0, 2.0, None, 2.0, 1.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 100.0, 100.0, 1.0, 100.0, 0.0, 0.0, 100.0, 1.0, None, None, 0.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635745965800000000, u'name': u'2015-08-08T02:09:40Z'}, u'breakdown_1': {u'id': 81093, u'name': u'Yahoo Test'}, u'breakdown_2': {u'id': 11, u'name': u'New York - Level3'}}, {u'host_Ip': u'206.190.36.105', u'synthetic_metrics': [12.0, 66.0, 119.0, 0.0, 126.0, 323.0, 9.0, 332.0, 81.0, 320.0, 2958.0, 4607.0, 4607.0, 34.12592697143555, None, 100.0, None, 332.0, None, 332.0, 0.0, None, None, 13.876505851745605, 2.0, 2.0, None, 2.0, 1.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 100.0, 100.0, 1.0, 100.0, 0.0, 0.0, 100.0, 1.0, None, None, 0.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635745967010000000, u'name': u'2015-08-08T02:11:41Z'}, u'breakdown_1': {u'id': 81093, u'name': u'Yahoo Test'}, u'breakdown_2': {u'id': 257, u'name': u'Los Angeles - TWTC'}}, {u'host_Ip': u'206.190.36.45', u'synthetic_metrics': [175.0, 51.0, 119.0, 0.0, 111.0, 456.0, 7.0, 463.0, 135.0, 288.0, 2958.0, 4608.0, 4608.0, 39.050846099853516, None, 91.0, None, 463.0, None, 463.0, 0.0, None, None, 9.952484130859375, 2.0, 2.0, None, 2.0, 1.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 100.0, 100.0, 1.0, 100.0, 0.0, 0.0, 100.0, 1.0, None, None, 0.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635745968200000000, u'name': u'2015-08-08T02:13:40Z'}, u'breakdown_1': {u'id': 81093, u'name': u'Yahoo Test'}, u'breakdown_2': {u'id': 28, u'name': u'San Francisco - VZN'}}, {u'host_Ip': u'2001:4998:58:c02::a9', u'synthetic_metrics': [40.0, 62.0, 98.0, 0.0, 124.0, 324.0, 11.0, 335.0, 111.0, 295.0, 2958.0, 4608.0, 4608.0, 34.13333511352539, None, 97.0, None, 335.0, None, 335.0, 0.0, None, None, 13.755224227905273, 2.0, 2.0, None, 2.0, 1.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 100.0, 100.0, 1.0, 100.0, 0.0, 0.0, 100.0, 1.0, None, None, 0.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635745969470000000, u'name': u'2015-08-08T02:15:47Z'}, u'breakdown_1': {u'id': 81093, u'name': u'Yahoo Test'}, u'breakdown_2': {u'id': 171, u'name': u'Chicago - Level3 IPv6'}}]}, u'timezone': {u'id': 4, u'name': u'UTC'}}

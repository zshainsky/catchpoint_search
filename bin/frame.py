#overview: retains and enumerates key of a dictionary key value pair
def enumerate_data(structure):
    if type(structure) is dict:
        return dict(enumerate(structure))
    if type(structure) is list:
        return list(enumerate(structure))

# overview: initiates the mapping algorithm.
# returns new mapped dictionary, which will become a field under it's parent key -- 'detail'
def init_map(data, LENGTH, blueprint, values_list):
    an_item = {}
    elements = ['synthetic_metrics', 'host_Ip', 'breakdown_2', 'breakdown_1', 'dimension']

    # overview: for each element x, create a new key/value pair within the dictionary named 'an_item'
    # by completing case matches against the element x. if case is found, index into the value_collection at element x
    # and return. The return value will become the 'value' field within the key/value pair structure.
    for x in elements:
        an_item[x] = case_match_metrics(x, data, LENGTH, blueprint, values_list)
    return an_item

'''
@param LENGTH:
    represents the length of value_collection dictionary indexed at 'synthetic_metric' --
    hence, LENGTH can be described the length of the synthetic_metric array
    note: value_collection is simply a large array filled entirely of values. more pointedly, 
    value_collection contains all the values to be mapped for the parent key 'detail'.
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
Logic: If we iterate through the 'value_collection_AT_synthetic_metrics_INDEX' array while, at the same time, iterating through
the blueprint structure as the desired indices, we are able to perform dynamic mappings across all synthetic_metrics values.
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
the information fetched can then be set as a value field of 'key/value' object within a brand new data structure.
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
'''
def case_match_metrics(x, data, LENGTH, blueprint, values_list):
    return {
        'synthetic_metrics' : map_synthetic(LENGTH, blueprint, values_list),
        'host_Ip': data[x],
        'breakdown_2': data[x],
        'breakdown_1': data[x],
        'dimension': data[x]
    }.get(x, None)


# overview: maps raw data values into a key/value structure 
# -- the function walks through the raw data (data structure) and executes a mapping
# of fields specified by the raw data 
# -- returns an array of dictionaries containing mapped metrics 
def search(structure):
    data = structure
    structure = enumerate_data(structure)
    details = {}
    simple_metrics = {}
    
    if structure is None:
        return
    if len(structure) > 0:

        # overview: the algorithm begins by searching through the four main keys of the structure:
        # 'start', 'end', 'timezone' and 'details'
        for i in range(len(structure)):

            # case match against the first three main fields
            simple_metrics[structure[i]] = case_match_main(structure[i], data)

            if structure[i] == 'detail':
                # overview: create a dictionary of detail's value to access its contents by indexing into
                a_detail_index = enumerate_data(data[structure[i]])
                for j in range(len(data[structure[i]])):

                    # overview: the 'blueprint' or 'keys'. the place-holding structure we will use as a scaffold to build our
                    # desired mapping with the values in the 'items' field
                    if a_detail_index[j] == 'fields':
                        value_collection_key = data[structure[i]][a_detail_index[j]] # save the template to map into
                        value_collection_key_count = len(data[structure[i]][a_detail_index[j]])

                    # overview: the 'items' field is the foundation of the value_collection array
                    # the 'items' field holds all the values which need to be mapped into their respective placeholders
                    if a_detail_index[j] == 'items':
                        value_collection = data[structure[i]][a_detail_index[j]]

                        # overview: for each k index within the value_collection array (an array which holds only values
                        # waiting to be mapped), initiates the mapping algorithm and returns a key/value pair structure.
                        for k in range(value_collection_key_count):
                            index = "details_{0}".format(k)
                            details[index] = init_map(value_collection[k],
                                                      len(value_collection[k]['synthetic_metrics']),
                                                      value_collection_key['synthetic_metrics'],
                                                      value_collection[k]['synthetic_metrics'])

    simple_metrics["detail"] = details
    return simple_metrics

# testing purposes.
# dictionary = {u'start': u'2015-06-05T13:18:46.3915259Z', u'end': u'2015-06-05T13:33:46.3915259Z', u'detail': {u'fields': {u'synthetic_metrics': [{u'index': 0, u'name': u'DNS (ms)'}, {u'index': 1, u'name': u'Connect (ms)'}, {u'index': 2, u'name': u'SSL (ms)'}, {u'index': 3, u'name': u'Send (ms)'}, {u'index': 4, u'name': u'Wait (ms)'}, {u'index': 5, u'name': u'Time To First Byte (ms)'}, {u'index': 6, u'name': u'Load (ms)'}, {u'index': 7, u'name': u'Response (ms)'}, {u'index': 8, u'name': u'Redirect (ms)'}, {u'index': 9, u'name': u'Server Response (ms)'}, {u'index': 10, u'name': u'File Size'}, {u'index': 11, u'name': u'Downloaded Bytes'}, {u'index': 12, u'name': u'Total Downloaded Bytes'}, {u'index': 13, u'name': u'Throughput'}, {u'index': 14, u'name': u'DOM Load (ms)'}, {u'index': 15, u'name': u'Content Load (ms)'}, {u'index': 16, u'name': u'Document Complete (ms)'}, {u'index': 17, u'name': u'Webpage Response (ms)'}, {u'index': 18, u'name': u'Wire Time (ms)'}, {u'index': 19, u'name': u'Client Time (ms)'}, {u'index': 20, u'name': u'Render Start (ms)'}, {u'index': 21, u'name': u'Time to Title (ms)'}, {u'index': 22, u'name': u'Webpage Throughput'}, {u'index': 23, u'name': u'# Connections'}, {u'index': 24, u'name': u'# Hosts'}, {u'index': 25, u'name': u'# Zones'}, {u'index': 26, u'name': u'# Items (Total)'}, {u'index': 27, u'name': u'# Redirect'}, {u'index': 28, u'name': u'# Html'}, {u'index': 29, u'name': u'Html Bytes'}, {u'index': 30, u'name': u'# Image'}, {u'index': 31, u'name': u'Image Bytes'}, {u'index': 32, u'name': u'# Script'}, {u'index': 33, u'name': u'Script Bytes'}, {u'index': 34, u'name': u'# Css'}, {u'index': 35, u'name': u'Css Bytes'}, {u'index': 36, u'name': u'# Flash'}, {u'index': 37, u'name': u'Flash Bytes'}, {u'index': 38, u'name': u'# Xml'}, {u'index': 39, u'name': u'Xml Bytes'}, {u'index': 40, u'name': u'# Media'}, {u'index': 41, u'name': u'Media Bytes'}, {u'index': 42, u'name': u'# Font'}, {u'index': 43, u'name': u'Font Bytes'}, {u'index': 44, u'name': u'# Other'}, {u'index': 45, u'name': u'Other Bytes'}, {u'index': 46, u'name': u'% Ping Packet Loss'}, {u'index': 47, u'name': u'Ping Round Trip (ms)'}, {u'index': 48, u'name': u'% Availability'}, {u'index': 49, u'name': u'% Content Availability'}, {u'index': 50, u'name': u'Apdex'}, {u'index': 51, u'name': u'# Runs'}, {u'index': 52, u'name': u'Page Speed Score'}, {u'index': 53, u'name': u'# JS Errors per Page'}, {u'index': 54, u'name': u'# Content Load Errors'}, {u'index': 55, u'name': u'# Tests with JS Errors'}, {u'index': 56, u'name': u'# DNS Failures'}, {u'index': 57, u'name': u'# Connection Failures'}, {u'index': 58, u'name': u'# SSL Failures'}, {u'index': 59, u'name': u'# Response Failures'}, {u'index': 60, u'name': u'# Timeout Failures'}, {u'index': 61, u'name': u'# Test Errors'}], u'host_Ip': True, u'breakdown_2': {u'id': 2, u'name': u'Node'}, u'breakdown_1': {u'id': 1, u'name': u'Test'}, u'error': True, u'dimension': {u'id': 0, u'name': u'Time'}}, u'items': [{u'host_Ip': u'64.233.177.103', u'synthetic_metrics': [37.0, 41.0, 96.0, 1.0, 104.0, 279.0, 123.0, 402.0, 89.0, 365.0, 48141.0, 49806.0, 383055.0, 219.40969848632812, 453.0, 788.0, 964.0, 991.0, 619.0, 345.0, 490.0, 0.0, 386.5338134765625, 5.0, 5.0, None, 13.0, 1.0, 1.0, 49806.0, 5.0, 48529.0, 5.0, 284455.0, 0.0, None, 0.0, None, 0.0, None, 0.0, None, 0.0, None, 0.0, None, None, None, 100.0, 100.0, 1.0, 1.0, None, 0.0, 0.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635691074040000000, u'name': u'2015-06-05T13:23:24Z'}, u'breakdown_1': {u'id': 76386, u'name': u'Google Test'}, u'breakdown_2': {u'id': 11, u'name': u'New York - Level3'}}, {u'host_Ip': u'216.58.192.4', u'synthetic_metrics': [6.0, 120.0, 142.0, 1.0, 231.0, 500.0, 97.0, 597.0, 155.0, 591.0, 48106.0, 49770.0, 382889.0, 151.73780822753906, 831.0, 2167.0, 2388.0, 2524.0, 1938.0, 450.0, 858.0, 0.0, 151.69927978515625, 4.0, 5.0, None, 13.0, 1.0, 1.0, 49770.0, 5.0, 48528.0, 5.0, 284326.0, 0.0, None, 0.0, None, 0.0, None, 0.0, None, 0.0, None, 0.0, None, None, None, 100.0, 100.0, 1.0, 1.0, None, 0.0, 0.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635691076700000000, u'name': u'2015-06-05T13:27:50Z'}, u'breakdown_1': {u'id': 76386, u'name': u'Google Test'}, u'breakdown_2': {u'id': 28, u'name': u'San Francisco - VZN'}}, {u'host_Ip': u'98.139.183.24', u'synthetic_metrics': [10.0, 34.0, 110.0, 1.0, 94.0, 249.0, 448.0, 697.0, 50.0, 687.0, 83567.0, 84723.0, 917848.0, 156.31549072265625, 1078.0, 2678.0, 1381.0, 2853.0, 1094.0, 287.0, 514.0, 0.0, 321.7132873535156, 7.0, 7.0, None, 36.0, 2.0, 3.0, 85980.0, 22.0, 503536.0, 6.0, 273460.0, 2.0, 53927.0, 0.0, None, 0.0, None, 0.0, None, 0.0, None, 0.0, None, None, None, 100.0, 0.0, 1.0, 1.0, None, 0.0, 1.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635691074300000000, u'name': u'2015-06-05T13:23:50Z'}, u'breakdown_1': {u'id': 81093, u'name': u'Yahoo Test'}, u'breakdown_2': {u'id': 134, u'name': u'Washington, DC - Zayo'}}, {u'host_Ip': u'98.139.183.24', u'synthetic_metrics': [71.0, 26.0, 83.0, 1.0, 82.0, 263.0, 324.0, 587.0, 104.0, 516.0, 82940.0, 84097.0, 592384.0, 207.13546752929688, 809.0, 2563.0, 1094.0, 2761.0, 1060.0, 34.0, 632.0, 0.0, 214.5541534423828, 8.0, 8.0, None, 37.0, 2.0, 3.0, 85352.0, 22.0, 178210.0, 6.0, 273570.0, 2.0, 53898.0, 0.0, None, 0.0, None, 0.0, None, 0.0, None, 0.0, None, None, None, 100.0, 0.0, 1.0, 1.0, None, 0.0, 1.0, None, None, None, None, None, None, None], u'dimension': {u'id': 635691077320000000, u'name': u'2015-06-05T13:28:52Z'}, u'breakdown_1': {u'id': 81093, u'name': u'Yahoo Test'}, u'breakdown_2': {u'id': 11, u'name': u'New York - Level3'}}]}, u'timezone': {u'id': 4, u'name': u'UTC'}}
# print search(dictionary)

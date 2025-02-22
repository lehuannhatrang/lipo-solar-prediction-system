from flask import request
from datetime import datetime

def extract_devices_info(all_devices, type):
    customer_id = request.customer_id
    devices_infos = list(filter(lambda device: device['type'] == type and device['customerId']['id'] == customer_id, all_devices['data']))
    extract_infos = [{'id': device['id']['id'], 'name': device['name']} for device in devices_infos]
    return extract_infos

def extract_timeseries_data(data):
    result_dict = {}
    for key in data.keys():
        field_data = [ {'timestamp': datetime.fromtimestamp(item['ts']/1000).isoformat(), key: item['value']} for item in data[key]]
        for item in field_data:
            if item['timestamp'] in result_dict:
                result_dict[item['timestamp']].update({key: item[key]})
            else:
                result_dict[item['timestamp']] = {key: item[key]}
    return [ {'timestamp': timestamp, **result_dict[timestamp]} for timestamp in result_dict.keys() ]
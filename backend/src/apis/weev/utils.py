from flask import request, jsonify
from datetime import datetime
from .request import WeevRequest
from .routes import get_weev_url, WEEVRouteName
import math

weev_request = WeevRequest()

MAX_DATA_POINTS = 700

def extract_devices_info(all_devices, type):
    devices_infos = list(filter(lambda device: device['type'] == type, all_devices['data']))

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

def get_timeseries_data(device_id, data_fields, start_time, end_time):
    interval = math.floor((end_time - start_time)/MAX_DATA_POINTS)
    params = {
        'keys': list(filter(lambda field: field != 'timestamp', data_fields)),
        'startTs': start_time,
        'endTs': end_time,
        'intervalType': 'MILLISECONDS',
        'interval': interval,
        'agg': 'AVG',
        'orderBy': 'ASC',
        'useStrictDataTypes': 'true'
    }
    response = weev_request.get(get_weev_url(WEEVRouteName.GET_TIMESERIES_DATA, device_id=device_id), params=params)

    if response.status_code != 200:
        logging.error(f"WEEV API error: {response.text}")
        return {"message": "Error fetching timeseries data from WEEV"}, response.status_code

    response_data = response.json()
    try:
        return extract_timeseries_data(response_data)
    except Exception as e:
        logging.error(f"Error processing timeseries data: {e}")
        return {"message": "Error processing timeseries data"}, 500
from flask import request
def extract_devices_info(all_devices, type):
    customer_id = request.customer_id
    devices_infos = list(filter(lambda device: device['type'] == type and device['customerId']['id'] == customer_id, all_devices['data']))
    extract_infos = [{'id': device['id']['id'], 'name': device['name']} for device in devices_infos]
    return extract_infos
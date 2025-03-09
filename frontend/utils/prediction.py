import time
from constants import DeviceType, rul_predict_fields
from authentication import AuthenRequest
from routes import RouteName, get_url

auth_request = AuthenRequest()

def get_rul_predict_fields(device_type: str, all_attributes: list[str]) -> list[str]:
    device_enum = DeviceType(device_type)
    allowed_fields = rul_predict_fields[device_enum]
    return [field for field in allowed_fields if field in all_attributes]

def request_rul_predictor(device_type, device_id, device_name, predict_field):
    body = {
        'device_type': device_type,
        'device_id': device_id,
        'device_name': device_name,
        'predict_field': predict_field,
    }
    response = auth_request.post(get_url(RouteName.POST_RUL_PREDICTION), json=body)
    return response.json()

def get_rul_predict_data(job_id):
    for i in range(0, 12):
        response = auth_request.get(get_url(RouteName.GET_RUL_PREDICTION, job_id=job_id)).json()
        if response["predict_data"]:
            break
        time.sleep(5)
    return response
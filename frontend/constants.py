from enum import Enum


class DeviceType(Enum):
    LIION_BATTERY = 'LIION_BATTERY'
    SOLAR_PANEL = 'SOLAR_PANEL'

device_type_labels = {
    'Li-ion Battery': DeviceType.LIION_BATTERY,
    'Solar Panel': DeviceType.SOLAR_PANEL
}

device_checkbox_labels = {
    'Li-ion Battery': 'Battery ID',
    'Solar Panel':'Solar Panel ID'
}


forecast_labels = {
    '5 days': '5_DAYS',
    '15 days': '15_DAYS',
    '30 days': '30_DAYS'
}

forecast_predict_fields = ['state_of_charge', 'state_of_health']
from enum import Enum


class DeviceType(Enum):
    LIION_BATTERY = 'LIION_BATTERY'
    SOLAR_PANEL = 'SOLAR_PANEL'

device_type_labels = {
    'Li-ion Battery': DeviceType.LIION_BATTERY,
    'Solar Panel': DeviceType.SOLAR_PANEL
}

device_checkbox_labels = {
    'Li-ion Battery': 'Battery Name',
    'Solar Panel':'Solar Panel Name'
}


forecast_labels = {
    '5 days': '5_DAYS',
    '15 days': '15_DAYS',
    '30 days': '30_DAYS'
}

forecast_predict_fields = ['state_of_charge', 'state_of_health', 'solar_battery_soc', 'solar_battery_soh', 'soc', 'soh']

chart_colour = [ "#00897b", "#1de9b6" , "#80cbc4", "#a7f2d2", "#236052", "#2a7b5e"]
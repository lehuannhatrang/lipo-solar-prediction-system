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
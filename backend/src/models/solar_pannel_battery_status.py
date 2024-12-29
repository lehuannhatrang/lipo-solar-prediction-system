from . import db
from .basemodel import BaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


class SolarPanelBatteryStatus(db.Model, BaseModel):
    __tablename__ = 'solar_panel_battery_status'
    
    # Unique entity ID
    entity_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    panel_id = db.Column(db.String(255), nullable=True)
    ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Solar panel and environmental attributes
    solar_irradiance = db.Column(db.Float, nullable=False)  # Solar Irradiance (W/m²)
    ambient_temperature = db.Column(db.Float, nullable=False)  # Ambient Temperature (°C)
    module_temperature = db.Column(db.Float, nullable=False)  # Module Temperature (°C)
    wind_speed = db.Column(db.Float, nullable=False)  # Wind Speed (m/s)
    
    # Power generation and output attributes
    energy_output = db.Column(db.Float, nullable=False)  # Energy Output (Wh)
    voltage = db.Column(db.Float, nullable=False)  # Voltage (V)
    current = db.Column(db.Float, nullable=False)  # Current (A)
    power_output = db.Column(db.Float, nullable=False)  # Power Output (W)
    
    # Battery-related attributes (for solar storage systems)
    state_of_charge = db.Column(db.Float, nullable=True)  # Battery State of Charge (SOC) in percentage
    
    # Inverter attributes
    inverter_efficiency = db.Column(db.Float, nullable=False)  # Inverter Efficiency (%)

    def __repr__(self):
        return f'<SolarPanelBatteryStatus {self.entity_id}>'
    
    def to_dict(self, selected_fields=None):
        object_dict = {
            'entity_id': str(self.entity_id),  # Converting UUID to string
            'panel_id': self.panel_id,
            'ts': self.ts.isoformat(),  # Convert datetime to ISO format
            'solar_irradiance': self.solar_irradiance,
            'ambient_temperature': self.ambient_temperature,
            'module_temperature': self.module_temperature,
            'wind_speed': self.wind_speed,
            'energy_output': self.energy_output,
            'voltage': self.voltage,
            'current': self.current,
            'power_output': self.power_output,
            'state_of_charge': self.state_of_charge,
            'inverter_efficiency': self.inverter_efficiency
        }
        if selected_fields:
            # Include only the fields that are in selected_fields and are present in the object_dict
            object_dict = {key: value for key, value in object_dict.items() if key in selected_fields}

        return object_dict
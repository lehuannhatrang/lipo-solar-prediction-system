"""
Define the Li-ion Battery model
"""
from . import db
from .basemodel import BaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


class LiionBatteryStatus(db.Model, BaseModel):
    __tablename__ = 'liion_battery_status'
    
    # Unique entity ID
    entity_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    battery_id = db.Column(db.String(255), nullable=True)
    ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Battery attributes
    voltage = db.Column(db.Float, nullable=False)  # Voltage (V)
    current = db.Column(db.Float, nullable=False)  # Current (A)
    state_of_charge = db.Column(db.Float, nullable=False)  # State of Charge (SOC) in percentage
    state_of_health = db.Column(db.Float, nullable=False)  # State of Health (SOH) in percentage
    temperature = db.Column(db.Float, nullable=False)  # Temperature (°C)
    impedance = db.Column(db.Float, nullable=False)  # Impedance/Resistance (Ω)
    charge_discharge_cycles = db.Column(db.Integer, nullable=False)  # Charge/Discharge Cycles
    energy = db.Column(db.Float, nullable=False)  # Energy (Wh)
    cycle_time = db.Column(db.Float, nullable=False)  # Cycle Time (s)
    capacity = db.Column(db.Float, nullable=False)  # Capacity (Ah)

    def __repr__(self):
        return f'<LiionBatteryStatus {self.entity_id}>'
    
    def to_dict(self, selected_fields=None):
        object_dict = {
            'entity_id': str(self.entity_id),
            'battery_id': self.battery_id,
            'ts': self.ts.isoformat() if self.ts else None,
            'voltage': self.voltage,
            'current': self.current,
            'state_of_charge': self.state_of_charge,
            'state_of_health': self.state_of_health,
            'temperature': self.temperature,
            'impedance': self.impedance,
            'charge_discharge_cycles': self.charge_discharge_cycles,
            'energy': self.energy,
            'cycle_time': self.cycle_time,
            'capacity': self.capacity
        }
        if selected_fields:
            # Include only the fields that are in selected_fields and are present in the object_dict
            object_dict = {key: value for key, value in object_dict.items() if key in selected_fields}
        
        return object_dict
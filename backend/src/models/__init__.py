from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .liion_battery_status import LiionBatteryStatus
from .prediction_job import PredictionJob
from .solar_pannel_battery_status import SolarPanelBatteryStatus
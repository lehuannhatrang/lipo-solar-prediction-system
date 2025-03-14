import uuid
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.ext.declarative import declarative_base
from . import db
from .basemodel import BaseModel
from datetime import datetime

Base = declarative_base()

class PredictionJob(db.Model, BaseModel):
    __tablename__ = 'prediction_job'

    job_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)  # Unique job ID
    created_by = Column(UUID(as_uuid=True), nullable=False)  # User UUID who created the job
    created_ts = Column(TIMESTAMP, nullable=False, default=datetime.now())  # Creation timestamp
    updated_ts = Column(TIMESTAMP, nullable=False, default=datetime.now(), onupdate=datetime.now())  # Updated timestamp
    type = Column(String(50), nullable=False)  # Type of prediction job ('forecast', 'anomaly', etc.)
    status = Column(String(50), nullable=False)  # Status of the job ('Pending', 'In Progress', 'Success')
    result_url = Column(String(255), nullable=True)  # URL for the result (optional)
    job_metadata = Column(JSON, nullable=True)  # Metadata field to store additional information in JSON format (optional)
    predict_data = Column(JSON, nullable=True)  # Metadata field to store additional information in JSON format (optional)

    def __repr__(self):
        return f"<PredictionJob(job_id={self.job_id}, created_by={self.created_by}, type={self.type}, status={self.status})>"
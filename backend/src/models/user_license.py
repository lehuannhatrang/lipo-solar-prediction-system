from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from . import db

class UserLicenseStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class UserLicense(db.Model):
    __tablename__ = 'user_license'

    email = Column(String, primary_key=True, nullable=False, unique=True)
    user_id = Column(String, nullable=True)
    expired_ts = Column(DateTime, nullable=True)
    status = Column(SQLEnum(UserLicenseStatus), nullable=False, default=UserLicenseStatus.INACTIVE)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_ts = Column(DateTime, nullable=True)

    def __init__(self, email, user_id=None, expired_ts=None, status=UserLicenseStatus.INACTIVE):
        self.email = email
        self.user_id = user_id
        self.expired_ts = expired_ts
        self.status = status

    def is_valid(self):
        """Check if the license is valid"""
        if self.status != UserLicenseStatus.ACTIVE:
            return False
            
        if self.expired_ts and self.expired_ts < datetime.utcnow():
            return False
            
        return True

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login_ts = datetime.utcnow()
        db.session.commit()

    @classmethod
    def get_by_email(cls, email):
        """Get user license by email"""
        return cls.query.filter_by(email=email).first()

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'email': self.email,
            'user_id': self.user_id,
            'expired_ts': self.expired_ts.isoformat() if self.expired_ts else None,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login_ts': self.last_login_ts.isoformat() if self.last_login_ts else None
        }

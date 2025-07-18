from datetime import datetime
import enum

from flask_login import UserMixin
from sqlalchemy import Column, String, BIGINT, DateTime, Index, text, TIMESTAMP

from extensions.ext_database import db


class AccountStatus(str, enum.Enum):
    PENDING = "pending"
    UNINITIALIZED = "uninitialized"
    ACTIVE = "active"
    BANNED = "banned"
    CLOSED = "closed"


class Account(UserMixin, db.Model):
    __tablename__ = 'accounts'

    id = Column(BIGINT, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, comment='邮箱', index=True)
    password = Column(String(255), nullable=True)
    password_salt = Column(db.String(255), nullable=True)
    status = Column(String(16), nullable=False, default='active')
    last_login_at = Column(db.DateTime)
    last_login_ip = Column(db.String(255),)
    last_active_at = Column(db.DateTime, default=datetime.now)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

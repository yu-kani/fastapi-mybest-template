from sqlalchemy import (
    Column, 
    String, 
    DateTime, 
    Float, 
    Integer, 
    Boolean,
    Text,
    func
)
from sqlalchemy.sql.functions import current_timestamp

from . import ModelBase
from core.database import Base
from core.utils import get_ulid


class User(Base, ModelBase):
    
    __tablename__ = 'users'
    mysql_charset='utf8mb4',
    mysql_collate='utf8mb4_unicode_ci'
    
    full_name = Column(String(64))
    email = Column(String(200), unique=True, index=True, nullable=False)
    email_verified = Column(Boolean, nullable=False, server_default='0')
    hashed_password = Column(Text, nullable=False)
    scopes = Column(Text)

    updated_at = Column(DateTime, nullable=False, default=current_timestamp(), onupdate=func.utc_timestamp())


    def to_dict(self):
        return self.__dict__.copy()
    
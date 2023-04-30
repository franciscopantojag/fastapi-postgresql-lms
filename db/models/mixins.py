from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_mixin, declared_attr


@declarative_mixin
class BaseMixin:
    __mapper_args__ = {'always_refresh': True}
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

import datetime

from sqlalchemy import Column, String, Integer, DateTime

from src.configs.database import Base


class Trial(Base):
    __tablename__ = "trials"

    id = Column(Integer, primary_key=True, index=True)
    trial_id = Column(String, unique=True, index=True)
    name = Column(String)
    period = Column(String)
    scope = Column(String)
    category = Column(String)
    institution = Column(String)
    stage = Column(String)
    subjects_count = Column(Integer)
    department = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

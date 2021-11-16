from sqlalchemy import Boolean, Column, Integer, String
# from datetime   import Datetime
from database   import Base


class Trial(Base):
    __tablename__ = "trials"

    id = Column(Integer, primary_key=True, index=True)
    trial_id = Column(String, unique=True) # number?
    name = Column(String)
    period = Column(String)
    scope = Column(String)
    category = Column(String)
    institution = Column(String)
    stage = Column(String)
    subjects_count = Column(String)
    department = Column(String)
    create_at = Column(Datetime)
    updated_at = Column(Datetime)
    modified_at = Column(Datetime)

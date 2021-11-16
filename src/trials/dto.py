from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TrialListParams(BaseModel):
    start: Optional[datetime]
    end: Optional[datetime]


class TrialViewData(BaseModel):
    trial_id: str
    name: str
    period: str
    scope: str
    category: str
    institution: str
    stage: str
    subjects_count: int
    department: str
    updated_at: datetime

    class Config:
        orm_mode = True

from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# table 타입 설정
class TrialBase(BaseModel):
    id: int
    trial_id: UUID
    name: str
    period: str
    scope: str
    category: str
    institution: str
    stage: str
    subjects_count: str
    department: str
    create_at: datetime
    updated_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True
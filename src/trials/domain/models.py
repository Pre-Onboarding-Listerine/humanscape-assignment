from typing import Optional

from pydantic import BaseModel


class Trial(BaseModel):
    id: Optional[int] = None
    trial_id: str
    name: str
    period: str
    scope: str
    category: str
    institution: str
    stage: str
    subjects_count: int
    department: str

    class Config:
        orm_mode = True

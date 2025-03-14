from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RollBase(BaseModel):
    length: float
    weight: float

class RollCreate(RollBase):
    pass

class RollResponse(RollBase):
    id: int
    added_at: datetime
    removed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

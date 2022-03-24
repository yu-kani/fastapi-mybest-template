from typing import Optional, List
from pydantic import BaseModel
import datetime

from schemas.core import PagingMeta


class JobResponse(BaseModel):
    id: str
    title: str
    deleted_at: Optional[datetime.datetime]
    
    class Config:
        orm_mode = True
    
class JobCreate(BaseModel):
    title: str
    
class JobUpdate(BaseModel):
    title: Optional[str] = None
    
class JobsPagedResponse(BaseModel):
    data: Optional[List[JobResponse]]
    meta: Optional[PagingMeta]
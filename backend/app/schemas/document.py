from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    filename: str
    mime_type: Optional[str] = None
    status: str = "pending"

class DocumentCreate(DocumentBase):
    filepath: str

class DocumentResponse(DocumentBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

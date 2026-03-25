from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any
from datetime import datetime


T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: str = "Operation completed"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
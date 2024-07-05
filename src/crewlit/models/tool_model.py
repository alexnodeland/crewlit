from pydantic import BaseModel as PydanticBaseModel
from .base_model import BaseModel
from typing import Dict, Any, List, Optional

class Tool(BaseModel):
    description: str
    enabled: bool = True
    secrets: Optional[List[str]] = []
    config: Optional[Dict[str, Any]] = {}

from .base_model import BaseModel

class Task(BaseModel):
    title: str
    description: str
    expected_output: str
from .base_model import BaseModel

class Agent(BaseModel):
    role: str
    backstory: str
    goal: str
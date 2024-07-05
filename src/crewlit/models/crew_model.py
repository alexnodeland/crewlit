from pydantic import BaseModel as PydanticBaseModel, ConfigDict
from .base_model import BaseModel
from typing import Dict, Any, List, Optional

class AgentConfig(PydanticBaseModel):
    allow_delegation: bool = True
    verbose: bool = True
    llm: Optional[Dict[str, Any]] = None
    max_iter: int = 25
    max_execution_time: Optional[int] = None
    tools: List[str] = []

class LLMConfig(PydanticBaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    top_p: float = 1.0

class TaskConfig(PydanticBaseModel):
    agent: str = ""
    context: List[str] = []
    tools: List[str] = []
    human_input: bool = False
    output_file: Optional[str] = None
    create_directory: bool = True

class CrewConfig(PydanticBaseModel):
    process: str = "sequential"
    manager_llm: Optional[LLMConfig] = None
    manager_agent: Optional[Dict[str, AgentConfig]] = None
    verbose: bool = True
    default_agent_llm: LLMConfig = LLMConfig()
    output_log_file: str = "output/crew.log"

class Crew(BaseModel):
    label: str
    agents: Dict[str, AgentConfig] = {}
    tasks: Dict[str, TaskConfig] = {}
    crew: CrewConfig = CrewConfig()
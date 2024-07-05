from crewlit.utils import load_yaml, save_yaml, dump_yaml, format_title_key
from crewlit.models import Agent

class AgentService:
    def __init__(self, file_path):
        self.file_path = file_path
        self.agents = self._load_agents()

    def _load_agents(self):
        data = load_yaml(self.file_path)
        return {name: Agent.from_dict(name, agent_data) for name, agent_data in data.items()}

    def save_agents(self):
        data = {name: agent.to_dict() for name, agent in self.agents.items()}
        save_yaml(self.file_path, data)

    def get_all_agents(self):
        return self.agents

    def update_agent(self, old_name, role, backstory, goal):
        formatted_role, new_name = format_title_key(role)
        if new_name != old_name:
            del self.agents[old_name]
        self.agents[new_name] = Agent(name=new_name, role=formatted_role, backstory=backstory, goal=goal)
        self.save_agents()
        return formatted_role

    def delete_agent(self, name):
        agent = self.agents.pop(name)
        self.save_agents()
        return agent.role

    def create_agent(self, role, backstory, goal):
        formatted_role, new_name = format_title_key(role)
        if new_name not in self.agents:
            self.agents[new_name] = Agent(name=new_name, role=formatted_role, backstory=backstory, goal=goal)
            self.save_agents()
            return formatted_role
        return None
    
    def get_agents_yaml(self):
        data = {name: agent.to_dict() for name, agent in self.agents.items()}
        return dump_yaml(data)
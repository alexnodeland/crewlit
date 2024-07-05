from crewlit.utils import load_yaml, save_yaml, dump_yaml, format_title_key
from crewlit.models import Crew, CrewConfig, AgentConfig, TaskConfig

class CrewService:
    def __init__(self, file_path):
        self.file_path = file_path
        self.crews = self._load_crews()

    def _load_crews(self):
        data = load_yaml(self.file_path)
        return {name: Crew.from_dict(name, crew_data) for name, crew_data in data.items()}

    def save_crews(self):
        data = {name: crew.to_dict() for name, crew in self.crews.items()}
        save_yaml(self.file_path, data)

    def get_all_crews(self):
        return self.crews
    
    def get_crew(self, name):
        crew = self.crews.get(name)
        return crew

    def update_crew(self, old_name, label, agents, tasks, crew_config):
        formatted_label, new_name = format_title_key(label)
        if new_name != old_name:
            del self.crews[old_name]
        self.crews[new_name] = Crew(
            name=new_name,
            label=formatted_label,
            agents={name: config if isinstance(config, AgentConfig) else AgentConfig(**config) for name, config in agents.items()},
            tasks={name: config if isinstance(config, TaskConfig) else TaskConfig(**config) for name, config in tasks.items()},
            crew=crew_config if isinstance(crew_config, CrewConfig) else CrewConfig(**crew_config)
        )
        self.save_crews()
        return formatted_label

    def delete_crew(self, name):
        crew = self.crews.pop(name)
        self.save_crews()
        return crew.label

    def create_crew(self, label, agents, tasks, crew_config):
        formatted_label, new_name = format_title_key(label)
        if new_name not in self.crews:
            self.crews[new_name] = Crew(
                name=new_name,
                label=formatted_label,
                agents={name: config if isinstance(config, AgentConfig) else AgentConfig(**config) for name, config in agents.items()},
                tasks={name: config if isinstance(config, TaskConfig) else TaskConfig(**config) for name, config in tasks.items()},
                crew=crew_config if isinstance(crew_config, CrewConfig) else CrewConfig(**crew_config)
            )
            self.save_crews()
            return formatted_label
        return None

    def get_crews_yaml(self):
        data = {name: crew.to_dict() for name, crew in self.crews.items()}
        return dump_yaml(data)

    def add_agent_to_crew(self, crew_name, agent_name, agent_config):
        if crew_name in self.crews:
            self.crews[crew_name].agents[agent_name] = AgentConfig(**agent_config)
            self.save_crews()
            return True
        return False

    def remove_agent_from_crew(self, crew_name, agent_name):
        if crew_name in self.crews and agent_name in self.crews[crew_name].agents:
            del self.crews[crew_name].agents[agent_name]
            self.save_crews()
            return True
        return False

    def add_task_to_crew(self, crew_name, task_name, task_config):
        if crew_name in self.crews:
            self.crews[crew_name].tasks[task_name] = TaskConfig(**task_config)
            self.save_crews()
            return True
        return False

    def remove_task_from_crew(self, crew_name, task_name):
        if crew_name in self.crews and task_name in self.crews[crew_name].tasks:
            del self.crews[crew_name].tasks[task_name]
            self.save_crews()
            return True
        return False

    def update_crew_config(self, crew_name, crew_config):
        if crew_name in self.crews:
            self.crews[crew_name].crew = CrewConfig(**crew_config)
            self.save_crews()
            return True
        return False
    
    def update_agent_config(self, crew_name, agent_name, agent_config):
        if crew_name in self.crews and agent_name in self.crews[crew_name].agents:
            self.crews[crew_name].agents[agent_name] = AgentConfig(**agent_config)
            self.save_crews()
            return True
        return False

    def update_task_config(self, crew_name, task_name, task_config):
        if crew_name in self.crews and task_name in self.crews[crew_name].tasks:
            self.crews[crew_name].tasks[task_name] = TaskConfig(**task_config)
            self.save_crews()
            return True
        return False

import os
from crewlit.utils import load_yaml, save_yaml, dump_yaml, format_title_key
from crewlit.models import Tool

class ToolService:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tools = self._load_tools()

    def _load_tools(self):
        data = load_yaml(self.file_path)
        return {name: Tool(**tool_data) for name, tool_data in data.items()}

    def save_tools(self):
        data = {name: tool.dict() for name, tool in self.tools.items()}
        save_yaml(self.file_path, data)

    def get_all_tools(self):
        return self.tools

    def update_tool(self, name, description=None, enabled=None, secret_keys=None, config=None):
        if name not in self.tools:
            return None

        tool = self.tools[name]
        
        if description is not None:
            tool.description = description
        if enabled is not None:
            tool.enabled = enabled
        if secret_keys is not None:
            tool.secret_keys = secret_keys
        if config is not None:
            tool.config = config

        self.save_tools()
        return tool

    def delete_tool(self, name):
        tool = self.tools.pop(name)
        self.save_tools()
        return tool.description

    def create_tool(self, description, enabled=True, secrets=None, config=None):
        formatted_name, new_name = format_title_key(description)
        if new_name not in self.tools:
            self.tools[new_name] = Tool(description=formatted_name, enabled=enabled, secrets=secrets, config=config)
            self.save_tools()
            return formatted_name
        return None

    def get_tools_yaml(self):
        data = {name: tool.dict() for name, tool in self.tools.items()}
        return dump_yaml(data)

    def enable_tool(self, name):
        if name in self.tools:
            self.tools[name].enabled = True
            self.save_tools()
            return True
        return False

    def disable_tool(self, name):
        if name in self.tools:
            self.tools[name].enabled = False
            self.save_tools()
            return True
        return False

    def get_enabled_tools(self):
        return {name: tool for name, tool in self.tools.items() if tool.enabled}

    def get_disabled_tools(self):
        return {name: tool for name, tool in self.tools.items() if not tool.enabled}
    
    def get_secret(self, tool_name, secret_key):
        env_var_name = f"{secret_key.upper()}"
        return os.environ.get(env_var_name)

    def set_secret(self, secret_key, secret_value):
        env_var_name = f"{secret_key.upper()}"
        os.environ[env_var_name] = secret_value

import streamlit as st
from crewlit.utils import get_logger

logger = get_logger(__name__)

class ConfigComponent:
    def __init__(self, tool_service):
        self.tool_service = tool_service

    def render_config(self):
        logger.info("Rendering configuration page.")
        st.header("Configuration")

        default_secrets, tool_secrets, other = st.tabs(["Default Secrets", "Tool Secrets", "Other"])
        with default_secrets:
            self._default_secrets()
        with tool_secrets:
            self._tool_secrets()
        with other:
            st.write("Nothing here yet!")

    def _get_all_unique_secrets(self, tools):
        logger.debug("Collecting all unique secrets from tools.")
        all_secrets = set()
        for tool in tools.values():
            all_secrets.update(tool.secrets)
        return sorted(all_secrets)
    
    def _tool_secrets(self):
        logger.info("Rendering tool secrets.")
        enabled_tools = self.tool_service.get_enabled_tools()
        all_secrets = self._get_all_unique_secrets(enabled_tools)

        for secret_key in all_secrets:
            with st.form(key=f"{secret_key}_form"):
                # Get the current value from any tool that uses this secret
                current_value = next((self.tool_service.get_secret(tool_name, secret_key) 
                                      for tool_name, tool in enabled_tools.items() 
                                      if secret_key in tool.secrets), "")
                
                new_value = st.text_input(
                    secret_key,
                    value=current_value if current_value else "",
                    type="password"
                )
                
                # Display which tools use this secret
                tools_using_secret = [tool.name for tool in enabled_tools.values() if secret_key in tool.secrets]
                st.caption(f"Used by: {', '.join(tools_using_secret)}")
                
                if st.form_submit_button("Update Secret"):
                    if new_value and new_value != current_value:
                        self.tool_service.set_secret(secret_key, new_value)
                        st.success(f"Updated {secret_key} for all relevant tools")
                        logger.info(f"Updated secret {secret_key} for all relevant tools.")

    def _default_secrets(self):
        logger.info("Rendering default secrets.")
        default_secrets = {
            "OPENAI_API_KEY": "Enter your OpenAI API Key",
            "OPENAI_ORGANIZATION": "Enter your OpenAI Organization",
            "OPENAI_MODEL_NAME": "Enter your default OpenAI model"
        }

        for secret_key, placeholder in default_secrets.items():
            with st.form(key=f"default_{secret_key}_form"):
                current_value = self.tool_service.get_secret("default", secret_key)
                new_value = st.text_input(
                    secret_key,
                    value=current_value if current_value else "",
                    type="password",
                    placeholder=placeholder,
                    help=placeholder
                )
                
                if st.form_submit_button("Update Secret"):
                    if new_value and new_value != current_value:
                        self.tool_service.set_secret(secret_key, new_value)
                        st.success(f"Updated {secret_key}")
                        logger.info(f"Updated default secret {secret_key}.")

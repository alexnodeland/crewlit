import streamlit as st
from crewlit.utils import get_logger

logger = get_logger(__name__)

class ToolComponent:
    def __init__(self, tool_service):
        self.tool_service = tool_service

    def render_tool_explorer(self):
        logger.info("Rendering tool explorer")
        with st.container(border=True):
            tools = self.tool_service.get_all_tools()
            title, download = st.columns([3, 1])
            with title:
                st.write("#### My Tools")
            with download:
                if tools:
                    self._render_download_button()
            if not tools:
                st.info("No tools available.")
            else:
                for tool_name, tool in tools.items():
                    self._display_and_edit_tool(tool_name, tool)

    def _display_and_edit_tool(self, tool_name, tool):
        logger.info(f"Displaying and editing tool: {tool_name}")
        with st.container(border=True):
            title, editor = st.columns([2, 3])
            with title:
                self._render_tool_header(tool)
            with editor:
                status, controls = st.columns([1, 1])
                with status:
                    self._render_tool_status(tool)
                with controls:
                    self._render_tool_controls(tool_name, tool)
                self._render_tool_editor(tool_name, tool)

    def _render_tool_header(self, tool):
        logger.info(f"Rendering tool header for: {tool.name}")
        st.write(f"**{tool.name}**")
        with st.popover("Description"):
            st.write(f"{tool.description}")

    def _render_tool_status(self, tool):
        logger.info(f"Rendering tool status for: {tool.name}")
        if tool.enabled:
            st.success("Enabled")
        else:
            st.error("Disabled")

    def _render_tool_controls(self, tool_name, tool):
        logger.info(f"Rendering tool controls for: {tool_name}")
        if tool.enabled:
            if st.button("Disable", key=f"disable_{tool_name}", use_container_width=True):
                logger.info(f"Disabling tool: {tool_name}")
                self.tool_service.disable_tool(tool_name)
                st.rerun()
        else:
            if st.button("Enable", key=f"enable_{tool_name}", use_container_width=True):
                logger.info(f"Enabling tool: {tool_name}")
                self.tool_service.enable_tool(tool_name)
                st.rerun()

    def _render_tool_editor(self, tool_name, tool):
        logger.info(f"Rendering tool editor for: {tool_name}")
        with st.popover("Edit", disabled=not tool.enabled, use_container_width=True):
            config, secrets = st.tabs(["Config", "Secrets"])
            with config:
                self._render_config_editor(tool_name, tool)
            with secrets:
                self._render_secrets_editor(tool_name, tool)

    def _render_config_editor(self, tool_name, tool):
        logger.info(f"Rendering config editor for: {tool_name}")
        if tool.config:
            updated_config = {}
            for config_key, config_value in tool.config.items():
                updated_value = st.text_input(
                    config_key,
                    value=config_value,
                    key=f"config_{tool_name}_{config_key}"
                )
                updated_config[config_key] = updated_value
            
            if st.button("Update Config", key=f"update_config_{tool_name}"):
                logger.info(f"Updating config for: {tool_name}")
                self.tool_service.update_tool(tool_name, config=updated_config)
                st.success("Config updated successfully!")
                st.rerun()
        else:
            st.info("No config required for this tool.")

    def _render_secrets_editor(self, tool_name, tool):
        logger.info(f"Rendering secrets editor for: {tool_name}")
        if tool.secrets:
            updated_secrets = {}
            for secret_key in tool.secrets:
                current_value = self.tool_service.get_secret(tool_name, secret_key)
                updated_value = st.text_input(
                    secret_key,
                    value=current_value,
                    type="password",
                    key=f"secret_{tool_name}_{secret_key}"
                )
                updated_secrets[secret_key] = updated_value
            
            if st.button("Update Secrets", key=f"update_secrets_{tool_name}"):
                logger.info(f"Updating secrets for: {tool_name}")
                for secret_key, secret_value in updated_secrets.items():
                    self.tool_service.set_secret(secret_key, secret_value)
                st.success("Secrets updated successfully!")
                st.rerun()
        else:
            st.info("No secrets required for this tool.")

    def _render_download_button(self):
        logger.info("Rendering download button for tools")
        yaml_content = self.tool_service.get_tools_yaml()
        st.download_button(
            label=":file_folder: Download",
            data=yaml_content,
            file_name="tools.yaml",
            mime="text/yaml",
            use_container_width=True
        )
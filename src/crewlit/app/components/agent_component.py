import os
import streamlit as st
from crewlit.utils import get_logger

logger = get_logger(__name__)

class AgentComponent:
    def __init__(self, agent_service):
        self.agent_service = agent_service

    def render_agent_creator(self):
        logger.info("Rendering agent creator.")
        with st.expander("Add Agent", expanded=not self.agent_service.get_all_agents()):
            with st.popover("Instructions", use_container_width=True):
                st.write("If you have a new agent to add, enter the details here.")
            with st.form(key="create_agent_form"):
                new_agent_role = st.text_input("Role", help="Enter the role of the agent.")
                new_agent_backstory = st.text_area("Backstory", help="Enter the backstory of the agent.")
                new_agent_goal = st.text_area("Goal", help="Enter the goal of the agent.")
                submit_button = st.form_submit_button("Add Agent", use_container_width=True)

            if submit_button:
                logger.debug(f"Attempting to create agent with role: {new_agent_role}")
                formatted_role = self.agent_service.create_agent(new_agent_role, new_agent_backstory, new_agent_goal)
                if formatted_role:
                    st.success(f"Agent '{formatted_role}' created successfully!")
                    logger.info(f"Agent '{formatted_role}' created successfully.")
                    st.rerun()
                else:
                    st.error("An agent with this role already exists. Please choose a different role.")
                    logger.warning(f"Agent creation failed. Role '{new_agent_role}' already exists.")

    def render_agent_explorer(self):
        logger.info("Rendering agent explorer.")
        with st.container(border=True):
            agents = self.agent_service.get_all_agents()
            title, download = st.columns([3, 1])
            with title:
                st.write("#### My Agents")
                total_agents = len(self.agent_service.get_all_agents())
                st.metric("Total Tasks", total_agents)
            with download:
                if agents:
                    self._render_download_button()
                with st.popover("Upload", use_container_width=True):
                    self._render_upload_button()
            if not agents:
                st.info("No agents created yet. Use the form below to create your first agent.")
                logger.info("No agents found.")
            else:
                for agent_name, agent in agents.items():
                    self._display_and_edit_agent(agent_name, agent)

    def _display_and_edit_agent(self, agent_name, agent):
        logger.debug(f"Displaying and editing agent: {agent_name}")
        with st.container(border=True):
            title, editor = st.columns([1, 4])
            with title:
                st.write(f"{agent.role}")
            with editor:
                with st.expander("Edit", expanded=False):
                    role = st.text_input("Role", value=agent.role, key=f"role_{agent_name}")
                    backstory = st.text_area("Backstory", value=agent.backstory, key=f"backstory_{agent_name}")
                    goal = st.text_area("Goal", value=agent.goal, key=f"goal_{agent_name}")
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        update_button = st.button("Update", key=f"update_{agent_name}", use_container_width=True)
                    with col2:
                        delete_button = st.button("Delete", key=f"delete_{agent_name}", use_container_width=True)

                    if update_button:
                        logger.debug(f"Updating agent: {agent_name}")
                        formatted_role = self.agent_service.update_agent(agent_name, role, backstory, goal)
                        st.success(f"Agent '{formatted_role}' updated successfully!")
                        logger.info(f"Agent '{formatted_role}' updated successfully.")
                        st.rerun()
                                    
                    if delete_button:
                        logger.debug(f"Deleting agent: {agent_name}")
                        deleted_role = self.agent_service.delete_agent(agent_name)
                        st.success(f"Agent '{deleted_role}' deleted successfully!")
                        logger.info(f"Agent '{deleted_role}' deleted successfully.")
                        st.rerun()

    def _render_download_button(self):
        logger.info("Rendering download button for agents.")
        yaml_content = self.agent_service.get_agents_yaml()
        st.download_button(
            label=":file_folder: Download",
            data=yaml_content,
            file_name="agents.yaml",
            mime="text/yaml",
            use_container_width=True
        )
    
    def _render_upload_button(self):
        logger.info("Rendering upload button for agents.")
        AGENT_YAML = "data/agents.yaml"
        with st.form("upload_agent_form"):
            uploaded_file = st.file_uploader("Upload Agents", type="yaml", label_visibility="collapsed")
            submit_button = st.form_submit_button("Upload")

            if submit_button and uploaded_file is not None:
                try:
                    logger.debug("Uploading agents file.")
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(AGENT_YAML), exist_ok=True)
                    
                    # Save the uploaded file
                    with open(AGENT_YAML, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    st.success("Agents file uploaded successfully!")
                    logger.info("Agents file uploaded successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving agents file: {str(e)}")
                    logger.error(f"Error saving agents file: {str(e)}")

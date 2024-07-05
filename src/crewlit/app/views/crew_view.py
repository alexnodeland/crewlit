import streamlit as st
from crewlit.services import CrewService, AgentService, TaskService, ToolService
from crewlit.app.components import CrewComponent
from crewlit.app.components.shared_components import Footer
from crewlit.utils import get_logger

logger = get_logger(__name__)

CREWS_YAML = "data/crews.yaml"
AGENTS_YAML = "data/agents.yaml"
TASKS_YAML = "data/tasks.yaml"
TOOLS_YAML = "data/tools.yaml"

def Crews():
    logger.info("Setting up the Crews page.")
    st.set_page_config(page_title="Crewlit - Crews", page_icon="👥", layout="wide")

    st.title("Crew Manager")

    with st.expander("About Crews"):
        st.markdown("""
        Assemble and manage powerful AI crews for complex tasks and workflows.

        Here you can:
        - 👥 Create custom AI crews with specific agents and tasks
        - 🎯 Define crew objectives and strategies
        - 🔧 Assign tools and resources to your crews

        Effective crew composition is key to solving complex problems with multi-agent systems.
        """)

    st.info("💡 Tip: Assign agents to specific tasks and provide clear context to maximize your crew's effectiveness.")

    agent_service = AgentService(AGENTS_YAML)
    task_service = TaskService(TASKS_YAML)
    crew_service = CrewService(CREWS_YAML)
    tool_service = ToolService(TOOLS_YAML)
    crew_component = CrewComponent(crew_service, agent_service, task_service, tool_service)

    logger.debug("Rendering crew explorer.")
    crew_component.render_crew_explorer()
    logger.debug("Rendering crew creator.")
    crew_component.render_crew_creator()
    logger.info("Crews page setup complete.")

    Footer()

import streamlit as st
from crewlit.app.components import KickoffComponent
from crewlit.app.components.shared_components import Footer
from crewlit.services import KickoffService, CrewService, AgentService, TaskService, ToolService
from crewlit.utils import get_logger

logger = get_logger(__name__)

CREW_YAML = "data/crews.yaml"
AGENTS_YAML = "data/agents.yaml"
TASKS_YAML = "data/tasks.yaml"
TOOLS_YAML = "data/tools.yaml"

def Kickoff():
    logger.info("Setting up the Kickoff page.")
    st.set_page_config(page_title="Crewlit - Kickoff", page_icon="🚣", layout="wide")

    st.title("Kickoff Manager")

    with st.expander("About Kickoff"):
        st.markdown("""
        Launch your AI agent crews and start your multi-agent automations.

        Here you can:
        - 🚀 Initiate your configured AI crews
        - 👥 Assign tasks to your AI agents
        - 🔧 Enable necessary tools for your crew
        - 📊 Monitor real-time progress of your crew's execution

        Kicking off a crew means setting your AI agents in motion to accomplish the tasks you've defined.
        """)

    st.info("💡 Tip: Ensure all your agents, tasks, and tools are properly configured before kicking off a crew for optimal performance.")

    crew_service = CrewService(CREW_YAML)
    agent_service = AgentService(AGENTS_YAML)
    task_service = TaskService(TASKS_YAML)
    tool_service = ToolService(TOOLS_YAML)
    kickoff_service = KickoffService(crew_service, agent_service, task_service, tool_service)

    kickoff_component = KickoffComponent(kickoff_service, crew_service)

    logger.debug("Rendering kickoff component.")
    kickoff_component.render_kickoff()
    logger.info("Kickoff page setup complete.")

    Footer()
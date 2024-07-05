import streamlit as st
from crewlit.services import TaskService
from crewlit.app.components import TaskComponent
from crewlit.app.components.shared_components import Footer
from crewlit.utils import get_logger

logger = get_logger(__name__)

TASKS_YAML = "data/tasks.yaml"

def Tasks():
    logger.info("Setting up the Tasks page.")
    st.set_page_config(page_title="Crewlit - Tasks", page_icon="📋", layout="wide")

    st.title("Task Manager")

    with st.expander("About Tasks"):
        st.markdown("""
        Create, manage, and organize tasks for your AI crews.

        Here you can:
        - ✅ Define tasks with specific goals and requirements
        - 📊 Organize tasks into projects or workflows
        - 🔄 Track task progress and completion

        Efficient task management is crucial for successful multi-agent automations.
        """)

    st.info("💡 Tip: Break down complex projects into smaller, manageable tasks for better AI agent performance.")

    task_service = TaskService(TASKS_YAML)
    task_component = TaskComponent(task_service)

    logger.debug("Rendering task explorer.")
    task_component.render_task_explorer()
    logger.debug("Rendering task creator.")
    task_component.render_task_creator()
    logger.info("Tasks page setup complete.")

    Footer()
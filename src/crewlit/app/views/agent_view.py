import streamlit as st
from crewlit.services import AgentService
from crewlit.app.components import AgentComponent
from crewlit.app.components.shared_components import Footer
from crewlit.utils import get_logger

logger = get_logger(__name__)

AGENTS_YAML = "data/agents.yaml"

def Agents():
    logger.info("Setting up the Agents page.")
    st.set_page_config(page_title="Crewlit - Agents", page_icon="🚣", layout="wide")

    st.title("Agent Manager")

    with st.expander("About Agents"):
        st.markdown("""
        Design and orchestrate powerful AI agents for your multi-agent crews.

        Here you can:
        - 🤖 Create custom AI agents with specific roles and goals
        - 🧠 Define agent backstories and expertise
        - 📊 Manage and organize your agent roster

        Effective agent design is the cornerstone of building powerful multi-agent systems.
        """)

    # Add a tip or best practice
    st.info("💡 Tip: Define clear goals & backstories for each agent to ensure optimal performance in your AI crews.")

    agent_service = AgentService(AGENTS_YAML)
    agent_component = AgentComponent(agent_service)

    logger.debug("Rendering agent explorer.")
    agent_component.render_agent_explorer()
    logger.debug("Rendering agent creator.")
    agent_component.render_agent_creator()
    logger.info("Agents page setup complete.")

    Footer()
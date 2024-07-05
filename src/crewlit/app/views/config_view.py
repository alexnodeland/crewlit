import streamlit as st
from crewlit.app.components import ConfigComponent
from crewlit.app.components.shared_components import Footer
from crewlit.services import ToolService
from crewlit.utils import get_logger

logger = get_logger(__name__)

TOOLS_YAML = "data/tools.yaml"

def Config():
    logger.info("Setting up the Config page.")
    st.set_page_config(page_title="Crewlit - Config", page_icon="🚣", layout="wide")

    st.title("Configuration Manager")

    with st.expander("About Config"):
        st.markdown("""
        Welcome to Crewlit's Configuration Manager! 🎛️

        Crewlit is an open-source Streamlit application that brings the power of CrewAI to your browser. This configuration page allows you to:

        - 🔧 Set up global configurations for your AI crews
        - 🔑 Manage API keys for various services
        
        Proper configuration is crucial for unleashing the full potential of your multi-agent AI systems.
        """)

    st.info("💡 Tip: Keep your API keys secure and regularly update your configurations to ensure smooth operation of your AI crews.")


    tool_service = ToolService(TOOLS_YAML)

    config_component = ConfigComponent(tool_service)

    logger.debug("Rendering config component.")
    config_component.render_config()
    logger.info("Config page setup complete.")

    Footer()
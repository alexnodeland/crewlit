import streamlit as st
from crewlit.services import ToolService
from crewlit.app.components import ToolComponent
from crewlit.app.components.shared_components import Footer
from crewlit.utils import get_logger

logger = get_logger(__name__)

TOOLS_YAML = "data/tools.yaml"

def Tools():
    logger.info("Setting up the Tools page.")
    st.set_page_config(page_title="Crewlit - Tools", page_icon="🛠️", layout="wide")

    st.title("Tool Manager")

    with st.expander("About Tools"):
        st.markdown("""
        Explore and manage powerful tools to enhance your AI agents' capabilities.

        Here you can:
        - 🔧 Browse a wide range of pre-configured tools
        - 🛠️ Enable and configure tools to enhance your agents' capabilities
        - 🔑 Manage keys for various services
                    
        Effective tool utilization is key to creating versatile and powerful AI agent crews.
        """)

    st.info("💡 Tip: Combine multiple tools to create sophisticated AI workflows and solve complex problems.")


    tool_service = ToolService(TOOLS_YAML)
    tool_component = ToolComponent(tool_service)

    logger.debug("Rendering tool explorer.")
    tool_component.render_tool_explorer()
    logger.info("Tools page setup complete.")

    Footer()
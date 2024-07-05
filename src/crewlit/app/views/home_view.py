import streamlit as st
from crewlit.app.components import HomeComponent
from crewlit.app.components.shared_components import Footer
from crewlit.utils import get_logger

logger = get_logger(__name__)

def Home():
    logger.info("Setting up the Home page.")
    st.set_page_config(page_title="Crewlit", page_icon="🚣", layout="wide")

    st.title('🚣 Crewlit')
    st.info("Welcome to Crewlit! This is a tool for managing and executing [crewAI](https://crewai.com/) crews, via a simple [Streamlit](https://streamlit.io/) web app.")

    logger.debug("Rendering app section.")
    HomeComponent.render_app_section()
    logger.debug("Rendering connections section.")
    HomeComponent.render_connections_section()
    logger.debug("Rendering information section.")
    HomeComponent.render_information_section()
    logger.info("Home page setup complete.")

    Footer()
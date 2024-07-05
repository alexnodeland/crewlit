import streamlit as st
from crewlit.utils import get_logger

from crewlit.app.views.agent_view import Agents
from crewlit.app.views.task_view import Tasks
from crewlit.app.views.crew_view import Crews
from crewlit.app.views.kickoff_view import Kickoff
from crewlit.app.views.tool_view import Tools
from crewlit.app.views.config_view import Config
from crewlit.app.views.about_view import About
from crewlit.app.views.linked_docs_view import Linked_Docs

logger = get_logger(__name__)

class HomeComponent:
    @staticmethod
    def render_app_section():
        logger.info("Rendering app section")
        with st.container(border=True):
            st.write("### 🚀 Build Your AI Crew")
            st.write("Create and manage AI agents, tasks, and crews for powerful multi-agent automations.")
            
            col1, col2 = st.columns(2)
            with col1:
                HomeComponent._render_card("Tasks", "📝", "Define objectives for your AI agents.", Tasks)
                HomeComponent._render_card("Agents", "👩‍💼", "Create specialized AI agents with unique roles.", Agents)
            with col2:
                HomeComponent._render_card("Crews", "👥", "Assemble AI teams for complex workflows.", Crews)
                HomeComponent._render_card("Kickoff", "🏁", "Launch your AI crews and monitor their progress.", Kickoff)

    @staticmethod
    def render_connections_section():
        logger.info("Rendering connections section")
        with st.container(border=True):
            st.write("### 🔗 Enhance Your Crew")
            st.write("Integrate tools and configure your CrewAI environment.")
            
            col1, col2 = st.columns(2)
            with col1:
                HomeComponent._render_card("Tools", "🛠️", "Add powerful capabilities to your agents.", Tools)
            with col2:
                HomeComponent._render_card("Config", "⚙️", "Customize your CrewAI setup.", Config)

    @staticmethod
    def render_information_section():
        logger.info("Rendering information section")
        with st.container(border=True):
            st.write("### ℹ️ Explore CrewAI")
            st.write("Discover the potential of multi-agent AI automations.")
            
            col1, col2 = st.columns(2)
            with col1:
                HomeComponent._render_card("About", "ℹ️", "Learn about CrewAI's features and benefits.", About)
            with col2:
                HomeComponent._render_card("Docs", "📄", "Access comprehensive CrewAI documentation.", Linked_Docs)

    @staticmethod
    def _render_card(label, icon, help_text, page):
        with st.container(border=True):
            st.page_link(st.Page(page), label=f"{icon} {label}", help=help_text, use_container_width=True)
            st.caption(help_text)

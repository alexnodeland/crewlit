import streamlit as st
from crewlit.app.components.shared_components import Footer
from crewlit.utils import get_logger

logger = get_logger(__name__)

def About():
    logger.info("Setting up the About page.")
    st.set_page_config(page_title="Crewlit - About", page_icon="ℹ️", layout="wide")

    st.title('🚀 About Crewlit')
    
    st.markdown("""
    ## Unleash the Power of Multi-Agent AI Systems

    Crewlit brings CrewAI's robust framework to your browser, making AI agent crews accessible to everyone.
    """
    )
    st.info("[Star us](https://github.com/alexnodeland/crewlit) on GitHub and contribute to the future of AI agent crews!")
    st.markdown("""
    ### 🌟 Key Features
    - **Create & Manage AI Agents**: Custom roles, goals, and backstories
    - **Define Tasks**: Set objectives for your AI crews
    - **Assemble Teams**: Build powerful AI crews effortlessly
    - **Configure Tools**: Enhance agent capabilities
    - **Real-time Execution**: Monitor crew progress instantly

    ### 💪 Why Crewlit?
    - **User-Friendly**: No coding required
    - **Flexible**: Use templates or create custom solutions
    - **Open-Source**: Community-driven development
    - **Powered by CrewAI**: Production-ready multi-agent automations

    ### 🛠️ Start Building Today
    Transform your workflows with AI agent crews - no expertise needed!
    """)

    Footer()

if __name__ == '__main__':
    About()
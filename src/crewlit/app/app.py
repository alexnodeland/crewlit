import streamlit as st

from crewlit.app.views import Home, Agents, Tasks, Crews, Tools, Config, Kickoff, About, Linked_Docs
from crewlit.utils import get_logger, setup_logging



def main():
    setup_logging()

    logger = get_logger("crewlit.app.app")

    logger.info("Setting up pages for the application.")
    pages = {
        "Home": [
            st.Page(Home, title="🚣 Home"),
        ],
        "AI Workspace": [
            st.Page(Tasks, title="📋 Tasks"),
            st.Page(Agents, title="🧑‍💼 Agents"),
            st.Page(Crews, title="👥 Crews"),
            st.Page(Kickoff, title="🏁 Kickoff"),
        ],
        "Integrations": [
            st.Page(Tools, title="🛠️ Tools"),
            st.Page(Config, title="⚙️ Config"),
        ],
        "Resources": [
            st.Page(About, title="ℹ️ About"),
            st.Page(Linked_Docs, title="📄 Linked Docs"),
        ],
    }
    logger.debug(f"Pages configuration: {pages}...")
    pg = st.navigation(pages)
    logger.info("Running the selected page.")
    pg.run()

if __name__ == '__main__':
    main()
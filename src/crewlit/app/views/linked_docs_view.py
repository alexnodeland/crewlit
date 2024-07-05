import streamlit as st

from crewlit.app.components.shared_components import Footer
from crewlit.utils import get_logger

logger = get_logger(__name__)

def Linked_Docs():
    logger.info("Setting up the Linked Docs page.")
    st.set_page_config(page_title="Crewlit - Linked Docs", page_icon="📄", layout="wide")

    st.header("Useful Resources")

    st.info("This project was built using Streamlit and CrewAI, along with some other great tools.\n\nHere are some additional resources to help you get started")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader("Streamlit")
            st.write("Essential documentation and resources:")
            st.page_link("https://streamlit.io/", label="Streamlit Website", icon="🚀")
            st.page_link("https://docs.streamlit.io/", label="Streamlit Docs", icon="📚")
            st.page_link("https://streamlit.io/gallery", label="Streamlit Gallery", icon="🖼️")

    with col2:
        with st.container(border=True):
            st.subheader("CrewAI")
            st.write("Learn more about CrewAI:")
            st.page_link("https://crewai.com/", label="CrewAI Website", icon="🌐")
            st.page_link("https://docs.crewai.com/", label="CrewAI Docs", icon="🤖")
            st.page_link("https://github.com/joaomdmoura/crewAI", label="CrewAI GitHub", icon="📂")

    with col3:
        with st.container(border=True):
            st.subheader("Additional Resources")
            st.write("Explore other AI tools used in this project:")
            st.page_link("https://python.langchain.com/docs/get_started/introduction", label="LangChain Docs", icon="🦜")
            st.page_link("https://platform.openai.com/docs/introduction", label="OpenAI API Docs", icon="🧠")
            st.page_link("https://huggingface.co/docs", label="Hugging Face Docs", icon="🤗")

    Footer()
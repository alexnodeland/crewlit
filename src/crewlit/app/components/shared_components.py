import streamlit as st

def Footer():
    st.divider()
    st.markdown("Created with ❤️ by [Alex Nodeland](https://github.com/alexnodeland)")
    st.markdown("[Crewlit GitHub](https://github.com/alexnodeland/crewlit/) | [CrewAI Docs](https://docs.crewai.com)")
    with st.expander("Feedback"):
        st.write("Have suggestions for Crewlit? We'd love to hear from you!")
        st.page_link(
            "https://github.com/alexnodeland/crewlit/issues",
            label="Submit Feedback on GitHub",
            icon="📢"
        )
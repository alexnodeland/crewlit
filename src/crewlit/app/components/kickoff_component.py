import streamlit as st
from crewlit.utils import get_logger

logger = get_logger(__name__)

class KickoffComponent:
    def __init__(self, kickoff_service, crew_service):
        self.kickoff_service = kickoff_service
        self.crew_service = crew_service

    def render_kickoff(self):
        logger.info("Rendering kickoff page")
        with st.container(border=True):
            st.write("#### Execute Crew")

            crews = self.crew_service.get_all_crews()
            if not crews:
                st.warning("No crews available. Please create a crew first.")
                return
            crew_options = {crew.label: name for name, crew in crews.items()}
            
            selected_crew_label = st.selectbox("Select a crew to execute", list(crew_options.keys()), help="Select a crew and click 'Execute Crew' to start the execution.")
            selected_crew_name = crew_options[selected_crew_label]
            logger.debug(f"Selected crew: {selected_crew_label} ({selected_crew_name})")

            if st.button("Execute Crew", use_container_width=True):
                logger.info(f"Executing crew: {selected_crew_name}")
                with st.spinner("Executing crew..."):
                    try:
                        result = self.kickoff_service.execute_crew(selected_crew_name)
                        st.success("Crew execution completed!")
                        with st.expander("Execution Result", expanded=True):
                            st.write("Result:", result)
                        logger.info(f"Crew execution completed successfully for: {selected_crew_name}")
                    except Exception as e:
                        st.error(f"An error occurred during execution: {str(e)}")
                        logger.error(f"Error during crew execution for {selected_crew_name}: {str(e)}")
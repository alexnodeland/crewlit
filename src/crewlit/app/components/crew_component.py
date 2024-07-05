import streamlit as st
import os
from crewlit.models import Crew, AgentConfig, TaskConfig, LLMConfig, CrewConfig
from crewlit.utils import get_logger

logger = get_logger(__name__)

class CrewComponent:
    def __init__(self, crew_service, agent_service, task_service, tool_service):
        self.crew_service = crew_service
        self.agent_service = agent_service
        self.task_service = task_service
        self.tool_service = tool_service

    def render_crew_creator(self):
        logger.info("Rendering crew creator")
        with st.expander("Create Crew", expanded=not self.crew_service.get_all_crews()):
            with st.form(key="create_crew_form"):
                crew_name = st.text_input("Name", help="Enter the name of the crew")
                selected_agent_names, selected_task_names, crew_config = self._crew_creator()
                submit_button = st.form_submit_button("Create Crew")

                if submit_button:
                    agents = {name: {} for name in selected_agent_names}
                    tasks = {name: {} for name in selected_task_names}
                    self.crew_service.create_crew(label=crew_name, agents=agents, tasks=tasks, crew_config=crew_config)
                    st.success(f"Crew '{crew_name}' created successfully!")
                    logger.info(f"Crew '{crew_name}' created successfully")
        
    def _task_selector(self):
        logger.info("Selecting tasks")
        all_tasks = self.task_service.get_all_tasks()
        task_options = [task.title for task in all_tasks.values()]
        selected_tasks = st.multiselect("Select Tasks", options=task_options, help="Choose tasks for this crew")
        selected_task_names = [name for name, task in all_tasks.items() if task.title in selected_tasks]
        logger.debug(f"Selected tasks: {selected_task_names}")
        return selected_task_names
    
    def _agent_selector(self):
        logger.info("Selecting agents")
        all_agents = self.agent_service.get_all_agents()
        agent_options = [agent.role for agent in all_agents.values()]
        selected_agents = st.multiselect("Select Agents", options=agent_options, help="Choose agents for this crew")
        selected_agent_names = [name for name, agent in all_agents.items() if agent.role in selected_agents]
        logger.debug(f"Selected agents: {selected_agent_names}")
        return selected_agent_names
    
    def _llm_settings(self):
        logger.info("Configuring LLM settings")
        model = st.selectbox("Model", ["gpt-4o", "gpt-3.5-turbo"], help="Select the model for the crew")
        temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=1.0, help="Set the default temperature for the LLM")
        top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=1.0, help="Set the default top p for the LLM")
        llm_config = LLMConfig(model_name=model, temperature=temperature, top_p=top_p)
        logger.debug(f"LLM settings: {llm_config}")
        return llm_config
    
    def _crew_creator(self):
        logger.info("Creating crew")
        tab1, tab2, tab3, tab4 = st.tabs(["Tasks", "Agents", "Process", "Output"])
        with tab1:
            selected_task_names = self._task_selector()
        with tab2:
            selected_agent_names = self._agent_selector()  
            with st.popover("Default Agent LLM", help="Set the default LLM settings for the agents in the crew.", use_container_width=True):
                st.info("*This can be overwritten on a per-agent basis, later.*")     
                default_agent_llm = self._llm_settings()
        with tab3:
            process = st.selectbox("Process", ["sequential", "hierarchical"], help="Select the process for the crew")
        with tab4:
            verbose = st.checkbox("Verbose", help="Enable verbose mode for the crew", value=True)
            output_log_file = st.text_input("Output Log File", help="Enter the output log file for the crew", value="output/crew.log")

        crew_config = CrewConfig(process=process, verbose=verbose, output_log_file=output_log_file, default_agent_llm=default_agent_llm)
        logger.debug(f"Crew config: {crew_config}")

        return selected_agent_names, selected_task_names, crew_config
    
    def render_crew_explorer(self):
        logger.info("Rendering crew explorer")
        with st.container(border=True):
            crews = self.crew_service.get_all_crews()
            title, download = st.columns([3, 1])
            with title:
                st.write("#### My Crews")
                total_crews = len(self.crew_service.get_all_crews())
                st.metric("Total Crews", total_crews)
            with download:
                if crews:
                    self._render_download_button()
                with st.popover("Upload", use_container_width=True):
                    self._render_upload_button()
            if not crews:
                st.info("No crews created yet. Use the form above to create your first crew.")
            else:
                for crew_name, crew in crews.items():
                    self._display_and_edit_crew(crew_name, crew)

    def _display_and_edit_crew(self, crew_name, crew):
        logger.info(f"Displaying and editing crew: {crew_name}")
        with st.container(border=True):
            title, editor = st.columns([1, 4])
            with title:
                st.write(f"{crew.label}")
            with editor:
                with st.expander("Edit", expanded=False):
                    new_label = st.text_input("Name", value=crew.label, key=f"name_{crew_name}")
                    
                    tab1, tab2, tab3 = st.tabs(["Crew Configuration", "Agents", "Tasks"])
                    
                    with tab1:
                        new_crew_config = self._edit_crew_config(crew.crew, crew_name)
                    
                    with tab2:
                        new_agents = self._edit_agents(crew.agents, crew_name)
                    
                    with tab3:
                        new_tasks = self._edit_tasks(crew.tasks, crew_name)
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        update_button = st.button("Update", key=f"update_{crew_name}", use_container_width=True)
                    with col2:
                        delete_button = st.button("Delete", key=f"delete_{crew_name}", use_container_width=True)

                    if update_button:
                        self.crew_service.update_crew(crew_name, new_label, new_agents, new_tasks, new_crew_config)
                        st.success(f"Crew '{new_label}' updated successfully!")
                        logger.info(f"Crew '{new_label}' updated successfully")
                        st.rerun()
                                
                    if delete_button:
                        deleted_label = self.crew_service.delete_crew(crew_name)
                        st.success(f"Crew '{deleted_label}' deleted successfully!")
                        logger.info(f"Crew '{deleted_label}' deleted successfully")
                        st.rerun()

    def _edit_crew_config(self, crew_config, crew_name):
        logger.info(f"Editing crew config for: {crew_name}")
        tab1, tab2 = st.tabs(["General", "Default Agent LLM"])
        with tab1:
            process = st.selectbox("Process", ["sequential", "hierarchical"], index=0 if crew_config.process == "sequential" else 1, key=f"process_{crew_name}")
            verbose = st.checkbox("Verbose", value=crew_config.verbose, key=f"verbose_{crew_name}")
            output_log_file = st.text_input("Output Log File", value=crew_config.output_log_file, key=f"output_log_{crew_name}")
        with tab2:    
            default_agent_llm = self._edit_llm_config(crew_config.default_agent_llm, f"default_{crew_name}")
                
        return CrewConfig(
            process=process,
            verbose=verbose,
            output_log_file=output_log_file,
            default_agent_llm=default_agent_llm
        )

    def _edit_agents(self, agents, crew_name):
        logger.info(f"Editing agents for crew: {crew_name}")
        new_agents = {}
        for agent_name, agent_config in agents.items():
            with st.container(border=True):
                st.write(f"Agent: {agent_name.replace('_', ' ').title()}")
                new_agents[agent_name] = self._edit_agent_config(agent_config, f"{agent_name}_{crew_name}")
        return new_agents

    def _edit_agent_config(self, agent_config, key):
        logger.info(f"Editing agent config: {key}")
        col1, col2 = st.tabs(["Agent", "LLM"])
        with col1:
            allow_delegation = st.checkbox("Allow Delegation", value=agent_config.allow_delegation, key=f"allow_delegation_{key}", help="Allow the agent to delegate tasks to other agents")
            verbose = st.checkbox("Verbose", value=agent_config.verbose, key=f"verbose_{key}", help="Enable verbose output for the agent, showing detailed logs")
            max_iter = st.number_input("Max Iterations", value=agent_config.max_iter, min_value=1, key=f"max_iter_{key}", help="Set the maximum number of iterations for the agent, before being forced to make their best aanswer for the task")
            max_execution_time = st.number_input("Max Execution Time", value=agent_config.max_execution_time or 0, min_value=0, key=f"max_exec_time_{key}")
            enabled_tools = self.tool_service.get_enabled_tools()
            tool_options = [tool.name for tool in enabled_tools.values()]
            tool_keys = list(enabled_tools.keys())
            selected_tools = st.multiselect(
                "Tools",
                options=tool_options,
                default=[enabled_tools[tool_key].name for tool_key in agent_config.tools if tool_key in enabled_tools],
                key=f"tools_{key}"
            )
            selected_tool_keys = [tool_keys[tool_options.index(tool)] for tool in selected_tools]
        with col2:    
            with st.container(border=True):
                st.write("LLM Settings")
                llm_config = self._edit_llm_config(LLMConfig(**agent_config.llm) if agent_config.llm else None, f"llm_{key}")
                
        return AgentConfig(
            allow_delegation=allow_delegation,
            verbose=verbose,
            llm=llm_config.dict() if llm_config else None,
            max_iter=max_iter,
            max_execution_time=max_execution_time or None,
            tools=selected_tool_keys
        )

    def _edit_tasks(self, tasks, crew_name):
        logger.info(f"Editing tasks for crew: {crew_name}")
        new_tasks = {}
        crew = self.crew_service.get_crew(crew_name)
        agent_names = [name.replace('_', ' ').title() for name in crew.agents.keys()]
        for task_name, task_config in tasks.items():
            with st.container(border=True):
                st.write(f"Task: {task_name.replace('_', ' ').title()}")
                new_tasks[task_name] = self._edit_task_config(task_config, task_name, f"{task_name}_{crew_name}", tasks.keys(), agent_names)
        return new_tasks

    def _edit_task_config(self, task_config, task_name, key, all_task_names, all_agent_names):
        logger.info(f"Editing task config: {task_name}")
        tab1, tab2 = st.tabs(["Task", "Output"])
        with tab1:
            selected_agent = st.selectbox("Agent", options=all_agent_names, index=all_agent_names.index(task_config.agent) if task_config.agent in all_agent_names else 0, key=f"agent_{key}")
            agent = selected_agent.replace(' ', '_').lower()
            
            current_task = task_name
            other_tasks = [task.replace('_', ' ').title() for task in all_task_names if task != current_task]
            selected_context = st.multiselect("Context (Other Tasks)", options=other_tasks, default=task_config.context, key=f"context_{key}")
            context = [task.replace(' ', '_').lower() for task in selected_context]

            enabled_tools = self.tool_service.get_enabled_tools()
            tool_options = [tool.name for tool in enabled_tools.values()]
            tool_keys = list(enabled_tools.keys())
            selected_tools = st.multiselect(
                "Tools",
                options=tool_options,
                default=[enabled_tools[tool_key].name for tool_key in task_config.tools if tool_key in enabled_tools],
                key=f"tools_{key}"
            )
            selected_tool_keys = [tool_keys[tool_options.index(tool)] for tool in selected_tools]
            human_input = st.checkbox("Human Input", value=task_config.human_input, key=f"human_input_{key}")
        with tab2:
            output_file = st.text_input("Output File", value=task_config.output_file or "", key=f"output_file_{key}")
            create_directory = st.checkbox("Create Directory", value=task_config.create_directory, key=f"create_dir_{key}")
        
        return TaskConfig(
            agent=agent,
            context=context,
            tools=selected_tool_keys,
            human_input=human_input,
            output_file=output_file or None,
            create_directory=create_directory
        )

    def _edit_llm_config(self, llm_config, key):
        logger.info(f"Editing LLM config: {key}")
        if llm_config is None:
            llm_config = LLMConfig()
        
        model_name = st.selectbox("Model Name", ["gpt-3.5-turbo", "gpt-4o"], index=0 if llm_config.model_name == "gpt-3.5-turbo" else 1, key=f"model_{key}")
        temperature = st.slider("Temperature", min_value=0.00, max_value=1.00, value=llm_config.temperature, step=0.01, key=f"temp_{key}")
        top_p = st.slider("Top P", min_value=0.00, max_value=1.00, value=llm_config.top_p, step=0.01, key=f"top_p_{key}")
        
        return LLMConfig(
            model_name=model_name,
            temperature=temperature,
            top_p=top_p
        )

    def _render_download_button(self):
        logger.info("Rendering download button")
        yaml_content = self.crew_service.get_crews_yaml()
        st.download_button(
            label=":file_folder: Download",
            data=yaml_content,
            file_name="crews.yaml",
            mime="text/yaml",
            use_container_width=True
        )

    def _render_upload_button(self):
        logger.info("Rendering upload button")
        CREW_YAML = "data/crews.yaml"
        with st.form("upload_crew_form"):
            st.warning("Uploading a new crews file will overwrite the existing crews.")
            uploaded_file = st.file_uploader("Upload Crews", type="yaml", label_visibility="collapsed")
            submit_button = st.form_submit_button("Upload", use_container_width=True)

            if submit_button and uploaded_file is not None:
                try:
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(CREW_YAML), exist_ok=True)
                    
                    # Save the uploaded file
                    with open(CREW_YAML, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    st.success("Crews file uploaded successfully!")
                    logger.info("Crews file uploaded successfully")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving crews file: {str(e)}")
                    logger.error(f"Error saving crews file: {str(e)}")

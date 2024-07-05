import os
import streamlit as st
from crewlit.utils import get_logger

logger = get_logger(__name__)

class TaskComponent:
    def __init__(self, task_service):
        self.task_service = task_service

    def render_task_creator(self):    
        with st.expander("Add Task", expanded=not self.task_service.get_all_tasks()):
            with st.popover("Instructions", use_container_width=True):
                st.write("If you have a new task to add, enter the details here.")
            with st.form(key="create_task_form"):
                new_task_title = st.text_input("Title", help="Enter the title of the task.")
                new_task_description = st.text_area("Description", help="Enter the description of the task.")
                new_task_expected_output = st.text_area("Expected Output", help="Enter the expected output of the task.")
                submit_button = st.form_submit_button("Add Task", use_container_width=True)

            if submit_button:
                logger.info("Submit button clicked for creating a new task.")
                formatted_title = self.task_service.create_task(new_task_title, new_task_description, new_task_expected_output)
                if formatted_title:
                    logger.info(f"Task '{formatted_title}' created successfully.")
                    st.success(f"Task '{formatted_title}' created successfully!")
                    st.rerun()
                else:
                    logger.warning("A task with this title already exists.")
                    st.error("A task with this title already exists. Please choose a different title.")

    def render_task_explorer(self):
        with st.container(border=True):
            tasks = self.task_service.get_all_tasks()
            title, download = st.columns([3, 1])
            with title:
                st.write("#### My Tasks")
                total_tasks = len(self.task_service.get_all_tasks())
                st.metric("Total Tasks", total_tasks)
            with download:
                if tasks:
                    self._render_download_button()
                with st.popover("Upload", use_container_width=True):
                    self._render_upload_button()
            if not tasks:
                st.info("No tasks created yet. Use the form below to create your first task.")
            else:
                for task_name, task in tasks.items():
                    self._display_and_edit_task(task_name, task)

    def _display_and_edit_task(self, task_name, task):
        with st.container(border=True):
            title, editor = st.columns([1, 4])
            with title:
                st.write(f"{task.title}")
            with editor:
                with st.expander("Edit", expanded=False):
                    title = st.text_input("Title", value=task.title, key=f"title_{task_name}")
                    description = st.text_area("Description", value=task.description, key=f"description_{task_name}")
                    expected_output = st.text_area("Expected Output", value=task.expected_output, key=f"expected_output_{task_name}")
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        update_button = st.button("Update", key=f"update_{task_name}", use_container_width=True)
                    with col2:
                        delete_button = st.button("Delete", key=f"delete_{task_name}", use_container_width=True)

                    if update_button:
                        logger.info(f"Update button clicked for task '{task_name}'.")
                        formatted_title = self.task_service.update_task(task_name, title, description, expected_output)
                        logger.info(f"Task '{formatted_title}' updated successfully.")
                        st.success(f"Task '{formatted_title}' updated successfully!")
                        st.rerun()
                                    
                    if delete_button:
                        logger.info(f"Delete button clicked for task '{task_name}'.")
                        deleted_title = self.task_service.delete_task(task_name)
                        logger.info(f"Task '{deleted_title}' deleted successfully.")
                        st.success(f"Task '{deleted_title}' deleted successfully!")
                        st.rerun()
    
    def _render_download_button(self):
        yaml_content = self.task_service.get_tasks_yaml()
        st.download_button(
            label=":file_folder: Download",
            data=yaml_content,
            file_name="tasks.yaml",
            mime="text/yaml",
            use_container_width=True
        )

    def _render_upload_button(self):
        TASK_YAML = "data/tasks.yaml"
        
        with st.form("upload_task_form"):
            uploaded_file = st.file_uploader("Upload Tasks", type="yaml", label_visibility="collapsed")
            submit_button = st.form_submit_button("Upload")

            if submit_button and uploaded_file is not None:
                try:
                    logger.info("Upload button clicked for uploading tasks.")
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(TASK_YAML), exist_ok=True)
                    
                    # Save the uploaded file
                    with open(TASK_YAML, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    logger.info("Tasks file uploaded successfully.")
                    st.success("Tasks file uploaded successfully!")
                    st.rerun()
                except Exception as e:
                    logger.error(f"Error saving tasks file: {str(e)}")
                    st.error(f"Error saving tasks file: {str(e)}")
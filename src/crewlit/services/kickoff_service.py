from crewai import Agent, Crew, Process, Task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from langchain_openai import ChatOpenAI

from crewlit.services import CrewService, AgentService, TaskService, ToolService
from crewlit.utils import setup_logging, get_logger

logger = get_logger(f"services.{__name__}")

class KickoffService:
    def __init__(self, crew_service, agent_service, task_service, tool_service):
        self.crew_service = crew_service
        self.agent_service = agent_service
        self.task_service = task_service
        self.tool_service = tool_service
        self.agent_objects = {}
        self.task_objects = {}
        logger.debug("KickoffService initialized with provided services.")

    def create_crew(self, crew_name) -> Crew:
        logger.info(f"Creating crew: {crew_name}")
        crew_data = self.crew_service.get_crew(crew_name)
        if not crew_data:
            logger.error(f"Crew '{crew_name}' not found")
            raise ValueError(f"Crew '{crew_name}' not found")

        crew_class = self.generate_crew_class(crew_data)
        logger.info(f"Crew '{crew_name}' created successfully")
        return crew_class

    def generate_crew_class(self, crew_data) -> Crew:
        class_name = f"{crew_data.label.replace(' ', '')}Crew"
        logger.debug(f"Generating crew class: {class_name}")
        
        # Dynamically add agent objects
        self.agent_objects = {}
        for agent_name, agent_config in crew_data.agents.items():
            agent_data = self.agent_service.get_all_agents().get(agent_name)
            if agent_data:
                logger.debug(f"Constructing agent object for: {agent_name}")
                agent_object_config = {
                    "role": agent_data.role,
                    "goal": agent_data.goal,
                    "backstory": agent_data.backstory,
                    "allow_delegation": agent_config.allow_delegation,
                    "verbose": agent_config.verbose,
                    "tools": [self.generate_tool_object(tool) for tool in agent_config.tools],
                    "llm": self.generate_llm_object(agent_config.llm),
                    "max_iter": agent_config.max_iter,
                    "max_execution_time": agent_config.max_execution_time,
                }
                agent_object = self.generate_agent_object(**agent_object_config)
                self.agent_objects[agent_name.lower().replace(' ', '_')] = agent_object
                logger.info(f"Agent object for '{agent_name}' created successfully.")
    
        # First pass: Create task objects without context
        self.task_objects = {}
        for task_name, task_config in crew_data.tasks.items():
            task_data = self.task_service.get_all_tasks().get(task_name)
            if task_data:
                logger.debug(f"Creating task object for: {task_name}")
                task_object = self.generate_task_object_without_context(task_name, task_data, task_config)
                self.task_objects[task_name.lower().replace(' ', '_')] = task_object
                logger.info(f"Task object for '{task_name}' created successfully.")

        # Second pass: Set context for all tasks
        self.set_task_contexts(crew_data.tasks)
        logger.debug("Task contexts set successfully.")

        crew = Crew(agents=list(self.agent_objects.values()), tasks=list(self.task_objects.values()), process=Process.sequential)
        logger.info(f"Crew '{crew_data.label}' created successfully with agents and tasks.")
        return crew

    def generate_agent_object(self, role, goal, backstory, allow_delegation, verbose, tools, llm, max_iter, max_execution_time):
        logger.debug(f"Generating agent object with role: {role}, goal: {goal}")
        agent_object = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            allow_delegation=allow_delegation,
            verbose=verbose,
            tools=tools,
            llm=llm,
            max_iter=max_iter,
            max_execution_time=max_execution_time
        )
        logger.info(f"Agent object for role '{role}' created successfully.")
        return agent_object


    def generate_task_object_without_context(self, task_name, task_data, task_config):
        logger.debug(f"Generating task object for task: {task_name}")
        task_object = Task(
            description=task_data.description,
            expected_output=task_data.expected_output,
            agent=self.agent_objects.get(task_config.agent.lower().replace(' ', '_')),
            context=[], # Set context in set_task_contexts
            human_input=task_config.human_input,
            output_file=task_config.output_file,
            create_directory=task_config.create_directory
        )
        logger.info(f"Task object for task '{task_name}' created successfully.")
        return task_object
    
    def set_task_contexts(self, tasks_config):
        for task_name, task in self.task_objects.items():
            logger.debug(f"Setting context for task: {task_name}")
            task_config = tasks_config.get(task_name)
            if task_config and task_config.context:
                context_tasks = []
                for context_task_name in task_config.context:
                    context_task = self.task_objects.get(context_task_name.lower().replace(' ', '_'))
                    if context_task:
                        context_tasks.append(context_task)
                    else:
                        logger.warning(f"Context task '{context_task_name}' not found for task '{task_name}'.")
                task.context = context_tasks
    
    def generate_llm_object(self, llm_config):
        logger.debug(f"Generating LLM object with config: {llm_config}")
        llm =  ChatOpenAI(
            model_name=llm_config.get("model_name"),
            temperature=llm_config.get("temperature"),
            model_kwargs = {
                "top_p": llm_config.get("top_p")
            }
        )
        logger.info("LLM object created successfully.")
        return llm
    
    def generate_tool_object(self, tool_name):
        logger.debug(f"Generating tool object for tool: {tool_name}")
        tool_classes = {
                "scrape_website": ScrapeWebsiteTool,
                "serper_dev": SerperDevTool
            }
        tool_data = self.tool_service.get_all_tools().get(tool_name)
        if tool_data:
            key = tool_data.name.replace(' ', '_').lower()
            tool_class = tool_classes.get(key)
            if tool_class:
                logger.info(f"Tool object for '{tool_name}' created successfully.")
                return tool_class()
            else:
                logger.warning(f"Tool class for '{tool_name}' not found.")
        else:
            logger.warning(f"Tool data for '{tool_name}' not found.")

    def execute_crew(self, crew_name):
        logger.info(f"Executing crew: {crew_name}")
        dynamic_crew = self.create_crew(crew_name)
        result = dynamic_crew.kickoff()
        logger.info(f"Crew execution result: {result}")
        return result
    
def main():
    setup_logging()

    logger.info("Initializing services...")
    crew_service = CrewService("data/crews.yaml")
    agent_service = AgentService("data/agents.yaml")
    task_service = TaskService("data/tasks.yaml")
    tool_service = ToolService("data/tools.yaml")
    kickoff_service = KickoffService(crew_service, agent_service, task_service, tool_service)

    logger.info("Executing crew...")
    kickoff_service.execute_crew("market_research_crew")

if __name__ == "__main__":
    main()
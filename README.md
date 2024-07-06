# 🚣 Crewlit

Crewlit is an open-source Streamlit application that brings the power of [CrewAI](https://crewai.com/) to your browser. It provides a user-friendly interface for creating, managing, and executing AI agent crews, making multi-agent AI systems accessible to everyone.

![Crewlit Screenshot](assets/crewlit_home.png)

## 🌟 Features

- 🤖 **AI Agent Management**: Create and customize AI agents with unique roles, backstories, and goals.
- 📋 **Task Definition**: Craft specific tasks for your AI agents to accomplish.
- 👥 **Crew Assembly**: Combine agents and tasks to form powerful AI crews.
- 🛠️ **Tool Integration**: Enhance your agents' capabilities with various configurable tools.
- ⚙️ **Configuration Management**: Set up global settings, including API keys and default parameters.
- 📊 **Execution Dashboard**: Launch and monitor your AI crews' progress in real-time.
- 🖱️ **User-Friendly Interface**: Navigate effortlessly with our intuitive Streamlit-based UI.

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- Poetry for dependency management

### Installation

1. Clone the repository:

```bash
git clone https://github.com/alexnodeland/crewlit.git
cd crewlit
```

2. Run the application:

   a. Using the provided script (recommended):

    ```bash
    ./scripts/run.sh
    ```

    This script will:
    - Check if Poetry is installed and install it if necessary
    - Install or update project dependencies
    - Run the Streamlit app

   b. Alternatively, if you prefer manual setup:

    ```bash
    poetry install && poetry run app
    ```

    This command installs dependencies and runs the app using Poetry.

3. Open your browser and navigate to [`http://localhost:8501`](http://localhost:8501) to start using Crewlit!

## 📖 Usage

Refer to the [Crewlit Guide](GUIDE.md) for detailed instructions on using the application.

## 🔗 Related Projects

- [CrewAI](https://github.com/joaomdmoura/crewAI): The underlying framework for multi-agent AI systems.
- [Streamlit](https://github.com/streamlit/streamlit): The web app framework used for the user interface.

## 🗺️ Roadmap

✅ Completed:
- UI for creating and managing tasks, agents, and crews
- Crew execution interface

🚧 In Progress:
- Multi-tenant configuration support
- Enhanced output handling (default directory, zip download, incremental display)
- Comprehensive in-app help system

🔮 Future Plans:
- Docker containerization
- Live demo deployment
- Expanded crew, agent, and task configuration options
- Single task execution support

We're constantly evolving! For feature requests or suggestions, please [open an issue](https://github.com/alexnodeland/crewlit/issues).

## 📄 License

Crewlit is open-source software licensed under the MIT license. See the [LICENSE](LICENSE) file for more details.

## 🙏 Acknowledgements

I'd like to thank the creators of [CrewAI](https://crewai.com/) ([@joaomdmoura](https://github.com/joaomdmoura/)), [Streamlit](https://streamlit.io/), and all the other open-source projects that make Crewlit possible.

## 🤝 Support

If you encounter any issues or have questions, please [open an issue](https://github.com/alexnodeland/crewlit/issues) on the GitHub repository.

---

Made with ❤️ by [@alexnodeland](https://github.com/alexnodeland)

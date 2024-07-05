import subprocess

def run_streamlit_app():
    subprocess.run(["poetry", "run", "streamlit", "run", "src/crewlit/app/app.py"])

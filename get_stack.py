import subprocess
import os 

project_path = "C:/Users/lemda/Documents/test"
script_name = "test.py"
env_name = "env"

def run_script(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr

# Correct path for Windows venv
interpeter = os.path.join(project_path, env_name, "Scripts", "python.exe")

script_path = os.path.join(project_path, script_name)
command = [interpeter, script_path]

stdout, stderr = run_script(command)
print(stdout, stderr)

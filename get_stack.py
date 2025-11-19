import subprocess
import os
from typing import Tuple

def run_in_venv(project_path: str, script_name: str, env_name: str = "env") -> Tuple[str, str]:
    

    # Detect OS (Windows uses Scripts/, Linux/Mac use bin/)
    if os.name == "nt":  # Windows
        interpreter = os.path.join(project_path, env_name, "Scripts", "python.exe")
    else:                # Linux/Mac
        interpreter = os.path.join(project_path, env_name, "bin", "python")

    script_path = os.path.join(project_path, script_name)

    # Run script
    result = subprocess.run(
        [interpreter, script_path],
        capture_output=True,
        text=True
    )

    return result.stdout, result.stderr

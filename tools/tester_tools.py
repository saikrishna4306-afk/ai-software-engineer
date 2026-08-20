import os
import subprocess
import sys


IMAGE = "ai-engineer-sandbox"


def run_tests(project):

    project = os.path.abspath(project)

    # Streamlit Cloud does not use our local Docker Desktop sandbox.
    if os.getenv("STREAMLIT_CLOUD"):

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
            ],
            cwd=project,
            capture_output=True,
            text=True,
            timeout=60,
        )

    else:

        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--network",
                "none",
                "--memory",
                "512m",
                "--cpus",
                "1",
                "--pids-limit",
                "100",
                "--read-only",
                "--tmpfs",
                "/tmp",
                "-v",
                f"{project}:/workspace:rw",
                IMAGE,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

    return {
        "passed": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
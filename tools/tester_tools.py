import subprocess
import sys
from pathlib import Path


def run_tests(
    project_path: str
) -> dict:

    project_path = Path(
        project_path
    ).resolve()

    if not project_path.exists():

        raise FileNotFoundError(
            f"Project directory does not exist: "
            f"{project_path}"
        )

    if not project_path.is_dir():

        raise NotADirectoryError(
            f"Project path is not a directory: "
            f"{project_path}"
        )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest"
        ],
        cwd=str(project_path),
        capture_output=True,
        text=True
    )

    return {
        "passed":
            result.returncode == 0,

        "return_code":
            result.returncode,

        "stdout":
            result.stdout,

        "stderr":
            result.stderr
    }
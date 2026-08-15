import subprocess
import sys

from tools.file_tools import (
    list_files,
    read_file
)


def collect_project_context(
    project_path: str
) -> str:

    files = list_files(
        project_path
    )

    context = ""

    for file in files:

        if not file.endswith(".py"):
            continue

        try:

            content = read_file(
                project_path,
                file
            )

            context += (
                f"\n\n===== {file} =====\n"
            )

            context += content

        except Exception as error:

            context += (
                f"\n\n===== {file} =====\n"
                f"Could not read file: {error}"
            )

    return context


def run_project_tests(
    project_path: str
) -> dict:

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest"
        ],
        cwd=project_path,
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


def build_review_context(
    project_path: str,
    repair_plan: str
) -> dict:

    test_results = run_project_tests(
        project_path
    )

    project_context = (
        collect_project_context(
            project_path
        )
    )

    return {
        "repair_plan":
            repair_plan,

        "project_context":
            project_context,

        "tests_passed":
            test_results["passed"],

        "return_code":
            test_results["return_code"],

        "pytest_output":
            test_results["stdout"],

        "pytest_errors":
            test_results["stderr"]
    }
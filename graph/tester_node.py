from graph.state import ProjectState

from tools.tester_tools import (
    run_tests
)


def tester_node(
    state: ProjectState
) -> ProjectState:

    result = run_tests(
        state["project_path"]
    )

    return {
        **state,

        "test_output":
            result["stdout"],

        "test_errors":
            result["stderr"],

        "tests_passed":
            result["passed"]
    }
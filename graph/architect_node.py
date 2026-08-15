from graph.state import ProjectState

from agents.architect import (
    architect_agent
)

from tools.tester_tools import (
    run_tests
)


def architect_node(
    state: ProjectState
) -> ProjectState:

    result = run_tests(
        state["project_path"]
    )

    plan = architect_agent(
        state["project_path"],
        result["stdout"],
        result["stderr"]
    )

    return {
        **state,

        "repair_plan":
            plan,

        "test_output":
            result["stdout"],

        "test_errors":
            result["stderr"],

        "tests_passed":
            result["passed"]
    }
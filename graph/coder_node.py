from graph.state import ProjectState

from agents.coder import (
    coder_agent
)


def coder_node(
    state: ProjectState
) -> ProjectState:

    result = coder_agent(
        state["project_path"],
        state["repair_plan"]
    )

    return {
        **state,

        "corrected_files":
            result["corrected_files"],

        "corrected_code":
            result["corrected_code"],

        "iteration":
            state["iteration"] + 1
    }

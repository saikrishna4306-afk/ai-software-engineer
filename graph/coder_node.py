from graph.state import ProjectState

from agents.coder import (
    coder_agent
)


def coder_node(
    state: ProjectState
) -> ProjectState:

    corrected_files = coder_agent(
        state["project_path"],
        state["repair_plan"]
    )

    return {
        **state,

        "corrected_files":
            corrected_files,

        "iteration":
            state["iteration"] + 1
    }

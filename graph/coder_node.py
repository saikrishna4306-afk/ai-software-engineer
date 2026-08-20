from pathlib import Path

from graph.state import ProjectState

from agents.coder import coder_agent


def coder_node(
    state: ProjectState
) -> ProjectState:

    project = Path(
        state["project_path"]
    )

    # Save original source BEFORE Coder modifies files
    original_code = {}

    for file in state.get("files", []):

        path = project / file

        if path.exists():
            original_code[file] = path.read_text(
                encoding="utf-8"
            )

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

        "original_code":
            original_code,

        "iteration":
            state["iteration"] + 1
    }
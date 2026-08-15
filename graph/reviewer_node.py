from graph.state import ProjectState

from agents.reviewer import (
    reviewer_agent
)


def reviewer_node(
    state: ProjectState
) -> ProjectState:

    review = reviewer_agent(
        state["project_path"],
        state["repair_plan"]
    )

    return {
        **state,

        "review_result":
            review
    }

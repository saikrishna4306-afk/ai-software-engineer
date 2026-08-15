from graph.state import ProjectState


def review_router(
    state: ProjectState
) -> str:

    review = (
        state["review_result"]
        .strip()
        .upper()
    )

    # Only the actual decision at the beginning
    # counts as approval.

    if review.startswith(
        "APPROVED"
    ):

        return "approved"

    if state["iteration"] >= 3:

        return "max_iterations"

    return "retry"
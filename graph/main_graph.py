from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.state import ProjectState

from graph.architect_node import (
    architect_node
)

from graph.coder_node import (
    coder_node
)

from graph.tester_node import (
    tester_node
)

from graph.reviewer_node import (
    reviewer_node
)

from graph.router import (
    review_router
)


graph = StateGraph(
    ProjectState
)


graph.add_node(
    "architect",
    architect_node
)

graph.add_node(
    "coder",
    coder_node
)

graph.add_node(
    "tester",
    tester_node
)

graph.add_node(
    "reviewer",
    reviewer_node
)


graph.add_edge(
    START,
    "architect"
)

graph.add_edge(
    "architect",
    "coder"
)

graph.add_edge(
    "coder",
    "tester"
)

graph.add_edge(
    "tester",
    "reviewer"
)


graph.add_conditional_edges(
    "reviewer",
    review_router,
    {
        "approved": END,
        "retry": "coder",
        "max_iterations": END
    }
)


app = graph.compile()
from graph.main_graph import app
from graph.state import ProjectState


initial_state: ProjectState = {
    "project_path": "sample_projects/buggy_calculator",
    "files": [],
    "repair_plan": "",
    "corrected_files": [],
    "test_output": "",
    "test_errors": "",
    "tests_passed": False,
    "review_result": "",
    "iteration": 0
}


result = app.invoke(initial_state)


print("\n======= FINAL RESULT =======")

print(
    "Tests Passed:",
    result["tests_passed"]
)

print(
    "Iteration:",
    result["iteration"]
)

print(
    "Corrected Files:",
    result["corrected_files"]
)

print("\n======= REVIEW =======")

print(
    result["review_result"]
)
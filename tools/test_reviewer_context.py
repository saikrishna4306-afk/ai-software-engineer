from reviewer_tools import build_review_context


project_path = "sample_projects/buggy_calculator"


repair_plan = """
### Bug 1

File name: calculator.py

Function: add

The add function should correctly add two numbers.

### Bug 2

File name: calculator.py

Function: multiply

The multiply function should correctly multiply two numbers.
"""


print("========== REVIEWER CONTEXT TEST ==========")


context = build_review_context(
    project_path,
    repair_plan
)


print("\n========== REPAIR PLAN ==========")

print(
    context["repair_plan"]
)


print("\n========== TEST STATUS ==========")

print(
    "Tests passed:",
    context["tests_passed"]
)

print(
    "Return code:",
    context["return_code"]
)


print("\n========== PYTEST OUTPUT ==========")

print(
    context["pytest_output"]
)


print("\n========== PYTEST ERRORS ==========")

print(
    context["pytest_errors"]
)


print("\n========== PROJECT SOURCE ==========")

print(
    context["project_context"]
)
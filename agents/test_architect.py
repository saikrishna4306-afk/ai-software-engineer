from agents.architect import architect_agent
from tools.tester_tools import run_tests


project_path = "sample_projects/buggy_calculator"


# Run the project's tests first
test_result = run_tests(project_path)


print("========== ARCHITECT TEST ==========")

print("\n========== TEST STATUS ==========")
print("Tests passed:", test_result["passed"])
print("Return code:", test_result["return_code"])

print("\n========== PYTEST OUTPUT ==========")
print(test_result["stdout"])

print("\n========== PYTEST ERRORS ==========")
print(test_result["stderr"])


# Send actual test results to the Architect
plan = architect_agent(
    project_path,
    test_result["stdout"],
    test_result["stderr"]
)


print("\n========== ARCHITECT PLAN ==========")
print(plan)
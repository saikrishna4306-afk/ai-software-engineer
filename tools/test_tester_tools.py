from tester_tools import run_tests


project_path = "sample_projects/buggy_calculator"

print("TEST PROJECT PATH:")
print(project_path)


result = run_tests(project_path)


print("---test results---")
print("passed:", result["passed"])
print("return code:", result["return_code"])


print("-----pytest output-----")
print(result["stdout"])


print("-----pytest errors-----")
print(result["stderr"])
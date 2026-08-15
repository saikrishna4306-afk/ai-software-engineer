from file_tools import read_file, write_file


project_path = "sample_projects/buggy_calculator"

file_name = "calculator.py"


print("========== BEFORE ==========")

original_code = read_file(
    project_path,
    file_name
)

print(original_code)


corrected_code = """def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b
"""


print("\n========== WRITING ==========")

write_file(
    project_path,
    file_name,
    corrected_code
)


print("File written successfully.")


print("\n========== AFTER ==========")

updated_code = read_file(
    project_path,
    file_name
)

print(updated_code)
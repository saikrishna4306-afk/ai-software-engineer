from code_tools import extract_file_names
from file_tools import read_file


project_path = "sample_projects/buggy_calculator"

repair_plan = """
### Bug 1

1. **File name:** `calculator.py`
2. **Function:** `add`
3. **What is wrong:** Addition is implemented incorrectly.

### Bug 2

1. **File name:** `calculator.py`
2. **Function:** `multiply`
3. **What is wrong:** Multiplication is implemented incorrectly.
"""


print("========== CODER GENERIC TEST ==========")


# Step 1: Extract files from repair plan

files = extract_file_names(repair_plan)

print("\nFiles identified by Coder:")

for file in files:
    print(file)


# Step 2: Read each affected file

print("\n========== CURRENT CODE ==========")

for file in files:

    print(f"\n----- {file} -----")

    current_code = read_file(
        project_path,
        file
    )

    print(current_code)
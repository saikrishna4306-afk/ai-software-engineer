from code_tools import extract_file_names


repair_plan = """
### Bug 1

1. **File name:** `calculator.py`
2. **Function:** `add`
3. **What is wrong:** Wrong operator.

### Bug 2

1. **File name:** `services/user_service.py`
2. **Function:** `create_user`
3. **What is wrong:** Incorrect validation.

### Bug 3

1. **File name:** `tests/test_auth.py`
2. **Function:** `test_login`
3. **What is wrong:** Missing assertion.
"""


files = extract_file_names(repair_plan)


print("===== FILES FOUND =====")

for file in files:
    print(file)
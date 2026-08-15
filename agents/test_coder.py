from agents.coder import coder_agent

project_path="sample_projects/buggy_calculator"

repair_plan="""
              # Repair Plan

### Bug 1

File: calculator.py

Function: add

Problem:
The function uses subtraction instead of addition.

Fix:
Change a - b to a + b.

### Bug 2

File: calculator.py

Function: multiply

Problem:
The function uses addition instead of multiplication.

Fix:
Change a + b to a * b.
  """
corrected_code=coder_agent(
    project_path,
    repair_plan
)
print("======corrected code======")
print(corrected_code)
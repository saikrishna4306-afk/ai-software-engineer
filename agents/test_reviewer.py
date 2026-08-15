from agents.reviewer import reviewer_agent
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
test_output="""
                3 passed
                """
review=reviewer_agent(
    project_path,
    repair_plan,
    test_output
)
print("----review result====")
print(review)
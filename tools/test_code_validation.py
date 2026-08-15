from code_tools import validate_python_code


valid_code = """
def add(a, b):
    return a + b


def multiply(a, b):
    return a * b
"""


invalid_code = """
def add(a, b)
    return a + b
"""


print("========== VALID CODE TEST ==========")

try:

    validate_python_code(valid_code)

    print("Valid Python: PASS")

except ValueError as error:

    print("Valid Python: FAIL")
    print(error)


print("\n========== INVALID CODE TEST ==========")

try:

    validate_python_code(invalid_code)

    print("Invalid Python: FAIL")

except ValueError as error:

    print("Invalid Python correctly rejected: PASS")
    print(error)
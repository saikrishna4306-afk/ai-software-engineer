import ast
import re


def extract_file_names(
    repair_plan: str
) -> list[str]:

    if not repair_plan:
        return []

    if (
        "NO REPAIR REQUIRED"
        in repair_plan.upper()
    ):
        return []

    patterns = [

        # **File name:** `calculator.py`
        r"\*\*File name:\*\*\s*`([^`]+\.py)`",

        # **File:** `calculator.py`
        r"\*\*File:\*\*\s*`([^`]+\.py)`",

        # File name: `calculator.py`
        r"File name:\s*`([^`]+\.py)`",

        # File: `calculator.py`
        r"File:\s*`([^`]+\.py)`",

        # File: calculator.py
        r"File:\s*([A-Za-z0-9_.\-/\\]+\.py)",

        # File name: calculator.py
        r"File name:\s*([A-Za-z0-9_.\-/\\]+\.py)",
    ]

    files = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            repair_plan,
            flags=re.IGNORECASE
        )

        for file in matches:

            file = file.strip().strip("`")

            if file not in files:

                files.append(file)

    return files


def validate_python_code(
    code: str
) -> bool:

    if not code or not code.strip():

        raise ValueError(
            "Generated code is empty."
        )

    try:

        ast.parse(code)

    except SyntaxError as error:

        raise ValueError(
            "Generated code contains "
            f"invalid Python syntax: {error}"
        )

    return True
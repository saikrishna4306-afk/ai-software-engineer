from typing import TypedDict


class ProjectState(TypedDict):

    project_path: str

    files: list[str]

    repair_plan: str

    corrected_files: list[str]

    test_output: str

    test_errors: str

    tests_passed: bool

    review_result: str

    iteration: int
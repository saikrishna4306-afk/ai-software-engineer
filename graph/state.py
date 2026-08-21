from typing import TypedDict


class ProjectState(TypedDict):
    project_path: str
    files: list[str]
    repair_plan: str
    original_code: dict[str, str]
    corrected_files: list[str]
    corrected_code: dict[str, str]
    test_output: str
    test_errors: str
    tests_passed: bool
    review_result: str
    iteration: int
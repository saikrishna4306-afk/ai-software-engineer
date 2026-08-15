from pathlib import Path


def get_project_path(project_path: str) -> Path:

    path = Path(project_path).resolve()

    if not path.exists():
        raise FileNotFoundError(
            f"Project not found: {path}"
        )

    if not path.is_dir():
        raise NotADirectoryError(
            f"Project path is not a directory: {path}"
        )

    return path


def list_files(project_path: str) -> list[str]:

    project_path = get_project_path(
        project_path
    )

    ignored_directories = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "myenv",
        "node_modules",
        ".pytest_cache"
    }

    files = []

    for path in project_path.rglob("*"):

        if not path.is_file():
            continue

        if any(
            part in ignored_directories
            for part in path.parts
        ):
            continue

        relative_path = path.relative_to(
            project_path
        )

        files.append(
            str(relative_path)
        )

    return sorted(files)


def read_file(
    project_path: str,
    file_path: str
) -> str:

    project_path = get_project_path(
        project_path
    )

    target = (
        project_path / file_path
    ).resolve()

    try:

        target.relative_to(
            project_path
        )

    except ValueError:

        raise PermissionError(
            "Cannot read a file outside "
            "the project directory."
        )

    if not target.exists():

        raise FileNotFoundError(
            f"File not found: {target}"
        )

    if not target.is_file():

        raise IsADirectoryError(
            f"Not a file: {target}"
        )

    return target.read_text(
        encoding="utf-8"
    )


def write_file(
    project_path: str,
    file_path: str,
    content: str
):

    project_path = get_project_path(
        project_path
    )

    target = (
        project_path / file_path
    ).resolve()

    try:

        target.relative_to(
            project_path
        )

    except ValueError:

        raise PermissionError(
            "Cannot write a file outside "
            "the project directory."
        )

    target.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    target.write_text(
        content,
        encoding="utf-8"
    )

    return (
        f"File written successfully: "
        f"{file_path}"
    )
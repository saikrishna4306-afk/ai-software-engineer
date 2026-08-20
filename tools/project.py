import io
import tempfile
import zipfile
from pathlib import Path


MAX_SIZE_MB = 50


def prepare_project(uploaded_file):
    if not uploaded_file.name.lower().endswith(".zip"):
        raise ValueError("Please upload a .zip Python project.")

    data = uploaded_file.getvalue()

    if len(data) > MAX_SIZE_MB * 1024 * 1024:
        raise ValueError(f"Project exceeds the {MAX_SIZE_MB} MB limit.")

    root = Path(tempfile.mkdtemp(prefix="ai_engineer_"))

    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for member in archive.infolist():
            target = (root / member.filename).resolve()

            if not str(target).startswith(str(root.resolve())):
                raise ValueError("Unsafe ZIP file detected.")

            if not member.is_dir():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(member))

    folders = [p for p in root.iterdir() if p.is_dir()]
    project = folders[0] if len(folders) == 1 else root

    python_files = [
        str(p.relative_to(project))
        for p in project.rglob("*.py")
        if "venv" not in p.parts
        and ".venv" not in p.parts
        and "__pycache__" not in p.parts
    ]

    test_files = [
        file for file in python_files
        if file.startswith("test")
        or "/test" in file
        or file.endswith("_test.py")
    ]

    if not python_files:
        raise ValueError("No Python files were found in the project.")

    if not test_files:
        raise ValueError("No pytest test files were found in the project.")

    return project, python_files, test_files
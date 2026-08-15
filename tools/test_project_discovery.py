from file_tools import list_files, read_file


project_path = "sample_projects/buggy_calculator"


print("========== PROJECT FILES ==========")

files = list_files(project_path)

for file in files:
    print(file)


print("\n========== PYTHON FILES ==========")

python_files = [
    file
    for file in files
    if file.endswith(".py")
]

for file in python_files:
    print(file)


print("\n========== PYTHON SOURCE CODE ==========")

for file in python_files:

    print(f"\n----- {file} -----")

    content = read_file(
        project_path,
        file
    )

    print(content)
from file_tools import list_files, read_file


project_path = "sample_projects/buggy_calculator"


print("===== PROJECT FILES =====")

files = list_files(project_path)

for file in files:
    print(file)


print("\n===== READ CALCULATOR =====")

content = read_file(
    project_path,
    "calculator.py"
)

print(content)
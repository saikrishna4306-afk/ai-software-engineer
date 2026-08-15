from config.llm import get_llm

from langchain_core.prompts import (
    ChatPromptTemplate
)

from tools.file_tools import (
    list_files,
    read_file
)


llm = get_llm()


prompt = ChatPromptTemplate.from_template("""
You are a senior software debugging architect.

Analyze the Python project using:

1. The source code.
2. The existing tests.
3. The actual pytest results.

PROJECT FILES:
{files}

PROJECT SOURCE CODE:
{contents}

PYTEST OUTPUT:
{test_output}

PYTEST ERRORS:
{test_errors}

Your task is to identify ONLY the real bugs causing
the current test failures.

IMPORTANT RULES:

- Pytest failures are the primary evidence.
- Do not invent requirements.
- Do not add features.
- Do not refactor working code.
- Do not add type annotations.
- Do not add unnecessary validation.
- Do not modify tests merely to make them pass.
- Do not change behavior without evidence.
- Prefer changing application/source files.
- Do not propose changes to test files unless the
  tests themselves are clearly incorrect.
- Identify the smallest change required.

VERY IMPORTANT:

Every bug MUST use exactly this format:

File: calculator.py
Function: add
Failing test: test_add
Actual behavior: add(2, 3) returns -1
Expected behavior: add(2, 3) should return 5
Minimal change: Change a - b to a + b

If multiple bugs exist, repeat the same format.

If there are no failing tests or no confirmed bugs,
return exactly:

NO REPAIR REQUIRED

Do not generate code.

Only provide the repair plan.
""")


architect_chain = prompt | llm


def architect_agent(
    project_path: str,
    test_output: str,
    test_errors: str
) -> str:

    files = list_files(
        project_path
    )

    contents = ""

    for file in files:

        if not file.endswith(".py"):
            continue

        content = read_file(
            project_path,
            file
        )

        contents += (
            f"\n\n===== {file} =====\n"
        )

        contents += content

    response = architect_chain.invoke(
        {
            "files": files,
            "contents": contents,
            "test_output": test_output,
            "test_errors": test_errors
        }
    )

    print(
        "\n========== ARCHITECT =========="
    )

    print(
        response.content
    )

    if isinstance(
        response.content,
        list
    ):

        return "\n".join(
            block["text"]
            for block in response.content
            if block.get("type") == "text"
        ).strip()

    return response.content.strip()
from config.llm import get_llm

from langchain_core.prompts import ChatPromptTemplate

from tools.file_tools import (
    read_file,
    write_file
)

from tools.code_tools import (
    extract_file_names,
    validate_python_code
)


llm = get_llm()


prompt = ChatPromptTemplate.from_template("""
You are a senior Python developer.

Fix ONLY the bugs described in the repair plan.

FILE NAME:
{file_name}

CURRENT CODE:
{current_code}

REPAIR PLAN:
{repair_plan}

STRICT RULES:

1. Fix only the specified bug.
2. Make the smallest possible change.
3. Do not modify unrelated code.
4. Do not add new features.
5. Do not refactor working code.
6. Do not add unnecessary validation.
7. Do not modify test files.
8. Do not remove existing functions.
9. Do not rename existing functions.
10. Preserve the existing structure.
11. Return the COMPLETE corrected Python source code.
12. Return ONLY Python source code.
13. Do not use markdown code fences.
14. Do not provide explanations.
15. Do not return the word corrected_code.
""")


coder_chain = prompt | llm


def clean_code_response(content) -> str:

    if isinstance(content, list):
        code = "\n".join(
            block["text"]
            for block in content
            if block.get("type") == "text"
        )
    else:
        code = content

    code = code.strip()

    if code.startswith("```python"):
        code = code[len("```python"):].strip()

    elif code.startswith("```"):
        code = code[len("```"):].strip()

    if code.endswith("```"):
        code = code[:-3].strip()

    if code == "corrected_code":
        raise ValueError(
            "Coder returned 'corrected_code' "
            "instead of Python source code."
        )

    validate_python_code(code)

    return code


def coder_agent(
    project_path: str,
    repair_plan: str
) -> dict:

    print("\n========== CODER ==========")

    print("Repair Plan:")
    print(repair_plan)

    # --------------------------------------------------
    # NO REPAIR
    # --------------------------------------------------

    if "NO REPAIR REQUIRED" in repair_plan.upper():

        print("Coder: No repair required.")

        return {
            "corrected_files": [],
            "corrected_code": {}
        }

    # --------------------------------------------------
    # EXTRACT FILES
    # --------------------------------------------------

    files = extract_file_names(repair_plan)

    print("\nFiles identified by Coder:")
    print(files)

    if not files:

        raise ValueError(
            "No source files were found "
            "in the repair plan.\n\n"
            "Architect repair plan:\n"
            f"{repair_plan}"
        )

    # --------------------------------------------------
    # REMOVE TEST FILES
    # --------------------------------------------------

    source_files = []

    for file in files:

        normalized = file.replace("\\", "/")
        name = normalized.split("/")[-1]

        if name.startswith("test_"):
            print(f"Skipping test file: {file}")
            continue

        if normalized.startswith("tests/"):
            print(f"Skipping test file: {file}")
            continue

        if file not in source_files:
            source_files.append(file)

    if not source_files:

        raise ValueError(
            "The repair plan only references "
            "test files. The Coder will not "
            "modify tests."
        )

    # --------------------------------------------------
    # PROCESS SOURCE FILES
    # --------------------------------------------------

    corrected_files = []
    corrected_sources = {}

    for file_name in source_files:

        print(
            f"\nCODER: Processing {file_name}"
        )

        current_code = read_file(
            project_path,
            file_name
        )

        response = coder_chain.invoke(
            {
                "file_name": file_name,
                "current_code": current_code,
                "repair_plan": repair_plan
            }
        )

        corrected_code = clean_code_response(
            response.content
        )

        # Validate BEFORE writing
        validate_python_code(
            corrected_code
        )

        write_file(
            project_path,
            file_name,
            corrected_code
        )

        corrected_files.append(
            file_name
        )

        # Keep the actual corrected source
        corrected_sources[file_name] = corrected_code

        print(
            f"CODER: Updated {file_name}"
        )

    # --------------------------------------------------
    # RETURN RESULTS
    # --------------------------------------------------

    return {
        "corrected_files": corrected_files,
        "corrected_code": corrected_sources
    }
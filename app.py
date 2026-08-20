import difflib
from pathlib import Path

import streamlit as st

from graph.main_graph import app
from graph.state import ProjectState
from tools.project import prepare_project


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Software Engineer",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI Software Engineer")

st.write(
    "Automatically analyze, repair, test and review a Python project."
)

st.divider()


# ============================================================
# PROJECT SETTINGS
# ============================================================

st.subheader("⚙️ Project Settings")

uploaded_file = st.file_uploader(
    "📦 Upload a Python project as a ZIP file",
    type=["zip"],
    help="Upload a ZIP containing a Python project and Pytest tests."
)

st.caption(
    "Workflow: Architect → Coder → Tester → Reviewer"
)


# ============================================================
# WORKFLOW DISPLAY
# ============================================================

st.divider()

st.subheader("🔄 Agent Workflow")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 🏗️")
    st.write("**Architect**")

with col2:
    st.markdown("### 💻")
    st.write("**Coder**")

with col3:
    st.markdown("### 🧪")
    st.write("**Tester**")

with col4:
    st.markdown("### 🔍")
    st.write("**Reviewer**")


# ============================================================
# PROJECT VALIDATION
# ============================================================

if uploaded_file:

    st.divider()

    st.success(
        f"📁 Uploaded: `{uploaded_file.name}`"
    )

    try:

        project, python_files, test_files = prepare_project(
            uploaded_file
        )

        st.success(
            "✅ Python project validated."
        )

        info1, info2, info3 = st.columns(3)

        with info1:
            st.metric(
                "Python Files",
                len(python_files)
            )

        with info2:
            st.metric(
                "Test Files",
                len(test_files)
            )

        with info3:
            st.metric(
                "Project",
                uploaded_file.name
            )

        with st.expander("📂 View Project Files"):

            for file in python_files:
                st.write(
                    f"📄 `{file}`"
                )

        st.session_state["project"] = project
        st.session_state["python_files"] = python_files
        st.session_state["test_files"] = test_files

    except Exception as e:

        st.error(
            f"❌ Project validation failed:\n\n{e}"
        )

        st.stop()


# ============================================================
# RUN WORKFLOW
# ============================================================

st.divider()

run_workflow = st.button(
    "🚀 Analyze & Fix Project",
    type="primary",
    use_container_width=True,
    disabled=not uploaded_file
)


if run_workflow:

    project = st.session_state.get(
        "project"
    )

    python_files = st.session_state.get(
        "python_files",
        []
    )

    test_files = st.session_state.get(
        "test_files",
        []
    )

    if not project:

        st.error(
            "❌ Please upload a valid Python project first."
        )

        st.stop()


    # ========================================================
    # INITIAL STATE
    # ========================================================

    initial_state: ProjectState = {

        "project_path":
            str(project),

        "files":
            python_files,

        "repair_plan":
            "",

        "original_code":
            {},

        "corrected_files":
            [],

        "corrected_code":
            {},

        "test_output":
            "",

        "test_errors":
            "",

        "tests_passed":
            False,

        "review_result":
            "",

        "iteration":
            0
    }


    # ========================================================
    # SHOW PROJECT
    # ========================================================

    st.info(
        f"📁 Project: `{uploaded_file.name}`"
    )

    st.info(
        f"🐍 Python files: {len(python_files)} | "
        f"🧪 Test files: {len(test_files)}"
    )


    # ========================================================
    # RUN LANGGRAPH WORKFLOW
    # ========================================================

    with st.spinner(
        "🤖 AI Software Engineer is analyzing and repairing the project..."
    ):

        try:

            result = app.invoke(
                initial_state
            )

        except ValueError as e:

            error_message = str(e)

            if (
                "No files were found in the repair plan"
                in error_message
            ):

                st.warning(
                    "⚠️ The Architect could not identify "
                    "a file that needs repair."
                )

                st.info(
                    "The project may already be correct, "
                    "or the repair plan may not contain "
                    "the expected file information."
                )

            else:

                st.error(
                    f"❌ Workflow could not continue:\n\n"
                    f"{error_message}"
                )

            with st.expander(
                "Show technical details"
            ):

                st.exception(e)

            st.stop()


        except FileNotFoundError as e:

            st.error(
                f"❌ File error:\n\n{e}"
            )

            with st.expander(
                "Show technical details"
            ):

                st.exception(e)

            st.stop()


        except NotADirectoryError as e:

            st.error(
                f"❌ Invalid project directory:\n\n{e}"
            )

            with st.expander(
                "Show technical details"
            ):

                st.exception(e)

            st.stop()


        except Exception as e:

            st.error(
                "❌ The AI Engineer workflow failed."
            )

            st.info(
                "Check the technical details below "
                "for the exact error."
            )

            with st.expander(
                "Show technical details"
            ):

                st.exception(e)

            st.stop()


    # ========================================================
    # FINAL RESULT
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Final Result"
    )

    result_col1, result_col2, result_col3 = st.columns(3)


    # --------------------------------------------------------
    # TEST RESULT
    # --------------------------------------------------------

    with result_col1:

        if result.get(
            "tests_passed"
        ):

            st.success(
                "✅ Tests Passed"
            )

        else:

            st.error(
                "❌ Tests Failed"
            )


    # --------------------------------------------------------
    # ITERATIONS
    # --------------------------------------------------------

    with result_col2:

        st.metric(
            "Iterations",
            result.get(
                "iteration",
                0
            )
        )


    # --------------------------------------------------------
    # REVIEW RESULT
    # --------------------------------------------------------

    with result_col3:

        review_result = result.get(
            "review_result",
            ""
        )

        if (
            "APPROVED"
            in review_result.upper()
        ):

            st.success(
                "✅ APPROVED"
            )

        elif (
            "REJECTED"
            in review_result.upper()
        ):

            st.error(
                "❌ REJECTED"
            )

        else:

            st.warning(
                "⚠️ REVIEW INCOMPLETE"
            )


    # ========================================================
    # REPAIR PLAN
    # ========================================================

    st.subheader(
        "🧠 Repair Plan"
    )

    repair_plan = result.get(
        "repair_plan",
        ""
    )

    if repair_plan:

        st.code(
            repair_plan,
            language="text"
        )

    else:

        st.info(
            "No repair plan was generated."
        )


    # ========================================================
    # CORRECTED FILES
    # ========================================================

    st.subheader(
        "📝 Corrected Files"
    )

    corrected_files = result.get(
        "corrected_files",
        []
    )

    if corrected_files:

        for file in corrected_files:

            st.markdown(
                f"📄 `{file}`"
            )

    else:

        st.info(
            "No files were modified."
        )


    # ========================================================
    # CORRECTED CODE
    # ========================================================

    corrected_code = result.get(
        "corrected_code",
        {}
    )

    if corrected_code:

        st.subheader(
            "💻 Corrected Code"
        )

        selected_file = st.selectbox(
            "Select corrected file",
            list(
                corrected_code.keys()
            ),
            key="corrected_file"
        )

        st.code(
            corrected_code[
                selected_file
            ],
            language="python"
        )


    # ========================================================
    # CODE CHANGES
    # ========================================================

    original_code = result.get(
        "original_code",
        {}
    )

    if (
        original_code
        and corrected_code
    ):

        st.subheader(
            "🔄 Code Changes"
        )

        changed_files = [
            file
            for file in corrected_code
            if file in original_code
        ]

        if changed_files:

            selected_diff_file = st.selectbox(
                "Select file to view changes",
                changed_files,
                key="diff_file"
            )

            diff = "".join(
                difflib.unified_diff(
                    original_code[
                        selected_diff_file
                    ].splitlines(True),

                    corrected_code[
                        selected_diff_file
                    ].splitlines(True),

                    fromfile=(
                        f"{selected_diff_file} "
                        "(before)"
                    ),

                    tofile=(
                        f"{selected_diff_file} "
                        "(after)"
                    )
                )
            )

            st.code(
                diff or "No changes detected.",
                language="diff"
            )

        else:

            st.info(
                "No code changes detected."
            )


    # ========================================================
    # PYTEST OUTPUT
    # ========================================================

    test_output = result.get(
        "test_output",
        ""
    )

    test_errors = result.get(
        "test_errors",
        ""
    )


    if test_output:

        st.subheader(
            "🧪 Pytest Output"
        )

        st.code(
            test_output,
            language="text"
        )


    if test_errors:

        st.subheader(
            "⚠️ Pytest Errors"
        )

        st.code(
            test_errors,
            language="text"
        )


    # ========================================================
    # CODE REVIEW
    # ========================================================

    review_result = result.get(
        "review_result",
        ""
    )

    if review_result:

        st.subheader(
            "🔍 Code Review"
        )

        cleaned_review = (
            review_result.strip()
        )

        if cleaned_review.upper().startswith(
            "APPROVED"
        ):

            cleaned_review = cleaned_review[
                len("APPROVED"):
            ].strip()

            st.success(
                "APPROVED"
            )

        elif cleaned_review.upper().startswith(
            "REJECTED"
        ):

            cleaned_review = cleaned_review[
                len("REJECTED"):
            ].strip()

            st.error(
                "REJECTED"
            )

        if cleaned_review:

            st.markdown(
                cleaned_review
            )

    else:

        st.info(
            "No reviewer result was generated."
        )
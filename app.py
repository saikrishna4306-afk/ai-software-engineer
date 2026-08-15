import streamlit as st

from graph.main_graph import app
from graph.state import ProjectState


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

project_path = st.text_input(
    "Project Path",
    value="sample_projects/buggy_calculator"
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
# RUN WORKFLOW
# ============================================================

st.divider()

run_workflow = st.button(
    "🚀 Analyze & Fix Project",
    type="primary",
    use_container_width=True
)


if run_workflow:

    # --------------------------------------------------------
    # INITIAL STATE
    # --------------------------------------------------------

    initial_state: ProjectState = {
        "project_path": project_path,
        "files": [],
        "repair_plan": "",
        "corrected_files": [],
        "test_output": "",
        "test_errors": "",
        "tests_passed": False,
        "review_result": "",
        "iteration": 0
    }

    # --------------------------------------------------------
    # BASIC PROJECT VALIDATION
    # --------------------------------------------------------

    from pathlib import Path

    project = Path(project_path).resolve()

    if not project.exists():

        st.error(
            f"❌ Project directory does not exist:\n\n"
            f"`{project}`"
        )

        st.stop()

    if not project.is_dir():

        st.error(
            f"❌ Project path is not a directory:\n\n"
            f"`{project}`"
        )

        st.stop()

    python_files = list(project.glob("*.py"))

    if not python_files:

        st.warning(
            "⚠️ No Python files were found in the selected project."
        )

        st.stop()

    # --------------------------------------------------------
    # SHOW PROJECT
    # --------------------------------------------------------

    st.info(
        f"📁 Project: `{project}`"
    )

    # --------------------------------------------------------
    # RUN LANGGRAPH WORKFLOW
    # --------------------------------------------------------

    with st.spinner(
        "🤖 AI Software Engineer is analyzing and repairing the project..."
    ):

        try:

            result = app.invoke(initial_state)

        except ValueError as e:

            error_message = str(e)

            if "No files were found in the repair plan" in error_message:

                st.warning(
                    "⚠️ The Architect could not identify a file "
                    "that needs repair."
                )

                st.info(
                    "The project may already be correct, or the "
                    "repair plan may not contain the expected file "
                    "information."
                )

            else:

                st.error(
                    f"❌ Workflow could not continue:\n\n"
                    f"{error_message}"
                )

            with st.expander("Show technical details"):

                st.exception(e)

            st.stop()

        except FileNotFoundError as e:

            st.error(
                f"❌ File error:\n\n{e}"
            )

            with st.expander("Show technical details"):

                st.exception(e)

            st.stop()

        except NotADirectoryError as e:

            st.error(
                f"❌ Invalid project directory:\n\n{e}"
            )

            with st.expander("Show technical details"):

                st.exception(e)

            st.stop()

        except Exception as e:

            st.error(
                "❌ The AI Engineer workflow failed."
            )

            st.info(
                "Check the technical details below for the "
                "exact error."
            )

            with st.expander("Show technical details"):

                st.exception(e)

            st.stop()

    # ========================================================
    # FINAL RESULT
    # ========================================================

    st.divider()

    st.subheader("📊 Final Result")

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:

        if result.get("tests_passed"):

            st.success("✅ Tests Passed")

        else:

            st.error("❌ Tests Failed")

    with result_col2:

        st.metric(
            "Iterations",
            result.get("iteration", 0)
        )

    with result_col3:

        review_result = result.get(
            "review_result",
            ""
        )

        if "APPROVED" in review_result.upper():

            st.success("✅ APPROVED")

        elif "REJECTED" in review_result.upper():

            st.error("❌ REJECTED")

        else:

            st.warning("⚠️ REVIEW INCOMPLETE")

    # ========================================================
    # REPAIR PLAN
    # ========================================================

    repair_plan = result.get(
        "repair_plan",
        ""
    )

    if repair_plan:

        st.subheader("🧠 Repair Plan")

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

    corrected_files = result.get(
        "corrected_files",
        []
    )

    if corrected_files:

        st.subheader("📝 Corrected Files")

        for file in corrected_files:

            st.markdown(
                f"📄 `{file}`"
            )

    else:

        st.info(
            "No files were modified."
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

        st.subheader("🧪 Pytest Output")

        st.code(
            test_output,
            language="text"
        )

    if test_errors:

        st.subheader("⚠️ Pytest Errors")

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

        st.subheader("🔍 Code Review")

        # Prevent duplicate APPROVED heading.
        cleaned_review = review_result.strip()

        if cleaned_review.upper().startswith("APPROVED"):

            cleaned_review = cleaned_review[
                len("APPROVED"):
            ].strip()

            st.success("APPROVED")

        elif cleaned_review.upper().startswith("REJECTED"):

            cleaned_review = cleaned_review[
                len("REJECTED"):
            ].strip()

            st.error("REJECTED")

        st.markdown(
            cleaned_review
        )

    else:

        st.info(
            "No reviewer result was generated."
        )

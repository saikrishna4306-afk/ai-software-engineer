from config.llm import get_llm

from langchain_core.prompts import (
    ChatPromptTemplate
)

from tools.reviewer_tools import (
    build_review_context
)


llm = get_llm()


prompt = ChatPromptTemplate.from_template("""
You are a senior software reviewer.

Review the project after the coder attempted
to repair the bugs.

REPAIR PLAN:
{repair_plan}

PROJECT SOURCE CODE:
{project_context}

TESTS PASSED:
{tests_passed}

PYTEST OUTPUT:
{pytest_output}

PYTEST ERRORS:
{pytest_errors}

APPROVE the repair ONLY when:

1. The bugs from the repair plan are fixed.
2. The Python code is valid.
3. The tests pass.
4. No unnecessary changes were introduced.
5. The implementation follows the repair plan.

If any requirement fails, REJECT the repair.

Your response MUST begin with exactly one of:

APPROVED

or:

REJECTED

Then provide:

### Explanation

Explain the decision.

Do not modify files.
""")


reviewer_chain = prompt | llm


def reviewer_agent(
    project_path: str,
    repair_plan: str
) -> str:

    review_context = (
        build_review_context(
            project_path,
            repair_plan
        )
    )

    response = reviewer_chain.invoke(
        {
            "repair_plan":
                review_context["repair_plan"],

            "project_context":
                review_context[
                    "project_context"
                ],

            "tests_passed":
                review_context[
                    "tests_passed"
                ],

            "pytest_output":
                review_context[
                    "pytest_output"
                ],

            "pytest_errors":
                review_context[
                    "pytest_errors"
                ]
        }
    )

    if isinstance(
        response.content,
        list
    ):

        review = "\n".join(
            block["text"]
            for block in response.content
            if block.get("type") == "text"
        )

    else:

        review = response.content

    return review.strip()
# 🤖 AI Software Engineer

An autonomous multi-agent AI system that analyzes, repairs, tests, and reviews Python projects automatically.

The system uses a structured workflow:

**Architect → Coder → Tester → Reviewer**

It is built using **Python, LangGraph, LangChain, Gemini, Pytest, and Streamlit**.

---

## 🚀 Project Overview

The AI Software Engineer is designed to automate a software debugging and repair workflow.

Instead of simply asking an LLM to fix a bug, the system separates the work into specialized agents.

```text
                 Python Project
                       │
                       ▼
              🏗️ Architect Agent
                       │
                Repair Plan
                       │
                       ▼
                💻 Coder Agent
                       │
                 Code Changes
                       │
                       ▼
                  🧪 Tester
                       │
                 Test Results
                       │
                       ▼
                🔍 Reviewer
                       │
              ┌────────┴────────┐
              │                 │
          APPROVED           REJECTED
              │                 │
              ▼                 ▼
             END              Retry
```

---

# ✨ Features

- 🤖 Multi-agent AI software engineering workflow
- 🏗️ Automated bug analysis and repair planning
- 💻 AI-powered code correction
- 🧪 Automatic Pytest execution
- 🔍 Automated code review
- 🔄 Iterative repair workflow
- 🧠 LangGraph state-based orchestration
- 🌐 Streamlit web interface
- 🔑 Google Gemini API integration
- 🦙 Optional Ollama/local LLM support
- 🐍 Python code validation
- 📊 Test results and repair results displayed in the UI
- 🛡️ Error handling for invalid projects and workflow failures

---

# 🏗️ Agent Workflow

## 1. 🏗️ Architect Agent

The Architect analyzes the Python project and test results.

It determines:

- Which tests are failing
- Which files contain the problem
- Which functions are affected
- What the actual behavior is
- What the expected behavior should be
- What minimal change is required

Example:

```text
File: calculator.py
Function: add
Failing test: test_add

Actual behavior:
add(2, 3) returns -1

Expected behavior:
add(2, 3) should return 5

Minimal change:
Change a - b to a + b
```

---

## 2. 💻 Coder Agent

The Coder receives the repair plan from the Architect.

It:

1. Identifies the affected files
2. Reads the source code
3. Generates the corrected implementation
4. Validates the generated Python code
5. Applies the required changes

The Coder is instructed to follow the repair plan and avoid unnecessary modifications.

---

## 3. 🧪 Tester

The Tester executes the project's test suite using Pytest.

```bash
python -m pytest
```

The Tester captures:

- Test status
- Return code
- Pytest output
- Pytest errors

The results are stored in the LangGraph state and passed to the Reviewer.

---

## 4. 🔍 Reviewer Agent

The Reviewer verifies whether the repair was successful.

A repair is approved only when:

1. The reported bugs are fixed.
2. The Python code is valid.
3. The tests pass.
4. No unnecessary changes were introduced.
5. The implementation follows the repair plan.

The Reviewer returns:

```text
APPROVED
```

or:

```text
REJECTED
```

---

# 🔄 Iterative Repair

If the Reviewer rejects the repair, the workflow can return to the Coder.

```text
Architect
    ↓
Coder
    ↓
Tester
    ↓
Reviewer
    │
    ├── APPROVED → END
    │
    └── REJECTED → Coder
```

The workflow uses an iteration limit to prevent an infinite repair loop.

---

# 🧠 LangGraph State

The workflow maintains project information through a shared state.

The state contains information such as:

```text
project_path
files
repair_plan
corrected_files
test_output
test_errors
tests_passed
review_result
iteration
```

This allows information produced by one agent to be passed to the next agent.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| LangChain | LLM application framework |
| LangGraph | Agent workflow orchestration |
| Gemini | AI reasoning and code generation |
| Ollama | Optional local LLM support |
| Pytest | Automated testing |
| Streamlit | Web interface |
| python-dotenv | Environment configuration |

---

# 📁 Project Structure

```text
ai-software-engineer/
│
├── agents/
│   ├── architect.py
│   ├── coder.py
│   └── reviewer.py
│
├── config/
│   └── llm.py
│
├── graph/
│   ├── state.py
│   ├── architect_node.py
│   ├── coder_node.py
│   ├── tester_node.py
│   ├── reviewer_node.py
│   ├── router.py
│   ├── main_graph.py
│   └── run_graph.py
│
├── tools/
│   ├── code_tools.py
│   ├── file_tools.py
│   ├── reviewer_tools.py
│   └── tester_tools.py
│
├── sample_projects/
│   └── buggy_calculator/
│       ├── calculator.py
│       └── test_calculator.py
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-software-engineer
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the URL of this repository.

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv myenv
myenv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv myenv
source myenv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Gemini API Configuration

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=your_gemini_api_key
```

The repository contains `.env.example` as a template.

**Never commit your real Gemini API key to GitHub.**

The `.env` file is excluded through `.gitignore`.

---

# 🖥️ Run the Streamlit Application

Start the application:

```bash
streamlit run app.py
```

The Streamlit interface allows you to specify the Python project that should be analyzed.

Example:

```text
sample_projects/buggy_calculator
```

Then click:

```text
🚀 Analyze & Fix Project
```

---

# 🧪 Sample Project

The repository includes an intentionally buggy calculator project.

Initial implementation:

```python
def add(a, b):
    return a - b


def multiply(a, b):
    return a + b


def divide(a, b):
    return a / b
```

The tests expect:

```python
add(2, 3) == 5
multiply(2, 3) == 6
divide(6, 2) == 3
```

---

# 📊 Example Execution

## Initial Test Result

The intentionally broken project produces:

```text
2 failed, 1 passed
```

The failures are:

```text
test_add       FAILED
test_multiply  FAILED
test_divide    PASSED
```

---

## 🏗️ Architect

The Architect identifies the two problems:

```text
add:
a - b → a + b

multiply:
a + b → a * b
```

---

## 💻 Coder

The Coder applies the required changes to:

```text
calculator.py
```

---

## 🧪 Tester

The repaired project is tested again.

Result:

```text
3 passed
```

---

## 🔍 Reviewer

The Reviewer verifies the repair:

```text
APPROVED
```

---

# 📈 Evaluation Result

| Metric | Result |
|---|---:|
| Initial tests | 1 passed / 2 failed |
| Bugs identified | 2 |
| Corrected files | 1 |
| Final tests | 3 passed / 0 failed |
| Repair iterations | 1 |
| Reviewer result | APPROVED |

### Complete workflow

```text
❌ 2 failed, 1 passed
          ↓
🏗️ Architect
          ↓
💻 Coder
          ↓
🧪 Tester
          ↓
✅ 3 passed
          ↓
🔍 Reviewer
          ↓
✅ APPROVED
```

---

# 🛡️ Error Handling

The Streamlit application handles common workflow errors, including:

- Project directory does not exist
- Project path is not a directory
- No Python files found
- Invalid repair plan
- File errors
- Unexpected workflow errors

Technical details can be displayed through the Streamlit interface when required.

---

# 🔐 Security

The project follows basic security practices:

- API keys are stored in environment variables.
- `.env` is excluded from Git.
- Virtual environments are excluded from Git.
- API keys are not stored in source code.
- The application operates on the selected project directory.

---

# 🚧 Future Improvements

Planned improvements include:

- 👤 Human approval before applying generated changes
- 🔍 Git diff visualization
- ↩️ Automatic rollback
- 🐳 Docker sandbox execution
- 🔗 GitHub repository integration
- 📚 Codebase RAG
- 🌐 Support for additional programming languages
- ☁️ Cloud deployment
- 📊 Advanced evaluation metrics
- 🧠 Structured outputs from agents
- 🔐 Improved sandboxing and execution isolation

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Multi-agent AI systems
- LangGraph
- LangChain
- Generative AI
- LLM-based code generation
- Agent orchestration
- Automated software testing
- AI-assisted debugging
- Self-healing software workflows
- Python code validation
- Streamlit application development

---

# 👨‍💻 Author

**Sai Krishna**

AI / Generative AI Engineer

---

# ⭐ Project Summary

The AI Software Engineer demonstrates how multiple specialized AI agents can collaborate to perform an autonomous software engineering workflow.

Instead of relying on a single LLM response, the system uses separate responsibilities:

```text
🏗️ Architect
      ↓
💻 Coder
      ↓
🧪 Tester
      ↓
🔍 Reviewer
```

This creates a structured, test-driven, and review-based approach to autonomous Python software repair.

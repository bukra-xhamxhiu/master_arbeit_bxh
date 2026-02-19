
---

# Kanban Application UI Test Agent (`kanban_ai`)

This folder contains a Python + Playwright agent for automated UI test generation on the Kanban Task Management web application.

The Kanban environment  lives in a dedicated folder named `kanban_ai/` at the root of the Kanban repository.

## How it works: 
**Two-step process:**

      Step 1: Exploration   
        kanban_ai_agent.py 
        Launches browser
        Finds interactive elements (buttons, links, checkboxes, textboxes, etc )
        Clicks with priority: add, create, edit, delete actions first 
        Writes to logs/kanban_explore.jsonl

      Step 2: Test Generation   
        generate_tests_from_log.py 
        -  Reads successful actions from log
        -  Converts to Playwright test code 
        -  Outputs tests_generated/test_*.py 

---

## 1. Folder structure

Inside `kanban_ai/` you will find:

- `env/`
  - `kanban_env.py` – Playwright environment (`KanbanPlaywrightEnv`) wrapping the Kanban app.
  - `kanban_actions.py` – Helper actions for:
    - Creating, updating, moving, and deleting tasks.
    - Interacting with boards and columns.
- `agents/`
  - `structured_kanban_agent.py` – Structured scenario agent (board creation, tasks, column transitions).
  - (optional) `random_kanban_agent.py` – Random exploration baseline.
- `logs/`
  - `agent_runs/` – Text logs for each run.
  - `test_runs/` – JSON test summaries.
- `requirements.txt` – Dependencies for the Kanban environment.
- `.env` – Target URL and optional extra configuration.

---

## 2. Prerequisites

- Python 3.10+
- Git (if Windows)
- Playwright for Python
- Node.js (to run the Kanban app’s dev server, if needed)

Ensure the Kanban application itself is installed and runnable according to its own README.

---

## 3. Installation

From the root of the Kanban application repository:

```bash
cd kanban_ai
``` 

## Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate
 

## Install dependencies:
pip install -r requirements.txt


## Run the Kanban application outside /kanban_ai path
npm install
npm run dev

Configure base url: APP_BASE_URL=http://localhost:3001
 
## Run AI agent:
 cd kanban_ai
  python kanban_ai_agent.py  

## Generate Tests from Logs
  python generate_tests_from_log.py 

## Run Generated Tests   
python tests_generated/test_kanban_generated.py


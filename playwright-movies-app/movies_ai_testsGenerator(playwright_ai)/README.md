
---

```markdown
# Movies Application UI Test Agent (`playwright_ai`)

This folder contains a Python + Playwright agent that automatically explores the Movies web application and generates UI test traces, logs, and metrics.

---

## 1. Folder structure

Inside `playwright_ai/` of the Movies app you will find:

- `env/`
  - `movies_env.py` – Playwright environment (`MoviesPlaywrightEnv`) wrapping the Movies application.
  - `movies_actions.py` – Helper functions for interacting with menus, movie cards, theme toggle, etc.
- `agents/`
  - `structured_movies_agent.py` – Main structured exploration agent.
- `logs/`
  - `agent_runs/` – Text logs per run.
  - `test_runs/` – JSON summary per run.
- `requirements.txt` – Dependencies specific to the Movies test environment.
- `.env` –  environment variables, including the base URL.

---

## 2. Prerequisites

- Python 3.10+  
- Git  
- Playwright for Python  
- Node.js (for running the Movies app locally, if required by the app)  

If the Movies app uses `npm`/`yarn` to run a dev server, ensure that environment is set up according to the app’s own README.

---

## 3. Installation

From the root of the Movies app repository:

```bash
cd playwright_ai

### 3.1 Create and activate virtual environment

From the root of the `web_complexity` repository:

```bash
python -m venv .venv

Activate it:
source .venv/bin/activate

Install requirements : pip install -r requirements.txt


Install Playwright Browsers : playwright install
 
 Run the ai agent: python agents/heuristic_movies_agent.py




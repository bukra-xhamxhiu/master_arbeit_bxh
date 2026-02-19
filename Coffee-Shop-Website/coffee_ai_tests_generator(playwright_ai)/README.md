# Coffee-Shop UI Test Agent (`playwright_ai`)

This folder contains a Python and  Playwright based agent that automatically explores the Coffee-Shop website and generates UI test cases, logs, and basic UI metrics. It can be successfully executed only when the Coffee Shop Website is active and running in local host. 

The folder must to be placed inside the root of the Coffee-Shop repository (for example a fork of `Coffee-Shop-Website` that contains a `playwright_ai/` subfolder).

---

## 1. Folder structure

Inside `playwright_ai/` there is this  repo:

- `env/`
  - `coffee_env.py` – Playwright environment wrapper for the Coffee website.
  - `coffee_actions.py` – Helper functions to identify, find and click UI elements (buttons, links, forms).
- `agents/`
  - `random_agent.py` – Main agent that randomly explores the website.
  - `dqn_agent.py` – Deep Q-Network agent (placeholder).
  - `marl_coordinator.py` – Multi-agent RL coordinator (placeholder).
- `logs/`
  - `agent_runs/` – Human readable logs (one file per run).
  - `test_runs/` – JSON summary of every test run, that will be needed for the complexity management later.
- `requirements.txt` – Python dependencies for this environment (if present).
- `.env` –  environment variables .

---

## 2. Prerequisites

- Python 3.10+  
- Git  
- Playwright for Python  
- A modern browser (Playwright will install its own binaries)  

If you want to run the Coffee website locally instead of using the public demo URL, you also need:

- Node.js (v16+ or v18+) to serve the Coffee website. You can also open the index.html file directly in your browser. 

---

## 3. Installation

From the root of the Coffee repository (where `playwright_ai/` lives):

```bash
cd playwright_ai
```
---

## Create and activate python environment (macOS)
python -m venv .venv
.\.venv\Scripts\activate

## Install Python dependencies 
pip install -r requirements.txt
pip install  playwright 

## Install Playwright Browsers 
playwright  install
 
Configure target main url: 
https://lchua2314.github.io/Coffee-Shop-Website/dist/index.html

## Run UI test agent (please note that python virtual environment must be active)
python run_env_text.py #(test basic click and scroll)
python agents/random_agent.py #(run explaration only)

 python run_generation_pipeline.py #(run full pipeline, generate test files )

## After a successful run, you will be able to see: 
- logs/agent_runs/agent_run_YYYYMMDD_HHMMSS.log
- tests/generated/test_generated_ui.py #(executable playwright tests)
- logs/ - JSON logs with step details #(needed for complexity evaluator later)

## Run generated tests: 
python tests/generated/test_generated_ui.py 

---

## In the case of troubleshooting : 
  ┌──────────────────────────────┬──────────────────────────────────────────────┐
  │            Error             │                   Solution                   │
  ├──────────────────────────────┼──────────────────────────────────────────────┤
  │ No module named 'env'        │ Run from parent folder, not inside agents/   │
  ├──────────────────────────────┼──────────────────────────────────────────────┤
  │ No module named 'playwright' │ pip install playwright && playwright install │
  ├──────────────────────────────┼──────────────────────────────────────────────┤
  │ net::ERR_CONNECTION_REFUSED  │ Start local server or use live URL           │
  └──────────────────────────────┴──────────────────────────────────────────────┘     
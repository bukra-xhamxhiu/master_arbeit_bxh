
---
# Movies Application UI Test Agent (`playwright_ai`)

This folder contains a Python + Playwright agent that automatically explores the Movies web application and generates UI test traces, logs, and metrics.

# How it works 

  1.STRUCTURED EXPLORATION (StructuredMoviesAgent) 
- Phase 1: Explore menus (header/nav links) 
- Phase 2: Explore movie cards (click → detail page)
- Phase 3: Actions on pages (scroll, theme toggle)

  2.GROUPED TEST PLAN (StructuredTestPlanBuilder)  
- Groups actions by: menus, navigation, actions   
- Filters successful steps only

  3.MULTI-FILE CODE GENERATION (MultiFileCodeGenerator) 
- tests/generated/test_movies_menus.py
- tests/generated/test_movies_navigation.py 
- tests/generated/test_movies_actions.py


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
- Git  (if Windows).
- Playwright for Python
- Node.js (for running Movies app locally)

If the Movies app uses `npm`/`yarn` to run a dev server, ensure that environment is set up according to the app’s own README. 
cd ../movies-app 
npm install
npm run dev
 App runs at http://localhost:3000  

---

## 3. Installation

From the root of the Movies app repository:

```bash
cd movies_ai_TestGenerator_improved 
```
Activate python environment :
``` source .venv/bin/activate
```
Install requirements : pip install -r requirements.txt

Install Playwright Browsers : playwright install

Run the ai agent: python run_generation_pipeline_movies_structured.py 

## Expected Output: 

===MENU EXPLORATION ===
[1] menu item found

=== NAVIGATION & ACTIONS EXPLORATION===
[Card] Click card 0 (card_0) with selector a[href='...']
[Actions] Scroll and attempt theme toggle
[Actions] Toggle theme via button:has-text("☀")
[Card] Click card 1 (Page 2) with selector a[href='...']

===GROUPED TEST PLANS===
actions: 4 steps 
navigation: 1 step

## Generated Tests: 
tests/generated/test_movies_actions.py
tests/generated/test_movies_navigation.py

## Run Tests: 
  #Run individual test files
python tests/generated/test_movies_actions.py
python tests/generated/test_movies_navigation.py

  #or with pytest        
pytest tests/generated/ -v --headed 



# Exploration Strategy 
The structured agent explores in these phases: 

Phase 1: Menus 
- Finds header/nav links 
- Clicks each, returns to base URL

 Phase 2: Movie Cards                    
  - Gets visible movie cards (up to 3) 
  - Clicks each to visit detail page 
  - Returns to base URL after each    

  Phase 3: Actions (on each page)                     
  - Scrolls down (1000px)  
  - Toggles theme if toggle button exists


 Comparison: Original vs Improved 
 
 Original (movies_ai_testsGenerator(playwright_ai))
 - Random exploration
 - Single test file output
 - Multiple run scripts 
 
 Improved (movies_ai_TestGenerator_improved)
  - Structured exploration (menus, then cards, then actions)
  - Multiple grouped test files 
  - Single entry point  
  - Cleaner separation of concerns   

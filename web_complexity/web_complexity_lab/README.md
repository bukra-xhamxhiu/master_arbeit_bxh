
# This Application analysis and estimates the compexity of a given web application. 
This application is a python based tool that analyzes and estimates the UI complexity of web applications by combining metrics from: 
- UI structure (pages, elements, interactables) 
- Test coverage (test files, assertions) 
- Test execution logs (JUnit results)
- AI agent exploration logs   

This work is part of a Master Thesis condicted in the Techincal University of Chemnitz,completed on December 2025. 


# Web Complexity Lab     

## How does it work: 

 1.Collectors
 - UIStructureCollector :crawls pages, counts elements 
 - TestParser : parses Playwright test files 
 - LogParser : reads JUnit XML results
 - AgentLogParser:  reads AI agent JSONL logs

 2.Features 
- ui_metrics: page count, DOM size, interactable elements
- test_metrics: test count, assertions, test coverage
- log_metrics: pass/fail rates, error rates, durations (time)
- agent_metrics: steps, rewards, exploration coverage  


 3.Aggregation and Compexity Index - AGGREGATION & COMPLEXITY INDEX 
 - Combines all metrics per application
 - Computes weighted complexity score  

 4.Export
 complexity_results/results.csv
 complexity_results/results.json  

## Files 
config.yaml  # Application Configurations 
cli.py  #Command Line Inteface (CLI)
config.py #Configuration loader 
pipeline.py #Is the main pipeline 

## Must Haves: 
python 3.10+ 

## Installation 
```bash 
cd web_complexity 
#Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  
.venv\Scripts\activate   
Install packagepip install -e .
```
## Usage: 
 #. Run Evaluation: wcx evaluate --config config.yaml  
 #. Run directly: python -m web_complexity_lab.cli evaluate --config config.yaml 

## Make sure to insert the right paths in Configuration file (config.yaml) 

Supported Applications are Movies App, kanban board and Coffee Shop. 
If you want to add a new application: 
                  
  1. Add entry to config.yaml
  :applications: 
  - id:"my_new_app"
    root_path: "/full/path/to/app"
    base_url: "http://localhost:PORT"# ... 
    #...rest of config
    
2. Ensure the app has:
- Test files in specified test_paths
- JUnit logs in junit_paths (that is optional)
- Agent logs in agent_log_paths (also optional)

3. Run evaluation:
wcx evaluate --config config.yaml                                                                                              
                                        
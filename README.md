
# Project Description

This repository contains multiple sub folders and overall servce to automatically generate UI tests for these we applications: 
Coffee Shop Web Application - https://github.com/lchua2314/Coffee-Shop-Website
Movies Land Web Application - https://github.com/debs-obrien/playwright-movies-app
Kanban Board web application - https://github.com/dodoburner/kanban-task-management-web-app


## Usage
This project can be used in sections which run in parallel. 
For each web application, the original repository linked above must be running locally, in oder that agents can perform tasks on websites and generate UI tests.

## Repository structure

For the following folders, it is important that you clone the web applications from above and then proceed with ai_test cases. 

- `coffee_ai_tests_generator(playwright_ai)/` – is the folder which stores all the logic about agents, environment and tests generated for Coffee Shop App. 
- `kanban_ai/` –  is thefolder which stores all the logic about agents, environment and tests generated for Kanban App. 
- `movies_ai_testsGerator(playwright_ai)/` -  is thefolder which stores all the logic about agents, environment and tests generated for  Movies Land App. 
- `web_complexity`is a command line interface. 

For each of these folders, there is a READ.me file created. 
It is important to follow the steps written there, to sucessfully execute the tools. 

To properly configure these subfolders with the respective web application please follow this logic. 

For example: movies app 
1 - clone the movies app from Github - Git Clone https://github.com/debs-obrien/playwright-movies-app.git  
2- in the main directory, paste `movies_ai_testsGerator(playwright_ai)/` folder. 
3 - run the main movies project locally, then follow the READ.me file under  `movies_ai_testsGerator(playwright_ai)/` to run the scripts in the right order. 

The same steps can be used to reproduce this logic in Coffee Shop and Kanban App. 


## Authorship
This application is part of a Master Thesis Research, conducted in Technische Universität Chemnitz. 
It is part of the Department of Computer Science, Disctibuted and Sels-organising Systems Faculty. 

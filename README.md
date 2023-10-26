# Web Application Process Planning Language (WAPPL) [working title]
Disclaimer: This is only a prototype implementation and far from production ready. Due to the nature of prototyping, the code needs refactoring.
This repository holds the prototype implementation of my Masterthesis to showcase the capabilities of the designed domain-specific languages for modeling (Business) Process Management Systems.

## Installation
- Python 3.8.10 (instructions: https://www.python.org/downloads/)
- pip
- install requirements: `pip -r requirements.txt`

## Execution of examples
- `wappl` directory holds executable examples of the simulated interaction layer
- the relevant files are `fixed_price_request_execution.txt`, `perioperative_care_execution.txt`, `order_management_execution.txt` and `course_management_execution.txt` (not executable, see thesis document for explaination)
- execute one of the files (we suggest `order_management_execution.txt` because it showcases most capabilities of the DSL) using python: `python <file-name>`

## Execution of tests
- in root directory: `make` (requires make to be installed)

## Execution of planning experiments
- `planning_experiments` contains the files for the automated planning capability evaluation
- use VSCode and PDDL VSCode Extension: https://marketplace.visualstudio.com/items?itemName=jan-dolejsi.pddl
- start a docker container that runs planutils using `cd planning_experiments && ./run.sh` (might require sudo, depending on your installation of docker)
- install TFD planner according to planutils documentation (https://github.com/AI-Planning/planutils)
- open `*_problem.pddl` file of you choice, press ALT+P and run execution against locally running planutils server
- PDDL extension of VSCode automatically visualizes the plan the planner came up with

## Metrics
- the `metrics` directory holds the script used to calculate the token count for the GPL and DSL implementations as mentioned in the thesis' section 7.2
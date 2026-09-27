# mini-orchestrator
A combination of my multiple articles about Apache Airflow and Google Cloud Platform

# Concept

```mermaid
flowchart TD
    A1[Configuration] --> B[[DAG Factory]]
    A2[Python Notebook] --> B
    B --> C[DAG]
    C -- Upload DAG --> D[[Cloud Composer]]
    C -- Upload Notebook --> E[(Cloud Storage)]
    D -- Trigger --> F[[Cloud Run]]
    E -- Pulled Papermill --> F
    F --> G[(Result Table)]
```

# To Run
## Notebook dry run
1. Rename or copy `env_template` into `.env`
    - [P1](pipelines/pipeline1/env_template)
    - [P2](pipelines/pipeline2/env_template)
2. Config environment parameters
3. Run the notebook from top cell
    - [P1](pipelines/pipeline1/p1.ipynb)
    - [P2](pipelines/pipeline2/p2.ipynb)
    
*Requirements and documentation were already provided in the notebook

## With Apache Airflow and Cloud Run
### Deploy Cloud Run with Papermill
1. Open Cloud Run notebook [HERE](cloud_run/create_cloud_run.ipynb)
2. Set up parameters
3. Run cell by cell

### Run Mini Dag Factory
1. Config parameters in config files
    - [P1](pipelines/pipeline1/config.yaml)
    - [P2](pipelines/pipeline2/config.yaml)
2. Run this command to trigger mini dag factory : `python mini_factory_run.py`

### Apache Airflow
1. Run this command to change to Airflow's directory : `cd airflow`
2. Run this command to start Airflow's containers `docker compose up -d`
3. Open `http:localhost:8080`, log in with `airflow` and `airflow`

*Or just use existing GCC
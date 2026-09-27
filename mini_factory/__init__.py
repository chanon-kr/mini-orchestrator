# Import Jinja
from jinja2 import Environment, FileSystemLoader
# Import Utilities
from glob import glob
from yaml import safe_load
import os
from pathlib import Path

PIPELINE_DIR= os.path.join('pipelines', '*' , 'config.yaml')
DAG_DIR= os.path.join('airflow','dags')

def _create_dag_path(text) :
    path = Path(text).parts
    # Ensure Dir
    dag_dir= os.path.join(DAG_DIR, path[-2])
    folder_path= Path(dag_dir)
    folder_path.mkdir(parents=True, exist_ok=True)
    # Return
    return os.path.join(dag_dir, 'dag.py')

def mini_factory() :
    # Load Template
    environment = Environment(loader=FileSystemLoader('mini_factory'))
    based_string = environment.get_template("template.py.jinja")

    # Get Config
    all_config= glob(PIPELINE_DIR)
    for config_dir in all_config :
        # Prep Path
        dag_path= _create_dag_path(config_dir)
        # Render from Config
        with open(config_dir) as f : config= safe_load(f)
        dag_string= based_string.render(config)
        # Render Result or Save into DAG files
        with open(dag_path, 'w') as f : f.write(dag_string)

#!/bin/bash

python3 update_import.py
#python3 update_import2.py
export FLASK_APP=project
flask run --host 0.0.0.0

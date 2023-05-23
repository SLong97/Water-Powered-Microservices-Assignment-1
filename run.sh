#!/bin/sh

./wait-for-it.sh -t 0 rabbitmq:5672
python3 update_import.py
export FLASK_APP=project
flask run --host 0.0.0.0

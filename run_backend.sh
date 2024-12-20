#!/bin/bash

python -m venv aurora_server_environ
source aurora_server_environ/bin/activate 

or
 
source /Users/osnatshabtay/Desktop/aurora_server/aurora_server_environ/bin/activate

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

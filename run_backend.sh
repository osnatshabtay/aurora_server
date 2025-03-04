#!/bin/bash

python -m venv aurora_server_environ
source aurora_server_environ/bin/activate 

or
 
source /Users/osnatshabtay/Desktop/aurora_server/aurora_server_environ/bin/activate

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

http://127.0.0.1:8000/docs#/

unalias python




# tests
/Users/osnatshabtay/Desktop/aurora_server/aurora_server_environ/bin/python -m pytest app/tests/test_user_routes.py
/Users/osnatshabtay/Desktop/aurora_server/aurora_server_environ/bin/python -m pytest app/tests/test_post_routes.py
/Users/osnatshabtay/Desktop/aurora_server/aurora_server_environ/bin/python -m pytest app/tests/test_chatbot_routes.py

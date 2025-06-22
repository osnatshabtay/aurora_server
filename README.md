# Aurora Server (FastAPI Backend)

This is the **backend** of the Aurora project — an AI-powered mental health support platform.  
It powers all core logic and data flow between the mobile client and the server, including chatbot communication, content personalization, user management, and more.

## Technologies

- Python 
- FastAPI
- MongoDB (via `motor`)
- OpenAI API + Sentence Transformers (for chatbot & personalization)
- FAISS for vector search
- Auth via `python-jose` and `passlib`

## Project Structure

├── README.md
├── app
│   ├── FAISS_data
│   ├── __init__.py
│   ├── __pycache__
│   ├── db.py
│   ├── main.py
│   ├── models
│   ├── modules
│   ├── openai.py
│   ├── routes
│   ├── services
│   ├── tests
│   └── utils
├── aurora_server_environ
│   ├── bin
│   ├── include
│   ├── lib
│   ├── pyvenv.cfg
│   └── share
├── reprocess_existing_users.py
├── requirements.txt
└── run_backend.sh


## Running the Server

`python -m venv aurora_server_environ`
`source aurora_server_environ/bin/activate`
`pip install -r requirements.txt`
`uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

- Your API will be available at:
    http://127.0.0.1:8000/docs (Swagger UI)


## Running Tests

# User routes
aurora_server_environ/bin/python -m pytest app/tests/test_user_routes.py

# Post approval and admin
aurora_server_environ/bin/python -m pytest app/tests/test_admin_post_routes.py

# Chatbot
aurora_server_environ/bin/python -m pytest app/tests/test_chatbot_routes.py

# Enrichment content
aurora_server_environ/bin/python -m pytest app/tests/test_enrichment_content_routes.py

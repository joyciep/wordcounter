# wordcounter

`wordcounter` is an API which counts how many times a word exists in a given web page

# Development

## Installation

[`poetry`](https://python-poetry.org/) is used for setting up dependencies and environment

```
poetry install
poetry shell
```

## Running

Run the application

```
uvicorn app.main:app
```

Application will be available in http://localhost:8000

## Tests

```
pytest tests/
```

## Code Formatter

```
black .
```

# Deployment

```
docker build -t wordcounter:v1.0.0 .
docker run -p 8000:8000 wordcounter:v1.0.0
```

# API Contract

Go to http://localhost:8000/docs for the Swagger documentation

# Project Structure

```
app
├── api              - API handler / web route
├── core             - application configuration, startup events, logging
├── db               - database related code
│   └── repositories - all CRUD operations
├── models           - pydantic and sqlalchemy models for this application
│   ├── domain       - main models for database
│   └── schemas      - schemas for using in web route
├── services         - logic aside from CRUD
└── main.py          - FastAPI application creation and configuration.
```

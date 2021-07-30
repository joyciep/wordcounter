# wordcounter

`wordcounter` is an API which counts how many times a word exists in a given web page.

# Development

## Installation

[`poetry`](https://python-poetry.org/) is used for setting up dependencies and environment

```
poetry install
poetry shell
```

## App Configuration

```sh
export DEBUG=true (default: false)
export CREATE_TABLES=false (default: true)
export DATABASE_URL=sqlite+aiosqlite:///path/to/wordcounter.db (default: sqlite+aiosqlite:///./wordcounter.db)
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

# API Endpoints

- GET `/docs` or `/redoc` for the API documentation
- POST `/wordcount` (see `/docs` or `/redoc` for documentation)

# Project Structure

```
app - main application code
├── api              - API handler / web route
├── core             - application configuration, startup events, logging
├── db               - database related code
│   └── repositories - all CRUD operations
├── models           - pydantic and sqlalchemy models for this application
│   ├── domain       - main models for database
│   └── schemas      - schemas for using in web route
├── services         - logic aside from CRUD
└── main.py          - FastAPI application creation and configuration.
tests - unit tests
```

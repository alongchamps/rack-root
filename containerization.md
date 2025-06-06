# Intro
This whole project has been about learning, so why stop at just writing the frontend and the backend and running it locally. I want to make some containers with these and publish them.

The docs below contain the key points and environment variables that will need to be set in order to make it work in a containerized environment.

# Database

This project supports using a `postgres` container for the database.

# Backend

Holds all the code to run FastAPI, does not contain any frontend code.

## Environment Variables

`DATABASE_URL` - contains the connection string in the format of `postgresql+psycopg2://{username}:{password}@{hostname}:{port}/postgres`

Default:
```
postgresql+psycopg2://postgres:postgres-fastapi@localhost:5432/postgres
```

# Frontend

Holds all the code to run the frontend in production. Does not contain any backend code.

## Environment Variables

`BACKEND_SERVER` - hostname for the backend

`BACKEND_PORT` - port for the backend


##### Todo
This file has a long way to go before it's 'ready' so most of what's on here is a placeholder.

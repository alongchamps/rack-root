# How I Built This Project
*Or at least how I got started*

Line by line from my terminal, this is how I built this project.

# Frontend

The frontend of this code was initialized via `npm create vuetify@latest` which scaffolded a base Vue/Vuetify project for me after I answered some questions.

The first time I created this, I think I forgot to install the Recommended preset, and only did the Default one. As a side effect, my server had issues serving up `.vue` files. Therefore, I reinitialized the project with the output you can now see below:

```
aaron@Aarons-MacBook-Pro rack-root % npm create vuetify@latest

> npx
> create-vuetify


Vuetify.js - Material Component Framework for Vue

✔ Project name: … frontend
✔ Which preset would you like to install? › Recommended (Everything from Default. Adds auto importing, layouts & pinia)
✔ Use TypeScript? … No / Yes
✔ Would you like to install dependencies with yarn, npm, pnpm, or bun? › npm
✔ Install Dependencies? … No / Yes

◌ Generating scaffold...
◌ Installing dependencies with npm...


added 336 packages, and audited 337 packages in 16s

118 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities

frontend has been generated at /Users/aaron/github/rack-root/frontend

Discord community: https://community.vuetifyjs.com
Github: https://github.com/vuetifyjs/vuetify
Support Vuetify: https://github.com/sponsors/johnleider
```

To start the front end, I run:

```
cd frontend
npm run dev
```

And we're up! The Vue app is now running on https://localhost:3000. Check it out ;)

# venv

I'm using a virtual environment for this project with the following commands:

```
python3 -m venv venv-rr
source ./venv-rr/bin/active
pip3 install -r requirements.txt
```

# Backend

The backend for this app will be powered by FastAPI. Essential packages will be installed via requirements.txt.

## Testing
I'm using pytest to run the tests for the backend which should allow me to develop more quickly later. My intention is that for every API endpoint, I have a test of some kind that will cover that code. Code coverage might get to 100%, but we'll see.

In my `pytest.ini` file, I have one directive and that's to set an environmental variable for the databse file name. Since I'm only using a local sqlite database file for this app, I set the environment variable `DATABASE_URL` to be `nonproduction.db` for testing. When I am running via pytest, I drop every piece of data to 'reset' the database without totally deleting and recreating it.

I came about this solution since I can use calls like `os.getenv("DATABASE_URL", "sqlite:///./backend/production.db")` in order to find out what database file I'm using.

The pytest command I run looks like this and you can see where I'm importing the pytest.ini file:

```
pytest --import-mode prepend -c ./backend/tests/pytest.ini -v
```

Pytest will automatically search inside the backend/tests directory for any files matching `test*` and inside those python files, any function calls starting with `test*`. I try to use somewhat descriptive names, such as `TestItemThatDoesntExist` or `TestItemCreate` as I'm writing these.

## Running the app
In order for the frontend to talk to the backend, it has to be allowed in the `main.py` app via the CORSMiddleware allowed origins functionality. I specify that `localhost:3000` is allowed and register that to the FastAPI app instance.

Starting the backend in dev mode will enable file watching for faster development. Update a file and when you save it to disk, the program will reload with the changes.

```
fastapi dev backend/main.py
```

And with that, our front end is talking to our back end and serving up data.

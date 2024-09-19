# How I Built This Project
*Or at least how I got started*

Line by line from my terminal, this is how I built this project.

# Frontend

The frontend of this code was initialized via `pnpm create vuetify`.

```
aaron@Aarons-MacBook-Pro rack-root % pnpm create vuetify
.../192080151c3-13640                    |   +9 +
.../192080151c3-13640                    | Progress: resolved 9, reused 0, downloaded 9, added 9, done

Vuetify.js - Material Component Framework for Vue

✔ Project name: … frontend
✔ Which preset would you like to install? › Default (Adds routing, ESLint & SASS variables)
✔ Use TypeScript? … No
✔ Would you like to install dependencies with yarn, npm, pnpm, or bun? › pnpm
✔ Install Dependencies? … Yes

◌ Generating scaffold...
◌ Installing dependencies with pnpm...

 WARN  5 deprecated subdependencies found: @humanwhocodes/config-array@0.13.0, @humanwhocodes/object-schema@2.0.3, glob@7.2.3, inflight@1.0.6, rimraf@3.0.2
Packages: +294
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Progress: resolved 331, reused 3, downloaded 291, added 294, done
node_modules/.pnpm/core-js@3.38.1/node_modules/core-js: Running postinstall script, done in 42ms
node_modules/.pnpm/esbuild@0.21.5/node_modules/esbuild: Running postinstall script, done in 294ms

dependencies:
+ @mdi/font 7.4.47
+ core-js 3.38.1
+ roboto-fontface 0.10.0
+ vue 3.5.6
+ vuetify 3.7.2

devDependencies:
+ @vitejs/plugin-vue 5.1.4
+ eslint 8.57.1 (9.10.0 is available)
+ eslint-config-standard 17.1.0
+ eslint-plugin-import 2.30.0
+ eslint-plugin-n 16.6.2 (17.10.3 is available)
+ eslint-plugin-node 11.1.0
+ eslint-plugin-promise 6.6.0 (7.1.0 is available)
+ eslint-plugin-vue 9.28.0
+ sass 1.77.6 (1.79.1 is available)
+ unplugin-fonts 1.1.1
+ unplugin-vue-components 0.27.4
+ unplugin-vue-router 0.10.8
+ vite 5.4.6
+ vite-plugin-vuetify 2.0.4
+ vue-router 4.4.5

Done in 7s

frontend has been generated at /Users/aaron/github/rack-root/frontend

Discord community: https://community.vuetifyjs.com
Github: https://github.com/vuetifyjs/vuetify
Support Vuetify: https://github.com/sponsors/johnleider
```

To run this, I then ran:

```
cd frontend
npm run dev
```

And we're up! The Vue app is now running on https://localhost:3000.

# Backend

The backend for this app will be powered by FastAPI.


# venv

I'm using a virtual environment for this space with the following commands:

```
python3 -m venv venv-rr
source ./venv-rr/bin/active
pip3 install -r requirements.txt
```

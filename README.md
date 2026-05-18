# Cut Tube

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Description

**Cut Tube** is a full-stack web application that lets you extract and download a specific segment from any YouTube video. Instead of downloading an entire video, you simply provide the YouTube URL, specify a start time and end time (in `HH:MM:SS` format), give the clip a custom filename, and Cut Tube handles the rest.

Under the hood, the Flask backend fetches the best available video stream from YouTube using `pytubefix`, temporarily stores it on the server, and then uses `moviepy` to cut the exact segment you requested. The resulting `.mp4` clip is saved on the server and immediately made available for download through the browser.

The React + TypeScript frontend guides you through the whole process with a clean, responsive form. Once the clip is ready, you are taken to a result view where you can download it to your device or delete it from the server once you no longer need it. The UI adapts to different screen sizes and provides real-time feedback during processing via a loading state managed with Redux.

The main use case is saving short highlights, tutorial excerpts, or any meaningful moment from a YouTube video without needing to keep the full original file. The workflow is entirely self-contained: clip, download, delete — no accounts, no third-party storage, no external dependencies beyond the YouTube URL itself.

## Technologies used

The stack is split between a React frontend, a Flask backend, and a containerized deployment layer.

### Frontend

1. React JS
2. TypeScript
3. Tailwind CSS
4. CSS3
5. HTML5
6. Vite

### Backend

1. Python -> Flask

### Deploy

1. Docker
2. Nginx
3. Gunicorn

## Libraries used

The exact dependencies pinned for each side of the project are listed below.

### Frontend

#### Dependencies

```
"@reduxjs/toolkit": "^2.2.2"
"axios": "^1.6.8"
"react": "^19.2.4"
"react-dom": "^19.2.4"
"react-router-dom": "7.13.2"
"react-icons": "^5.0.1"
"react-redux": "^9.1.0"
```

#### devDependencies

```
"@eslint/js": "^9.0.0"
"@testing-library/dom": "^10.4.0"
"@testing-library/jest-dom": "^6.6.3"
"@testing-library/react": "^16.0.1"
"@testing-library/user-event": "^14.5.2"
"@types/jest": "^30.0.0"
"@types/node": "^22.0.0"
"@types/react": "^19.2.14"
"@types/react-dom": "^19.2.3"
"@vitejs/plugin-react": "^5.0.2"
"eslint": "^9.0.0"
"eslint-config-prettier": "^9.0.0"
"eslint-plugin-prettier": "^5.5.5"
"eslint-plugin-react-hooks": "^5.0.0"
"eslint-plugin-react-refresh": "^0.4.0"
"globals": "^15.0.0"
"jest": "^30.3.0"
"jest-environment-jsdom": "^30.3.0"
"lint-staged": "^15.0.0"
"msw": "2.10.4"
"prettier": "^3.0.0"
"ts-jest": "^29.4.6"
"autoprefixer": "^10.4.18"
"postcss": "^8.4.37"
"tailwindcss": "^3.4.1"
"typescript": "^5.2.2"
"typescript-eslint": "^8.0.0"
"undici": "^7.25.0"
"vite": "^7.1.6"
```

### Backend

#### Runtime (`[project.dependencies]`)

```
pytubefix==10.7.2
flask==3.1.3
moviepy==2.2.1
pydantic==2.11.9
gunicorn==23.0.0
```

#### Dev (`[project.optional-dependencies]` dev)

```
pre-commit==4.3.0
pip-audit==2.7.3
ruff==0.11.12
mypy==1.13.0
```

#### Test (`[project.optional-dependencies]` test)

```
pytest==9.0.3
pytest-env==1.1.5
pytest-cov==4.1.0
pytest-timeout==2.3.1
pytest-xdist==3.5.0
```

## Getting Started

With the dependencies in mind, the following steps will get the full stack running locally via Docker.

1. Clone the repository with `git clone "repository link"`
2. Copy `.env.example.dev` to `.env` so the containers pick up the required configuration (the env keys are documented in the next section).
3. Join to `cut-tube-app` folder and execute: `npm install` or `yarn install` in the terminal
4. Go to the previous folder and execute: `docker-compose -f dev.docker-compose.yml build --no-cache` in the terminal
5. Once built, you must execute the command: `docker-compose -f dev.docker-compose.yml up --force-recreate` in the terminal

NOTE: You have to be standing in the folder containing the: `dev.docker-compose.yml` and you need to install `Docker Desktop` if you are in Windows.

### Pre-Commit for Development (Python)

NOTE: Install **pre-commit** inside: `cut-tube-api` folder.

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

## Env Keys

The application reads its configuration from these environment variables.

1. `TZ`: Refers to the timezone setting for the container.
2. `VITE_API_URL`: Refers to the base URL of the backend API the frontend consumes.
3. `HOST`: Refers to the network interface where the backend API listens (e.g., 0.0.0.0 to allow external connections).
4. `PORT`: Refers to the port on which the backend API is exposed.
5. `WORK_DIR`: Refers to the docker working path.
6. `MAX_CONTENT_LENGTH`: Refers to the maximum allowed size in bytes for an incoming request body (defaults to 1 MiB).

```
# Backend

TZ=America/Argentina/Buenos_Aires

WORK_DIR=/home/app

HOST=0.0.0.0
PORT=5050
MAX_CONTENT_LENGTH=1048576

# Frontend

VITE_API_URL=http://host.docker.internal:5000
```

## Documentation API

Once the stack is running and pointed at the configured `VITE_API_URL`, the following endpoints are exposed by the Flask backend.

### **Version**

```
API VERSION: 0.0.3
README UPDATED: 18/05/2026
AUTHOR: Diego Libonati
```

### **Health Endpoints API**

- **Endpoint Name**: Health
- **Endpoint Route**: /api/v1/health/
- **Endpoint Method**: GET
- **Endpoint Fn**: This endpoint reports that the application is up and serving requests. Used by the production container `HEALTHCHECK`.

---

### **Cut Tube Endpoints API**

- **Endpoint Name**: Alive
- **Endpoint Route**: /api/v1/cut/alive
- **Endpoint Method**: GET
- **Endpoint Fn**: This endpoint returns the version, author and name of the api.

---

- **Endpoint Name**: Clip Video
- **Endpoint Route**: /api/v1/cut/<filename>/clip
- **Endpoint Method**: POST
- **Endpoint Fn**: This endpoint downloads the video from youtube, obtains the best stream based on the quality and clips based on the parameters entered through the body.
- **Endpoint Params**:

```ts
{
  filename: string;
}
```

- **Endpoint Body**:

```ts
{
  url: string;
  start: string;
  end: string;
}
```

---

- **Endpoint Name**: Download Clip
- **Endpoint Route**: /api/v1/cut/<filename>/download
- **Endpoint Method**: GET
- **Endpoint Fn**: This endpoint downloads the clip to the user's browser once the clip has been clicked and exists on the server. The name of the file with the extension .mp4 is entered via the URL.
- **Endpoint Params**:

```ts
{
  filename: string;
}
```

---

- **Endpoint Name**: Delete Clip
- **Endpoint Route**: /api/v1/cut/<filename>
- **Endpoint Method**: DELETE
- **Endpoint Fn**: This endpoint removes from the server if it exists the clip that is entered via URL based on its name and its .mp4 extension.
- **Endpoint Params**:

```ts
{
  filename: string;
}
```

## Testing

With the API contract in mind, both sides of the project ship their own test suites.

### Frontend

1. Navigate to the project folder
2. Execute: `npm test`

For coverage report:

```bash
npm run test:coverage
```

### Backend

1. Join to the correct path of the clone and join to: `cut-tube-api`
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute: `pip install -e ".[test]"`
5. Execute: `pytest --log-cli-level=INFO`

## Continuous Integration

The repository ships with a **GitHub Actions** pipeline defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml). It runs automatically on every `push` and `pull_request` targeting the `main` branch and validates both sides of the monorepo plus the Docker images, in that order.

### Pipeline overview

```
                ┌── PR or push to main ──┐
                ▼                        ▼
        ┌──────────────────────────┐
        │  backend-lint-and-audit  │   ruff · ruff format · mypy · pip-audit
        └────────────┬─────────────┘
                     ▼
        ┌──────────────────────────┐
        │      backend-test        │   pytest
        └────────────┬─────────────┘
                     ▼
        ┌──────────────────────────┐
        │ frontend-lint-and-audit  │   eslint · tsc --noEmit · npm audit
        └────────────┬─────────────┘
                     ▼
        ┌──────────────────────────┐
        │      frontend-test       │   jest + MSW
        └────────────┬─────────────┘
                     ▼
        ┌──────────────────────────┐
        │      frontend-build      │   tsc + vite build
        └────────────┬─────────────┘
                     ▼
        ┌─────────────────────────────────────────┐
        │      docker-build (matrix, parallel)    │
        │  cut-tube-api:dev   cut-tube-api:prod   │
        │  cut-tube-app:dev   cut-tube-app:prod   │
        └─────────────────────────────────────────┘
```

### Validation jobs (run on every PR and push)

1. **`backend-lint-and-audit`** — sets up Python from `cut-tube-api/.python-version`, installs `[dev]` extras and runs `ruff check`, `ruff format --check`, `mypy --config-file=pyproject.toml .` and `pip-audit --skip-editable`.
2. **`backend-test`** — installs `[test]` extras and runs `python -m pytest --tb=short`.
3. **`frontend-lint-and-audit`** — sets up Node from `cut-tube-app/.nvmrc`, runs `npm ci --ignore-scripts`, then `npm run lint`, `npm run type-check` and `npm audit --audit-level=high` (informational, `continue-on-error`).
4. **`frontend-test`** — `npm run test` (Jest + Testing Library + MSW with the `undici` polyfills).
5. **`frontend-build`** — `npm run build` (`tsc -p tsconfig.app.json && vite build`).
6. **`docker-build`** — `docker/build-push-action` runs in a matrix that builds the four images (api dev/prod and app dev/prod) **in parallel**. `fail-fast: false` so one failing image does not cancel the others. Images are built but **not pushed**.

> **Note:** the `--ignore-scripts` flag on `npm ci` skips the `prepare` hook that wires `core.hooksPath` to `.githooks/`. CI runners do not need the local pre-commit hooks installed.

### Skipping CI

To push a change to `main` without running the workflow (e.g. fixing a typo in the README), append GitHub's standard marker `[skip ci]` to the commit message:

```bash
git commit -m "docs: fix typo in README [skip ci]"
```

### Running the same checks locally

**Backend** (from `cut-tube-api/`, with the virtual environment activated):

```bash
pip install -e ".[dev]" ".[test]"

ruff check .
ruff format --check .
mypy --config-file=pyproject.toml .
pip-audit --skip-editable \
  --ignore-vuln GHSA-cfh3-3jmp-rvhc \
  --ignore-vuln GHSA-whj4-6x5x-4v2j \
  --ignore-vuln GHSA-wjx4-4jcj-g98j \
  --ignore-vuln GHSA-5xmw-vc9v-4wf2 \
  --ignore-vuln GHSA-r73j-pqj5-w3x7 \
  --ignore-vuln GHSA-pwv6-vv43-88gr
python -m pytest --tb=short
```

**Frontend** (from `cut-tube-app/`):

```bash
npm ci

npm run lint
npm run type-check
npm run test
npm run build
```

**Docker images** (from the repo root):

```bash
docker build -f cut-tube-api/Dockerfile.development -t cut-tube-api:dev cut-tube-api
docker build -f cut-tube-api/Dockerfile.production  -t cut-tube-api:prod cut-tube-api
docker build -f cut-tube-app/Dockerfile.development -t cut-tube-app:dev cut-tube-app
docker build -f cut-tube-app/Dockerfile.production  -t cut-tube-app:prod cut-tube-app
```

### Where the build outputs live

| Output | Location |
|---|---|
| Validation logs (lint, tests, build) | **Actions** tab on GitHub |
| Docker images | Ephemeral, inside the runner (not pushed to any registry) |
| Coverage reports (when run locally) | `cut-tube-api/htmlcov/`, `cut-tube-app/coverage/` |

## Security Audit

In addition to functional tests, both sides of the project can be audited for known dependency vulnerabilities.

### Backend (Python)

You can check your dependencies for known vulnerabilities using **pip-audit**.

1. Go to the repository folder
2. Activate your virtual environment
3. Execute: `pip install -e ".[dev]"`
4. Execute: `pip-audit -r requirements.txt`

### Frontend

#### npm audit

Check for vulnerabilities in dependencies:

```bash
npm audit
```

#### React Doctor

Run a health check on the project (security, performance, dead code, architecture):

```bash
npm run doctor
```

Use `--verbose` to see specific files and line numbers:

```bash
npm run doctor -- --verbose
```

## Known Issues

Issues surfaced by the audits above that are tracked but not yet resolved are documented here.

### [SERVER] — Pillow vulnerabilities (transitive dependency via moviepy)

`pillow 11.3.0` is pulled in transitively by `moviepy==2.2.1` and is currently flagged by `pip-audit` with the following advisories:

| Advisory | Fixed in |
|---|---|
| GHSA-cfh3-3jmp-rvhc | 12.1.1 |
| GHSA-whj4-6x5x-4v2j | 12.2.0 |
| GHSA-wjx4-4jcj-g98j | 12.2.0 |
| GHSA-5xmw-vc9v-4wf2 | 12.2.0 |
| GHSA-r73j-pqj5-w3x7 | 12.2.0 |
| GHSA-pwv6-vv43-88gr | 12.2.0 |

None of these vulnerabilities are reachable through any code path in Cut Tube. The API only processes video streams downloaded from YouTube; Pillow is loaded transitively by `moviepy` for internal frame manipulation and is **never** exposed to user-supplied images, archives, or arbitrary file paths. The known attack vectors (crafted PSD / ICO / EPS / TGA and similar image files) cannot be reached from any endpoint.

Upgrading Pillow to 12.x is blocked by `moviepy==2.2.1`, which declares `pillow<12.0` as a dependency constraint. This will be resolved automatically once moviepy releases a version that lifts that cap.

To keep CI auditable while tracking these accepted advisories explicitly, both the `backend-lint-and-audit` job in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) and the local example below pass each advisory ID through `pip-audit --ignore-vuln`. Any **other** advisory (Pillow or otherwise) still fails the audit — the allowlist is intentionally narrow.

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/cut-tube`](https://www.diegolibonati.com.ar/#/project/cut-tube)

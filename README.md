# Cut Tube

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Getting Started

1. Clone the repository with `git clone "repository link"`
2. Join to `cut-tube-app` folder and execute: `npm install` or `yarn install` in the terminal
3. Go to the previous folder and execute: `docker-compose -f dev.docker-compose.yml build --no-cache` in the terminal
4. Once built, you must execute the command: `docker-compose -f dev.docker-compose.yml up --force-recreate` in the terminal

NOTE: You have to be standing in the folder containing the: `dev.docker-compose.yml` and you need to install `Docker Desktop` if you are in Windows.

### Pre-Commit for Development (Python)

NOTE: Install **pre-commit** inside: `cut-tube-api` folder.

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

## Description

**Cut Tube** is a full-stack web application that lets you extract and download a specific segment from any YouTube video. Instead of downloading an entire video, you simply provide the YouTube URL, specify a start time and end time (in `HH:MM:SS` format), give the clip a custom filename, and Cut Tube handles the rest.

Under the hood, the Flask backend fetches the best available video stream from YouTube using `pytubefix`, temporarily stores it on the server, and then uses `moviepy` to cut the exact segment you requested. The resulting `.mp4` clip is saved on the server and immediately made available for download through the browser.

The React + TypeScript frontend guides you through the whole process with a clean, responsive form. Once the clip is ready, you are taken to a result view where you can download it to your device or delete it from the server once you no longer need it. The UI adapts to different screen sizes and provides real-time feedback during processing via a loading state managed with Redux.

The main use case is saving short highlights, tutorial excerpts, or any meaningful moment from a YouTube video without needing to keep the full original file. The workflow is entirely self-contained: clip, download, delete — no accounts, no third-party storage, no external dependencies beyond the YouTube URL itself.

## Technologies used

1. React JS
2. Typescript
3. Tailwind CSS
4. CSS3
5. HTML5
6. Vite

BackEnd:

1. Python -> Flask

Deploy:

1. Docker
2. Nginx
3. Gunicorn

## Libraries used

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
"husky": "^9.0.0"
"jest": "^30.3.0"
"jest-environment-jsdom": "^30.3.0"
"lint-staged": "^15.0.0"
"prettier": "^3.0.0"
"ts-jest": "^29.4.6"
"autoprefixer": "^10.4.18"
"postcss": "^8.4.37"
"tailwindcss": "^3.4.1"
"typescript": "^5.2.2"
"typescript-eslint": "^8.0.0"
"vite": "^7.1.6"
```

### Backend

#### Requirements.txt

```
pytubefix==8.8.2
flask==3.1.3
moviepy==2.1.1
pydantic==2.11.9
gunicorn==23.0.0
```

#### Requirements.dev.txt

```
pre-commit==4.3.0
pip-audit==2.7.3
ruff==0.11.12
```

#### Requirements.test.txt

```
pytest==8.4.2
pytest-env==1.1.5
pytest-cov==4.1.0
pytest-timeout==2.3.1
pytest-xdist==3.5.0
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/cut-tube`](https://www.diegolibonati.com.ar/#/project/cut-tube)

## Testing

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
4. Execute: `pip install -r requirements.txt`
5. Execute: `pip install -r requirements.test.txt`
6. Execute: `pytest --log-cli-level=INFO`

## Security Audit (Python)

You can check your dependencies for known vulnerabilities using **pip-audit**.

1. Go to the repository folder
2. Activate your virtual environment
3. Execute: `pip install -r requirements.dev.txt`
4. Execute: `pip-audit -r requirements.txt`

## Security Audit (Frontend)

### npm audit

Check for vulnerabilities in dependencies:

```bash
npm audit
```

### React Doctor (Frontend)

Run a health check on the project (security, performance, dead code, architecture):

```bash
npm run doctor
```

Use `--verbose` to see specific files and line numbers:

```bash
npm run doctor -- --verbose
```

## Documentation API

### **Version**

```
API VERSION: 0.0.2
README UPDATED: 01/02/2026
AUTHOR: Diego Libonati
```

### **Env Keys**

1. `TZ`: Refers to the timezone setting for the container.
2. `VITE_API_URL`: Refers to the base URL of the backend API the frontend consumes.
3. `HOST`: Refers to the network interface where the backend API listens (e.g., 0.0.0.0 to allow external connections).
4. `PORT`: Refers to the port on which the backend API is exposed.
5. `WORK_DIR`: Refers to the docker working path.

```
# Backend

TZ=America/Argentina/Buenos_Aires

WORK_DIR=/home/app

HOST=0.0.0.0
PORT=5050

# Frontend

VITE_API_URL=http://host.docker.internal:5000
```

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

## Known Issues

### [SERVER] - CVE-2026-25990 / GHSA-cfh3-3jmp-rvhc — Pillow out-of-bounds write (High)

pillow 10.4.0 (pulled in transitively by moviepy) is affected by an out-of-bounds write vulnerability triggered when loading specially crafted PSD image files. The fix is available in pillow 12.1.1.
This vulnerability does not affect this project in practice. Cut Tube only processes video streams downloaded from YouTube and never opens or accepts PSD files. The attack vector is not reachable through any code path in this API.
Upgrading Pillow to 12.1.1 is blocked by moviepy==2.1.1, which declares pillow<12.0 as a dependency constraint. This will be resolved once moviepy releases a version that lifts that cap.

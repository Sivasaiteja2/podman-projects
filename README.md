# Podman Practical Projects

This repository contains the first three hands-on Podman projects.

## Projects

### Project 1 - Basic Nginx Container
Learned:
- Pulling images
- Running containers
- Port mapping
- Logs
- Executing commands inside containers
- Starting, stopping, and removing containers

### Project 2 - Custom Nginx Image
Learned:
- Containerfile
- Building custom images
- `FROM`, `COPY`, and `EXPOSE`
- Image tags and versions
- Serving custom HTML pages

### Project 3 - Multi-Container Application
Built a three-tier containerized application:

```text
Browser
   |
   v
Nginx Frontend :8080
   |
   v
Flask Backend :5000
   |
   v
PostgreSQL :5432
```

Learned:
- Podman networks
- Container-to-container communication
- Container DNS
- Environment variables
- PostgreSQL containers
- Persistent volumes
- Flask backend
- Nginx frontend
- Multi-container architecture

---

# Prerequisites

Ubuntu with Podman installed.

Verify:

```bash
podman --version
podman info
```

---

# Project 1 - Basic Nginx

```bash
cd project1-nginx-basic

podman pull nginx
podman images

podman run -d --name my-nginx -p 8080:80 nginx
podman ps

curl http://localhost:8080
podman logs my-nginx
podman exec -it my-nginx /bin/bash

podman stop my-nginx
podman start my-nginx

podman stop my-nginx
podman rm my-nginx
```

---

# Project 2 - Custom Nginx

```bash
cd project2-custom-nginx

podman build -t my-nginx:v3 .
podman images

podman run -d --name podman-web -p 8080:80 my-nginx:v3
podman ps
```

Test:

```bash
curl http://localhost:8080
curl http://localhost:8080/about.html
```

Browser:

```text
http://localhost:8080
http://localhost:8080/about.html
```

---

# Project 3 - Multi-Container Application

## Architecture

```text
                    Browser
                       |
                       | :8080
                       v
              +----------------+
              |     Nginx      |
              |    Frontend    |
              +-------+--------+
                      |
                      | HTTP
                      v
              +----------------+
              |  Flask Backend |
              |     :5000      |
              +-------+--------+
                      |
                      | PostgreSQL
                      v
              +----------------+
              |   PostgreSQL   |
              |     :5432      |
              +-------+--------+
                      |
                postgres-data
                    volume
```

## Step 1 - Create the network

```bash
podman network create app-network
```

Verify:

```bash
podman network ls
```

## Step 2 - Create PostgreSQL volume

```bash
podman volume create postgres-data
```

## Step 3 - Run PostgreSQL

```bash
podman run -d   --name postgres-db   --network app-network   -e POSTGRES_USER=appuser   -e POSTGRES_PASSWORD=apppassword   -e POSTGRES_DB=appdb   -v postgres-data:/var/lib/postgresql/data   postgres:16
```

Verify:

```bash
podman ps
```

## Step 4 - Build backend

```bash
podman build -t podman-backend:v1 ./backend
```

## Step 5 - Run backend

```bash
podman run -d   --name backend-api   --network app-network   -e DB_HOST=postgres-db   -e DB_NAME=appdb   -e DB_USER=appuser   -e DB_PASSWORD=apppassword   -p 5000:5000   podman-backend:v1
```

Test:

```bash
curl http://localhost:5000
curl http://localhost:5000/health
curl http://localhost:5000/db
```

Expected database result contains:

```text
"status": "Connected"
```

## Step 6 - Build frontend

```bash
podman build -t podman-frontend:v1 ./frontend
```

## Step 7 - Run frontend

```bash
podman run -d   --name frontend-web   --network app-network   -p 8080:80   podman-frontend:v1
```

Verify all containers:

```bash
podman ps
```

Expected:

```text
frontend-web
backend-api
postgres-db
```

Open:

```text
http://localhost:8080
```

Click **Check Backend**.

---

# Useful Project 3 Commands

## Logs

```bash
podman logs frontend-web
podman logs backend-api
podman logs postgres-db
```

## Network

```bash
podman network inspect app-network
```

## Containers

```bash
podman ps
podman ps -a
```

## Volume

```bash
podman volume ls
podman volume inspect postgres-data
```

## Enter backend

```bash
podman exec -it backend-api /bin/bash
```

## Test PostgreSQL persistence

```bash
podman stop postgres-db
podman rm postgres-db
```

The `postgres-data` volume remains.

Recreate PostgreSQL using the same volume:

```bash
podman run -d   --name postgres-db   --network app-network   -e POSTGRES_USER=appuser   -e POSTGRES_PASSWORD=apppassword   -e POSTGRES_DB=appdb   -v postgres-data:/var/lib/postgresql/data   postgres:16
```

---

# Project 3 Challenge

After the basic project works:

1. Add a `/users` API endpoint.
2. Create a PostgreSQL users table.
3. Insert sample users.
4. Read users from PostgreSQL through Flask.
5. Display the users in the frontend.
6. Build `podman-backend:v2`.
7. Replace the running backend with v2.
8. Verify PostgreSQL data remains after recreating the database container.

---

# Important Podman Concepts Learned

| Concept | Example |
|---|---|
| Image | `nginx`, `postgres:16` |
| Container | `frontend-web`, `backend-api` |
| Containerfile | `backend/Containerfile` |
| Build | `podman build` |
| Network | `app-network` |
| Volume | `postgres-data` |
| Port mapping | `8080:80` |
| Environment variable | `DB_HOST=postgres-db` |
| Container DNS | `postgres-db` |
| Logs | `podman logs` |
| Exec | `podman exec` |
| Persistent storage | PostgreSQL volume |

---

# Repository Structure

```text
podman-projects-1-3/
│
├── README.md
│
├── project1-nginx-basic/
│   └── README.md
│
├── project2-custom-nginx/
│   ├── Containerfile
│   ├── index.html
│   ├── about.html
│   └── README.md
│
└── project3-multi-container-app/
    ├── backend/
    │   ├── Containerfile
    │   ├── app.py
    │   └── requirements.txt
    │
    └── frontend/
        ├── Containerfile
        └── index.html
```

## Note for GitHub

This repository intentionally does **not** contain built images or PostgreSQL data. Those are created locally by the Podman commands in the README.

The database password in this learning project is only a local demo credential. For a real project, use secrets/environment management rather than committing credentials to Git.

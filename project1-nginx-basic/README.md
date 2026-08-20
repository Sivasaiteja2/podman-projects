# Project 1 - Basic Nginx Container with Podman

## Objective
Run an Nginx container using Podman, expose it on port 8080, inspect logs, enter the container, and manage its lifecycle.

## Commands

```bash
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

## Concepts
- Podman images
- Containers
- Port mapping
- Logs
- `podman exec`
- Container lifecycle

# Project 2 - Custom Nginx Image with Podman

## Objective
Build a custom Nginx image using a Containerfile and serve custom HTML pages.

## Build

```bash
podman build -t my-nginx:v3 .
podman images
```

## Run

```bash
podman run -d --name podman-web -p 8080:80 my-nginx:v3
podman ps
```

## Test

```bash
curl http://localhost:8080
curl http://localhost:8080/about.html
```

Open in a browser:

- `http://localhost:8080`
- `http://localhost:8080/about.html`

## Concepts
- Containerfile
- `FROM`
- `COPY`
- `EXPOSE`
- Custom image creation
- Image versioning
- Nginx static content

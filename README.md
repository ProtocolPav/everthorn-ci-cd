# 🚀 Everthorn CI/CD

A lightweight CI/CD system that automates microservice deployments using Google Cloud Pub/Sub and Docker Compose with Discord notifications.

## Features

- Automated container deployments via Pub/Sub messages
- Docker Compose integration for service management
- Discord notifications with deployment status
- Self-updating capability with Cloud Build integration

## Prerequisites

- Docker and Docker Compose
- Google Cloud Project with Pub/Sub enabled
- Discord webhook URL
- Google Cloud service account with Pub/Sub permissions

## Installation

### 1. Set Up Google Cloud

Create a service account with Pub/Sub permissions and download the JSON credentials.

### 2. Create Discord Webhook

Create a webhook in your Discord server settings.

### 3. Configure Docker Compose

Create a `docker-compose.yml` file:

```yaml
name: your-compose-project

services:
  everthorn-cicd:
    build: .
    container_name: everthorn-cicd
    environment:
      DISCORD_WEBHOOK: https://discord.com/api/webhooks/your-webhook-url
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./single-inquiry-keyfile.json:/google-credentials.json:ro
      - ./docker-compose.yml:/everthorn-ci-cd/docker-compose.yml:ro
    restart: unless-stopped
```

**⚠️ The Docker socket mount is required for the service to function.**
**⚠️ You must also mount `docker-compose.yml` as a read-only volume for the service to function.**
**⚠️ Having a `name` set for your compose file is important for the service to function.**

## Usage

### Start the Service

```bash
docker-compose up -d
```

### Trigger Deployments

Send a JSON message to your Pub/Sub topic:

```json
{
  "compose-name": "my-service",
  "image": "gcr.io/project-id/my-service:latest"
}
```

- `compose-name`: Service name in your Docker Compose file
- `image`: Full image path with registry and tag

### Self-Updating

Configure Cloud Build to build new images of `everthorn-cicd` on code changes. 
Send a deployment message with the CI/CD service's own image to trigger automatic self-updates.

By default, the `image` and `compose-name` will reference `everthorn-cicd`. 
Ensure your service is named accordingly in Docker Compose to have self-updating.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP service account JSON |
| `DISCORD_WEBHOOK` | Discord webhook URL |

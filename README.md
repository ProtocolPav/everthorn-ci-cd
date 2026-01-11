# Everthorn CI/CD

A lightweight CI/CD system for managing microservices deployments using Google Cloud Pub/Sub and Docker Compose. Automatically deploys updated container images and sends real-time notifications to Discord.

## Overview

Everthorn CI/CD listens for deployment messages via Google Cloud Pub/Sub, pulls the latest Docker images, updates running services using Docker Compose, and provides comprehensive Discord notifications with rich embeds showing deployment status, service details, and timestamps.

## Setup

### Prerequisites

- Docker and Docker Compose installed on the host
- Google Cloud Project with Pub/Sub enabled
- Discord webhook URL for notifications

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd everthorn-ci-cd
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Cloud credentials and create a service account with Pub/Sub permissions

4. Create a Discord webhook in your server

### Configuration

This service should be run via Docker Compose to interface with the Docker host.

## ‼️Docker Socket Mount
This is the most important part, and the service will not work without it.

You must mount the Docker Socket from your host system to the local filesystem.

## Environment Variables

Configure these environment variables in your Docker Compose file:

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud service account JSON file
- `DISCORD_WEBHOOK`: Discord webhook URL for deployment notifications

### Example Docker Compose

```yaml
version: '3.8'
services:
  everthorn-cicd:
    build: .
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
      - DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /path/to/credentials.json:/path/to/credentials.json:ro
    restart: unless-stopped
```

## Usage

### Pub/Sub Message Format

Send messages to the `builds-sub` subscription with the following JSON structure:

```json
{
  "compose-name": "my-service",
  "image": "myregistry/my-service:latest"
}
```
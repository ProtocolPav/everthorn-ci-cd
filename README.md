# everthorn-ci-cd
Manages Everthorn's micro services by pulling latest images and restarting containers when needed

This service should be run via Docker Compose, as it interfaces with the docker host.

# Environment Variables
In your Docker Compose file, you must specify these following Environment Variables:
- `GOOGLE_APPLICATION_CREDENTIALS`: Should point to a filepath with your service account
- `DISCORD_WEBHOOK`: The URL of the discord webhook to send notifications to
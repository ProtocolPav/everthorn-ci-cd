import json
import subprocess
import logging

from webhook import send_webhook

logger = logging.getLogger(__name__)

def callback(message):
    """Process received Pub/Sub messages"""
    try:
        # Parse the message
        logger.info(f"Received message: {message.data.decode('utf-8')}")
        message_data = json.loads(message.data.decode('utf-8'))

        compose_name = message_data.get("compose-name")
        image = message_data.get("image")

        if not compose_name:
            logger.error("Missing compose-name in message")
            message.ack()
            return

        logger.info(f"Starting deployment for: {compose_name}")
        logger.info(f"Image: {image}")

        # Send start notification
        send_webhook("start", compose_name, image)

        # Step 1: Pull the compose service
        logger.info("Pulling Docker Compose service...")
        subprocess.run(["sudo", "docker", "compose", "pull", compose_name], check=True)

        # Step 2: Start the service
        logger.info("Starting Docker Compose service...")
        subprocess.run(["sudo", "docker", "compose", "up", compose_name, "-d"], check=True)

        # Step 3: Clean up
        logger.info("Cleaning up unused Docker resources...")
        subprocess.run(["sudo", "docker", "system", "prune", "-f"], check=True)

        # Step 4: Send Discord notification
        send_webhook("success", compose_name, image)

        # Acknowledge the message
        message.ack()
        logger.info(f"Message acknowledged: {message.message_id}")

    except subprocess.CalledProcessError as e:
        send_webhook("failure", compose_name, image, str(e))
        logger.error(f"Command failed: {e}")
        message.nack()

    except Exception as e:
        send_webhook("failure", compose_name, image, str(e))
        logger.error(f"Error processing message: {e}")
        message.nack()
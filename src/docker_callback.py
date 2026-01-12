import json
import logging
import subprocess

from webhook import send_webhook

logger = logging.getLogger(__name__)

def callback(message):
    """
    Processes receives Pub/Sub Messages and updates containers

    :param message:
    :return:
    """
    message_data = json.loads(message.data.decode('utf-8'))

    compose_name = message_data.get("compose-name")
    image = message_data.get("image")

    if not compose_name:
        logger.error(f"Missing compose-name in message {message_data}")
        message.ack()
        return

    try:
        logger.info(f"Starting deployment for: {compose_name}")
        logger.info(f"Image: {image}")

        send_webhook("start", compose_name, image)

        logger.info("Pulling latest Docker image...")
        subprocess.run(["sudo", "docker", "compose", "pull", compose_name], check=True)

        logger.info("Restarting Docker Compose service...")
        subprocess.run(["sudo", "docker", "compose", "up", compose_name, "-d"], check=True)

        logger.info("Pruning the Docker system...")
        subprocess.run(["sudo", "docker", "system", "prune", "-f"], check=True)

        send_webhook("success", compose_name, image)

        # Acknowledge the message
        message.ack()
        logger.info(f"Message acknowledged: {message.message_id}")

    except subprocess.CalledProcessError as e:
        error_message = f"Error: {e}"

        send_webhook("failure", compose_name, image, error_message)
        logger.error(error_message)
        message.nack()
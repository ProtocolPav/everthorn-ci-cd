import json
import logging

from webhook import send_webhook
from python_on_whales import DockerException, docker

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
        docker.compose.pull(compose_name)

        logger.info("Restarting Docker Compose service...")
        docker.compose.up(services=["everthorn-cicd"], detach=True, force_recreate=True)

        logger.info("Pruning the Docker system...")
        docker.system.prune()

        send_webhook("success", compose_name, image)

        # Acknowledge the message
        message.ack()
        logger.info(f"Message acknowledged: {message.message_id}")

    except DockerException as e:
        error_message = f"Docker Exit Code {e.return_code} while running {e.docker_command}. Error: {e.stderr}"

        send_webhook("failure", compose_name, image, error_message)
        logger.error(error_message)
        message.nack()
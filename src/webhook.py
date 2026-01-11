import os
import requests
import datetime
import logging

logger = logging.getLogger(__name__)

def send_webhook(status: str, service: str, image: str, error=None):
    """
    Send a Discord Webhook embed

    :param status: "start", "success", or "failure"
    :param service: the service name
    :param image: the source image
    :param error: error message if failure
    :return:
    """
    try:
        timestamp = datetime.datetime.now().isoformat()

        if status == "start":
            title = "Deployment Started"
            color = int(0x458dff)  # blue
            description = "Found a new update! Starting deployment..."
        elif status == "success":
            title = "Deployment Successful"
            color = int(0x44d059)  # green
            description = "Your service has been updated to the latest version, as specified by the image."
        elif status == "failure":
            title = "Deployment Failed"
            color = int(0xc90d0d)  # red
            description = f"Deployment failed. Error: {error}"
        else:
            raise ValueError("Invalid status")

        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": timestamp,
            "fields": [
                {"name": "📦 Service", "value": f"```{service}```", "inline": True},
                {"name": "📘 Image", "value": f"```{image}```", "inline": True}
            ],
            "footer": {"text": "Everthorn CI/CD"}
        }

        data = {"embeds": [embed]}
        response = requests.post(os.environ["DISCORD_WEBHOOK"], json=data)

        if response.status_code == 204:
            logger.info("Discord notification sent successfully")
        else:
            logger.error(f"Failed to send Discord message: {response.status_code}")
    except Exception as e:
        logger.error(f"Discord webhook error: {e}")
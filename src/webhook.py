import os
import requests
import datetime

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
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

        if status == "start":
            title = "Deployment Started"
            color = 0x0000ff  # blue
            description = "Found a new update! Starting deployment..."
        elif status == "success":
            title = "Deployment Successful"
            color = 0x00ff00  # green
            description = "Deployment completed!"
        elif status == "failure":
            title = "Deployment Failed"
            color = 0xff0000  # red
            description = f"Deployment failed. Error: {error}"
        else:
            raise ValueError("Invalid status")

        embed = {
            "title": title,
            "description": description,
            "color": color,
            "fields": [
                {"name": "Service", "value": service, "inline": True},
                {"name": "Image", "value": image, "inline": True}
            ],
            "footer": {"text": timestamp}
        }

        data = {"embeds": [embed]}
        response = requests.post(os.environ["DISCORD_WEBHOOK"], json=data)
        if response.status_code == 204:
            print("✅ Discord notification sent successfully")
        else:
            print(f"❌ Failed to send Discord message: {response.status_code}")
    except Exception as e:
        print(f"❌ Discord webhook error: {e}")
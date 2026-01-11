def send_webhook(content):
    """
    Send a Discord Webhook message

    :param content:
    :return:
    """
    try:
        data = {"content": content}
        response = requests.post(os.environ["DISCORD_WEBHOOK"], json=data)
        if response.status_code == 204:
            print("✅ Discord notification sent successfully")
        else:
            print(f"❌ Failed to send Discord message: {response.status_code}")
    except Exception as e:
        print(f"❌ Discord webhook error: {e}")
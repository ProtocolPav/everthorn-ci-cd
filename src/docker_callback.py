import json
import subprocess

from webhook import send_webhook

def callback(message):
    """Process received Pub/Sub messages"""
    try:
        # Parse the message
        print(f"📨 Received message: {message.data.decode('utf-8')}")
        message_data = json.loads(message.data.decode('utf-8'))

        compose_name = message_data.get("compose-name")
        image = message_data.get("image")

        if not compose_name:
            print("❌ Missing compose-name in message")
            message.ack()
            return

        print(f"🚀 Starting deployment for: {compose_name}")
        print(f"📦 Image: {image}")

        # Step 1: Pull the compose service
        print("⬇️  Pulling Docker Compose service...")
        subprocess.run(["sudo", "docker", "compose", "pull", compose_name], check=True)

        # Step 2: Start the service
        print("🔄 Starting Docker Compose service...")
        subprocess.run(["sudo", "docker", "compose", "up", compose_name, "-d"], check=True)

        # Step 3: Clean up
        print("🧹 Cleaning up unused Docker resources...")
        subprocess.run(["sudo", "docker", "system", "prune", "-f"], check=True)

        # Step 4: Send Discord notification
        success_message = f"🎉 **Deployment Successful!**\n📦 Service: `{compose_name}`\n🖼️ Image: `{image}`\n⏰ Deployment completed successfully!"
        send_webhook(success_message)

        # Acknowledge the message
        message.ack()
        print(f"✅ Message acknowledged: {message.message_id}")

    except subprocess.CalledProcessError as e:
        error_msg = f"❌ **Deployment Failed!**\n📦 Service: `{compose_name}`\n🚨 Error: `{str(e)}`"
        send_webhook(error_msg)
        print(f"❌ Command failed: {e}")
        message.nack()

    except Exception as e:
        error_msg = f"❌ **Deployment Error!**\n📦 Service: `{compose_name}`\n🚨 Error: `{str(e)}`"
        send_webhook(error_msg)
        print(f"❌ Error processing message: {e}")
        message.nack()
import os
import json

from google.cloud import pubsub
from python_on_whales import docker

from docker_callback import callback
from logging_config import setup_logging

setup_logging()

CREDENTIALS_PATH = "../google-credentials.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

with open(CREDENTIALS_PATH, 'r') as f:
    credentials_data = json.load(f)
    PROJECT_ID = credentials_data["project_id"]

    docker.login(
        server='europe-docker.pkg.dev',
        username='_json_key',
        password=json.dumps(credentials_data)
    )

SUBSCRIPTION_NAME = "builds-sub"

subscriber = pubsub.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)

def main():
    """
    Main subscriber loop for Google Cloud Pub/Sub

    :return:
    """
    # Configure flow control
    flow_control = pubsub.types.FlowControl(max_messages=10)

    # Start listening
    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=callback,
        flow_control=flow_control
    )

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()


if __name__ == "__main__":
    main()
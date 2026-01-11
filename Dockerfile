FROM python:3.13-alpine

# Install Docker CLI - Required for python-on-whales
RUN apk update && apk add --no-cache docker-cli

COPY . /everthorn-ci-cd/

RUN pip install -r /everthorn-ci-cd/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/everthorn-ci-cd/"

WORKDIR /everthorn-ci-cd

CMD ["python", "-u", "src/main.py"]

FROM alpine:latest

WORKDIR /app


# install python and it's requirements
RUN apk add --no-cache python3 py3-pip py3-virtualenv python3-dev libpq bash

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create a virtual env
RUN python3 -m venv venv

# install python requirements
COPY ./build/web/requirements.txt requirements.txt
RUN venv/bin/pip install -r requirements.txt

COPY ./build/web/run_app.sh run_app.sh
RUN chmod +x run_app.sh

COPY ./web .

# run run_app.sh as entry point
ENTRYPOINT [ "/bin/bash", "run_app.sh" ]

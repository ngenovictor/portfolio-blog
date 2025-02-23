FROM python:3.11

WORKDIR /root/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./web .

COPY ./build/web/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./build/web/run_app.sh run_app.sh
RUN chmod +x run_app.sh

# run run_app.sh as entry point
ENTRYPOINT [ "/bin/bash", "run_app.sh" ]

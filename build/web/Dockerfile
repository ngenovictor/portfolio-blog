FROM python:3.11

WORKDIR /root/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./web .

RUN pip install -r requirements.txt

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]

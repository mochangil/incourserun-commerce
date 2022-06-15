FROM python:3.8.11

RUN mkdir /opt/backend
WORKDIR /opt/backend

ADD . /opt/backend/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python manage.py collectstatic --noinput --clear

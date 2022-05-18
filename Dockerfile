FROM python:3.10-slim

WORKDIR /rock_paper_scissors
COPY . .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

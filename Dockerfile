# start from base
# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y \ 
    chromium-browser \ 
    chromium-chromedriver

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

RUN ["chmod", "777", "api/services/chromedriver"]


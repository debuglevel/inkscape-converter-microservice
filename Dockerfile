## Final image
#FROM python:3.9.2-buster
FROM python:3.9.2-slim-buster

RUN apt-get update && apt-get install -y inkscape

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src/ /app/

#RUN mkdir -p /app/temp /app/out /app/data

ENV FLASK_APP=rest.py
CMD [ "flask", "run", "--host=0.0.0.0", "--port=8080" ]

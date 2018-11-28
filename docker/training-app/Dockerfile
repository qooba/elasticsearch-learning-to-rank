FROM python:3

RUN \
    apt update && \
    apt-get -yq install default-jre
RUN mkdir -p /opt/services/flaskapp/src
COPY . /opt/services/flaskapp/src
WORKDIR /opt/services/flaskapp/src
RUN pip install -r requirements.txt
RUN python /opt/services/flaskapp/src/prepare.py
EXPOSE 5090
CMD ["python", "-u", "app.py"]
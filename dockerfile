FROM ubuntu:latest
MAINTAINER Robert Smith "robert.p.smith@nyu.edu"
RUN apt-get update -y
RUN apt-get install -y python3-pip
COPY ./spell /app/spell
COPY ./requirements.txt /app
COPY ./app.py /app
RUN pip3 install -r /app/requirements.txt
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["app.py"]

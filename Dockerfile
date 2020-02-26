FROM python:3.7.3-alpine3.9

LABEL maintainer="sunnydog0826@gmail.com"

ADD . /app

RUN pip3 install /app

WORKDIR /app

ENTRYPOINT ["cms","run"]
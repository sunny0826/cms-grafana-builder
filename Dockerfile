FROM python:3.7.3-alpine3.9

LABEL maintainer="sunnydog0826@gmail.com"

ADD . /app

COPY model /var/local/model

RUN pip3 install /app

ENTRYPOINT ["cmsbuilder"]
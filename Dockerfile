FROM python:3.7.3-alpine3.9

LABEL maintainer="sunnydog0826@gmail.com"



ADD . /app

COPY model /var/local/model

RUN echo "https://mirrors.aliyun.com/alpine/v3.9/main/" > /etc/apk/repositories \
    && apk update \
    && apk add --no-cache gcc g++ python3-dev python-dev linux-headers libffi-dev openssl-dev make \
    && pip3 install /app -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

WORKDIR /app

ENTRYPOINT ["uwsgi","--ini","uwsgi.ini"]
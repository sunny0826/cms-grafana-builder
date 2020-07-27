FROM grafana/grafana

LABEL maintainer="sunnydog0826@gmail.com"

ENV TZ Asia/Shanghai

USER root

RUN echo "https://mirrors.aliyun.com/alpine/v3.11/main/" > /etc/apk/repositories \
&& apk update \
&& apk add --no-cache bash python3 \
gcc g++ python3-dev python-dev linux-headers libffi-dev openssl-dev make tzdata

COPY . /app

RUN pip3 install /app

WORKDIR /app

ENV GF_INSTALL_PLUGINS=farski-blendstat-panel,grafana-simple-json-datasource,https://github.com/sunny0826/aliyun-cms-grafana/archive/master.zip;aliyun-cms-grafana
ENV GF_AUTH_ANONYMOUS_ENABLED=true
ENV GF_AUTH_BASIC_ENABLED=true

RUN mkdir /var/lib/grafana/cms-dashboards \
&& cp -r /app/chart/model/* /var/lib/grafana/cms-dashboards \
&& cp all-in-one/datasources.yaml /etc/grafana/provisioning/datasources/ \
&& cp all-in-one/dashboards.yaml /etc/grafana/provisioning/dashboards/


ENTRYPOINT ["/app/all-in-one/entrypoint.sh"]
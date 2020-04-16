#!/bin/bash

AK=$(printf "%s"${ACCESS_KEY_ID} | base64)
AS=$(printf "%s"${ACCESS_SECRET} | base64)

sed -i "s/#ak/$AK/g" /etc/grafana/provisioning/datasources/datasources.yaml
sed -i "s/#as/$AS/g" /etc/grafana/provisioning/datasources/datasources.yaml

cms refresh

nohup cms run &

/run.sh
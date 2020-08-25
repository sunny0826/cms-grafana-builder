cms-grafana
===========
English | [简体中文](README_CN.md)

![grafana](https://raw.githubusercontent.com/grafana/grafana/master/docs/logo-horizontal.png)

Aliyun CMS Grafana Dashboard

Current chart version is `0.5.1`



## Introduction

This chart helps you run a grafana server that include aliyun cms dashboard.

## Quick Start

You can use the `docker` to experience the full functionality, with this should only be applied to local, production environments please use `helm`.

```bash
docker run -d -p 3000:3000 -e ACCESS_KEY_ID={your_access_key_id} -e ACCESS_SECRET={your_access_secret}  guoxudongdocker/grafana-cms-run:0.5.0
```

## Installing the Chart

### Helm v3

Download `cms-grafana-0.5.0.tgz` package to install in [release](https://github.com/sunny0826/cms-grafana-builder/releases).

To install the chart with the release name `my-release`:

```bash
# start
$ helm install my-release cms-grafana-0.5.0.tgz \
--namespace {your_namespace} \
--set access_key_id={your_access_key_id} \
--set access_secret={your_access_secret} \
--set region_id={your_aliyun_region_id} \
--set password={admin_password}

# set ingress and open tls
helm install my-release cms-grafana-0.5.0.tgz \
--namespace {your_namespace} \
--set access_key_id={your_access_key_id} \
--set access_secret={your_access_secret} \
--set region_id={your_aliyun_region_id} \
--set password={admin_password} \
--set ingress.enabled=true \
--set ingress.hosts[0].host="{your_host}",ingress.hosts[0].paths[0]="/" \
--set ingress.tls[0].secretName="{your_tls_secret_name}",ingress.tls[0].hosts[0]="{your_tls_host}"
```
__Please resolve the DNS to ingress.__

### Viewing the Grafnan dashboard

To do without ingress, you can use `kubectl port-forward`.

```bash
kubectl port-forward -n {your_namespace} deployment/my-release-cms-grafana 8080:8080 &
```

Visit http://localhost:8080 in your web browser.

## Uninstall

To uninstall/delete the `my-release` deployment:

```bash
$ helm uninstall my-release -n {your_namespace}
```



## Chart Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| access_key_id | string | `""` | Aliyun Access Key Id. |
| access_secret | string | `""` | Aliyun Access Secret. |
| affinity | object | `{}` |  |
| anonymous | bool | `false` | grafana auth anonymous enables |
| backend_image.pullPolicy | string | `"Always"` | Init image backend policy. |
| backend_image.repository | string | `"guoxudongdocker/grafana-build"` | Image source repository of backend image. |
| backend_image.tag | string | `"0.5.0"` | Image tag of backend image. |
| backend_resources.limits.cpu | string | `"200m"` |  |
| backend_resources.limits.memory | string | `"256Mi"` |  |
| backend_resources.requests.cpu | string | `"100m"` |  |
| backend_resources.requests.memory | string | `"256Mi"` |  |
| cronjob_image.repository | string | `"guoxudongdocker/curl"` | Image source repository of cronjob image. |
| cronjob_image.tag | string | `"latest"` | Image tag of cronjob image. |
| dashboard | string | `"dashboard,ecs,rds,mongodb,oss,eip,redis,slb"` | module of dashboard |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy. |
| image.repository | string | `"grafana/grafana"` | Image source repository name. |
| ingress.annotations | object | `{}` |  |
| ingress.enabled | bool | `false` | Whether to open ingress. |
| ingress.hosts | list | `[{"host":"grafana.chart-example.local","paths":["/"]}]` | Ingress hosts. |
| ingress.tls | list | `[]` |  |
| init_image.pullPolicy | string | `"Always"` | Init image pull policy. |
| init_image.repository | string | `"guoxudongdocker/cms-grafana-jsonnet"` | Image source repository of init image. |
| init_image.tag | string | `"0.1.0"` | Image tag of init image. |
| nodeSelector | object | `{}` |  |
| password | string | `"admin"` | Grafana admin password. |
| plugins | string | `"farski-blendstat-panel,grafana-simple-json-datasource,yesoreyeram-boomtheme-panel,https://github.com/sunny0826/aliyun-cms-grafana/archive/master.zip;aliyun-cms-grafana"` | Grafana plugin list. |
| region_id | string | `"cn-shanghai"` | Aliyun Region Id. |
| replicaCount | int | `1` | replica count. |
| resources.limits.cpu | string | `"200m"` |  |
| resources.limits.memory | string | `"256Mi"` |  |
| resources.requests.cpu | string | `"100m"` |  |
| resources.requests.memory | string | `"256Mi"` |  |
| schedule | string | `"30 2 * * *"` | CronJob schedule. |
| service.port | int | `80` |  |
| service.type | string | `"ClusterIP"` |  |

### Dashboard

![Dashboard](docs/image/dashboard.png)

### ECS
![ecs](docs/image/ecs.png)

### RDS
![rds](docs/image/rds.png)

### OSS
![oss](docs/image/oss.png)

### SLB

**Layer 4**

![slb](docs/image/slb.png)

**Layer 7**

![slb-7](docs/image/slb-7.png)

### EIP
![eip](docs/image/eip.png)

### Redis
![redis](docs/image/redis.png)

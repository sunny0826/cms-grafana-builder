cms-grafana
===========
[English](README.md) | 简体中文

![grafana](https://raw.githubusercontent.com/grafana/grafana/master/docs/logo-horizontal.png)

Aliyun CMS Grafana Dashboard

Current chart version is `0.4.3`



## 介绍

运行部署 grafana 并展示一整套阿里云监控的仪表盘。

## 快速开始

你可以使用 `docker` 来快速体验全部功能，但这只适用于本地测试，并没有定时刷新资源信息等功能。在生产环境请使用 `helm` 部署。

```bash
docker run -d -p 3000:3000 -e ACCESS_KEY_ID={your_access_key_id} -e ACCESS_SECRET={your_access_secret}  guoxudongdocker/grafana-cms-run:0.4.3
```

## 使用 Helm 安装

### Helm v3

在 [release](https://github.com/sunny0826/cms-grafana-builder/releases) 页面下载 `cms-grafana-0.4.3.tgz` 包。

使用 `my-release` 名称安装：

```bash
# start
$ helm install my-release cms-grafana-0.4.3.tgz \
--namespace {your_namespace} \
--set access_key_id={your_access_key_id} \
--set access_secret={your_access_secret} \
--set region_id={your_aliyun_region_id} \
--set password={admin_password}

# 设置 ingress 和 SSL 证书
helm install my-release cms-grafana-0.4.3.tgz \
--namespace {your_namespace} \
--set access_key_id={your_access_key_id} \
--set access_secret={your_access_secret} \
--set region_id={your_aliyun_region_id} \
--set password={admin_password} \
--set ingress.enabled=true \
--set ingress.hosts[0].host="{your_host}",ingress.hosts[0].paths[0]="/" \
--set ingress.tls[0].secretName="{your_tls_secret_name}",ingress.tls[0].hosts[0]="{your_tls_host}"
```
__请将 DNS 解析到该 ingress。__

### 查看 Grafnan dashboard

如果不想使用 ingress，可以使用 `kubectl port-forward` 命令：

```bash
kubectl port-forward -n {your_namespace} deployment/my-release-cms-grafana 8080:8080 &
```

在浏览器中访问 http://localhost:8080。

## 卸载

```bash
$ helm uninstall my-release -n {your_namespace}
```



## Chart Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| access_key_id | string | `""` | Aliyun Access Key Id. |
| access_secret | string | `""` | Aliyun Access Secret. |
| affinity | object | `{}` |  |
| anonymous | bool | `false` |  |
| backend_image.pullPolicy | string | `"Always"` |  |
| backend_image.repository | string | `"guoxudongdocker/grafana-build"` |  |
| backend_image.tag | string | `"0.5.0"` |  |
| backend_resources.limits.cpu | string | `"200m"` |  |
| backend_resources.limits.memory | string | `"256Mi"` |  |
| backend_resources.requests.cpu | string | `"100m"` |  |
| backend_resources.requests.memory | string | `"256Mi"` |  |
| cronjob_image.repository | string | `"guoxudongdocker/curl"` |  |
| cronjob_image.tag | string | `"latest"` |  |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy. |
| image.repository | string | `"grafana/grafana"` | Image source repository name. |
| ingress.annotations | object | `{}` |  |
| ingress.enabled | bool | `false` | Whether to open ingress. |
| ingress.hosts | list | `[{"host":"grafana.chart-example.local","paths":["/"]}]` | Ingress hosts. |
| ingress.tls | list | `[]` |  |
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

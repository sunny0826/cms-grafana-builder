# cms-grafana-builder

[English](README.md) | 简体中文

![grafana](https://raw.githubusercontent.com/grafana/grafana/master/docs/logo-horizontal.png)

基于开源的监控和可视化组件 grafana，展示阿里云监控数据。

## 介绍

运行部署 grafana 并展示一整套阿里云监控的仪表盘。

## 快速开始

你可以使用 `docker` 来快速体验全部功能，但这只适用于本地测试，并没有定时刷新资源信息等功能。在生产环境请使用 `helm` 部署。

```bash
docker run -d -p 3000:3000 -e ACCESS_KEY_ID={your_access_key_id} -e ACCESS_SECRET={your_access_secret}  guoxudongdocker/grafana-cms-run:0.4.0-release
```

## 使用 Helm 安装

### Helm v3

在 [release](https://github.com/sunny0826/cms-grafana-builder/releases) 页面下载 cms-grafana-0.4.0.tgz 包。

使用 `my-release` 名称安装：

```bash
# start
$ helm install my-release cms-grafana-0.4.0.tgz \
--namespace {your_namespace} \
--set access_key_id={your_access_key_id} \
--set access_secret={your_access_secret} \
--set region_id={your_aliyun_region_id} \
--set password={admin_password}

# 设置 ingress 和 SSL 证书 
helm install my-release cms-grafana-0.4.0.tgz \
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

## 配置

配置参数：

参数                       	 	| 说明                                				| 默认值
------------------------------- | ------------------------------------------------- | ----------------------------------------------------------
`plugins`           	        | Grafana 插件列表。          	            		| `farski-blendstat-panel,grafana-simple-json-datasource,https://github.com/sunny0826/aliyun-cms-grafana/archive/master.zip;aliyun-cms-grafana`
`access_key_id`                	| 阿里云 Access Key Id。                  			| ``
`access_secret`                	| 阿里云 Access Secret。                  			| ``
`region_id`                    	| 阿里云 Region Id。                       			| `cn-shanghai`
`password`                    	| Grafana admin 密码。                      			| `admin`
`schedule`                    	| 定时任务配置。                            			| `"30 2 * * *"`
`image.repository`           	| 镜像 repository 名称。         	            		| `grafana/grafana`
`image.pullPolicy`         		| 镜像拉取策略。                        				| `Always`
`build_image.repository`        | init 镜像。                                  	    | `guoxudongdocker/grafana-build`
`build_image.tag`              	| 镜像 tag。                       		  	    	| `0.2.1-release`
`build_image.pullPolicy`       	| 镜像拉取策略。                          				| `Always`
`backend_image.repository`      | 自定义数据源镜像。                                   | `guoxudongdocker/grafana-build`
`backend_image.tag`             | 镜像 tag。                       		  	    	| `0.2.1-release`
`backend_image.pullPolicy`      | 镜像拉取策略。                          				| `Always`
`ingress.enabled`         		| 是否开启 ingress.                   				| `false`
`ingress.hosts`          		| Ingress hosts.                       				| `[]`

## 截图

### Dashboard

![Dashboard](docs/image/dashboard.png)

### ECS
![ecs](docs/image/ecs.png)

### RDS
![rds](docs/image/rds.png)

### OSS
![oss](docs/image/oss.png)

### SLB

**4层**

![slb](docs/image/slb.png)

**7层**

![slb-7](docs/image/slb-7.png)

### EIP
![eip](docs/image/eip.png)

### Redis
![redis](docs/image/redis.png)


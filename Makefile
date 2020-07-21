.PHONY: run build docker-run package build-all-in-one helm-run helm-install docker-clean

CMS_BUILDER_VERSION=0.4.2
run: export RUN_PORT=8088
run: export ACCESS_KEY_ID=$(PLUGIN_ACCESS_KEY_ID)
run: export ACCESS_SECRET=$(PLUGIN_ACCESS_SECRET)
docker-run: export ACCESS_KEY_ID=$(PLUGIN_ACCESS_KEY_ID)
docker-run: export ACCESS_SECRET=$(PLUGIN_ACCESS_SECRET)
helm-install: export ACCESS_KEY_ID=$(PLUGIN_ACCESS_KEY_ID)
helm-install: export ACCESS_SECRET=$(PLUGIN_ACCESS_SECRET)

build:
	pip install .

run: build
	runner

package:
	helm package chart

build-all-in-one:
	docker build -t grafana-all-in-one -f all-in-one/Dockerfile .

docker-run: build-all-in-one
	docker run -d -p 3000:3000 -e ACCESS_KEY_ID=$(ACCESS_KEY_ID) -e ACCESS_SECRET=$(ACCESS_SECRET) --name=grafana-all-in-one  grafana-all-in-one

docker-clean:
	# stop & remove docker
	docker stop grafana-all-in-one
	docker rm grafana-all-in-one
	# remove docker image
	docker rmi grafana-all-in-one -f

helm-install:
	helm install test chart \
	--set access_key_id=$(ACCESS_KEY_ID) \
	--set access_secret=$(ACCESS_SECRET)

helm-clean:
	# clean helm chart package
	rm -rf cms-grafana-*
	# uninstall helm chart
	helm uninstall test
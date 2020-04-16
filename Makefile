.PHONY: run build run-docker

CMS_BUILDER_VERSION=0.0.2
run: export RUN_PORT=8088
run: export ACCESS_KEY_ID=$(PLUGIN_ACCESS_KEY_ID)
run: export ACCESS_SECRET=$(PLUGIN_ACCESS_SECRET)
run-docker: export ACCESS_KEY_ID=$(PLUGIN_ACCESS_KEY_ID)
run-docker: export ACCESS_SECRET=$(PLUGIN_ACCESS_SECRET)

build:
	pip install .

run: build
	runner

build-all-in-one:
	docker build -t grafana-all-in-one -f all-in-one/Dockerfile .

run-docker:
	docker run -d -p 3000:3000 -e ACCESS_KEY_ID=$ACCESS_KEY_ID -e ACCESS_SECRET=$ACCESS_SECRET  grafana-all-in-one
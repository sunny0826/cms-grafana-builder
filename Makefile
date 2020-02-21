.PHONY: run build

CMS_BUILDER_VERSION=0.0.2
run: export RUN_PORT=8088
run: export ACCESS_KEY_ID=$(PLUGIN_ACCESS_KEY_ID)
run: export ACCESS_SECRET=$(PLUGIN_ACCESS_SECRET)

build:
	pip install .

run: build
	runner
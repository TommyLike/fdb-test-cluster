BOLD=$(shell tput bold)
ERROR=$(shell tput setaf 1)
RESET=$(shell tput sgr0)

build: ## Build FDB AMI with Packer
	@packer build packer_fdb.json

build_influxdb: ## Build FDB AMI with Packer
	@packer build packer_influx.json


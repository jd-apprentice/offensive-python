script_name ?= ports

all: script

script:
	@python3 scripts/$(script_name).py

.PHONY: script
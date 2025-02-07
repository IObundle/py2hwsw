# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

DOCKERFILE = Dockerfile
DOCKER_IMAGE = iob-py2
CONTAINER = iob-py2-container

build: $(DOCKERFILE)
	docker build . -t $(DOCKER_IMAGE)

run:
	# remove container if it exists
	docker rm $(CONTAINER)
	docker run --name $(CONTAINER) \
		-it \
		$(DOCKER_IMAGE)
		

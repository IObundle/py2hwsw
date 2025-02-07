<!--
SPDX-FileCopyrightText: 2025 IObundle

SPDX-License-Identifier: MIT
-->

# Py2HWSW Docker Images
Build a clean environment to test the Py2HWSW project.

## Prerequisites
- Install [Docker](https://docs.docker.com/engine/install/)

## Build image
Currently, the `Dockerfile` builds:
- a docker image based on Ubuntu 22.04 
- installs the nix package manager
- install py2hwsw depencencies in `py2hwsw/py2hwsw/lib/default.nix`
The default user is `iobdev` with sudo permissions.

Build the image with:
```bash
make build
```

## Run Docker Image
Run the docker image in interactive mode with:
```bash
make run
```
- Clone repositories and run as normal. For example:
```bash
git clone https://github.com/iobundle/iob-soc.git
cd iob-soc
make sim-run
# NOTE: dependencies take some time to install the 1st time
```

## Images in Github Container Registry
- The `docker-image.yml` workflow builds and publishes the docker image on each
  release
- To pull and run the docker image:
```bash
# pull latest version
docker run ghcr.io/iobundle/py2hwsw:latest
# pull specific <tag>
docker run ghcr.io/iobundle/py2hwsw:<tag>
```

## Other usefull commands
- Cleanup old docker images: `docker image prune`
- Check existing images: `docker images`

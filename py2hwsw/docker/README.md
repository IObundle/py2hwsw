<!--
SPDX-FileCopyrightText: 2024 IObundle

SPDX-License-Identifier: MIT
-->

# Py2HWSW Docker Images
Build a clean environment to test the Py2HWSW project.

## Prerequisites
- Install [Docker](https://docs.docker.com/engine/install/)

## Build image
Currently, the `Dockerfile` builds a docker image based on Ubuntu 22.04 and
installs the nix package manager.
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

## Other usefull commands
- Cleanup old docker images: `docker image prune`
- Check existing images: `docker images`

## TODO
- build and store images
    - Seems to be possible to store and manage Docker Images with [Github's
      Container
      registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- image with pre-installed nix dependencies?

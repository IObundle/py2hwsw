FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y locales ca-certificates curl \
    sudo xz-utils git && \
    apt-get clean

# Setup build users https://nix.dev/manual/nix/2.18/installation/multi-user
RUN groupadd -r nixbld 
RUN for n in $(seq 1 10); do useradd -c "Nix build user $n" \
    -d /var/empty -g nixbld -G nixbld -M -N -r -s "$(command -v nologin)" \
    "nixbld$n"; done

# Set up a non-root user for Nix
RUN useradd -m -s /bin/bash iobdev && \
    echo "iobdev ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch user
USER iobdev
ENV USER=iobdev
WORKDIR /home/iobdev

RUN sudo mkdir -m 0755 /nix && sudo chown iobdev /nix

# Install nix package manager
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN set -o pipefail && curl -L https://nixos.org/nix/install | bash

# Add the 'source nix.sh' command to .bashrc so it's sourced
# with every new bash session  that can be invoked via docker exec -it
RUN echo "source $HOME/.nix-profile/etc/profile.d/nix.sh" >> "$HOME/.bashrc"

#
# TODO: Install Py2HWSW Dependencies?
#
# RUN git clone https://github.com/IObundle/py2hwsw.git
# RUN cd pyhwsw/py2hwsw/lib && nix-shell --run "echo 'Dependencies Installed'"

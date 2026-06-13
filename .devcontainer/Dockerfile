# Base image: Amazon Linux 2023 (same as AWS environment)
FROM amazonlinux:2023

# Metadata
LABEL description="Claude Code Development Environment for Book Shelf Project (Amazon Linux 2023)"

# Install development tools, Python, and MariaDB dev libraries
RUN dnf update -y \
    && dnf install -y \
    git \
    vim \
    tar \
    gzip \
    python3 \
    python3-pip \
    python3-devel \
    sudo \
    && dnf clean all \
    && rm -rf /var/cache/dnf

# Create symlink for python
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Create developer user (vscode compatible)
RUN useradd -ms /bin/bash vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode
USER vscode

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/home/vscode/.local/bin:$PATH"

WORKDIR /workspaces
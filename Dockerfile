FROM python:3.13-slim

ARG TERRAFORM_VERSION=1.10.5
ARG SCALR_CLI_VERSION=0.17.7
ARG TARGETARCH

# System deps: graphviz, build tools, git, curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        graphviz libgraphviz-dev gcc libc6-dev git curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Install Terraform CLI
RUN ARCH="${TARGETARCH:-$(dpkg --print-architecture)}" && \
    curl -fsSL "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${ARCH}.zip" \
        -o /tmp/terraform.zip && \
    unzip /tmp/terraform.zip -d /usr/local/bin/ && \
    rm /tmp/terraform.zip

# Install Scalr CLI
RUN ARCH="${TARGETARCH:-$(dpkg --print-architecture)}" && \
    curl -fsSL "https://github.com/Scalr/scalr-cli/releases/download/v${SCALR_CLI_VERSION}/scalr-cli_${SCALR_CLI_VERSION}_linux_${ARCH}.zip" \
        -o /tmp/scalr-cli.zip && \
    unzip /tmp/scalr-cli.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/scalr && \
    rm /tmp/scalr-cli.zip

# Install terravision and Python dependencies
COPY . /opt/terravision
RUN cd /opt/terravision && pip install --no-cache-dir --break-system-packages .

# Copy entrypoint
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

RUN mkdir -p /workspace
WORKDIR /workspace

ENTRYPOINT ["entrypoint.sh"]

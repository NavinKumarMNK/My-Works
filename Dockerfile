# Use an official Ubuntu 22.04 LTS as a base image
FROM ubuntu:22.04 as base
ARG DEBIAN_FRONTEND=noninteractive

# Update the system and install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    software-properties-common

# Stage for installing and setting GCC 13 as default
FROM base as gcc-install
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test
RUN apt-get install -y gcc-13 g++-13

# Stage for Clang 17 installation
FROM base as clang-install
RUN wget -O - https://apt.llvm.org/llvm.sh | bash -s -- -v 19

# Stage for Rust installation
FROM base as rust-install
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Stage for Go installation
FROM base as go-install
ARG GO_URL=https://go.dev/dl/go1.22.2.linux-amd64.tar.gz
RUN wget -O go.tar.gz $GO_URL
RUN tar -xvf go.tar.gz
RUN mv go /usr/local

# Stage for Node.js installation
FROM base as node-install
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install 20

# Stage for python3 installation
FROM base as python-install
RUN apt-get install -y python3 python3-pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Final stage to gather all languages
FROM base
COPY --from=gcc-install /usr/bin/gcc-13 /usr/bin/gcc-13
COPY --from=gcc-install /usr/bin/g++-13 /usr/bin/g++-13
COPY --from=clang-install /usr/lib/llvm-18 /usr/lib/llvm-18
COPY --from=rust-install /root/.cargo /root/.cargo
COPY --from=go-install /usr/local/go /usr/local/go
COPY --from=node-install /root/.nvm /root/.nvm
COPY --from=python-install /usr/local /usr/local

ENV GOROOT=/usr/local/go
ENV GOPATH=$HOME/go
ENV PATH=$GOPATH/bin:$GOROOT/bin:$PATH
ENV PATH=/usr/lib/llvm-18/bin:$PATH
ENV PATH=/root/.cargo/bin:${PATH}
ENV NVM_DIR=/root/.nvm
ENV PATH=$NVM_DIR/versions/node/v20.12.2/bin:$PATH

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 10 --slave /usr/bin/g++ g++ /usr/bin/g++-13
RUN rustup default stable
RUN apt-get install vim
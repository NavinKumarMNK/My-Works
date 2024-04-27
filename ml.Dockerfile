FROM nvcr.io/nvidia/pytorch:24.03-py3
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    vim 

RUN pip install --upgrade pip && pip install -r requirements.txt

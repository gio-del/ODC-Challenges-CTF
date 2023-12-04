FROM ubuntu:21.04

RUN apt-get update && \
    apt-get install -y socat && \
    apt-get clean	

# Add non-root user
RUN adduser --home /chall --no-create-home --disabled-password --gecos '' chall

WORKDIR /chall

USER chall

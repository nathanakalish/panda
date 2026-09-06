FROM ubuntu:24.04

ENV WORKDIR=/tmp/panda/
ENV PYTHONUNBUFFERED=1
ENV PATH="$WORKDIR/.venv/bin:$PATH"

WORKDIR $WORKDIR

# deps install
COPY pyproject.toml setup.py packaging_backend.py setup.sh $WORKDIR
RUN mkdir -p $WORKDIR/panda/ && touch $WORKDIR/panda/__init__.py
RUN apt-get update && apt-get install -y --no-install-recommends sudo && DEBIAN_FRONTEND=noninteractive $WORKDIR/setup.sh

# refresh development tool dependencies
ARG CACHEBUST=1
RUN DEBIAN_FRONTEND=noninteractive $WORKDIR/setup.sh

RUN git config --global --add safe.directory $WORKDIR/panda
COPY . $WORKDIR

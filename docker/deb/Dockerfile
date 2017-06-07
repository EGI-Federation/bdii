# Docker image for building deb packages
FROM ubuntu:xenial
MAINTAINER Baptiste Grenier <baptiste.grenier@egi.eu>

ENV DEBIAN_FRONTEND noninteractive
ENV DEBIAN_PRIORITY critical
ENV DEBCONF_NOWARNINGS yes

# Install build tools
COPY 80-acquire-retries /etc/apt/apt.conf.d/
RUN apt-get -y update
RUN apt-get -o "Dpkg::Options::=--force-confnew" -y dist-upgrade
RUN apt-get -y --no-install-recommends install build-essential devscripts debhelper
RUN apt-get -y --no-install-recommends install rsync
RUN apt-get -y --no-install-recommends install python-support

VOLUME /output

COPY build-deb /root

ENTRYPOINT /root/build-deb

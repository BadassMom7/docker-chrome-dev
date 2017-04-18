FROM ubuntu:17.04
WORKDIR /tmp
RUN apt-get update
RUN apt-get install -y wget
RUN wget https://dl.google.com/linux/direct/google-chrome-unstable_current_amd64.deb
RUN dpkg -i google-chrome-unstable_current_amd64.deb; apt-get install -f -y --no-install-recommends
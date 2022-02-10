FROM ubuntu
MAINTAINER Kevin Hester <kevinh@geeksville.com>

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install --no-install-recommends gnome-builder x11vnc fluxbox sudo vim xvfb xdotool x11-utils xterm python3 python3-pip
COPY set_display.sh /root/set_display.sh

EXPOSE 5900
CMD ["/bin/bash", "--login", "-c", "/root/set_display.sh"]

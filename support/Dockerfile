FROM ubuntu
MAINTAINER Kevin Hester <kevinh@geeksville.com>

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install --no-install-recommends gnome-builder x11vnc fluxbox sudo vim xvfb xdotool x11-utils xterm
RUN useradd -rm -d /home/mesh -s /bin/bash -g root -G sudo -u 1001 mesh
COPY set_display.sh /home/mesh/set_display.sh

# Expose SSH and VNC when installed.
EXPOSE 22 5900

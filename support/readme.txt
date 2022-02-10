Dockerfiles for testing

To build:
	docker build -t meshtastic/gnome-builder .


docker run -ti --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix meshtastic/gnome-builder
chmod 1777 /tmp/.X11-unix
source /home/mesh/set_display.sh
set_display

# now you should be able to VNC to the docker instance

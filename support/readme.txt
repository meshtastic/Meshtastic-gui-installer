Dockerfiles for testing

docker build -t meshtastic/gnome-builder .

docker run -d --rm -v /tmp/.X11-unix:/tmp/.X11-unix -p 5900:5900 meshtastic/gnome-builder

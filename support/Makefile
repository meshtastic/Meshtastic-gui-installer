create:
	for tag in "20.04" "21.04" "22.04" ; do \
		cat _Dockerfile.ubuntu | sed "s/.*TAG/FROM ubuntu:$$tag/" > ubuntu.$$tag ; \
	done

build:
	for file in $$(ls ubuntu*); do \
		echo $$file ; \
		echo "About to run this: docker build -t meshtastic/$$file -f $$file ." ; \
		docker build -t meshtastic/$$file -f $$file . ; \
	done

run:
	docker run -d --rm -v /tmp/.X11-unix:/tmp/.X11-unix -p 5920:5900 --name ubuntu.20.04 meshtastic/ubuntu.20.04
	docker run -d --rm -v /tmp/.X11-unix:/tmp/.X11-unix -p 5921:5900 --name ubuntu.21.04 meshtastic/ubuntu.21.04
	docker run -d --rm -v /tmp/.X11-unix:/tmp/.X11-unix -p 5922:5900 --name ubuntu.22.04 meshtastic/ubuntu.22.04

clean:
	for file in $$(ls ubuntu*); do \
		echo "docker kill $$file" ; \
		docker kill $$file ; \
	done
	rm ubuntu*

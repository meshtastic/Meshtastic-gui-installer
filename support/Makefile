create:
	for tag in "20.04" "21.04" ; do \
		cat _Dockerfile.ubuntu | sed "s/.*TAG/FROM ubuntu:$$tag/" > ubuntu.$$tag ; \
	done

build:
	for file in $$(ls ubuntu*); do \
		echo $$file ; \
		docker build -t meshtastic/$$file -f $$file . ; \
	done

run:
	docker run -d --rm -v /tmp/.X11-unix:/tmp/.X11-unix -p 5900:5900 meshtastic/ubuntu.20.04

clean:
	rm ubuntu*
	# docker ps -a
	# docker kill

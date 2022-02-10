create:
	for tag in "18.04" "20.04" "21.04" "22.04" ; do \
		cat _Dockerfile.ubuntu | sed "s/.*TAG/FROM ubuntu:$$tag/" > ubuntu.$$tag ; \
	done

build:
	for file in $$(ls ubuntu*); do \
		echo $$file ; \
		echo "About to run this: docker build -t meshtastic/$$file -f $$file ." ; \
		docker build -t meshtastic/$$file -f $$file . ; \
	done

run_u2004:
	docker run -d --rm -v /tmp/.X11-unix:/tmp/.X11-unix -p 5900:5900 meshtastic/ubuntu.20.04

run_u2104:
	docker run -d --rm -v /tmp/.X11-unix:/tmp/.X11-unix -p 5900:5900 meshtastic/ubuntu.21.04

run_u2204:
	docker run -d --rm -v /tmp/.X11-unix:/tmp/.X11-unix -p 5900:5900 meshtastic/ubuntu.22.04

clean:
	rm ubuntu*
	# docker ps -a
	# docker kill

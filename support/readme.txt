Dockerfiles for testing

Note: Used snippets from https://stackoverflow.com/questions/36221215/using-vncserver-gui-application-virtual-display-in-docker-container

# This will build Ubuntu docker images for testing

make create
make build
make run
	# if you want to ssh to the running container
	docker exec -it ubuntu.18.04 /bin/bash

	# if you want to run commands
	docker exec -it ubuntu.18.04 /bin/bash -c "pip3 install --upgrade pip"

make test
	# now vnc to each one, close the warning about the missing fonts,
        # right click, "Applications", "Shells", "Bash"
	# cd Meshtastic-gui-installer
	# make test
	# Note: Ubuntu 18.04 does not have pyside6, so it is not supported

make clean

Dockerfiles for testing

Notes:
 1) Used snippets from https://stackoverflow.com/questions/36221215/using-vncserver-gui-application-virtual-display-in-docker-container
 2) This will not work on an arm-based host (like a Mac Air)

# This will build Ubuntu docker images for testing

docker system prune

make create
make build
make run
	# if you want to ssh to the running container
	docker exec -it ubuntu.20.04 /bin/bash

	# if you want to run commands
	docker exec -it ubuntu.20.04 /bin/bash -c "pip install --upgrade pip"

To test:
	# vnc to each one, right click, "Applications", "Shells", "Bash"
	# cd Meshtastic-gui-installer
	# make test

make clean

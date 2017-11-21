#!/bin/sh



if ! pgrep "python3" >/dev/null

then
        echo "Server not running. Now starting."
     	cd /home
	python3 /home/server.py >> /home/server.log 2>&1 &
	disown

fi


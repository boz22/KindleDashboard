#!/bin/bash

for file in ./*; do
	f="$(basename -- $file)"
	if [ $f == "env" ] || [ $f == "__pycache__" ] || [ $f == "tests" ]; then
  		echo "Skipping some folders"
	else
		if [[ -d $file ]]; then
			scp -r $file pi@rasp.local:/home/pi/KindleDashboard/	
		else
			scp $file pi@rasp.local:/home/pi/KindleDashboard/
		fi
	fi
	
done

#Running this each time takes some time. THis is only needed when new requirements are added. Perhaps it is not the best place
# to run it here.
#ssh pi@rasp.local 'cd /home/pi/KindleDashboard && pip3 install -r requirements.txt'

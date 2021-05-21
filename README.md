Make a new system for WaaromZoMoeilijk.

You need:
- raspberry pi (rpi), SD card >= 8Gb
- latest debian-lite from raspberry.org
- software to copy the image.

The planning is to use DietPy but this is not tested yet.

Copy the debian to the SD card.
Add a file on the SD card "ssh", without ".txt".

Put the SD card in the rpi and power it up.

Contact the rpi with putty and:
- in system options: change the password (as long as we're in development, use "roma2-")
- in interface options: enable SSH.

enter the next as one line:

wget https://github.com/timmeh1955/aaa/blob/052e2d017bf7048106c4b9ab27f6713844e96d7a/m.py?raw=true client.py -O client.py && python client.py

Take a coffee or two.

end.
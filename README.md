# raspi
Scripts and stuff for my RaspberryPi


## Developing
### sshfs

`sshfs -o idmap=user pi@192.168.10.50:/home/pi/ raspi_gh/`

`sshfs -o idmap=user pi@192.168.10.45:/home/pi/ raspi_mokinhenki/`


### Script autostart
Add lines to `/etc/rc.local`, e.g.:

`python /home/pi/code/raspi/thingspeak/mokinhenki/mokinhenki.py &`

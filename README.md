# kiosk
Embedded code for a self-checkout kiosk halloween costume

## Raspberry Pi Setup Steps
* Download stretch-lite image.
* Install display software with `sudo apt install raspberrypi-ui-mods`.
* `sudo apt install git`
* Install LCD driver `git clone https://github.com/goodtft/LCD-show.git`
* `sudo apt install omxplayer`.
* For pygame to work: `sudo apt-get install libsdl1.2debian libsdl-image1.2 libsdl-mixer1.2 libsdl-mixer1.2-dev libsdl-net1.2 libsdl-net1.2-dev timidity.`.

* `pip3 install pipenv`
* For USB printer to work, follow udev seup procedure [here](https://python-escpos.readthedocs.io/en/latest/user/installation.html)
	* NOTE: trigger new permissions with `sudo udevadm trigger`
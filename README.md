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

* If installing pre-release escpos with `pipenv install python-escpos --pre`, need to install development 

Getting the barcode scanner and magstripe to work
* `sudo vi /etc/udev/rules.d/99-pyusb.rules`
	* `SUBSYSTEM=="usb", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="e5e3", MODE="0664", GROUP="dialout"`
	* `SUBSYSTEM=="usb", ATTRS{idVendor}=="0801", ATTRS{idProduct}=="0001", MODE="0664", GROUP="dialout"`
	* Matches the Vendor ID and Device ID for the barcode scanner, with MODE such that owner and group can rw, everyone else can read.
	* Puts device in dialout group, can check that pi is in that group (from receipt printer setup) with `groups` bash command.
* `sudo udevadm trigger`
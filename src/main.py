import threading
import time
from enum import Enum
from random import randint

from light_service import LightService
from printer_service import Receipt, Item
from scanner_service import BarcodeScanner
from sound_service import SoundPlayer
from display_service import Display

from escpos.printer import Usb

# lights = LightService()
# scanner = BarcodeScanner()
# printer = Usb(0x04b8, 0x0202)
# receipt = Receipt(printer)
player = SoundPlayer()
display = Display(player)


def run_light_service():
	while(True):
		lights.run()

		time.sleep(0.01)

def run_scanner_service():
	while(True):
		code = scanner.run()
		if code is not "":
			stripped_code = code.strip()
			print(stripped_code)
			receipt.add_item(Item(stripped_code, randint(0, 10)))
			if "093573356025" in stripped_code:
				receipt.print()
				receipt.clear()


def main():
	print(display.keypad())
	
	light_service_thread = threading.Thread(target=run_light_service, daemon=True)
	light_service_thread.start()

	scanner_service_thread = threading.Thread(target=run_scanner_service, daemon=True)
	scanner_service_thread.start()


	while(True):
		lights.set_light_tower_state(LightService.Color.RED, LightService.State.FLASHING)
		time.sleep(5)
		lights.set_light_tower_state(LightService.Color.RED, LightService.State.ON)
		time.sleep(5)

	# player = SoundPlayer()
	# for i in range(100, 1000):
	# 	player.say_number(i)

	# for i in range(43):
	# 	player.play_track("track" + str(i))

	# scanner = BarcodeScanner()
	# while True:
	# 	code = scanner.run()
	# 	if code is not "":
	# 		print(code.strip())

	# printer = Usb(0x04b8, 0x0202)

	# receipt = Receipt(printer)
	# lights = LightService()

	lights.set_light_tower_state(LightService.Color.RED, LightService.State.FLASHING)
	lights.set_light_tower_state(LightService.Color.GREEN, LightService.State.ON)
	lights.set_light_tower_state(LightService.Color.YELLOW, LightService.State.ON)

	# receipt.add_item(Item("bear", 5))
	# receipt.add_item(Item("poo", 4.50))
	# receipt.print()

	while True:
		lights.run()

if __name__ == '__main__':
	main()
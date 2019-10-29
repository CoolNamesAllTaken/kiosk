import threading
import time
from enum import Enum
from random import randint

from event_service import EventListener
from light_service import LightService
from printer_service import Receipt, Item
from scanner_service import BarcodeScanner
from sound_service import SoundPlayer
from display_service import Display

from escpos.printer import Usb

unicode_to_track_map = {
	" ": "beep",
	"q": "track01",
	"w": "track11",
	"e": "track12",
	"r": "track13",
	"t": "track14",
	"a": "track21",
	"s": "track22",
	"d": "track23",
	"f": "track24",
	"g": "track25"
}

event_listener = EventListener()
lights = LightService()
scanner = BarcodeScanner()
printer = Usb(0x04b8, 0x0202)
receipt = Receipt(printer)
sound_player = SoundPlayer()
display = Display(event_listener, sound_player)

class PosState(Enum):
	GREETING 		= 0,
	ITEM_SCANNING 	= 1,
	PAYMENT 		= 2,
	FAREWELL 		= 3,
	ERROR 			= 4

state = PosState.GREETING

def run_light_service():
	while True:
		lights.run()

		time.sleep(0.01)

def run_scanner_service():
	while True:
		code = scanner.run()
		if code != "":
			sound_player.play_track("beep") # beep when item is scanned
			stripped_code = code.strip()
			print(stripped_code)
			price_dollars = randint(0, 10)
			price_cents = randint(10, 99)
			receipt.add_item(Item(stripped_code, price_dollars + price_cents / 100))
			sound_player.say_number(price_dollars)
			sound_player.say_number(price_cents)
			if "093573356025" in stripped_code:
				receipt.print()
				receipt.clear()

def run_sound_service():
	while True:
		key_events = event_listener.get_key_events()
		for key in key_events:
			key_code = key.unicode
			if (key_code in unicode_to_track_map.keys()):
				# valid key was pressed
				sound_player.play_track(unicode_to_track_map[key_code])


def run_event_service():
	while True:
		event_listener.run()

def main():

	light_service_thread = threading.Thread(target=run_light_service, daemon=True)
	light_service_thread.start()

	# COMMENT OUT THESE TWO LINES TO AVOID TEXT BARF ON ERR
	scanner_service_thread = threading.Thread(target=run_scanner_service, daemon=True)
	scanner_service_thread.start()

	event_listener_thread = threading.Thread(target=run_event_service, daemon=True)
	event_listener_thread.start()

	sound_service_thread = threading.Thread(target=run_sound_service, daemon=True)
	sound_service_thread.start()

	print(display.keypad())


	while(True):
		# set the lights
		if state == PosState.GREETING:
			lights.light_tower_state_list = [LightService.State.OFF, LightService.State.OFF, LightService.State.ON]
			sound_player.play_track("track01"); # "Welcome, please scan your first item"
			while len(receipt.item_list) is 0:
				time.sleep(0.1)
		elif state == PosState.ITEM_SCANNING:
			lights.light_tower_state_list = [LightService.State.OFF, LightService.State.ON, LightService.State.OFF]
		elif state == PosState.PAYMENT:
			lights.light_tower_state_list = [LightService.State.OFF, LightService.State.ON, LightService.State.OFF]
		elif state == PosState.FAREWELL:
			lights.light_tower_state_list = [LightService.State.OFF, LightService.State.OFF, LightService.State.ON]
		else: # error state
			lights.light_tower_state_list = [LightService.State.FLASHING, LightService.State.OFF, LightService.State.OFF]
			pass

		# lights.set_light_tower_state(LightService.Color.RED, LightService.State.FLASHING)
		# time.sleep(5)
		# lights.set_light_tower_state(LightService.Color.RED, LightService.State.ON)
		# time.sleep(5)

	# sound_player = SoundPlayer()
	# for i in range(100, 1000):
	# 	sound_player.say_number(i)

	# for i in range(43):
	# 	sound_player.play_track("track" + str(i))

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
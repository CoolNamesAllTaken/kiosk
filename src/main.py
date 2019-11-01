import threading
import time
from enum import Enum
import random

from event_service import EventListener
from light_service import LightService
from printer_service import Receipt, Item
from scanner_service import UsbScanner
from sound_service import SoundPlayer
from display_service import Display

from escpos.printer import Usb

UNLOCK_STRING = "1234"
RAND_ITEMS_LIST = ["none pizza with left beef", "streamed broccoli", "cows and cows and cows", "smoked meats",
 "pen-pinapple-apple pen", "spiced autumn pumpkin whipped iced cioccolocino", "semechki, blyat", "receipt paper",
 "haggis", "durian", "dragonfruit", "lutefisk", "unicornfruit", "fermented shark", "mot schutzen", "stolly", "chu-mat",
 "Karoun yogurt milk drink", "grocery", "perfectly generic object", "unidentified item", "ice cold determination", 
 "marshmallows", "horse fibers", "P. Sherman 42 Wallaby Way, Sydney", "help", "́ű̡̝̹̝̮͉ͨͥ̎̒̇ͤn̞̺ͤ̇ ͙ͮi̜̜̿̉͛ͧ̾ ̗͚̦̖͖ͩ̏ͣͥͅd͎̩̙͚͕͊ͨ͒̊͌ͬͮ̕ͅ ̡͈͚͉͐͐̑̂͌̊̚e̠͖̝ͭͤ͆ͪ̓ ͍̬̠̗ͭ́̽ͫ͟ñ̞͚̭͕̙ ̛̮̯̟̞̥̪͗͗ͤ̚ͅt̝̠̳͊̇͂̌͊̄ͮ̀ ͓͇̪̮̗ͬ̒̓͟ȉͩ͂ͪͤ̀͏͖̘̩̥͙̬ͅ ̬̖̰f͗ͫ͜ ̞͎͙̗̳̖̙ ̦̘́i̥̗̞̭ͫͦͮ͛ͭe̲͉̰̫̬̽ͤ̿̓ͤ͒̋͠ ͉̣̯̩̻̟̾̒͊͘ͅd̛́ͩ͑̾", 
 "carrot", "one (1) milk"]

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
	"g": "track25",
	"z": "track31",
	"x": "track32",
	"c": "track33",
	"v": "track34",
	"1": "track41",
	"2": "track42",
	"3": "track43",
	"0": "cena"
}

event_listener = EventListener()
lights = LightService()
barcode_scanner = UsbScanner(vendor_id = 0x1234, product_id = 0x5678)
# magstripe_scanner = UsbScanner(vendor_id = 0x0801, product_id = 0x0001)
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

def add_random_item(item_name):
	sound_player.play_track("beep") # beep when item is scanned
	price_dollars = random.randint(0, 10)
	price_cents = random.randint(10, 99)
	receipt.add_item(Item(item_name, price_dollars + price_cents / 100))
	sound_player.say_number(price_dollars)
	sound_player.say_number(price_cents)
	if random.randint(0, 2) == 1:
		sound_player.play_track(random.choice(["track11", "track14"])) # move item to bag

def run_light_service():
	while True:
		lights.run()

		time.sleep(0.01)

def run_scanner_service():
	while True:
		barcode = barcode_scanner.run()
		if barcode != "":
			stripped_barcode = barcode.strip()
			print(stripped_barcode)
			add_random_item(stripped_barcode)

		# magcode = magstripe_scanner.run()
		# if magcode != "":
		# 	display.keypad()

def run_control_service():
	global state
	while True:
		key_events = event_listener.get_key_events()
		for key in key_events:
			key_code = key.unicode
			if key_code in unicode_to_track_map.keys():
				# valid sound key was pressed
				sound_player.play_track(unicode_to_track_map[key_code])
			elif key_code == "`":
				# add item key was pressed
				add_random_item(random.choice(RAND_ITEMS_LIST))
			elif key_code == "j":
				# throw an error
				sound_player.play_track(random.choice(["track41", "track42", "track43"]))
				state = PosState.ERROR

def run_event_service():
	while True:
		event_listener.run()

def main():
	global state

	light_service_thread = threading.Thread(target=run_light_service, daemon=True)
	light_service_thread.start()

	# COMMENT OUT THESE TWO LINES TO AVOID TEXT BARF ON ERR
	scanner_service_thread = threading.Thread(target=run_scanner_service, daemon=True)
	scanner_service_thread.start()

	event_listener_thread = threading.Thread(target=run_event_service, daemon=True)
	event_listener_thread.start()

	event_control_thread = threading.Thread(target=run_control_service, daemon=True)
	event_control_thread.start()



	while(True):
		# set the lights
		if state == PosState.GREETING:
			display.message("Welcome")
			lights.light_tower_state_list = [LightService.State.OFF, LightService.State.OFF, LightService.State.ON]
			sound_player.play_track("track01"); # "Welcome, please scan your first item"
			while len(receipt.item_list) is 0:
				time.sleep(0.1)
			state = PosState.ITEM_SCANNING
		elif state == PosState.ITEM_SCANNING:
			lights.light_tower_state_list = [LightService.State.OFF, LightService.State.ON, LightService.State.OFF]
			button_val = display.receipt(receipt)
			if button_val == 1:
				state = PosState.PAYMENT
			
		elif state == PosState.PAYMENT:
			lights.light_tower_state_list = [LightService.State.OFF, LightService.State.ON, LightService.State.OFF]
			sound_player.play_track("track25") # how many bags
			num_bags = display.keypad()
			if num_bags == "":
				num_bags = "0"
			bags_item = Item("Bags", 0.25 * float(num_bags))
			sound_player.play_track("track32") # thanks for shopping
			receipt.add_item(bags_item)
			receipt.print()
			receipt.clear()
			sound_player.play_track("track34") # remove all bagged items
			state = PosState.FAREWELL
		elif state == PosState.FAREWELL:
			display.message("Goodbye!")
			lights.light_tower_state_list = [LightService.State.OFF, LightService.State.OFF, LightService.State.ON]
			sound_player.play_track("track33") # fast fun convenient
			event_listener.get_mouse_events() # flush clicks
			state = PosState.GREETING
		else: # error state
			lights.light_tower_state_list = [LightService.State.FLASHING, LightService.State.OFF, LightService.State.OFF]
			keycode = display.keypad()
			if keycode == UNLOCK_STRING:
				state = PosState.ITEM_SCANNING
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

	# barcode_scanner = UsbScanner()
	# while True:
	# 	code = barcode_scanner.run()
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

if __name__ == '__main__':
	main()
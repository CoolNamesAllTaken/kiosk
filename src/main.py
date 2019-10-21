from enum import Enum

from light_service import LightService
from printer_service import Receipt, Item

from escpos.printer import Usb

def main():
	printer = Usb(0x04b8, 0x0202)

	receipt = Receipt(printer)
	lights = LightService()

	lights.set_state(LightService.Color.RED, LightService.State.FLASHING)
	lights.set_state(LightService.Color.GREEN, LightService.State.ON)
	lights.set_state(LightService.Color.YELLOW, LightService.State.ON)

	receipt.add_item(Item("bear", 5))
	receipt.add_item(Item("poo", 4.50))
	receipt.print()

	while True:
		lights.update()

if __name__ == '__main__':
	main()
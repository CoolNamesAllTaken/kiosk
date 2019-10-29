import threading
import usb.core

VENDOR_ID = 0x1234
PRODUCT_ID = 0x5678

BUFFER_SIZE = 8 # bytes to read from scanner

def hid2ascii(lst):
	"""
	Lifted from https://github.com/vpatron/barcode_scanner_python/blob/master/usb_scanner_hid_read_demo.py

	The USB HID device sends an 8-byte code for every character. This
	routine converts the HID code to an ASCII character.

	See https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
	for a complete code table. Only relevant codes are used here."""

	# Example input from scanner representing the string "http:":
	#   array('B', [0, 0, 11, 0, 0, 0, 0, 0])   # h
	#   array('B', [0, 0, 23, 0, 0, 0, 0, 0])   # t
	#   array('B', [0, 0, 0, 0, 0, 0, 0, 0])    # nothing, ignore
	#   array('B', [0, 0, 23, 0, 0, 0, 0, 0])   # t
	#   array('B', [0, 0, 19, 0, 0, 0, 0, 0])   # p
	#   array('B', [2, 0, 51, 0, 0, 0, 0, 0])   # :

	assert len(lst) == 8, 'Invalid data length (needs 8 bytes)'
	conv_table = {
		0:['', ''],
		4:['a', 'A'],
		5:['b', 'B'],
		6:['c', 'C'],
		7:['d', 'D'],
		8:['e', 'E'],
		9:['f', 'F'],
		10:['g', 'G'],
		11:['h', 'H'],
		12:['i', 'I'],
		13:['j', 'J'],
		14:['k', 'K'],
		15:['l', 'L'],
		16:['m', 'M'],
		17:['n', 'N'],
		18:['o', 'O'],
		19:['p', 'P'],
		20:['q', 'Q'],
		21:['r', 'R'],
		22:['s', 'S'],
		23:['t', 'T'],
		24:['u', 'U'],
		25:['v', 'V'],
		26:['w', 'W'],
		27:['x', 'X'],
		28:['y', 'Y'],
		29:['z', 'Z'],
		30:['1', '!'],
		31:['2', '@'],
		32:['3', '#'],
		33:['4', '$'],
		34:['5', '%'],
		35:['6', '^'],
		36:['7' ,'&'],
		37:['8', '*'],
		38:['9', '('],
		39:['0', ')'],
		40:['\n', '\n'],
		41:['\x1b', '\x1b'],
		42:['\b', '\b'],
		43:['\t', '\t'],
		44:[' ', ' '],
		45:['_', '_'],
		46:['=', '+'],
		47:['[', '{'],
		48:[']', '}'],
		49:['\\', '|'],
		50:['#', '~'],
		51:[';', ':'],
		52:["'", '"'],
		53:['`', '~'],
		54:[',', '<'],
		55:['.', '>'],
		56:['/', '?'],
		100:['\\', '|'],
		103:['=', '='],
		}

	# A 2 in first byte seems to indicate to shift the key. For example
	# a code for ';' but with 2 in first byte really means ':'.
	if lst[0] == 2:
		shift = 1
	else:
		shift = 0
		
	# The character to convert is in the third byte
	ch = lst[2]
	if ch not in conv_table:
		print("Warning: data not in conversion table")
		return ''
	return conv_table[ch][shift]

class BarcodeScanner:
	def __init__(self, vendor_id=VENDOR_ID, product_id=PRODUCT_ID):
		"""
		Constructor: finds USB barcode scanner, detaches it from the kernel
		"""
		self.scanner_device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
		if self.scanner_device is None:
			raise ValueError("Cannot find scanner_device!")

		cfg = self.scanner_device.get_active_configuration()

		interface_number = cfg[(0,0)].bInterfaceNumber
		scanner_interface = usb.util.find_descriptor(cfg, bInterfaceNumber=interface_number)

		if self.scanner_device.is_kernel_driver_active(scanner_interface.bInterfaceNumber):
			self.scanner_device.detach_kernel_driver(scanner_interface.bInterfaceNumber)


		self.scanner_endpoint = usb.util.find_descriptor(
			scanner_interface,
			custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

		self.scanner_lock = threading.Lock()

	def run(self):
		"""
		Update function that reads in characters from the scanner.
		Return:
			string of ASCII characters read from the scanner, if it returned anything.
		"""
		with self.scanner_lock:
			code = ""
			done_reading = False
			while not done_reading:
				# lsusb -v : find wMaxPacketSize (8 in my case)
				try:
					data = self.scanner_endpoint.read(BUFFER_SIZE, timeout=20)
					if data is 0:
						done_reading = True
					else:
						code += hid2ascii(data)
				# try:
				# 	# lsusb -v : find wMaxPacketSize (8 in my case)
				# 	a = scanner_endpoint.read(64, timeout=2000)
				except usb.core.USBError:
					done_reading = True

		return code


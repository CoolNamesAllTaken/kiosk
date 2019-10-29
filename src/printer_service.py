import threading

from escpos.printer import Usb

class Item:
	def __init__(self, name, price):
		self.name = name
		self.price = price

class Receipt:
	"""
	Thread-safe list of items with helpful functions!
	NOTE: tax_rate is not thread safe.
	"""
	def __init__(self, printer, tax_rate=0.07):
		"""
		Constructor
		"""
		self.printer = printer
		self.tax_rate = tax_rate

		self.item_list = []

		self.item_list_lock = threading.Lock() # use for multithreading

	def clear(self):
		"""
		Empties the item list.
		"""
		with self.item_list_lock:
			self.item_list = []

	def add_item(self, item):
		"""
		Adds an item to the item list.
		"""
		with self.item_list_lock:
			self.item_list.append(item)

	def calc_totals(self):
		"""
		Calculates and returns subtotal, tax, and total for items in list.
		"""
		subtotal = 0
		with self.item_list_lock:
			for item in self.item_list:
				subtotal += item.price

			tax = subtotal * self.tax_rate

		return subtotal, tax, tax + subtotal


	def print(self):
		"""
		Prints a formatted receipt.
		Python-ESCPOS methods available here: https://python-escpos.readthedocs.io/en/latest/user/methods.html
		"""

		# set(align=u'left', font=u'a', bold=False, underline=0, width=1, height=1, 
		# 	density=9, invert=False, smooth=False, flip=False, double_width=False, 
		# 	double_height=False, custom_size=False)

		# display header image
		self.printer.image("../images/Bird Logo Banner Tiny.png", fragment_height=30000, center=False)

		with self.item_list_lock:
			# display items
			self.printer.set(align="right")
			for item in self.item_list:
				self.printer.text("{}\t{:.2f}\t\n".format(item.name, item.price))
			
		# display totals
		self.printer.text("\n\n")
		self.printer.set(align="right")
		subtotal, tax, total = self.calc_totals() # already thread safe, avoid double locking!
		self.printer.text("SUBTOTAL\t{:.2f}\t\n".format(subtotal))
		self.printer.text("TAX\t{:d}%\t{:.2f}\t\n".format(round(self.tax_rate*100), tax))
		self.printer.text("TOTAL\t\t{:.2f}\t\n".format(total))

		# display QR code
		self.printer.text("\n\n")
		self.printer.set(align="center", bold=True, underline=0, double_width=True, double_height=True)
		with self.item_list_lock:
			self.printer.text("# ITEMS: {}\n".format(len(self.item_list)))
		self.printer.set(align="center")
		self.printer.text("\nREDEEM YOUR CODE!\n")
		self.printer.qr("http://rickrollomatic.com", size=10)

		self.printer.cut()
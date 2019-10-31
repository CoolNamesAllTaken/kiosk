import sys, pygame

from sound_service import SoundPlayer
from printer_service import Item, Receipt

SCREEN_SIZE = (1024, 600) # x, y

KEYPAD_ORIGIN = (50, 50) # x, y

KEY_SPACING = (SCREEN_SIZE[0] / 4, SCREEN_SIZE[1] / 5) # x, y
KEY_SIZE = (200, 80)
KEY_COLOR_NUMBER_UP = (0, 0, 255)
KEY_COLOR_NUMBER_DOWN = (0, 255, 0)
KEY_COLOR_SPECIAL_UP = (255, 0, 0)
KEY_COLOR_SPECIAL_DOWN = (0, 255, 0)
KEY_COLOR_TEXT = (0, 0, 0)

KEYPAD_NUM_KEYS = 12

KEYPAD_KEY_POSITION_LIST = [
	(KEYPAD_ORIGIN[0] + 0 * KEY_SPACING[0] ,KEYPAD_ORIGIN[1] + 0 * KEY_SPACING[1]), # 1
	(KEYPAD_ORIGIN[0] + 1 * KEY_SPACING[0], KEYPAD_ORIGIN[1] + 0 * KEY_SPACING[1]), # 2
	(KEYPAD_ORIGIN[0] + 2 * KEY_SPACING[0], KEYPAD_ORIGIN[1] + 0 * KEY_SPACING[1]), # 3
	(KEYPAD_ORIGIN[0] + 0 * KEY_SPACING[0], KEYPAD_ORIGIN[1] + 1 * KEY_SPACING[1]), # 4
	(KEYPAD_ORIGIN[0] + 1 * KEY_SPACING[0], KEYPAD_ORIGIN[1] + 1 * KEY_SPACING[1]), # 5
	(KEYPAD_ORIGIN[0] + 2 * KEY_SPACING[0], KEYPAD_ORIGIN[1] + 1 * KEY_SPACING[1]), # 6
	(KEYPAD_ORIGIN[0] + 0 * KEY_SPACING[0], KEYPAD_ORIGIN[1] + 2 * KEY_SPACING[1]), # 7
	(KEYPAD_ORIGIN[0] + 1 * KEY_SPACING[0], KEYPAD_ORIGIN[1] + 2 * KEY_SPACING[1]), # 8
	(KEYPAD_ORIGIN[0] + 2 * KEY_SPACING[0], KEYPAD_ORIGIN[1] + 2 * KEY_SPACING[1]), # 9
	(KEYPAD_ORIGIN[0] + 0 * KEY_SPACING[0], KEYPAD_ORIGIN[1] + 3 * KEY_SPACING[1]), # CLR
	(KEYPAD_ORIGIN[0] + 1 * KEY_SPACING[0], KEYPAD_ORIGIN[1] + 3 * KEY_SPACING[1]), # 0
	(KEYPAD_ORIGIN[0] + 2 * KEY_SPACING[0], KEYPAD_ORIGIN[1] + 3 * KEY_SPACING[1]), # ENTR
] # list shown as (x, y) coordinates

KEYPAD_KEY_COLOR_LIST_UP = [
	KEY_COLOR_NUMBER_UP, # 1
	KEY_COLOR_NUMBER_UP, # 2
	KEY_COLOR_NUMBER_UP, # 3
	KEY_COLOR_NUMBER_UP, # 4
	KEY_COLOR_NUMBER_UP, # 5
	KEY_COLOR_NUMBER_UP, # 6
	KEY_COLOR_NUMBER_UP, # 7
	KEY_COLOR_NUMBER_UP, # 8
	KEY_COLOR_NUMBER_UP, # 9
	KEY_COLOR_SPECIAL_UP, # CLR
	KEY_COLOR_NUMBER_UP, # 0
	KEY_COLOR_SPECIAL_UP, # ENTR
]

KEYPAD_KEY_COLOR_LIST_DOWN = [
	KEY_COLOR_NUMBER_DOWN, # 1
	KEY_COLOR_NUMBER_DOWN, # 2
	KEY_COLOR_NUMBER_DOWN, # 3
	KEY_COLOR_NUMBER_DOWN, # 4
	KEY_COLOR_NUMBER_DOWN, # 5
	KEY_COLOR_NUMBER_DOWN, # 6
	KEY_COLOR_NUMBER_DOWN, # 7
	KEY_COLOR_NUMBER_DOWN, # 8
	KEY_COLOR_NUMBER_DOWN, # 9
	KEY_COLOR_SPECIAL_DOWN, # CLR
	KEY_COLOR_NUMBER_DOWN, # 0
	KEY_COLOR_SPECIAL_DOWN, # ENTR
]

KEYPAD_KEY_VALUE_LIST = [
	"1",
	"2",
	"3",
	"4",
	"5",
	"6",
	"7",
	"8",
	"9",
	"CLR",
	"0",
	"ENTR"
]

KEYPAD_TEXT_BAR_POSITION= (100, 100)
KEYPAD_TEXT_BAR_SIZE = (1000, 50)
KEYPAD_TEXT_BAR_COLOR = (255, 255, 255)
KEYPAD_TEXT_BAR_BACKGROUND_COLOR = (0, 0, 0)
KEYPAD_COLOR_BACKGROUND = (100, 0, 0)

RECEIPT_ITEM_ORIGIN = (100, 100)
RECEIPT_ITEM_SPACING = 50
RECEIPT_ITEM_COLOR = (255, 255, 255)
RECEIPT_ITEM_SIZE = (800, 30)
RECEIPT_COLOR_TEXT = (0, 0, 0)
RECEIPT_COLOR_BACKGROUND = (100, 100, 100)
RECEIPT_MAX_NUM_ITEMS = 8 # maximum number of items to render before scrolling


class Display:
	def __init__(self, event_listener, sound_player):
		# pygame already initialized by event_listener

		self.event_listener = event_listener
		self.sound_player = sound_player
		self.screen = pygame.display.set_mode(SCREEN_SIZE)

		self.key_font = pygame.font.SysFont("Arial", round(KEY_SIZE[1] / 2), bold=True, italic=False)
		self.key_rect_list = []
		self.key_text_list = []
		for i in range(KEYPAD_NUM_KEYS):
			self.key_rect_list.append(pygame.Rect(KEYPAD_KEY_POSITION_LIST[i], KEY_SIZE))
			self.key_text_list.append(self.key_font.render(str(KEYPAD_KEY_VALUE_LIST[i]), True, KEY_COLOR_TEXT))

		self.text_bar_rect = pygame.Rect(KEYPAD_TEXT_BAR_POSITION, KEYPAD_TEXT_BAR_SIZE)

		self.receipt_font = pygame.font.SysFont("Arial", round(RECEIPT_ITEM_SIZE[1]), bold=False, italic=False)
		self.receipt_rect_list = []
		for i in range(RECEIPT_MAX_NUM_ITEMS):
			item_position = (RECEIPT_ITEM_ORIGIN[0], RECEIPT_ITEM_ORIGIN[1] + RECEIPT_ITEM_SPACING * i)
			self.receipt_rect_list.append(pygame.Rect(item_position, RECEIPT_ITEM_SIZE))


	def _draw_keypad(self, key_status_list):
		self.screen.fill(RECEIPT_COLOR_BACKGROUND)
		for i in range(KEYPAD_NUM_KEYS):
			left, top = KEYPAD_KEY_POSITION_LIST[i]
			if key_status_list[i]:
				# key has been pressed
				key_color = KEYPAD_KEY_COLOR_LIST_DOWN[i]
			else:
				# key has not been pressed
				key_color = KEYPAD_KEY_COLOR_LIST_UP[i]
			pygame.draw.rect(self.screen, key_color, self.key_rect_list[i])
			self.screen.blit(self.key_text_list[i], self.key_rect_list[i])

		pygame.display.update()

	def _draw_receipt(self, receipt):
		self.screen.fill(RECEIPT_COLOR_BACKGROUND)
		item_list = receipt.get_item_list() # get copy of item list for thread safety
		if len(item_list) > RECEIPT_MAX_NUM_ITEMS:
			item_list = item_list[-RECEIPT_MAX_NUM_ITEMS:] # display the last X items that were scanned
		for i, item in enumerate(item_list):
			pygame.draw.rect(self.screen, RECEIPT_ITEM_COLOR, self.receipt_rect_list[i]) # draw item rectangles
			if i < len(item_list):
				item_text = "{:.2f}".format(item_list[i].price)
				item_font = self.receipt_font.render(item_text, True, RECEIPT_COLOR_TEXT)
				rect_right = self.receipt_rect_list[i].right
				item_font_width = item_font.get_width()
				item_position = (
					RECEIPT_ITEM_ORIGIN[0] + RECEIPT_ITEM_SIZE[0] - item_font_width,
					RECEIPT_ITEM_ORIGIN[1] + i * RECEIPT_ITEM_SPACING)
				self.screen.blit(item_font, item_position)

				price_text = str(item_list[i].name)
				price_font = self.receipt_font.render(price_text, True, RECEIPT_COLOR_TEXT)
				self.screen.blit(price_font, self.receipt_rect_list[i])
				
		pygame.display.update()

	def keypad(self):
		"""
		Displays a numeric keypad that prompts a user to enter a multi-digit number, then hit "OK".
		Once "ENTR" is hit, the entered number is returned.
		"""
		key_status_list = [False] * 12 # all keys start as unpressed

		entered_val = ""

		while True: # loops until enter is pressed
			self._draw_keypad(key_status_list)
			entered_val_text = self.key_font.render(entered_val, True, KEYPAD_TEXT_BAR_COLOR)
			pygame.draw.rect(self.screen, KEYPAD_TEXT_BAR_BACKGROUND_COLOR, self.text_bar_rect)
			self.screen.blit(entered_val_text, self.text_bar_rect)
			for event in self.event_listener.get_mouse_events():
				# if event.type == pygame.QUIT: sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					for i, key_rect in enumerate(self.key_rect_list):
						if (key_rect.collidepoint(event.pos)):
							# click was inside this key!
							key_status_list = [False] * KEYPAD_NUM_KEYS # unpress all other keys
							key_status_list[i] = True # press this key
							key_val = KEYPAD_KEY_VALUE_LIST[i]
							if key_val is "CLR":
								entered_val = ""
							elif key_val is "ENTR":
								return entered_val
							else:
								self.sound_player.say_number(int(KEYPAD_KEY_VALUE_LIST[i]))
								entered_val += KEYPAD_KEY_VALUE_LIST[i]

	def receipt(self, receipt):
		"""
		Accepts an instance of a receipt class, and displays its contents, with one item per line.
		Makes use of the calc_totals() function to display subtotal on bottom right of screen.
		"""
		self._draw_receipt(receipt)


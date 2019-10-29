import sys, pygame

from sound_service import SoundPlayer

SCREEN_SIZE = (1024, 600) # x, y

KEYPAD_ORIGIN = (200, 200) # x, y

KEY_SPACING = (SCREEN_SIZE[0] / 8, SCREEN_SIZE[1] / 8) # x, y
KEY_SIZE = (100, 40)
KEY_COLOR_NUMBER_UP = (0, 0, 255)
KEY_COLOR_NUMBER_DOWN = (0, 255, 0)
KEY_COLOR_SPECIAL_UP = (255, 0, 0)
KEY_COLOR_SPECIAL_DOWN = (0, 255, 0)
KEY_COLOR_TEXT = (0, 0, 0)

NUM_KEYS = 12

KEY_POSITION_LIST = [
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

KEY_COLOR_LIST_UP = [
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

KEY_COLOR_LIST_DOWN = [
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

KEY_VALUE_LIST = [
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

TEXT_BAR_POSITION= (100, 100)
TEXT_BAR_SIZE = (1000, 50)
TEXT_BAR_COLOR = (255, 255, 255)
TEXT_BAR_BACKGROUND_COLOR = (0, 0, 0)


class Display:
	def __init__(self, event_listener, sound_player):
		# pygame already initialized by event_listener

		self.event_listener = event_listener
		self.sound_player = sound_player
		self.screen = pygame.display.set_mode(SCREEN_SIZE)

		self.key_font = pygame.font.SysFont("Arial", round(KEY_SIZE[1] / 2), bold=True, italic=False)
		self.key_rect_list = []
		self.key_text_list = []
		for i in range(NUM_KEYS):
			self.key_rect_list.append(pygame.Rect(KEY_POSITION_LIST[i], KEY_SIZE))
			self.key_text_list.append(self.key_font.render(str(KEY_VALUE_LIST[i]), True, KEY_COLOR_TEXT))

		self.text_bar_rect = pygame.Rect(TEXT_BAR_POSITION, TEXT_BAR_SIZE)


	def _draw_keypad(self, key_status_list):
		for i in range(NUM_KEYS):
			left, top = KEY_POSITION_LIST[i]
			if key_status_list[i]:
				# key has been pressed
				key_color = KEY_COLOR_LIST_DOWN[i]
			else:
				# key has not been pressed
				key_color = KEY_COLOR_LIST_UP[i]
			pygame.draw.rect(self.screen, key_color, self.key_rect_list[i])
			self.screen.blit(self.key_text_list[i], self.key_rect_list[i])

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
			entered_val_text = self.key_font.render(entered_val, True, TEXT_BAR_COLOR)
			pygame.draw.rect(self.screen, TEXT_BAR_BACKGROUND_COLOR, self.text_bar_rect)
			self.screen.blit(entered_val_text, self.text_bar_rect)
			for event in self.event_listener.get_mouse_events():
				# if event.type == pygame.QUIT: sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					for i, key_rect in enumerate(self.key_rect_list):
						if (key_rect.collidepoint(event.pos)):
							# click was inside this key!
							key_status_list = [False] * NUM_KEYS # unpress all other keys
							key_status_list[i] = True # press this key
							key_val = KEY_VALUE_LIST[i]
							if key_val is "CLR":
								entered_val = ""
							elif key_val is "ENTR":
								return entered_val
							else:
								self.sound_player.say_number(int(KEY_VALUE_LIST[i]))
								entered_val += KEY_VALUE_LIST[i]

	def display_receipt(self, receipt):
		"""
		Accepts an instance of a receipt class, and displays its contents, with one item per line.
		Makes use of the calc_totals() function to display subtotal on bottom right of screen.
		"""
		pass


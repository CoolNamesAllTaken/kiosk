import pygame
import threading, time

ACCEPTED_MOUSE_EVENTS = [pygame.MOUSEBUTTONDOWN]
ACCEPTED_KEY_EVENTS = [pygame.KEYDOWN]

class EventListener:
	"""
	Service for listening to and categorizing pygame events.
	"""

	def __init__(self):
		pygame.init() # ok if this is called multiple times

		self.mouse_events = []
		self.key_events = []

		self.event_list_lock = threading.Lock()

	def run(self):
		events = pygame.event.get()
		for event in events:
			if event.type in ACCEPTED_MOUSE_EVENTS:
				with self.event_list_lock:
					self.mouse_events.append(event)
			elif event.type in ACCEPTED_KEY_EVENTS:
				with self.event_list_lock:
					self.key_events.append(event)

	def get_mouse_events(self):
		with self.event_list_lock:
			mouse_events = self.mouse_events.copy()
			self.mouse_events = []
		return mouse_events

	def get_key_events(self):
		with self.event_list_lock:
			key_events = self.key_events.copy()
			self.key_events = []
		return key_events



import RPi.GPIO as GPIO
import time

from enum import Enum

BLINK_PERIOD_S = 0.2 # blink time in seconds

class LightService:
	"""
	Service for controlling LED signal tower.
	"""

	class Color(Enum):
		RED = 0
		YELLOW = 1
		GREEN = 2

	class State(Enum):
		OFF = 0
		FLASHING = 1
		ON = 2

	def __init__(
		self, 
		light_tower_channel_list=[29, 31, 36], # IO5, IO6, IO16
		light_tower_state_list=[State.OFF, State.OFF, State.OFF]):
		"""
		Constructor
		Inputs:
			light_tower_channel_list = GPIO channels in order R, Y, G
			light_tower_state_list = Status of each light in ordrer R, Y, G (LightStatus enum)
		"""

		self.light_tower_channel_list = light_tower_channel_list
		self.light_tower_state_list = light_tower_state_list

		self.last_blink_time = time.time()

		GPIO.setmode(GPIO.BOARD)
		print(self.light_tower_channel_list)
		GPIO.setup(self.light_tower_channel_list, GPIO.OUT, initial=GPIO.LOW)

	def __del__(self):
		"""
		Destructor
		"""
		GPIO.cleanup()

	def update(self):
		"""
		Call this periodically to update the lights.
		"""
		
		# update blinking lights
		curr_time = time.time()
		if (curr_time - self.last_blink_time > BLINK_PERIOD_S):
			self.last_blink_time = curr_time
			for i, channel in enumerate(self.light_tower_channel_list):
				if self.light_tower_state_list[i] == LightService.State.FLASHING:
					# light is flashing, flip its state
					GPIO.output(channel, not GPIO.input(channel))

		# update solid lights
		for i, channel in enumerate(self.light_tower_channel_list):
			if self.light_tower_state_list[i] == LightService.State.ON:
				GPIO.output(channel, GPIO.HIGH)
			elif self.light_tower_state_list[i] == LightService.State.OFF:
				GPIO.output(channel, GPIO.LOW)

	def set_state(self, light_color, light_state):
		self.light_tower_state_list[light_color.value] = light_state
	
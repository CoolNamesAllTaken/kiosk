from pygame import mixer
import os
import time
import threading

class SoundPlayer:
	def __init__(self, audio_path = os.path.join("..", "audio")):
		mixer.init()

		mixer.music.load(os.path.join(audio_path, "static.wav"))
		mixer.music.set_volume(0.008)
		mixer.music.play(-1)

		# load number audio files
		self.number_dict = {}
		# for loop adding pygame mixer things
		numbers_directory = os.path.join(audio_path, "numbers")
		for filename in os.listdir(numbers_directory):
			if  "mp3" in filename:
				continue
			filename_no_ext = os.path.splitext(filename)[0]
			self.number_dict[filename_no_ext] = mixer.Sound(os.path.join(numbers_directory, filename))

		# load track audio files
		self.track_dict = {}
		# for loop pygame mixer things
		tracks_directory = os.path.join(audio_path, "tracks")
		for filename in os.listdir(tracks_directory):
			if  "mp3" in filename:
				continue
			filename_no_ext = os.path.splitext(filename)[0]
			self.track_dict[filename_no_ext] = mixer.Sound(os.path.join(tracks_directory, filename))

		self.mixer_lock = threading.Lock()

	def play_sound_and_sleep(self, sound):
		"""
		Thread safe function for playing a sound effect.
		"""
		with self.mixer_lock:
			sound.play()
		time.sleep(sound.get_length())

	def _say_ones(self, number):
		"""
		Internal function used to say the ones digit of a number.
		"""
		self.play_sound_and_sleep(self.number_dict[str(number)[1]])

	def _say_tens(self, number):
		"""
		Internal function used to say the tens digit of a number.
		"""
		self.play_sound_and_sleep(self.number_dict[str(number)[0] + "0"])

	def say_number(self, number):
		if number <= 20 and number >= 0:
			self.play_sound_and_sleep(self.number_dict[str(number)])
		elif number > 20 and number < 100:
			self._say_tens(number)
			if number % 10 is not 0:
				self._say_ones(number)
		elif number >= 100 and number < 1000:
			hundreds_digit = number // 100
			self.say_number(hundreds_digit) # say 100's digit
			self.play_sound_and_sleep(self.number_dict["hundred"])
			self.say_number(number % 100) # say 10's and below
		elif number >= 1000 and number < 10000:
			self.say_number(number // 1000) # say 1000's digit
			self.play_sound_and_sleep(self.number_dict["thousand"])
			self.say_number(number % 1000) # say 100's and below
		else:
			# unsupported number
			self.play_track("beep")

	def play_track(self, track):
		if track in self.track_dict:
			self.play_sound_and_sleep(self.track_dict[track])
		else:
			self.play_sound_and_sleep(self.track_dict["beep"])



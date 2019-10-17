# This script requires a Raspberry Pi 2, 3 or Zero. Circuit Python must
# be installed and it is strongly recommended that you use the latest
# release of Raspbian.
 
import time
# import os
# import board
# import digitalio

from pygame import mixer

# from omxplayer.player import OMXPlayer
 
print("press a button!")

mixer.init()
sound = mixer.Sound("../audio/tracks/track41.wav")
 
while True:

    sound.play()
 
    # omxplayer -o local <file>
    # omxplayer -o hdmi <file>
    # omxplayer -o both <file>

    # player = OMXPlayer("../audio/tracks/track41.wav")
    # player.play_sync()

    # player = OMXPlayer("../audio/numbers/1.wav")
    # player.play()
    # player2 = OMXPlayer("../audio/numbers/90.wav")
    # while player.is_playing():
    #     pass
    # player2.play()
    # player3 = OMXPlayer("../audio/numbers/9.wav")
    # while player2.is_playing():
    #     pass
    # player3.play()

    # os.system('omxplayer -o local ../audio/tracks/track41.wav --no-keys &')
 
    # time.sleep(1)
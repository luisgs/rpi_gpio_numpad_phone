import RPi.GPIO as GPIO
import time
import logging, sys
import pygame       # play sounds
from multiprocessing import Process


import lineButton   # user libraries


logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# This python file reads out a phone numpad from GPIO ports 
# Note: numpad is a matrix (4x4)
# Note: we are using a RPI B

#

def play_sound(sound_track, options):
  pygame.mixer.init()
  pygame.mixer.music.load(sound_track)
  pygame.mixer.music.set_volume(1)
  pygame.mixer.music.play(loops=options)
  logging.info("We ARE PLATying this track: " + sound_track)
  while pygame.mixer.music.get_busy() == True:
    continue
  pygame.mixer.quit()


# GPIO ports for reading
# We used BCM numbering for GPIO ports
L1 = 4
L2 = 17
L3 = 27
L4 = 22


C1 = 18
C2 = 23
C3 = 24
C3E = 11    # physical matrix has an additional cable
C4 = 25



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3E, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
  GPIO.output(line, GPIO.HIGH)
  digit = ""
  if (GPIO.input(C1) == 1):
    logging.info(characters[0])
    digit =  characters[0]
    play_sound("media/audio/cell-phone-1-nr0.mp3", 1)
  elif (GPIO.input(C2) == 1):
    logging.info(characters[1])
    digit =  characters[1]
    play_sound("media/audio/cell-phone-1-nr0.mp3", 1)
  elif ((GPIO.input(C3) == 1) or (GPIO.input(C3E) == 1)):
      logging.info(characters[2])
      digit =  characters[2]
      play_sound("media/audio/cell-phone-1-nr0.mp3", 1)
  elif (GPIO.input(C4) == 1):
    logging.info(tcharacters[3])
    digit =  characters[3]
    play_sound("media/audio/cell-phone-1-nr0.mp3", 1)
  
  GPIO.output(line, GPIO.LOW)
  return digit


def read_phone_number():
  # Step in time
  # seconds waiting to read all GPIO numpad ports
  step_in_time = 0.1

  # Waiting time (#steps)
  # time waiting to send out read code
  waiting_time = 30

  # treshold
  treshold = 0

  # FINAL CODE (string!)
  # Code that will be send out
  code = ""
  ori_code = code
  while lineButton.readLine():
#    play_sound("media/audio/phone-signal-tone.mp3")
    code += readLine(L1 ,["1", "2", "3", "A"])
    code += readLine(L2 ,["4", "5", "6", "B"])
    code += readLine(L3 ,["7", "8", "9", "C"])
    code += readLine(L4 ,["*", "0", "#", "D"])


    if (ori_code != code):  # code has been updated!
      # makenoise(button is clicked)
      ori_code = code
      treshold = 0          # start timer again
    elif (treshold == waiting_time):
      logging.info("Time is over!")
      logging.info("CODE is: " + code)
      return code

#    if (waiting_time == treshold) and code:
#      logging.info("CODE IS FOUND:" + code)
#      return code
#    else:
#      treshold = treshold % waiting_time
#
#    if ori_code != code:
#      treshold = 0
#      ori_code = code
#      logging.info("num is typed in:" + code)
  
    treshold += 1 

    logging.info("Treshold++:" + str(treshold))
    time.sleep(step_in_time)
  
  return code



try:
  while True:
#    logging.info("CODE: " + read_phone_number())
    if lineButton.readLine():   # phone is picked up!
      proc_sound = Process(target=play_sound, args=('media/audio/phone-signal-tone.mp3', -1, ))
      proc_sound.start()
      code = read_phone_number()
      logging.info("PHONE is UP")
      logging.info("We read this CODE:" + code)
      proc_sound.terminate()
      proc_sound.join()
    else:
      logging.info("PHONE is DOWN")

    time.sleep(0.1)


except KeyboardInterrupt:
    logging.error("Application stopped!")

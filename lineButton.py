import RPi.GPIO as GPIO
import time

import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)



def readLine():
  B1 = 7
  B2 = 8
  B3 = 9

  status = ["PICKED_UP", "HUNG_UP"]

  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(B1, GPIO.OUT)
  #GPIO.setup(B2, GPIO.OUT)
  #GPIO.setup(B3, GPIO.OUT)

  #GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(B2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  #GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  GPIO.output(B1, GPIO.HIGH)
  if (GPIO.input(B2) == 0):
    logging.info(status[0])
    return True
  if (GPIO.input(B2) == 1):
    logging.info(status[1])
    return False
  GPIO.output(B1, GPIO.LOW)


#try:
#  while True:
#    readLine()
#    time.sleep(0.1)
#except KeyboardInterrupt:
#    logging.error("Application stopped!")
    

import RPi.GPIO as GPIO
import time

# This python file reads out a phone numpad from GPIO ports 
# Note: numpad is a matrix (4x4)
# Note: we are using a RPI B

#


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
  if (GPIO.input(C1) == 1):
    print(characters[0])
  if (GPIO.input(C2) == 1):
    print(characters[1])
  if ((GPIO.input(C3) == 1) or (GPIO.input(C3E) == 1)):
      print(characters[2])
  if (GPIO.input(C4) == 1):
    print(characters[3])
  GPIO.output(line, GPIO.LOW)

try:
  while True:
    readLine(L1 ,["1", "2", "3", "A"])
    readLine(L2 ,["4", "5", "6", "B"])
    readLine(L3 ,["7", "8", "9", "C"])
    readLine(L4 ,["*", "0", "#", "D"])
    time.sleep(0.1)
except KeyboardInterrupt:
    print("\nApplication stopped!")

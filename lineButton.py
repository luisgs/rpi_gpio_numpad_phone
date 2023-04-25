import RPi.GPIO as GPIO
import time


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

def readLine(line, status):
  GPIO.output(line, GPIO.HIGH)
  if (GPIO.input(B2) == 0):
    print(status[0])
  if (GPIO.input(B2) == 1):
    print(status[1])
  GPIO.output(line, GPIO.LOW)

try:
  while True:
#    readLine(B3, status)
    readLine(B1, status)
    time.sleep(1)
except KeyboardInterrupt:
    print("\nApplication stopped!")

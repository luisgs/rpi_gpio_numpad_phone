import RPi.GPIO as GPIO
import time
import logging, sys
import pygame       # play sounds
from threading import Thread

import lineButton   # user libraries


logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# This python file reads out a phone numpad from GPIO ports 
# Note: numpad is a matrix (4x4)
# Note: we are using a RPI B


# GLOBAL VARIABLES
# Sound files
signal_tone = "media/audio/phone-signal-tone.mp3"
busy_line = "media/audio/phone-busy-1.mp3"

# Object for creating sounds
pygame.mixer.init()
pygame.mixer.set_num_channels(10)

#
#   PLAY_SOUND
#   PLays signal tone or busy line
def play_sound(option):
    global pygame
    global signal_tone

    logging.info("Play_sound:")

    pygame.mixer.music.load(signal_tone)

    while True:
        if lineButton.readLine():
#            logging.info("Play_sound: PHONE is ON")
            logging.info("Play_Sound: Signal tone: " + signal_tone)
            # pygame.mixer.music.load(signal_tone)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy() and lineButton.readLine():
                continue
        else:
#            logging.info("Play_sound: PHONE is OFF")
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()



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
    global pygame
    GPIO.output(line, GPIO.HIGH)
    digit = ""
    if (GPIO.input(C1) == 1):
        logging.info(characters[0])
        digit =  characters[0]
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("media/audio/cell-phone-1-nr1.mp3"))
        while pygame.mixer.Channel(2).get_busy():
            continue
    elif (GPIO.input(C2) == 1):
        logging.info(characters[1])
        digit =  characters[1]
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("media/audio/cell-phone-1-nr2.mp3"))
        while pygame.mixer.Channel(2).get_busy():
            continue
    elif ((GPIO.input(C3) == 1) or (GPIO.input(C3E) == 1)):
        logging.info(characters[2])
        digit =  characters[2]
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("media/audio/cell-phone-1-nr3.mp3"))
        while pygame.mixer.Channel(2).get_busy():
            continue
    elif (GPIO.input(C4) == 1):
        logging.info(tcharacters[3])
        digit =  characters[3]
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("media/audio/cell-phone-1-nr4.mp3"))
        while pygame.mixer.Channel(2).get_busy():
            continue

    GPIO.output(line, GPIO.LOW)
    return digit



#
#   READ_PHONE_NUMBER
#   
#       We read all key strokes from keypad during a max time
#
def read_phone_number():
    # Step in time
    # We read all GPIO every step_in_time seconds
    step_in_time = 0.01

    # Waiting time (#steps)
    # time waiting to send out read code
    waiting_time = 300

    # treshold
    treshold = 0

    # FINAL CODE (string!)
    # Code that will be send out
    code = ""
    ori_code = code

    # Read while phone is off the hook
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
        if (treshold >= waiting_time):
            logging.info("Time is over!")
            logging.info("CODE is: " + code)
            # RETURN CODE!
            return code

        treshold += 1 

#        logging.info("Treshold++:" + str(treshold))
        time.sleep(step_in_time)
 
    # This code shuold not be useful. PHONE is hung up
    return False 



#
#   MAIN
#
def main():
    global signal_tone
    global busy_line
    logging.info("MAIN:")
    # Fire up thread for singal or busy tone sounds
    thread_sound = Thread(target=play_sound, args=(1, ))
    thread_sound.setDaemon(True)    # Thread is set Daemon
    thread_sound.start()
    
    while True:
        code = False 
        if lineButton.readLine():   # phone is picked up!
            logging.info("MAIN: PHONE is UP")
            code = read_phone_number()
            if (not code):
                logging.info("MAIN: CODE is EMPTY")
                singal_tone = busy_line
                logging.info("busy tone: " + busy_line)
            else:
                logging.info("MAIN: CODE: " + code)
        else:
            logging.info("MAIN: PHONE is DOWN")

try:
    if __name__ == "__main__":
        main()

except KeyboardInterrupt:
    logging.error("Application stopped!")
    sys.exit()

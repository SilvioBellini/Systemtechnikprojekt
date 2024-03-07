try:
    import driver
    import flink
    import time
except ModuleNotFoundError:
    pass
from sharedData import *
from communication import *
from api import *
from stopWatch import *
from statusDisplay import *

username = "test" #team2
password = "test" #rHGpIGxo0o1k
topic = "test/team2" #Coop

if(__name__ == "__main__"):
    ginTronic = API()
    sharedData = SharedData()
    com = Communication(username, password, topic, sharedData)
    watch = StopWatch()
    mode = 0
    statusLED = StatusDisplay()

    # Test
    #ginTronic.drive(20)
    #time.sleep(5)
    #ginTronic.turn(20, 360)
    #time.sleep(5)
    #ginTronic.rotateGripper(270)
    #time.sleep(2)
    #ginTronic.rotateGripper(0)
    #print("Done")

    while True:
        statusLED.setColor(255, 0, 0)           # Red
        time.sleep(2)
        statusLED.setColor(0, 255, 0)           # Green
        time.sleep(2)
        statusLED.setColor(0, 0, 255)           # Blue
        time.sleep(2)
        statusLED.setColor(255, 255, 0)         # Yellow
        time.sleep(2)
        statusLED.setColor(0, 255, 255)         # Cyan
        time.sleep(2)
        statusLED.setColor(255, 0, 255)         # Magenta
        time.sleep(2)
        statusLED.setColor(255, 255, 255)       # White
        time.sleep(2)

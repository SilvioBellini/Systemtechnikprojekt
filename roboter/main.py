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

username = "test" #team2
password = "test" #rHGpIGxo0o1k
topic = "test/team2" #Coop

if(__name__ == "__main__"):
    ginTronic = API()
    sharedData = SharedData()
    com = Communication(username, password, topic, sharedData)
    watch = StopWatch()
    mode = 0

    # Test
    ginTronic.drive(20)
    time.sleep(5)
    ginTronic.turn(20, 360)
    time.sleep(5)
    ginTronic.rotateGripper(270)
    time.sleep(2)
    ginTronic.rotateGripper(0)
    print("Done")

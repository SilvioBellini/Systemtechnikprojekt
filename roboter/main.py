try:
    import driver
    import flink
    import time
except ModuleNotFoundError:
    pass

from api import *
from sharedData import *
from communication import *
from stopWatch import *
from audioManager import *
from statusDisplay import *
from task import *

#region Classattributes

username = "test" #team2
password = "test" #rHGpIGxo0o1k
topic = "test/team2" #Coop
mode = None

#endregion

if(__name__ == "__main__"):
    # Initializing Objects
    ginTronic = API()
    sharedData = SharedData()
    com = Communication(username, password, topic, sharedData)
    watch = StopWatch()
    audio = AudioManager()
    statusLED = StatusDisplay()
    task = Task()

    try:
        # Running main python code in here
        pass
    except Exception as error:
        # Setting the statusLed to red and displaying an error message
        statusLED.setColor(255, 0, 0)
        print("An error has occured: ", repr(error))
# region Imports

try:
    import driver
    import flink
    import time
except ModuleNotFoundError:
    pass

from api import API
from sharedData import SharedData
from communication import Communication
from stopWatch import StopWatch
from audioManager import AudioManager
from statusDisplay import StatusDisplay
from task import Task

#endregion

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
    statusLed = StatusDisplay()
    task = Task(mode, ginTronic, sharedData, com, audio, statusLed)

    try:
        # Running main python code in here
        pass
    except Exception as error:
        # Setting the statusLed to red and displaying an error message
        statusLed.setColor(255, 0, 0)
        print("An error has occured: ", repr(error))
    


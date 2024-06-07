# region Imports

try:
    import driver
    import flink
    import time
except ModuleNotFoundError:
    pass

from config import Config
from api import API
from sharedData import SharedData
from communication import Communication
from stopWatch import StopWatch
from audioManager import AudioManager
from statusDisplay import StatusDisplay
from task import Task
from testClass import TestClass

#endregion

#region Classattributes

username = "team2"
password = "rHGpIGxo0o1k"
topic = "team1_2/test"
mode = None

#endregion

if(__name__ == "__main__"):
    # Initializing Objects
    config = Config()
    watch = StopWatch()

    # Communication
    sharedData = SharedData()
    com = Communication(config, sharedData)

    # Status
    audio = AudioManager(config)
    statusLed = StatusDisplay(config)

    # Tasks
    api = API(config)
    mode = api.getMode()
    task = Task(mode, config, api, sharedData, com, audio, statusLed, watch)
    #testClass = TestClass(config, api, sharedData, com, watch, audio, statusLed, task)

    try:
        # Running main python code in here
        task.findObject(1)
        task.grabObject()
        task.moveToMid()

    except Exception as error:
        # Setting the statusLed to red and displaying an error message
        statusLed.setColor(255, 0, 0)
        print("An error has occured: ", repr(error))

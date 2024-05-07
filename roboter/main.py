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
from testClass import TestClass

#endregion

#region Classattributes

username = "team2"
password = "rHGpIGxo0o1k"
topic = "team2/test"
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
    mode = ginTronic.getMode()
    task = Task(mode, ginTronic, sharedData, com, audio, statusLed, watch)
    test = TestClass(ginTronic, sharedData, com, watch, audio, statusLed, task)

    try:
        # Running main python code in here

        # Test fill Servo
        test.testFillServo()         
        
        
    except Exception as error:
        # Setting the statusLed to red and displaying an error message
        statusLed.setColor(255, 0, 0)
        print("An error has occured: ", repr(error))
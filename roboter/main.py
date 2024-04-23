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
from test import Test


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
    task = Task(mode, ginTronic, sharedData, com, audio, statusLed)
    test = 

    try:
        # Running main python code in here

        # Test Audio
        audio.selectDevice()
        audio.setVolume(10)
        audio.playAudioClip(1, 3)
        time.sleep(15)
        audio.pause()

    except Exception as error:
        # Setting the statusLed to red and displaying an error message
        statusLed.setColor(255, 0, 0)
        print("An error has occured: ", repr(error))
        pass
    


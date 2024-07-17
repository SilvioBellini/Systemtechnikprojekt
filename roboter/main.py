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
    task = Task(config, api, sharedData, com, audio, statusLed, watch)
    testClass = TestClass(config, api, sharedData, com, watch, audio, statusLed, task)

    try:
        print("Starting")
        task.findObject(0)
        task.grabObject()
        """   
        # Startup
        print("Startup complete: Waiting for Input")
        audio.setVolume(config.defaultVolume)
        audio.playAudioClip(2, config.sfx[config.SFXs.IGNITION])

        # Waiting for Start-Input
        while True:
            if(api.gpio.getValue(2)):
                print("Start-Button pressed")
                break

            time.sleep(0.1)

        time.sleep(0.5)

        # Getting operation mode
        mode = api.getMode()
        
        # Process
        match mode:
            case 0:     # Glass
                print("Mode 0: Glass")

                task.findObject(mode)
                task.grabObject()
                #task.moveToMid()
                #task.moveToCounter()
                #task.place()
                #task.moveToEndPos(mode)

            case 1:     # Bottle
                print("Mode 1: Bottle")
                print("Waiting for approval Kitchen")

                # Waiting for approval from partner robot for the kitchen
                while True:
                    com.receiveMessage()
                    if(sharedData.approvalKitchen):
                        break

                    time.sleep(0.1)
                audio.playAudioClip(2, config.sfx[config.SFXs.APPROVAL_KITCHEN])
                
                task.findObject(mode)
                task.grabObject()
                task.moveToMid()

                print("Waiting for approval Counter")

                # Waiting for approval from partner robot for the counter
                while True:
                    com.receiveMessage()
                    if(sharedData.approvalCounter):
                        break

                    time.sleep(0.1)
                #statusLed.setColor(0, 255, 0)
                audio.playAudioClip(2, config.sfx[config.SFXs.APPROVAL_COUNTER])

                task.moveToCounter()
                task.fill()
                task.moveToEndPos(mode)
    """

    except Exception as error:
        # Setting the statusLed to red and displaying an error message
        statusLed.setColor(255, 0, 0)
        print("An error has occured: ", repr(error))
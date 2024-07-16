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

# endregion

# region Classattributes

username = "team2" 
password = "rHGpIGxo0o1k"
topic = "team1_2/test"
mode = None

# endregion

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
        print("Booting complete")
        audio.setVolume(config.defaultVolume)
        audio.playAudioClip(2, config.SFXs.IGNITION.value)
        
        # Running different programs with hex-switch for once after each switch 
        while True:
            if(api.gpio.getValue(2)): # Waiting for start input
                mode = api.getMode()
                time.sleep(3)
                match mode:
                    case 0: time.sleep(1)
                    case 1: testClass.testDrive()
                    case 2: testClass.testReadSensorValues()
                    case 3: testClass.testLimitSwitch()
                    case 4: testClass.testGripServo()
                    case 5: testClass.testFillServo()
                    case 6: testClass.testGripper()
                    case 7: testClass.testGetMode()
                    case 8: testClass.testSendMessage()
                    case 9: testClass.testSaveData()
                    case 10: testClass.testLed()
                    case 11: testClass.testAudio()
                    case _: break
                while mode == api.getMode():
                    time.sleep(1)
            
            time.sleep(0.1)
                
    except Exception as error:
        # Setting the statusLed to red and displaying an error message
        statusLed.setColor(255, 0, 0)
        print("An error has occured: ", repr(error))
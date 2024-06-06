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
    ginTronic = API(config)
    sharedData = SharedData()
    com = Communication(config, sharedData)
    watch = StopWatch()
    audio = AudioManager(config)
    statusLed = StatusDisplay(config)
    mode = ginTronic.getMode()
    task = Task(mode, config, ginTronic, sharedData, com, audio, statusLed, watch)
    test = TestClass(config, ginTronic, sharedData, com, watch, audio, statusLed, task)

    try:
        print("Booting complete")
        audio.setVolume(config.defaultVolume)
        audio.playAudioClip(2, config.SFXs.IGNITION.value)
        
        # Running different programs with hex-switch for once after each switch 
        while True:
            if(ginTronic.gpio.getValue(2)): # Waiting for start input
                mode = ginTronic.getMode()
                time.sleep(3)
                match mode:
                    case 0: time.sleep(1)
                    case 1: test.testDrive()
                    case 2: test.testReadSensorValues()
                    case 3: test.testLimitSwitch()
                    case 4: test.testGripServo()
                    case 5: test.testFillServo()
                    case 6: test.testGripper()
                    case 7: test.testGetMode()
                    case 8: test.testSendMessage()
                    case 9: test.testSaveData()
                    case 10: test.testLed()
                    case 11: test.testAudio()
                    case _: break
                while mode == ginTronic.getMode():
                    time.sleep(1)
            
            time.sleep(0.1)
                
    except Exception as error:
        # Setting the statusLed to red and displaying an error message
        statusLed.setColor(255, 0, 0)
        print("An error has occured: ", repr(error))
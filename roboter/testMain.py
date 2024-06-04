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

# endregion

# region Classattributes

username = "team2" 
password = "rHGpIGxo0o1k"
topic = "team1_2/test"
mode = None

# endregion

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
        print("Booting complete")
        audio.setVolume(30)
        audio.playAudioClip(2, 1)
        
        # Running different programs with hex-switch for once after each switch 
        while True:
            if(ginTronic.gpio.getValue(2)): # Waiting for start input
                mode = ginTronic.getMode()
                time.sleep(3)
                match mode:
                    case 0: time.sleep(1)
                    case 1: test.testDrive()
                    case 2: test.testReadSensorValues()
                    case 3: test.testGripServo()
                    case 4: test.testFillServo()
                    case 5: test.testGripper()
                    case 6: test.testGetMode()
                    case 7: test.testSendMessage()
                    case 8: test.testSaveData()
                    case 9: test.testLed()
                    case 10: test.testAudio()
                    case _: break
                while mode == ginTronic.getMode():
                    time.sleep(1)
            
            time.sleep(0.1)
                
    except Exception as error:
        # Setting the statusLed to red and displaying an error message
        statusLed.setColor(255, 0, 0)
        print("An error has occured: ", repr(error))
#region Imports

import time

from api import API
from sharedData import SharedData
from communication import Communication
from stopWatch import StopWatch
from audioManager import AudioManager
from statusDisplay import StatusDisplay
from task import Task

#endregion

class TestClass:
    """
    Class for testing parts of the robot(speakers, servos, etc.)
    """
    def __init__(self, api : API, sharedData : SharedData, communication : Communication, watch : StopWatch, audio : AudioManager, statusLed : StatusDisplay, task : Task):
        """
        Initializes the Test object with default values.
        """
        self.api = api
        self.sharedData = sharedData
        self.com = communication
        self.audio = audio
        self.statusLed = statusLed
        self.task = task

    def testAudio(self):
        """
        function to play music on the speaker
        """
        self.audio.selectDevice()
        self.audio.setVolume(10)
        self.audio.playAudioClip(1, 3)            
        time.sleep(15)
        self.audio.pause()
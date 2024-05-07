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
        self.watch = watch
        self.audio = audio
        self.statusLed = statusLed
        self.task = task

    #region API

    def testDrive(self) -> None:
        """
        Testing the functionality of the drive motors. Driving forward, backward and turning with increasing speeds.
        Tested (30.04.2024) with Board-Motors, own motors DONT WORK! 

        Returns
        ----------
        None
        """
        print("Starting to drive")
        speedMultiplicator = 0.5
        for i in range(4):
            self.api.drive(i * speedMultiplicator)
            time.sleep(2)

        print("Stopping 1")
        self.api.stop()
        time.sleep(3)

        print("Driving backwards")
        for i in range(4):
            self.api.drive(i * -speedMultiplicator)
            time.sleep(2)

        print("Stopping 2")
        self.api.stop()
        time.sleep(3)

        print("Turning")
        for i in range(4):   
            self.api.turn(i * speedMultiplicator, 3600)
            time.sleep(2)

        print("Finished")
        self.api.stop()

    def testReadSensorValues(self) -> None:
        """
        Testing the functionality of the sensors. Reading and printing each value multiple times.

        Returns
        ----------
        None
        """
        for i in range(3):
            for sensor in range(7):
                print("Sensor {}: {} ".format(sensor, self.api.readSensorValue(sensor)))
            time.sleep(2)

    def testGripServo(self) -> None:
        """
        Testing the functionality of the servomotor that grips the object. Opening and closing the gripper.
        Tested (30.04.2024)

        Wiring
        ----------
        Orange: PWM (Y17)
        Red:    +5V
        Black:  GND

        Returns
        ----------
        None
        """
        self.api.rotateServo(self.api.pwmChGrip, 0, 0)
        time.sleep(3)
        self.api.rotateServo(self.api.pwmChGrip, 0, 45)
        time.sleep(3)
        self.api.rotateServo(self.api.pwmChGrip, 0, 0)

    def testFillServo(self) -> None:
        """
        Testing the functionality of the servomotor that rotates the gripper to fill the glas. Rotating for different angles.
        Tested (30.04.2024)

        Wiring
        ----------
        Orange: PWM (Y16)
        Red:    +5V
        Black:  GND

        Returns
        ----------
        None
        """
        self.api.rotateServo(self.api.pwmChFill, 1, 0) # Set the servo in 0° (horizontal) Position

        angleMultiplicator = 20         # Rotating in steps of 20°
        for i in range(10):
            self.api.rotateServo(self.api.pwmChFill, 50, i * angleMultiplicator)
            self.api.rotateServo(self.api.pwmChFill, 1, 0) # Set the servo in 0° (horizontal) Position

    def testGetMode(self) -> None:
        """
        Testing the functionality of the Hex-Switch to set the mode.
        Tested (30.04.2024)
        
        Wiring
        ----------
        1:  Ch1 (L16)
        2:  Ch2 (L17)
        4:  Ch4 (H16)
        8:  Ch8 (H17)
        C:  +3.3V

        Returns
        ----------
        None
        """
        for i in range(5):
            print(self.api.getMode())
            time.sleep(3)
    
    #endregion

    #region Communication

    def testSendMessage(self):
        for i in range(10):
            self.com.sendMessage(0, i)
            time.sleep(0.5)

    def testSaveData(self):
        for i in range(20):
            self.com.receiveMessage()
            print(self.sharedData.getData(0))
            print(self.sharedData.getData(1))
            print(self.sharedData.getData(2))
            print("")

            time.sleep(1)

    #endregion

    #region Status

    def testLed(self):
        """
        Testing the functionality of the status LED. Setting to different colors (white -> red -> green -> blue)
        Tested (30.04.2024)

        Wiring
        ----------
        Red:    PWM Red (U12)
        Green:  PWM Green (V12)
        Orange: PWM Blue (W13)
        Black:  GND


        Returns
        ----------
        None
        """
        self.statusLed.setColor(255, 255, 255)
        time.sleep(2)
        self.statusLed.setColor(255, 0, 0)
        time.sleep(2)
        self.statusLed.setColor(0, 255, 0)
        time.sleep(2)
        self.statusLed.setColor(0, 0, 255)

    def testAudio(self) -> None:
        """
        Testing the functionality of the soundboard. Playing an Audioclip for 15 seconds, then pausing.
        Tested (23.04.2024)

        Wiring
        ----------
        RX:     TX (V18)
        TX:     RX (W19)
        VCC:    +5V
        GND:    GND

        Returns
        ----------
        None
        """
        self.audio.selectDevice()
        self.audio.setVolume(10)
        self.audio.playAudioClip(1, 3)            
        time.sleep(15)
        self.audio.pause()

    #endregion
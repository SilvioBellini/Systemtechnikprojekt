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
    Class for testing parts of the robot (speakers, servos, etc.)
    
    Parameters
    ----------
    api:            Object of the API class
    sharedData:     Object of the SharedData class
    communication:  Object of the Communication class
    audio:          Object of the AudioManager class
    statusLed:      Object of the StatusDisplay class
    watch:          Object of the StopWatch class
    taks:           Object of the TestClass class
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
        Tested (10.05.2024)

        Wiring
        ----------
        PWM_A_Left:     U13
        PWM_B_Left:     T10
        ENC_A_Left:     P19
        ENC_B_Left:     P20

        PWM_A_Right:    T14
        PWM_B_Right:    V13
        ENC_A_Right:    T20
        ENC_B_Right:    V20

        Returns
        ----------
        None
        """
        
        print("Starting to drive")
        speedMultiplicator = 0.04
        for i in range(4):
            print("Driving with: ", i * speedMultiplicator)
            self.api.drive(i * speedMultiplicator)
            time.sleep(2)

        print("Stopping 1")
        self.api.stop()
        time.sleep(3)

        print("Driving backwards")
        for i in range(4):
            print("Driving with: ", i * -speedMultiplicator)
            self.api.drive(i * -speedMultiplicator)
            time.sleep(2)

        print("Stopping 2")
        self.api.stop()
        time.sleep(3)

        print("Turning")
        for i in range(4):
            print("Turning with: ", i * speedMultiplicator) 
            self.api.turn(i * speedMultiplicator, 3600)
            time.sleep(2)

        self.api.stop()
        print("Finished")

    def testReadSensorValues(self) -> None:
        """
        Testing the functionality of the sensors. Reading and printing each value multiple times.
        (Tested 10.05.2024)

        Wiring
        ----------
        Trig:       L14
        A0:         N16
        A1:         L15
        Out:        ADC7476

        Returns
        ----------
        None
        """

        self.watch.start(20)
        while True: #not self.watch.isFinished()
            for sensor in range(self.api.amountOfSensors):
                print("Sensor {}: {}".format(sensor, self.api.readSensorValue(sensor)))
            
            print("")
            time.sleep(3)

    def testLimitSwitch(self):
        self.watch.start(20)
        while not self.watch.isFinished():
            print("Limit Switch front side: {}".format(self.api.readSensorValue(9)))
            print("Limit switch back side:  {}".format(self.api.readSensorValue(10)))
            
            print("")
            time.sleep(1)

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
        angle = 25 # the angle for gripping, tested
        print("Starting")
        time.sleep(3)
        self.api.rotateServo(self.api.pwmChGrip, 50, 0)
        time.sleep(3)
        print(f"Rotating to {angle}°")
        self.api.rotateServo(self.api.pwmChGrip, 50, angle)
        time.sleep(3)
        print("Rotating back")
        self.api.rotateServo(self.api.pwmChGrip, 50, 0)
        

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
        self.api.rotateServo(self.api.pwmChFill, 50, 0) # Set the servo in 0° (horizontal) Position

        angleMultiplicator = 15         # Rotating in steps of 20°
        for i in range(7):
            self.api.rotateServo(self.api.pwmChFill, 50, i * angleMultiplicator)
            print(i * angleMultiplicator)
            time.sleep(1)

        self.api.rotateServo(self.api.pwmChFill, 100, 0) # Set the servo to 0° (horizontal) Position

    def testGripper(self) -> None:
        """
        Testing the functionality of the gripper including the fill and grip servo. 

        Returns
        ----------
        None
        """
        # Moving to start position
        self.api.rotateServo(self.api.pwmChFill, 100, 0)
        time.sleep(1)

        # Grabbing object
        self.api.rotateServo(self.api.pwmChGrip, 50, 0)
        time.sleep(2)
        self.api.rotateServo(self.api.pwmChGrip, 50, 25)
        time.sleep(1)

        # Filling
        self.api.rotateServo(self.api.pwmChFill, 100, 85)
        time.sleep(5)
        self.api.rotateServo(self.api.pwmChFill, 100, 0)
        time.sleep(1)

        # Releasing object
        self.api.rotateServo(self.api.pwmChGrip, 1, 0)
        time.sleep(1)

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
        for i in range(15):
            print(self.api.getMode())
            time.sleep(3)
    
    #endregion

    #region Communication

    def testSendMessage(self) -> None:
        """
        Testing the functionality of sending messages to the server for the partner team to read them

        Wiring
        ----------
        None

        Returns
        ----------
        None
        """
        flipFlop = False

        for i in range(10):
            self.com.sendMessage(2, (i % 5) + 1)
            time.sleep(1)
        
        for i in range(5):
            flipFlop = not flipFlop
            self.com.sendMessage(0, flipFlop)
            time.sleep(1)

        flipFlop = False

        for i in range(5):
            flipFlop = not flipFlop
            self.com.sendMessage(1, flipFlop)
            time.sleep(1)

    def testSaveData(self) -> None:
        """
        Testing the functionality of receiving messages from the partner team and saving them

        Wiring
        ----------
        None

        Returns
        ----------
        None
        """
        thankYouKitchen = False
        thankYouCounter = False
        for i in range(20):
            self.com.receiveMessage()
            print(self.sharedData.getData(0))
            print(self.sharedData.getData(1))
            print(self.sharedData.getData(2))
            print("")

            dataKitchen = self.sharedData.getData(0)
            dataCounter = self.sharedData.getData(1)
            if dataKitchen != thankYouKitchen:
                thankYouKitchen = dataKitchen
                if thankYouKitchen == True:
                    self.audio.setVolume(25)
                    self.audio.playAudioClip(2, 2)
                    time.sleep(3)
            if dataCounter != thankYouCounter:
                thankYouCounter = dataCounter
                if thankYouCounter == True:
                    self.audio.setVolume(25)
                    self.audio.playAudioClip(2, 3)
                    time.sleep(3)

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
        time.sleep(2)
        self.statusLed.setColor(0, 0, 0)

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
        #self.audio.selectDevice()
        self.audio.setVolume(25)
        self.audio.playAudioClip(1, 1)
        time.sleep(15)
        self.audio.pause()
        time.sleep(3)
        self.audio.playAudioClip(2, 4)

    #endregion
#region Imports

from api import API
from sharedData import SharedData
from communication import Communication
from audioManager import AudioManager
from statusDisplay import StatusDisplay
from stopWatch import StopWatch

#endregion

class Task:
    def __init__(self, mode : int, api : API, sharedData : SharedData, communication : Communication, audio : AudioManager, statusLed : StatusDisplay, watch : StopWatch):
        """
        Initializes the Task object with default values.
        """
        self.mode = mode
        self.api = api
        self.sharedData = sharedData
        self.com = communication
        self.audio = audio
        self.statusLed = statusLed
        self.watch = watch

    def findObject(self, mode : int) -> None:
        """
        Finding either the glass or bottle specified with the mode.

        Parameters
        ----------
        mode: Specifying what object should be found

        Returns
        ----------
        None
        """
        mode = self.api.getMode()

        self.watch.start(1000)                  # move forward from Startposition
        while not self.watch.isFinished():
            self.api.drive(0.03)
        self.api.stop()                         # stop after Time finished

        self.api.turn(0.03, -90)                # turn to Counter 
        
        while self.api.readSensorValue(0) > 0:  # Find the FIRST white line
            self.api.drive(0.03)
            self.api.readSensorValue(0)
        
        slot = 5

        while True:
            if mode == 0:
                while True:
                    if self.api.readSensorValue(7) < 0 and self.api.readSensorValue(8) > 0:     # Sensor 1 active and Sensor 2 inactive
                        self.api.stop()
                        break

                while self.api.readSensorValue(0) > 0:  # Find the white line
                    self.api.drive(0.03)
                    self.api.readSensorValue(0)

            elif mode == 1:
                while True:
                    if self.api.readSensorValue(7) < 0 and self.api.readSensorValue(8) < 0:     # Sensor 1 active and Sensor 2 active
                        self.api.stop()
                        break
            break

        self.grabObject()


    def grabObject(self) -> None:
        """
        Grabbing the currently detected object.

        Returns
        ----------
        None
        """
        
        #Turn 90 degrees and recognize the line

        self.api.turn(speed=0.02, angle=0) # Starts rotating at a slow speed, angle=0 is handled as turning indefinitely

        #keep rotating until both sensors 3 and 5 are over the line
        while True:
            sensor3 = self.api.readSensorValue(3)
            sensor5 = self.api.readSensorValue(5)
            if sensor3 > 0.5 and sensor5 > 0.5 #Adjust Threshold for line detection
                self.api.stop()
                break


        #Rotate arm to initial position (0degrees)
        self.api.rotateServo(channel=10, stepCount=0, angle=0)

        #Open the gripper (move to 270 degrees)
        self.api.rotateServo(channel=12, stepCount=0, angle=270)

        #Drive forward until limit switch turns on
        limitswitchsensoren????
        while True:
            self.api.drive(0.03)
            limitSwitchTriggered = limitswitchslot()
            if limitSwitchTriggered > 1:
                self.api.stop()
                break
        ??????????????????????????????

        
        #Close the gripper (return to 0 degrees)
        self.api.rotateServo(channel=12, stepCount=0, angle=0)

        #Lift the object off the table by rotating the arm to 5 degrees)
        self.api.rotateServo(channel=10, tepCount=0 angle=5)

        #Drive backwards for a specified duration
        self.watch.start(11)
        while not self.watch.isFinished():
            self.api.drive (-0.1)
        self.api.stop



    def moveToCounter(self, glassSlot : int) -> None:
        """
        Driving to the specific slot at the counter.

        Parameters
        ----------
        glassSlot: The slot where the glass is located

        Returns
        ----------
        None
        """


    def switchSlot(self) -> None:
        """
        Switching the slot if an obstacle is detected

        Returns
        ----------
        None
        """        
        pass

    def place(self) -> None:
        """
        Placing either glass or bottle onto the counter.

        Returns
        ----------
        None
        """
        pass

    def fill(self) -> None:
        """
        Filling the glass with the bottle by tipping it over its head.

        Returns
        ----------
        None
        """
        pass

    def moveToEndPos(self, mode : int) -> None:
        """
        Moving the robot to the end position based on the specified mode

        Parameters
        ----------
        mode: Specifying the endposition based on what object got handled

        Returns
        ----------
        None
        """
        pass

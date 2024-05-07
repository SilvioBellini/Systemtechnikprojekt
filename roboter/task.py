#region Imports

from api import API
from sharedData import SharedData
from communication import Communication
from audioManager import AudioManager
from statusDisplay import StatusDisplay
from stopWatch import StopWatch

#endregion

class Task:

    slotCounter = 6

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

        lastDetectedLine = False #Flag for counting lines on the ground (so that if sensor on the line it doesnt count multiple times)
        objectFound = False

        while not objectFound:
            #read sensors for line detection
            sensor0 = self.api.readSensorValue(0)
            sensor2 = self.api.readSensorValue(2)

            #update state of sensors
            if sensor0 > 0.5:
                sensor0DetectedLine = True
            if sensor2 > 0.5:
                sensor2DetectedLine = True

            # Detect if crossing a line
            if (sensor0DetectedLine or sensor2DetectedLine) and not lastDetectedLine:
                Task.slotCounter -= 1  # Decrement the slot counter on line cross
                lastDetectedLine = True  # Set flag when a line is detected
                sensor0DetectedLine = False  # Reset detection states
                sensor2DetectedLine = False
            elif sensor0 < 0.5 and sensor2 < 0.5 and lastDetectedLine:
                lastDetectedLine = False  # Reset the flag when no line is detected

            # Sensor values for object detection
            sensor7 = self.api.readSensorValue(7)
            sensor8 = self.api.readSensorValue(8)

            # Object detection logic based on mode
            if mode == 0:  # Looking for glass
                if sensor7 < 0 and sensor8 > 0:
                    objectFound = True
                    self.api.stop()
            elif mode == 1:  # Looking for bottle
                if sensor7 < 0 and sensor8 < 0:
                    objectFound = True
                    self.api.stop()
                
        self.api.turn(0.03, 90)
            

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
            sensor0 = self.api.readSensorValue(0)
            sensor2 = self.api.readSensorValue(2)
            if sensor0 > 0.5 and sensor2 > 0.5: # Adjust Threshold for line detection
                self.api.stop()
                break


        #Rotate arm to initial position (0degrees)
        self.api.rotateServo(channel=10, stepCount=0, angle=0)

        #Open the gripper (move to 270 degrees)
        self.api.rotateServo(channel=12, stepCount=0, angle=270)

        #Drive forward until limit switch turns on
        #
        while True:
            self.api.drive(0.03)
            #reading the GPIO pin 13 "Endschalter Küche"
            limitSwitchState = self.api.gpio.getValue(13)
            if limitSwitchState == 1: #1 means limitswitch pressed (assuming)
                self.api.stop()
                break

        
        #Close the gripper (return to 0 degrees)
        self.api.rotateServo(channel=12, stepCount=0, angle=0)

        #Lift the object off the table by rotating the arm to 5 degrees)
        self.api.rotateServo(channel=10, stepCount=0 ,angle=5)

        #Drive backwards for a specified duration
        self.watch.start(11)
        while not self.watch.isFinished():
            self.api.drive (-0.1)
        self.api.stop

    def moveToMid(self):
        
        #read sensors for line detection
        sensor0 = self.api.readSensorValue(0)
        sensor2 = self.api.readSensorValue(2)

        if Task.slotCounter > 3:

            #Turn 90 degrees and recognize the line

            self.api.turn(speed=0.02, angle=-0) # Starts rotating at a slow speed, angle=0 is handled as turning indefinitely

            #keep rotating until both sensors 4 and 5 are over the line
            while True:
                if sensor0 > 0.5 and sensor2 > 0.5: # Adjust Threshold for line detection
                    self.api.stop()
                    break

            #update state of sensors
            if sensor0 > 0.5:
                sensor0DetectedLine = True
            if sensor2 > 0.5:
                sensor2DetectedLine = True

            # Detect if crossing a line
            if (sensor0DetectedLine or sensor2DetectedLine) and not lastDetectedLine:
                Task.slotCounter -= 1  # Decrement the slot counter on line cross
                lastDetectedLine = True  # Set flag when a line is detected
                sensor0DetectedLine = False  # Reset detection states
                sensor2DetectedLine = False
            elif sensor0 < 0.5 and sensor2 < 0.5 and lastDetectedLine:
                lastDetectedLine = False  # Reset the flag when no line is detected

        if Task.slotCounter < 3:
            #Turn 90 degrees and recognize the line

            self.api.turn(speed=0.02, angle=0) # Starts rotating at a slow speed, angle=0 is handled as turning indefinitely

            #keep rotating until both sensors 4 and 5 are over the line
            while True:
                sensor0 = self.api.readSensorValue(4)
                sensor2 = self.api.readSensorValue(5)
                if sensor0 > 0.5 and sensor2 > 0.5: # Adjust Threshold for line detection
                    self.api.stop()
                    break

            #update state of sensors
            if sensor0 > 0.5:
                sensor0DetectedLine = True
            if sensor2 > 0.5:
                sensor2DetectedLine = True

            # Detect if crossing a line
            if (sensor0DetectedLine or sensor2DetectedLine) and not lastDetectedLine:
                Task.slotCounter += 1  # Decrement the slot counter on line cross
                lastDetectedLine = True  # Set flag when a line is detected
                sensor0DetectedLine = False  # Reset detection states
                sensor2DetectedLine = False
            elif sensor0 < 0.5 and sensor2 < 0.5 and lastDetectedLine:
                lastDetectedLine = False  # Reset the flag when no line is detected





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

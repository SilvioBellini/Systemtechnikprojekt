#region Imports

from api import API
from sharedData import SharedData
from communication import Communication
from audioManager import AudioManager
from statusDisplay import StatusDisplay
from stopWatch import StopWatch

import time

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
        lineDetected = False    # Flag to save that both sensors are one the mark
        objectFound = False
        self.api.drive(self.api.defaultSpeed)

        while not objectFound:
            # Update Sensor Values
            sensor0Value = self.api.readSensorValue(0)
            sensor2Value = self.api.readSensorValue(2)

            # Resetting flag
            if(sensor0Value < self.api.valueWhite or sensor2Value < self.api.valueWhite):
                lineDetected = False

            # Aligning if one sensor is on the mark, setting the flag
            if((sensor0Value > self.api.valueWhite or sensor2Value > self.api.valueWhite) and not lineDetected):
                self.api.align(self.api.Directions.Perpendicular)
                self.slotCounter -= 1
                lineDetected = True
                self.api.drive(self.api.defaultSpeed)
                time.sleep(0.5)     # Ensure that both sensors get off the mark before resetting flag

            # Object detection based on mode
            sensor7Value = self.api.getSensorValues(7)
            sensor8Value = self.api.getSensorValues(8)

            match mode:
                case 0:     # Glass
                    if(sensor7Value and not sensor8Value):
                        objectFound = True
                        self.api.stop()

                case 1:     # Bottle
                    if(sensor7Value and sensor8Value):
                        objectFound = True
                        self.api.stop()
            
            time.sleep(0.05)

            """
            #update state of sensors
            if sensor0Value > 0.5:
                sensor0DetectedLine = True
            if sensor2Value > 0.5:
                sensor2DetectedLine = True

            # Detect if crossing a line
            if (sensor0DetectedLine or sensor2DetectedLine) and not lastDetectedLine:
                Task.slotCounter -= 1  # Decrement the slot counter on line cross
                lastDetectedLine = True  # Set flag when a line is detected
                sensor0DetectedLine = False  # Reset detection states
                sensor2DetectedLine = False
            elif sensor0Value < 0.5 and sensor2Value < 0.5 and lastDetectedLine:
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
        """    

    def grabObject(self) -> None:
        """
        Grabbing the currently detected object.

        Returns
        ----------
        None
        """
        # Turning 90° and alining
        self.api.turn(-0.02)
        self.api.align(self.api.Directions.Parallel)

        """
        #keep rotating until both sensors 0 and 3 are over the line
        while True:
            sensor0 = self.api.readSensorValue(0)
            sensor2 = self.api.readSensorValue(2)
            if sensor0 > 0.5 and sensor2 > 0.5: # Adjust Threshold for line detection
                self.api.stop()
                break
        """

        # Rotating and opening the gripper
        self.api.rotateServo(self.api.pwmChFill, 1, 0)
        self.api.rotateServo(self.api.pwmChGrip, 10, 45)

        self.api.drive(self.api.defaultSpeed)

        # Driving forward until limit switch turns on
        while True:
            limitSwitchState = self.api.gpio.getValue(self.api.limitSwitchKitchen)

            if(limitSwitchState):
                time.sleep(2)
                self.api.stop()
                break

            time.sleep(0.1)

        # Closing and lifting the gripper
        self.api.rotateServo(self.api.pwmChGrip, 10, 0)
        self.api.rotateServo(self.api.pwmChFill, 10, 5)

        self.api.drive (-self.api.defaultSpeed)

        # Driving backwards for a specified duration
        self.watch.start(3)
        while True:
            if(self.watch.isFinished()):
                self.api.stop()
                break
            
            time.sleep(0.1)

    def moveToMid(self):
        
        #read sensors for line detection
        sensor0 = self.api.readSensorValue(0)
        sensor2 = self.api.readSensorValue(2)

        if Task.slotCounter == 3:
                self.api.turn(-0.03)
                self.watch.start(1)

                while True:
                    sensor1 = self.api.readSensorValue(1)
                    sensor3 = self.api.readSensorValue(3)
                    
                    if sensor3 > 0.5 and sensor1 > 0.5: # Adjust Threshold for line detection
                        self.api.stop()
                        break
                    break

        if Task.slotCounter > 3:
            #Turn 90 degrees and recognize the line

            self.api.turn(speed=0.03) # Starts rotating at a slow speed

            #keep rotating until both sensors 4 and 5 are over the line
            while True:
                if sensor0 > 0.5 and sensor2 > 0.5: # Adjust Threshold for line detection
                    self.api.stop()
                    break
   
            while Task.slotCounter != 3:
                self.api.drive(0.03)
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

            self.api.turn(0.03)
            while True:
                sensor1 = self.api.readSensorValue(1)
                sensor3 = self.api.readSensorValue(3)
                if sensor3 > 0.5 and sensor1 > 0.5: # Adjust Threshold for line detection
                    self.api.stop()
                    break

        if Task.slotCounter < 3:
            #Turn 90 degrees and recognize the line

            self.api.turn(speed=-0.03) # Starts rotating at a slow speed

            #keep rotating until both sensors 4 and 5 are over the line
            while True:
                sensor0 = self.api.readSensorValue(0)
                sensor2 = self.api.readSensorValue(2)
                if sensor0 > 0.5 and sensor2 > 0.5: # Adjust Threshold for line detection
                    self.api.stop()
                    break

            while Task.slotCounter != 3:
    
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

            self.api.turn(-0.03)
            while True:
                sensor1 = self.api.readSensorValue(1)
                sensor3 = self.api.readSensorValue(3)
                if sensor3 > 0.5 and sensor1 > 0.5: # Adjust Threshold for line detection
                    self.api.stop()
                    break





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
        pass

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

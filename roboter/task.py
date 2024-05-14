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
    lineDetected = False    # Flag to save that both sensors are one the mark

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

    def movePerpendicular(self, modeFactor : int) -> None:
        """
        Helpermethod for changing slots by moving perpendicular to the marks on the floor.

        Parameters
        ----------
        modeFactor: Factor used to differentiate rotating and driving directions

        Returns
        ----------
        None
        """
        # Updating sensor values
        sensor0Value = self.api.readSensorValue(0)
        sensor2Value = self.api.readSensorValue(2)

        # Resetting flag if both sensors are off the mark
        if(sensor0Value < self.api.valueWhite and sensor2Value < self.api.valueWhite):
            self.lineDetected = False

        # Aligning if one sensor is on the mark, setting the flag
        if((sensor0Value > self.api.valueWhite or sensor2Value > self.api.valueWhite) and not self.lineDetected):
            self.api.align(self.api.Directions.Perpendicular)
            self.slotCounter -= modeFactor * 1
            self.lineDetected = True
            self.api.drive(self.api.defaultSpeed)

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
        self.lineDetected = False  
        objectFound = False
        self.api.drive(self.api.defaultSpeed)
        modeFactor = 1

        while not objectFound:
            self.movePerpendicular(modeFactor)

            # Object detection based on mode
            sensor0Value = self.api.readSensorValue(0)
            sensor2Value = self.api.readSensorValue(2)
            sensor7Value = self.api.getSensorValues(7)
            sensor8Value = self.api.getSensorValues(8)

            # Ensuring the robot is on the mark when stopping
            if(sensor0Value > self.api.valueWhite and sensor2Value > self.api.valueWhite):
                match mode:
                    # Glass
                    case 0:
                        if(sensor7Value and not sensor8Value):
                            self.api.stop()
                            objectFound = True

                    # Bottle
                    case 1:
                        if(sensor7Value and sensor8Value):
                            self.api.stop()
                            objectFound = True

            time.sleep(0.1)

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
        # Turning 90° and aligning
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
        self.api.rotateServo(self.api.pwmChFill, 10, 0)
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

        # Driving backwards for a specified duration
        self.api.drive(-self.api.defaultSpeed)
        self.watch.start(3)
        
        while True:
            if(self.watch.isFinished()):
                self.api.stop()
                break
            
            time.sleep(0.1)

    def moveToMid(self):        
        match self.slotCounter:
            # Already in mid
            case 3:
                # Turning for 180°
                self.api.turn(-self.api.defaultSpeed)
                time.sleep(1)       # Ensure the mark doesn't instantly get recongnized again
                self.api.align(self.api.Directions.Parallel)

            # Not in mid
            case _:
                self.switchSlot(3)

        """
        # Updating sensor values
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
        """

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

    def switchSlot(self, targetSlot) -> None:
        """
        Switching a slot and turning back to the original direction
    
        Parameters
        ----------
        targetSlot: Slot the robot should move to

        Returns
        ----------
        None
        """ 

        if(self.slotCounter != targetSlot):
            modeFactor = 0

            # Setting the multiplicator for coming calculations
            if(self.slotCounter < targetSlot):
                modeFactor = -1
            else:
                modeFactor = 1

            # Turning CW or CCW according to multiplicator
            self.api.turn(modeFactor * self.api.defaultSpeed)
            time.sleep(1)

            # Turning until one sensor detects the mark and rotating a little further
            while True:
                sensor0Value = self.api.readSensorValue(0)
                sensor2Value = self.api.readSensorValue(2)

                if(sensor0Value > self.api.valueWhite or sensor2Value > self.api.valueWhite):
                    time.sleep(0.05)
                    self.api.stop()
                    break

            self.api.drive(self.api.defaultSpeed)
            time.sleep(0.5)
            
            while self.slotCounter != targetSlot:            
                self.movePerpendicular(modeFactor)

            # Turning back to previous direction
            self.api.stop()
            time.sleep(0.5)
            self.api.turn(-modeFactor * self.api.defaultSpeed)
            time.sleep(1)
            self.api.align(self.api.Directions.Parallel)

    def place(self) -> None:
        """
        Placing either glass or bottle onto the counter.

        Returns
        ----------
        None
        """
        
        """ 
        #step 1: Transmit the current slot to the partner robot
        #step 2: rotate 180ish degrees
        self.api.turn(self.api.defaultSpeed, 180)

        #step 3: Align with the line
        while True:
            self.api.getSensorValues()
            if sensor > self.api.valueWhite and sensor > self.api.valueWhite:
                self.api.stop()
                break
            else:
                self.api.turn(self.api.defaultSpeed,5)

        #step 4: Drive forward until limit switch triggered
        while self.api.readSensorValue(self.api.limitSwitchBar) == 0:
            self.api.drive(self.api.defaultSpeed)

        self.api.stop()

        #step 5: lower and open gripper
        self.api.rotateServo(self.api.pwmChGrip, 10, 90)

        self.api.rotateServo(self.api.pwmChGrip, 10, 0)
        
        #moveToEndPos()
        """

    def fill(self) -> None:
        """
        Filling the glass with the bottle by tipping it over its head.

        Returns
        ----------
        None
        """

        """
        #step 1: drive backwards until limit switch goes off
        while self.api.readSensorValue(self.api.limitSwitchBar) == 0:
            self.api.drive(-self.api.defaultSpeed)
        self.api.stop()

        #step 2: lift the gripper
        self. api.rotateServo(self.api.pwmChGrip, 10, 90) # 10 steps to 90 degrees

        #step 3: wait until upper switch goes off
        while self.api.readSensorValue(self.api.limitSwitchKitchen) == 0:
            pass # waiting for loop being true

        #step 4: wait for a defined time
        time.sleep(5)

        #step 5: lower the gripper
        self.api.rotateServo(self.api.pwmChGrip, 10, 0) #10 steps back to 0 degrees
        #step 6: moveToEndPos
        """
        

    def moveToEndPos(self, mode : int) -> None:
        """
        Moving the robot to the end position based on the specified mode

        Parameters
        ----------
        mode: Specifying the endposition based on what object got handled
        mode 0 = Glass
        mode 1 = Bottle

        Returns
        ----------
        None
        """
        pass

#region Imports

from config import Config
from api import API
from sharedData import SharedData
from communication import Communication
from audioManager import AudioManager
from statusDisplay import StatusDisplay
from stopWatch import StopWatch

import time

#endregion

class Task:
    """
    Class for detailed tasks the robot should do

    Parameters
    ----------
    mode:           Specifying what object should be handeled
    api:            Object of the API class
    sharedData:     Object of the SharedData class
    communication:  Object of the Communication class
    audio:          Object of the AudioManager class
    statusLed:      Object of the StatusDisplay class
    watch:          Object of the StopWatch class
    """

    slotCounter = 6
    lineDetected = False    # Flag to save that both sensors are one the mark

    def __init__(self, mode : int, config : Config, api : API, sharedData : SharedData, communication : Communication, audio : AudioManager, statusLed : StatusDisplay, watch : StopWatch):
        """
        Initializes the Task object with default values.
        """
        self.mode = mode
        self.config = config
        self.api = api
        self.sharedData = sharedData
        self.com = communication
        self.audio = audio
        self.statusLed = statusLed
        self.watch = watch

    def movePerpendicular(self, calcFactor : int) -> None:
        """
        Helpermethod for changing slots by moving perpendicular to the marks on the floor.

        Parameters
        ----------
        calcFactor: Factor used to calculate slots properly
            = 1  -> Current slot > target slot\n
            = -1 -> Current slot < target slot

        Returns
        ----------
        None
        """
        # Updating sensor values
        sensor0Value = self.api.readSensorValue(0)
        sensor2Value = self.api.readSensorValue(2)

        # Resetting flag if both sensors are off the mark
        if(sensor0Value < self.config.minValueWhite and sensor2Value < self.config.minValueWhite):
            self.lineDetected = False

        # Aligning if one sensor is on the mark, setting the flag
        if((sensor0Value > self.config.minValueWhite or sensor2Value > self.config.minValueWhite) and not self.lineDetected):
            print("Found line")
            print("Sensor 0: {}".format(self.api.readSensorValue(0)))
            print("Sensor 2: {}".format(self.api.readSensorValue(2)))
            print("")

            self.api.align(self.config.Directions.Perpendicular)
            self.slotCounter -= calcFactor * 1
            self.lineDetected = True
            self.api.drive(self.config.defaultSpeed)

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
        # Variables
        self.lineDetected = False  
        objectFound = False
        calcFactor = 1

        self.api.drive(self.config.defaultSpeed)

        while not objectFound:
            self.movePerpendicular(calcFactor)

            # Object detection based on mode
            sensor0Value = self.api.readSensorValue(0)
            sensor2Value = self.api.readSensorValue(2)
            sensor7Value = self.api.readSensorValue(7)
            sensor8Value = self.api.readSensorValue(8)

            # Ensuring the robot is on the mark when stopping
            if(sensor0Value > self.config.minValueWhite and sensor2Value > self.config.minValueWhite):
                match mode:
                    case 0: # Glass
                        if(sensor7Value and not sensor8Value):
                            self.api.stop()
                            objectFound = True

                    case 1: # Bottle
                        if(sensor7Value and sensor8Value):
                            self.api.stop()
                            objectFound = True

            time.sleep(0.1)

    def grabObject(self) -> None:
        """
        Grabbing the currently detected object.

        Returns
        ----------
        None
        """
        # Turning 90° CCW and aligning
        self.api.turn(-0.02)
        self.api.align(self.config.Directions.Parallel)

        # Lowering and opening the gripper
        self.api.rotateServo(self.config.pwmChFill, 10, 0)
        self.api.rotateServo(self.config.pwmChGrip, 10, 45)

        self.api.drive(self.config.defaultSpeed)

        # Driving forward until limit switch turns on
        while True:
            limitSwitchState = self.api.gpio.getValue(self.config.gpioChLimitSwitchGripper)

            if(limitSwitchState):
                time.sleep(2)
                self.api.stop()
                break

            time.sleep(0.1)

        # Closing and lifting the gripper
        self.api.rotateServo(self.config.pwmChGrip, 10, 0)
        self.api.rotateServo(self.config.pwmChFill, 10, 5)

        # Driving backwards for a specified duration
        self.api.drive(-self.config.defaultSpeed)
        self.watch.start(3)
        
        while True:
            if(self.watch.isFinished()):
                self.api.stop()
                break
            
            time.sleep(0.1)

    def moveToMid(self) -> None:
            """
            Moving to the middle slot, doing nothing if already in mid
            
            Returns
            ----------
            None
            """
            # Current slot > mid slot
            if(self.slotCounter > 3):
                turnFactor = 1
                self.switchSlot(3, turnFactor)

            # Current slot < mid slot
            else:
                turnFactor = -1
                self.switchSlot(3, turnFactor)

            self.api.turn(-turnFactor)
            time.sleep(1)
            self.api.align(self.config.Directions.Parallel)

    def moveToCounter(self) -> None:
        """
        Driving to the counter, switching slot if an obstacle is in the way.

        Returns
        ----------
        None
        """
        # Drive backwards
        self.api.drive(-self.config.defaultSpeed)

        # Drive to end Line
        while True:
            sensor6Value = self.api.readSensorValue(6)
            sensor0Value = self.api.readSensorValue(0)
            sensor2Value = self.api.readSensorValue(2)

            # Switch Slot
            if (sensor6Value > self.config.minValueWhite): 
                turnFactor = 1
                self.api.stop()
                self.switchSlot(2, turnFactor)

                # Turning to original orientation
                self.api.turn(-turnFactor)
                time.sleep(1)
                self.api.align(self.config.Directions.Parallel)

                self.api.drive(-self.config.defaultSpeed)  
            
            # Drive to end Line and align
            if (sensor0Value > self.config.minValueWhite or sensor2Value > self.config.minValueWhite): 
                self.api.stop()
                self.api.align(self.config.Directions.Perpendicular)
                break
            
            time.sleep(0.1)
        
    def switchSlot(self, targetSlot : int, turnFactor : int) -> None:
        """
        Switching a slot, always drives forward (gripper direction). Not turning back to original orientation.
    
        Parameters
        ----------
        targetSlot: Slot the robot should move to
        turnFactor: Factor used to differentiate rotating directions
            = 1  -> Rotate CW\n
            = -1 -> Rotate CCW

        Returns
        ----------
        None
        """ 

        # Doing nothing if the current slot already is the target slot
        if(self.slotCounter != targetSlot):
            calcFactor = 0

            # Setting the multiplicator for coming calculations in movePerpendicular()
            if(self.slotCounter < targetSlot):
                calcFactor = -1
            else:
                calcFactor = 1

            # Turning CW or CCW according to multiplicator
            self.api.turn(turnFactor * self.config.defaultSpeed)
            time.sleep(1)

            # Turning until one sensor detects the mark and rotating a little further
            while True:
                sensor0Value = self.api.readSensorValue(0)
                sensor2Value = self.api.readSensorValue(2)

                if(sensor0Value > self.config.minValueWhite or sensor2Value > self.config.minValueWhite):
                    time.sleep(0.05)
                    self.api.stop()
                    break
            
            # Changing slot
            self.api.drive(self.config.defaultSpeed)
            time.sleep(0.5)
            
            while self.slotCounter != targetSlot:            
                self.movePerpendicular(calcFactor)

    def place(self) -> None:
        """
        Placing either glass or bottle onto the counter.

        Returns
        ----------
        None
        """

        # Transmitting the current slot to the partner robot
        self.com.sendMessage(2, self.slotCounter)

        # Rotating for 180°        
        self.api.turn(self.config.defaultSpeed)
        time.sleep(1)
        self.api.align(self.config.Directions.Parallel)

        self.api.drive(self.config.defaultSpeed)

        # Driving forward until limit switch turns on
        while True:
            limitSwitchState = self.api.gpio.getValue(self.config.gpioChLimitSwitchGripper)

            if(limitSwitchState):
                time.sleep(2)
                self.api.stop()
                break

            time.sleep(0.1)

        # Lowering and opening the gripper
        self.api.rotateServo(self.config.pwmChGrip, 10, 90)
        self.api.rotateServo(self.config.pwmChGrip, 10, 0)
        
    def fill(self) -> None:
        """
        Filling the glass with the bottle by tipping it over its head.

        Returns
        ----------
        None
        """

        self.api.drive(-self.config.defaultSpeed)

        # Driving backward until limit switch turns on
        while True:
            limitSwitchState = self.api.gpio.getValue(self.config.gpioChLimitSwitchHopper)

            if(limitSwitchState):
                time.sleep(2)
                self.api.stop()
                break

            time.sleep(0.1)

        # Lifting the gripper and waiting for the water to drain
        self. api.rotateServo(self.config.pwmChFill, 10, 85)
        time.sleep(3)

        # Lowering the gripper
        self.api.rotateServo(self.config.pwmChFill, 10, 5)

    def moveToEndPos(self) -> None:
        """
        Moving the robot to the end position based on the specified mode

        Parameters
        ----------
        mode: Specifying the endposition based on what object got handled
            0 = Glass\n
            1 = Bottle

        Returns
        ----------
        None
        """
        # Setting a factor to define movement direction of robot based on mode
        match self.mode:
            case 0:
                modeFactor = -1
            case 1:
                modeFactor = 1
        
        # Driving backward and check for line
        self.api.drive(modeFactor * self.config.defaultSpeed)

        while True:
            # Updating sensor values
            sensor0Value = self.api.readSensorValue(0)
            sensor2Value = self.api.readSensorValue(2)
            
            # Checking if both sensors are on the mark, correcting if not
            if(sensor0Value > self.config.minValueWhite and sensor2Value > self.config.minValueWhite):
                self.api.stop()
                break
            # Correction depending on mode (Either gripper or hopper in driving direction)
            if(sensor0Value > self.config.minValueWhite):
                self.api.setMotorSpeeds(0, -modeFactor * 0.005)
            elif(sensor2Value > self.config.minValueWhite):
                self.api.setMotorSpeeds(modeFactor * 0.005, 0)

        match self.mode:
            case 0:
                # Switching slot
                self.switchSlot(1, -1)
            
                # Driving a little further, then stopping and giving permission to partner robot
                self.api.drive(self.config.defaultSpeed)
                time.sleep(2)
                self.api.stop()
                self.com.sendMessage(1, True)

            case 1:
                # Switching slot
                self.switchSlot(4, 1)

                # Turning 90°
                self.api.turn(-self.config.defaultSpeed)
                time.sleep(1)
                self.api.align(self.config.Directions.Parallel)
                
                # Driving forward until limit switch turns on
                while True:
                    limitSwitchState = self.api.gpio.getValue(self.config.gpioChLimitSwitchGripper)

                    if(limitSwitchState):
                        time.sleep(2)
                        self.api.stop()
                        break

                time.sleep(0.1)

                # Lowering and opening gripper
                self.api.rotateServo(self.config.pwmChFill, 10, 0)
                self.api.rotateServo(self.config.pwmChGrip, 10, 45)

                # Driving backward a little
                self.api.drive(-self.config.defaultSpeed)
                time.sleep(2)
                self.api.stop()
            
            case _:
                print("Unknown mode!")
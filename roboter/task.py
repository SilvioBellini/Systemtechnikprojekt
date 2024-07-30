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
    config:         Object of the Config class
    api:            Object of the API class
    sharedData:     Object of the SharedData class
    communication:  Object of the Communication class
    audio:          Object of the AudioManager class
    statusLed:      Object of the StatusDisplay class
    watch:          Object of the StopWatch class
    """

    slotCounter = 6
    lineDetected = False    # Flag to save that both sensors are one the mark

    def __init__(self, config : Config, api : API, sharedData : SharedData, communication : Communication, audio : AudioManager, statusLed : StatusDisplay, watch : StopWatch):
        # Initializing instances
        self.config = config
        self.api = api
        self.sharedData = sharedData
        self.com = communication
        self.audio = audio
        self.statusLed = statusLed
        self.watch = watch
        self.sillWatch = StopWatch()
        self.backwardsWatch = StopWatch()

    # region Helpermethods

    def teachValues(self):
        difference = 900

        sensor0Value = self.api.readSensorValue(0)
        sensor1Value = self.api.readSensorValue(1)
        sensor2Value = self.api.readSensorValue(2)
        sensor3Value = self.api.readSensorValue(3)
        sensor4Value = self.api.readSensorValue(4)
        sensor5Value = self.api.readSensorValue(5)

        self.config.setValueWhite0(sensor0Value, sensor0Value + difference)
        self.config.setValueWhite1(sensor1Value, sensor1Value + difference)
        self.config.setValueWhite2(sensor2Value, sensor2Value + difference)
        self.config.setValueWhite3(sensor3Value, sensor3Value + difference)
        self.config.setValueWhite4(sensor4Value, sensor4Value + difference)
        self.config.setValueWhite5(sensor5Value, sensor5Value + difference)

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
        self.api.drive(self.config.defaultSpeed)

        # Updating sensor values
        sensor0Value = self.api.readSensorValue(0)
        sensor2Value = self.api.readSensorValue(2)

        # Resetting flag if both sensors are off the mark
        if(sensor0Value < self.config.minValueWhite0 and sensor2Value < self.config.minValueWhite2):
            self.lineDetected = False

        # Aligning if one sensor is on the mark, setting the flag
        if((sensor0Value > self.config.minValueWhite0 or sensor2Value > self.config.minValueWhite2) and not self.lineDetected):
            self.api.align(self.config.Directions.Perpendicular)
            self.slotCounter -= calcFactor * 1
            self.lineDetected = True

    def followLine(self, delayTime):
        sensor4Value = self.api.readSensorValue(4)
        sensor5Value = self.api.readSensorValue(5)
        
        if(self.watch.isFinished()):
                # Checking if sensor 4 or 5 is on the line, correcting if so
                if((sensor4Value > self.config.minValueWhite4 and sensor4Value < self.config.minValueGrey) and not sensor5Value > self.config.minValueWhite5):
                    self.api.stop()
                    self.api.setMotorSpeeds(-0.02, 0)
                    time.sleep(0.3)

                    self.api.stop()
                    self.api.drive(-self.config.defaultSpeedFast)
                    self.watch.start(delayTime)

                elif((sensor5Value > self.config.minValueWhite5 and sensor5Value < self.config.minValueGrey) and not sensor4Value > self.config.minValueWhite4):
                    self.api.stop()
                    self.api.setMotorSpeeds(0, -0.02)
                    time.sleep(0.3)

                    self.api.stop()
                    self.api.drive(-self.config.defaultSpeedFast)
                    self.watch.start(delayTime)

    def switchSlot(self, targetSlot : int, turnFactor : int) -> None:
        """
        Switching a slot, always drives forward (gripper direction). Not turning back to original orientation.
    
        Parameters
        ----------
        targetSlot: Slot the robot should move to
        turnFactor: Factor used to differentiate rotating directions
            = 1  -> Rotate CCW\n
            = -1 -> Rotate CW

        Returns
        ----------
        None
        """ 
        
        print("Switching slot from {} to {}".format(self.slotCounter, targetSlot))

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

            # Turning until sensors detect the mark and rotating a little further
            while True:
                sensor0Value = self.api.readSensorValue(0)
                sensor2Value = self.api.readSensorValue(2)

                if(sensor0Value > self.config.minValueWhite0 and sensor2Value > self.config.minValueWhite2):
                    time.sleep(0.1)
                    self.api.stop()
                    break
            
            time.sleep(0.5)
            
            # Changing slot
            self.api.drive(self.config.defaultSpeed)
            time.sleep(0.5)
            
            while self.slotCounter != targetSlot:            
                self.movePerpendicular(calcFactor)

    # endregion

    # region Main methods
    
    def findObject(self, mode : int) -> None:
        """
        Finding either the glass or bottle specified with the mode.

        Parameters
        ----------
        mode: Specifying what object should be 
            0 = Glass\n
            1 = Bottle

        Returns
        ----------
        None
        """

        print("Searching for Object")

        self.teachValues()

        # Variables
        self.lineDetected = False  
        objectFound = False
        calcFactor = 1

        self.api.drive(self.config.defaultSpeed)
        
        while True:
            self.movePerpendicular(calcFactor)

            # Object detection based on mode
            sensor0Value = self.api.readSensorValue(0)
            sensor2Value = self.api.readSensorValue(2)
            sensor7Value = self.api.readSensorValue(7)
            sensor8Value = self.api.readSensorValue(8)

            match mode:
                case 0: # Glass
                    if(sensor7Value and not sensor8Value):
                        objectFound = True
                        self.api.drive(self.config.defaultSpeedSlow)

                case 1: # Bottle
                    if(sensor7Value and sensor8Value):
                        objectFound = True
                        self.api.drive(self.config.defaultSpeedSlow)

            # Ensuring the robot is on the mark when stopping
            if(sensor0Value > self.config.minValueWhite0 and sensor2Value > self.config.minValueWhite2 and objectFound):
                print("\nSensor 0: ", sensor0Value)
                print("Sensor 2: ", sensor2Value)
                print("")
                self.api.stop()
                break
                
            time.sleep(0.05)

    def grabObject(self) -> None:
        """
        Grabbing the currently detected object.

        Returns
        ----------
        None
        """

        print("Grabbing Object")
        time.sleep(0.5)

        # Turning 90° CCW and aligning
        self.api.turn(self.config.defaultSpeed)
        self.api.align(self.config.Directions.Parallel)

        # Lowering and opening the gripper
        time.sleep(0.1)
        self.api.rotateServo(self.config.pwmChFill, 50, 0)
        self.api.rotateServo(self.config.pwmChGrip, 50, 0)

        time.sleep(0.1)
        self.api.drive(self.config.defaultSpeed)

        # Driving forward until limit switch turns on
        while True:
            limitSwitchState = self.api.gpio.getValue(self.config.gpioChLimitSwitchGripper)

            if(not limitSwitchState):       # Normally True
                #time.sleep(0.5)
                self.api.stop()
                break

            time.sleep(0.1)

        # Closing and lifting the gripper, driving back a little in between to prevent displacement of robot
        time.sleep(0.1)
        self.api.rotateServo(self.config.pwmChGrip, 10, 25)

        time.sleep(0.1)
        self.api.drive(-self.config.defaultSpeed)

        time.sleep(0.2)
        self.api.stop()
        self.api.rotateServo(self.config.pwmChFill, 10, 5)

        # Driving backwards for a specified distance (0.1 m)
        self.api.drive(-self.config.defaultSpeed)
        self.backwardsWatch.start(0.1 / self.config.defaultSpeed)
        self.watch.start(0.1)
        
        while True:
            self.followLine(0.1)

            if(self.backwardsWatch.isFinished()):
                self.api.stop()
                break
            
            time.sleep(0.1)

        time.sleep(0.5)

    def moveToMid(self) -> None:
            """
            Moving to the middle slot, doing nothing if already there
            
            Returns
            ----------
            None
            """

            print("Moving to middle slot")

            if(self.slotCounter != 3):
                # Current slot > mid slot
                if(self.slotCounter > 3):
                    turnFactor = -1
                    self.switchSlot(3, turnFactor)

                # Current slot < mid slot
                else:
                    turnFactor = 1
                    self.switchSlot(3, turnFactor)
                
                time.sleep(0.2)
                self.api.turn(-turnFactor * self.config.defaultSpeed)
                time.sleep(1)
                self.api.align(self.config.Directions.Parallel)

            time.sleep(0.5)

    def moveToCounter(self) -> None:
        """
        Driving to the counter, switching slot if an obstacle is in the way.

        Returns
        ----------
        None
        """

        print("Moving to Counter")

        # Granting approval for the kitchen to the partner robot
        self.com.sendMessage(0, True)

        # Drive backwards
        self.api.drive(-self.config.defaultSpeedFast)
        self.sillWatch.start(10)

        # Drive to end Line
        while True:
            sensor0Value = self.api.readSensorValue(0)
            sensor2Value = self.api.readSensorValue(2)
            sensor6Value = self.api.readSensorValue(6)

            # Drive to end line and align
            if(self.sillWatch.isFinished()):
                if(sensor0Value > self.config.minValueWhite0 and sensor2Value > self.config.minValueWhite2):
                    print("Stopping")
                    self.api.stop()
                    time.sleep(1)
                    #self.api.align(self.config.Directions.Perpendicular)
                    break

            # Switch Slot
            if (sensor6Value > self.config.minValueObstacle):
                print("Recognized obstacle")
                turnFactor = -1
                self.api.stop()
                self.switchSlot(2, turnFactor)

                # Turning to original orientation
                self.api.turn(-turnFactor * self.config.defaultSpeed)
                time.sleep(1)
                self.api.align(self.config.Directions.Parallel)

                self.api.drive(-self.config.defaultSpeedFast)

            self.followLine(0.5)
            time.sleep(0.02)

    def place(self) -> None:
        """
        Placing either glass or bottle onto the counter.

        Returns
        ----------
        None
        """

        print("Placing glass")

        # Transmitting the current slot to the partner robot
        self.com.sendMessage(2, self.slotCounter)

        # Rotating for 180°
        for i in range(2):
            self.api.turn(self.config.defaultSpeed)
            time.sleep(1)
            self.api.align(self.config.Directions.Parallel)
            time.sleep(0.1)

        self.api.drive(self.config.defaultSpeed)

        # Driving forward until limit switch turns on
        while True:
            limitSwitchState = self.api.gpio.getValue(self.config.gpioChLimitSwitchGripper)

            if(not limitSwitchState):   # Normally True
                time.sleep(1)
                self.api.stop()
                break

            time.sleep(0.1)

        # Lowering and opening the gripper
        self.api.rotateServo(self.config.pwmChFill, 20, 0)
        self.api.rotateServo(self.config.pwmChGrip, 50, 0)
        
    def fill(self) -> None:
        """
        Filling the glass with the bottle by tipping it over its head.

        Returns
        ----------
        None
        """

        print("Filling glas")

        self.api.drive(-self.config.defaultSpeed)

        # Driving backward until limit switch turns on
        while True:
            self.followLine(0.1)
            limitSwitchState = self.api.gpio.getValue(self.config.gpioChLimitSwitchHopper)

            if(not limitSwitchState):   # Normally True
                time.sleep(0.5)
                self.api.stop()
                break

            time.sleep(0.1)

        # Lifting the gripper and waiting for the water to drain
        self. api.rotateServo(self.config.pwmChFill, 100, 85)
        time.sleep(7)

        # Lowering the gripper
        self.api.rotateServo(self.config.pwmChFill, 100, 5)

    def moveToEndPos(self, mode) -> None:
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

        print("Moving to end position")
        
        # Setting a factor to define movement direction of robot based on mode
        match mode:
            case 0:
                modeFactor = -1
            case 1:
                modeFactor = 1
        
        # Driving backward and check for line
        self.api.drive(modeFactor * self.config.defaultSpeed)

        while True:
            if(mode == 0):
                self.followLine(0.1)

            # Updating sensor values
            sensor0Value = self.api.readSensorValue(0)
            sensor2Value = self.api.readSensorValue(2)

            # Checking if both sensors are on the mark, correcting if not
            if(sensor0Value > self.config.minValueWhite0 and sensor2Value > self.config.minValueWhite2):
                self.api.stop()
                time.sleep(0.1)
                break
            # Correction depending on mode (Either gripper or hopper in driving direction)
            if(sensor0Value > self.config.minValueWhite0):
                self.api.setMotorSpeeds(modeFactor * 0.01, 0)
            elif(sensor2Value > self.config.minValueWhite2):
                self.api.setMotorSpeeds(0, modeFactor * 0.01)
            
            time.sleep(0.05)

        match mode:
            case 0:
                # Switching slot
                self.switchSlot(1, 1)
            
                # Driving a little further, then stopping and giving permission to partner robot
                self.api.drive(self.config.defaultSpeed)
                time.sleep(0.15 / self.config.defaultSpeed)
                self.api.stop()
                self.com.sendMessage(1, True)

            case 1:
                # Switching slot
                self.switchSlot(4, 1)

                # Turning 90°
                self.api.turn(self.config.defaultSpeed)
                time.sleep(2)
                self.api.align(self.config.Directions.Parallel)

                time.sleep(0.5)
                self.api.drive(self.config.defaultSpeed)
                
                # Driving forward until limit switch turns on
                while True:
                    limitSwitchState = self.api.gpio.getValue(self.config.gpioChLimitSwitchGripper)

                    if(not limitSwitchState):   # Normally True
                        time.sleep(0.5)
                        self.api.stop()
                        break

                    time.sleep(0.1)

                # Lowering and opening gripper
                self.api.rotateServo(self.config.pwmChFill, 50, 0)
                self.api.rotateServo(self.config.pwmChGrip, 50, 0)

                # Driving backward a little
                self.api.drive(-self.config.defaultSpeed)
                time.sleep(2)
                self.api.stop()
            
            case _:
                print("Unknown mode!")

    # endregion
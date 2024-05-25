from enum import Enum
from typing import List

import driver
import flink        
import math
import time

class API:
    """
    Class for basic functions of the robot (locomotion, sensors, etc.)
    """
    #region Classattributes

    # PWM Channels
    pwmChLeftA = 2  # Chanel vertauscht mit Herrn Graf - Motoren funktionieren
    pwmChLeftB = 0  # Chanel vertauscht mit Herrn Graf - Motoren funktionieren
    pwmChRightA = 6 # Chanel vertauscht mit Herrn Graf - Motoren funktionieren
    pwmChRightB = 4 # Chanel vertauscht mit Herrn Graf - Motoren funktionieren
    pwmChFill = 10
    pwmChGrip = 12
    activateServoCh = 18

    # FQD Channels
    fqdLeft = 0
    fqdRight = 1

    # GPIO Channels
    enableServo = 18
    sensorChBottle = 21
    sensorChGlas = 23
    modeCh1 = 4
    modeCh2 = 6
    modeCh4 = 8
    modeCh8 = 10
    limitSwitchGripper = 13
    limitSwitchHopper = 15

    # Configuration motors
    ts = 0.01
    kp = 0.1
    tn = 0.011                  # 0.011   # 0.1
    ticksPerRotation = 256      # 256     # 100
    gearRatio = 152/1            # 152/1   # 16/1
    motorVoltage = 5
    pwmFreq = 50

    # Globally used values    
    defaultSpeed = 0.03
    Directions = Enum("Directions", ["Perpendicular", "Parallel"])
    amountOfSensors = 4 # 7

    valueWhite = 1000
    valueGrey = 600

    #endregion

    def __init__(self):
        # Initializing instances
        self.m1 = driver.SignMagnitude(self.ts, self.pwmChLeftA, self.pwmChLeftB, self.fqdLeft, self.ticksPerRotation, self.motorVoltage, self.gearRatio, self.kp, self.tn)
        self.m2 = driver.SignMagnitude(self.ts, self.pwmChRightA, self.pwmChRightB, self.fqdRight, self.ticksPerRotation, self.motorVoltage, self.gearRatio, self.kp, self.tn)
        
        self.gpio = flink.FlinkGPIO()
        self.pwm = flink.FlinkPWM()

        self.sensorValues : List[int] = []
        self.gpio.setDir(self.sensorChBottle, False)
        self.gpio.setDir(self.sensorChGlas, False)
        self.gpio.setDir(self.activateServoCh, True)

        self.gpio.setDir(self.modeCh1, False)
        self.gpio.setDir(self.modeCh2, False)
        self.gpio.setDir(self.modeCh4, False)
        self.gpio.setDir(self.modeCh8, False)

    def setMotorSpeeds(self, leftSpeed : float, rightSpeed : float) -> None:
        """
        Helper method to set the speed for both motors individually.
        Turns the input from m/s in rad/s. w = v / r

        Parameters
        ----------
        leftSpeed: Speed for the left motor in m/s
        rightSpeed: Speed for the right motor in m/s

        Returns
        ----------
        None
        """

        wheelRadius = 0.03265 # meters
        self.m1.setSpeed(leftSpeed / wheelRadius)
        self.m2.setSpeed(rightSpeed / wheelRadius)        

    def drive(self, speed : float) -> None:
        """
        Letting both of the robot's wheels move with the same speed and direction by setting to opposite speeds
        because the motors face opposite ways.

        Parameters
        ----------
        speed: Speed with which the wheels turn in m/s
            > 0: Forward
            < 0: Backward
        
        Returns
        ----------
        None
        """
        
        self.setMotorSpeeds(speed, -speed)

    def turn(self, speed : float, angle : float) -> None:
        """
        Letting both of the robot's wheels move with the same speed but with opposite direction by setting to the same
        speeds because the motors face opposite ways, resulting in a rotation of the robot for a specified angle.

        Parameters
        ----------
        speed: Speed with which the wheels turn in m/s
            > 0: Clockwise
            < 0: Counterclockwise
        angle: Angle by which the robot should rotate

        Returns
        ----------
        None
        """

        # Setting the desired speed for both motors
        self.setMotorSpeeds(speed, speed)

    def stop(self) -> None:
        """
        Stopping the robot's current movement by setting the wheels speed to 0.

        Returns
        ----------
        None
        """

        self.setMotorSpeeds(0.0, 0.0)

    def getSensorValues(self) -> None:
        """
        Getting every sensor's current value and saving it to a list.
        Should be called before using readSensorValue().
 
        Returns
        ----------
        None
        """

        self.irSensors = flink.FlinkReflectiveSensor()
        self.sensorValues = [self.irSensors.getValue(i) for i in range(self.amountOfSensors)]

        self.sensorValues.append(self.gpio.getValue(self.sensorChGlas))
        self.sensorValues.append(self.gpio.getValue(self.sensorChBottle))
 
    def readSensorValue(self, index : int) -> int:
        """
        Getting the last saved value of a specific sensor.
        Should only be called after using getSensorValues().
 
        Parameters
        ----------
        index: Specified index of the targeted sensor (Documentation)
 
        Returns
        ----------
        int
        """

        self.getSensorValues()
        
        return self.sensorValues[index]

    def align(self, direction : Directions) -> None:
        """
        Aligning the robot to the marks on the floor depending on the direction the robot is currently moving

        Parameters
        ----------
        direction: Direction in which the robot is moving using an enumerator
            Parallel:       Aligning parallel to the marks on the floor
            Perpendicular:  Aligning perpendicular to the marks on the floor

        Returns
        ----------
        None
        """
        while True:
            match direction:
                case self.Directions.Perpendicular:
                    # Updating sensor values
                    sensor0Value = self.readSensorValue(0)
                    sensor2Value = self.readSensorValue(2)
                    
                    # Checking if both sensors are on the mark, correcting if not
                    if(sensor0Value > self.valueWhite and sensor2Value > self.valueWhite):
                        self.stop()
                        break
                    if(sensor0Value > self.valueWhite):
                        self.setMotorSpeeds(0, -0.005)
                    elif(sensor2Value > self.valueWhite):
                        self.setMotorSpeeds(0.005, 0)

                case self.Directions.Parallel:
                    # Updating sensor values
                    sensor1Value = self.readSensorValue(1)
                    sensor3Value = self.readSensorValue(3)

                    # Stopping if both sensors are on the marks after moving a little futher
                    # Might need to get reworked if sensor 1 gets off the mark while rotating
                    if(sensor1Value > self.valueWhite and sensor3Value > self.valueWhite):
                        time.sleep(0.05)
                        self.stop()
                        break
            
            time.sleep(0.1)

    def rotateServo(self, channel : int, stepCount : int, angle : float) -> None:
        """
        Rotating the gripper/arm for a specified angle using a servo

        Parameters
        ----------
        channel: Channel of the motor that should rotate
        stepCount: Number of steps to reach final Angle
        angle: Angle by which the gripper should rotate
                    Grip: 0° = Closed
                    Fill: 0° = Horizontal front

        Returns
        ----------
        None
        """
        
        # Enabling servo motors
        self.gpio.setValue(self.activateServoCh, True)

        # Limits
        minAngle = 0
        maxAngle = 270 
        minHighTimeMs = 0.5
        maxHighTimeMs = 2.5

        # Ensuring that the angle is within the valid range
        angle = max(min(angle, maxAngle), minAngle)

        # Calculating highTime in milliseconds (0.5 - 2.5) and converting it to a factor of the frequency
        highTimeMs = minHighTimeMs + (angle / maxAngle) * (maxHighTimeMs - minHighTimeMs)
        highTimeFactor = (highTimeMs * self.pwmFreq) / 1000
   
        # Calculating current angle/highTime
        period = self.pwm.getBaseClock() / self.pwmFreq
        currentHighTimeFactor = self.pwm.getHighTime(channel) / period

        # Cancelling method if target angle is current angle
        if(currentHighTimeFactor == highTimeFactor):
            print("Already there")
            return None
        
        # Rotating servo in steps
        currentStep = 1

        while currentStep <= stepCount:
            highTimeFactorStep = (highTimeFactor - currentHighTimeFactor) * (currentStep / stepCount)
            self.pwm.setPeriod(channel, int(period))
            self.pwm.setHighTime(channel, int(period * (currentHighTimeFactor + highTimeFactorStep)))
            
            currentStep += 1
            time.sleep(0.025)
        
        # Disabling servo motors
        self.gpio.setValue(self.activateServoCh, False)

    def getMode(self) -> int:
        """
        Getting and returning the mode that specifies what object has to be handeled as an integer (0-15)
        0:  Glass
        1:  Bottle

        Returns:
        ----------
        int
        """
        
        # Reading each input signal and converting it to an integer from 0-15
        inputValues = [self.gpio.getValue(self.modeCh1), self.gpio.getValue(self.modeCh2), self.gpio.getValue(self.modeCh4), self.gpio.getValue(self.modeCh8)]
        mode = 0

        for i in range(inputValues.__len__()):
            if(inputValues[i]):
                mode += 2 ** i

        return mode
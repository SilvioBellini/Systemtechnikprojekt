from enum import Enum
from typing import List

import driver
import flink        
import math
import time

from config import Config

class API:
    """
    Class for basic functions of the robot (locomotion, sensors, etc.)

    Parameters
    ----------
    config: Object of the Config class
    """
    
    def __init__(self, config : Config):
        # Initializing instances
        self.config = config
        self.m1 = driver.SignMagnitude(self.config.ts, self.config.pwmChLeftA, self.config.pwmChLeftB, self.config.fqdChLeft, self.config.ticksPerRotation, self.config.motorVoltage, self.config.gearRatio, self.config.kp, self.config.tn)
        self.m2 = driver.SignMagnitude(self.config.ts, self.config.pwmChRightA, self.config.pwmChRightB, self.config.fqdChRight, self.config.ticksPerRotation, self.config.motorVoltage, self.config.gearRatio, self.config.kp, self.config.tn)
        
        self.gpio = flink.FlinkGPIO()
        self.pwm = flink.FlinkPWM()
        self.sensorValues : List[int] = []

        # Setting GPIO Directions
        self.gpio.setDir(self.config.gpioChStart, False)
        self.gpio.setDir(self.config.gpioChStop, False)

        self.gpio.setDir(self.config.gpioChMode1, False)
        self.gpio.setDir(self.config.gpioChMode2, False)
        self.gpio.setDir(self.config.gpioChMode4, False)
        self.gpio.setDir(self.config.gpioChMode8, False)

        self.gpio.setDir(self.config.gpioChLimitSwitchGripper, False)
        self.gpio.setDir(self.config.gpioChLimitSwitchHopper, False)

        self.gpio.setDir(self.config.gpioChSleepDrive, True)
        self.gpio.setDir(self.config.gpioChEnableServo, True)

        self.gpio.setDir(self.config.gpioChSensorBottle, False)
        self.gpio.setDir(self.config.gpioChSensorGlass, False)


    def setMotorSpeeds(self, leftSpeed : float, rightSpeed : float) -> None:
        """
        Helper method to set the speed for both motors individually. Setting to opposite speeds
        because the motors face opposite ways.
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
        self.m1.setSpeed(-leftSpeed / wheelRadius)
        self.m2.setSpeed(rightSpeed / wheelRadius)

    def drive(self, speed : float) -> None:
        """
        Letting both of the robot's wheels move with the same speed and direction.

        Parameters
        ----------
        speed: Speed with which the wheels turn in m/s
            > 0: Forward
            < 0: Backward
        
        Returns
        ----------
        None
        """
        
        #self.gpio.setValue(self.config.gpioChSleepDrive, False)
        self.setMotorSpeeds(speed, speed)

    def turn(self, speed : float) -> None:
        """
        Letting both of the robot's wheels move with the same speed but with opposite directions.

        Parameters
        ----------
        speed: Speed with which the wheels turn in m/s
            > 0: Counterclockwise
            < 0: Clockwise

        Returns
        ----------
        None
        """

        # Setting the desired speed for both motors
        #self.gpio.setValue(self.config.gpioChSleepDrive, False)
        self.setMotorSpeeds(-speed, speed)

    def stop(self) -> None:
        """
        Stopping the robot's current movement by setting the wheels speed to 0.

        Returns
        ----------
        None
        """

        self.setMotorSpeeds(0.0, 0.0)
        #self.gpio.setValue(self.config.gpioChSleepDrive, True)

    def getSensorValues(self) -> None:
        """
        Getting every sensor's current value and saving it to a list.
        Should be called before using readSensorValue().
 
        Returns
        ----------
        None
        """

        self.irSensors = flink.FlinkReflectiveSensor()        
        self.sensorValues : List[int] = []

        for i in range(self.config.amountOfIRSensors):
            self.sensorValues.append(self.irSensors.getValue(i))

        self.sensorValues.append(self.gpio.getValue(self.config.gpioChSensorGlass))             # Normally False
        self.sensorValues.append(self.gpio.getValue(self.config.gpioChSensorBottle))            # Normally False

        self.sensorValues.append(self.gpio.getValue(self.config.gpioChLimitSwitchGripper))      # Normally True
        self.sensorValues.append(self.gpio.getValue(self.config.gpioChLimitSwitchHopper))       # Normally True
 
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

    def align(self, direction) -> None:
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
                case self.config.Directions.Perpendicular:
                    # Updating sensor values
                    sensor0Value = self.readSensorValue(0)
                    sensor2Value = self.readSensorValue(2)

                    print("Aligning")
                    print("Sensor 0: {}".format(self.readSensorValue(0)))
                    print("Sensor 2: {}".format(self.readSensorValue(2)))
                    
                    # Checking if both sensors are on the mark, correcting if not
                    if(sensor0Value > self.config.minValueWhite and sensor2Value > self.config.minValueWhite):
                        time.sleep(0.5)
                        self.stop()
                        time.sleep(1)
                        break
                    if(sensor0Value > self.config.minValueWhite):
                        self.setMotorSpeeds(0.01, 0)
                    elif(sensor2Value > self.config.minValueWhite):
                        self.setMotorSpeeds(0, 0.01)

                case self.config.Directions.Parallel:
                    # Updating sensor values
                    sensor1Value = self.readSensorValue(1)
                    sensor3Value = self.readSensorValue(3)

                    # Stopping if both sensors are on the marks after moving a little futher
                    # Might need to get reworked if sensor 1 gets off the mark while rotating
                    if(sensor1Value > self.config.minValueWhite and sensor3Value > self.config.minValueWhite):
                        time.sleep(0.5)
                        self.stop()
                        break
            
            time.sleep(0.1)

    def rotateServo(self, channel : int, stepCount : int, angle : float) -> None:
        """
        Rotating the gripper/arm for a specified angle using a servo

        Parameters
        ----------
        channel: Channel of the motor that should rotate
        stepCount: Number of steps to reach final angle
        angle: Angle by which the gripper should rotate
                    Grip: 0° = Open
                    Fill: 0° = Horizontal front

        Returns
        ----------
        None
        """
        
        # Enabling servo motors
        self.gpio.setValue(self.config.gpioChEnableServo, True)

        # Limits
        minAngle = 0
        maxAngle = 270 
        minHighTimeMs = 0.5
        maxHighTimeMs = 2.5

        # Ensuring that the angle is within the valid range
        angle = max(min(angle, maxAngle), minAngle)

        # Calculating highTime in milliseconds (0.5 - 2.5) and converting it to a factor of the frequency
        highTimeMs = minHighTimeMs + (angle / maxAngle) * (maxHighTimeMs - minHighTimeMs)
        highTimeFactor = (highTimeMs * self.config.pwmMotorFreq) / 1000
   
        # Calculating current angle/highTime
        period = self.pwm.getBaseClock() / self.config.pwmMotorFreq
        currentHighTimeFactor = self.pwm.getHighTime(channel) / period

        # Cancelling method if target angle is current angle
        if(currentHighTimeFactor == highTimeFactor):
            print("Already there")
            return None
        
        # Rotating servo in steps
        currentStep = 1

        # Calculating the highTime of the current step and converting it to a factor. Adding factor to current highTime
        while currentStep <= stepCount:
            highTimeFactorStep = (highTimeFactor - currentHighTimeFactor) * (currentStep / stepCount)
            self.pwm.setPeriod(channel, int(period))
            self.pwm.setHighTime(channel, int(period * (currentHighTimeFactor + highTimeFactorStep)))
            
            currentStep += 1
            time.sleep(0.025)
        
        # Disabling servo motors
        self.gpio.setValue(self.config.gpioChEnableServo, False)

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
        inputValues = [self.gpio.getValue(self.config.gpioChMode1), self.gpio.getValue(self.config.gpioChMode2), self.gpio.getValue(self.config.gpioChMode4), self.gpio.getValue(self.config.gpioChMode8)]
        mode = 0

        for i in range(inputValues.__len__()):
            if(inputValues[i]):
                mode += 2 ** i

        return mode
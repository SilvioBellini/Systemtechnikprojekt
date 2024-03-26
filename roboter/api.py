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
    pwmChLeftA = 0
    pwmChLeftB = 2
    pwmChRightA = 4
    pwmChRightB = 6
    pwmChFill = 10
    pwmChGrip = 12

    # FQD Channels
    fqdLeft = 1
    fqdRight = 0

    # GPIO Channels
    modeCh1 = 4
    modeCh2 = 6
    modeCh4 = 8
    modeCh8 = 10

    # Configuration motors
    ts = 0.01
    kp = 0.1
    tn = 0.1
    ticksPerRotation = 100
    gearRatio = 16/1
    motorVoltage = 5
    pwmFreq = 50

    #endregion

    def __init__(self):
        # Initializing instances
        self.sensorValues = []
        self.m1 = driver.SignMagnitude(API.ts, API.pwmChLeftA, API.pwmChLeftB, API.fqdLeft, API.ticksPerRotation, API.motorVoltage, API.gearRatio, API.kp, API.tn)
        self.m2 = driver.SignMagnitude(API.ts, API.pwmChRightA, API.pwmChRightB, API.fqdRight, API.ticksPerRotation, API.motorVoltage, API.gearRatio, API.kp, API.tn)

    def setMotorSpeeds(self, leftSpeed : float, rightSpeed : float) -> None:
        """
        Helper method to set the speed for both motors individually.

        Parameters
        ----------
        leftSpeed: Speed for the left motor
        rightSpeed: Speed for the right motor

        Returns
        ----------
        None
        """

        self.m1.setSpeed(leftSpeed)
        self.m2.setSpeed(rightSpeed)        

    def drive(self, speed : float) -> None:
        """
        Letting both of the robot's wheels move with the same speed and direction by setting to opposite speeds
        because the motors face opposite ways.

        Parameters
        ----------
        speed: Speed with which the wheels turn 
            > 0: Forward
            < 0: Backward
        
        Returns
        ----------
        None
        """
        
        self.setMotorSpeeds(speed,-speed)

    def turn(self, speed : float, angle : float) -> None:
        """
        Letting both of the robot's wheels move with the same speed but with opposite direction by setting to the same
        speeds becasue the motors face opposite ways, resulting in a rotation of the robot for a specified angle.

        Parameters
        ----------
        speed: Speed with which the wheels turn 
            > 0: Forward
            < 0: Backward
        angle: Angle by which the robot should rotate
        
        Returns
        ----------
        None
        """
        
        # Calculating the time needed for the motors to rotate for the desired angle
        if (speed != 0):
            timeToRotate = angle / speed

        # Setting the desired speed for both motors
        self.setMotorSpeeds(speed, speed)

        # Waiting for the calculated time to rotate to the desired angle
        time.sleep(timeToRotate)

        # Stopping the motors after reaching the desired angle
        self.stop()

    def stop(self) -> None:
        """
        Stopping the robot's current movement by setting the wheels speed to 0.

        Returns
        ----------
        None
        """

        self.setMotorSpeeds(0, 0)

    def getSensorValues(self) -> None:
        """
        Getting every sensor's current value and saving it to a list.
        Should be called before using readSensorValue().
 
        Returns
        ----------
        None
        """

        sensor = flink.FlinkReflectiveSensor()

        amountOfSensors = 4
        values = []

        for i in range(amountOfSensors):
            values.append(sensor.getValue(i))
        
        return values
 
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

        """if self.values:
                # make sure Index is valid
                if 0 <= index < len(self.sensor_values):
                    # last saved index
                    return self.sensor_values[index]
                else:
                    print("Invalid sensor index.")
        else:
            print("Sensor values have not been fetched yet. Call getSensorValues() first.")
            
        # if sensorvalues not available return none
        return None"""

        values = self.getSensorValues()
        
        return values[index]

    def align(self) -> None:
        """
        Aligning the robot to the marks on the floor

        Returns
        ----------
        None
        """
        pass

    def rotateGripper(self, angle : float) -> None:
        """
        Rotating the gripper for a specified angle using a servo

        Parameters
        ----------
        angle: Angle by which the gripper should rotate

        Returns
        ----------
        None
        """
        
        pwm = flink.FlinkPWM()
        period = pwm.getBaseClock() / API.pwmFreq
        
        # Angle limits
        minAngle = 0
        maxAngle = 270 

        # Ensuring that the angle is within the valid range
        angle = max(min(angle, maxAngle), minAngle)

        # Hightime limits in milliseconds
        minHighTimeMs = 0.5
        maxHighTimeMs = 2.5

        # Calculating highTime in milliseconds (0.5 - 2.5) and converting it to a factor of the frequency
        highTimeMs = minHighTimeMs + (angle / maxAngle) * (maxHighTimeMs - minHighTimeMs)
        highTimeFactor = (highTimeMs * API.pwmFreq) / 1000

        # Setting period and highTime according to the calculated factor
        pwm.setPeriod(API.pwmChFill, int(period))
        pwm.setHighTime(API.pwmChFill, int(period * highTimeFactor))

        # Delay to reach desired angle before continuing
        time.sleep(2)

    def getMode(self) -> int:
        """
        Getting and returning the mode that specifies what object has to be handeled as an integer (0-15)
        0:  Glass
        1:  Bottle

        Returns:
        ----------
        int
        """

        # Initializing
        gpio = flink.FlinkGPIO()
        gpio.setDir(self.modeCh1, False)   
        gpio.setDir(self.modeCh2, False)  
        gpio.setDir(self.modeCh4, False)   
        gpio.setDir(self.modeCh8, False)

        # Reading each input signal and converting it to an integer from 0-15
        inputValues = [gpio.getValue(self.modeCh1), gpio.getValue(self.modeCh2), gpio.getValue(self.modeCh4), gpio.getValue(self.modeCh8)]
        mode = 0

        for i in range(inputValues.__len__()):
            if inputValues[i]:
                mode += 2 ** i

        return mode
    
        
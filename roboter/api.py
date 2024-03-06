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

    def drive(self, speed):
        """
        Letting both of the robot's wheels move with the same speed and direction 

        Parameters:
            speed: Speed with which the wheels turn
                + -> Forward
                - -> Backward
        """
        
        self.driveMotors(speed,speed)

    def turn(self, speed, angle):
        """
        Letting both of the robot's wheels move with the same speed but with opposite direction of rotation
        resulting in a rotation of the robot for a specified angle

        Parameters:
            speed: Speed with which the wheels turn
                + -> Forward
                - -> Backward
            angle: Angle by which the robot should rotate
        """
        # Calculating the time needed for the motors to rotate for the desired angle
        if (speed != 0):
            timeToRotate = angle / speed

        # Setting the desired speed for both motors
        self.driveMotors(speed, -speed)

        # Waiting for the calculated time to rotate to the desired angle
        time.sleep(timeToRotate)

        # Stopping the motors after reaching the desired angle
        self.stop()

    def stop(self):
        """
        Stopping the robot's current movement by setting the wheels speed to 0
        """

        self.driveMotors(0, 0)

    def driveMotors(self, leftSpeed, rightSpeed):
        """
        Helper method to set the speed for both motors

        Parameters:
            leftSpeed: Speed for the left motor
            rightSpeed: Speed for the right motor
        """

        self.m1.setSpeed(leftSpeed)
        self.m2.setSpeed(rightSpeed)        

    def getSensorValues(self):
        """
        Getting every sensor's current value and saving it to a list
        Should be called before using readSensorValue()
        """
        pass

    def readSensorValue(self, index) -> int:
        """
        Getting the last saved value of a specific sensor
        Should only be called after using getSensorValues()

        Parameters:
            index: Specified index of the targeted sensor (Documentation)
        """
        return None

    def align(self):
        """
        Aligning the robot to the marks on the floor
        """
        pass

    def rotateGripper(self, angle):
        """
        Rotating the gripper for a specified angle using a servo

        Parameters:
            angle: Angle by which the gripper should rotate
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

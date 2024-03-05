import driver
import flink        
import math
import time

class API:
    """
    Class for basic functions of the robot (locomotion, sensors, etc.)
    """

  

    # Motor-Parameter als Klassenattribute
    PWM_CH0 = 0
    PWM_CH1 = 1
    PWM_CH2 = 2
    PWM_CH3 = 3
    FQD_1 = 0
    FQD_2 = 1
    ts = 0.01
    kp = 0.1
    tn = 0.1
    ticksPerRotation = 100
    gearRatio = 16/1
    motorVoltage = 5
    servoChannel = 8
    pwmFreq = 50

    def __init__(self):
        self.sensorValues = []

        # Initialisierung der Motor-Instanzen als Klassenattribute
        self.m1 = driver.SignMagnitude(API.ts, API.PWM_CH0, API.PWM_CH1, API.FQD_1, API.ticksPerRotation, API.motorVoltage, API.gearRatio, API.kp, API.tn)
        self.m2 = driver.SignMagnitude(API.ts, API.PWM_CH2, API.PWM_CH3, API.FQD_2, API.ticksPerRotation, API.motorVoltage, API.gearRatio, API.kp, API.tn)

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
        
        # Angle limits
        minAngle = 0
        maxAngle = 270 

        # Ensure that the angle is within the valid range
        if angle > maxAngle:
            angle = maxAngle
        elif angle < minAngle:
            angle = minAngle

        # Calculating hightimte limits
        period = pwm.getBaseClock() / API.pwmFreq
        minHighTime = (period * 0.06)           # 1.2 ms -> 0.5ms auf Datenblatt?
        maxHighTime = (period * 0.11)           # 2.2 ms -> 2.5ms auf Datenblatt?

        # Calculating highTime according to angle and converting it into a factor of 0-1 
        highTime = (angle / maxAngle) + (minHighTime / 100000)
        factor = (highTime * API.pwmFreq) / 1000
        print(factor)

        # Setting the high time according to the calculated factor
        pwm.setPeriod(API.servoChannel, int(period))
        pwm.setHighTime(API.servoChannel, int(period * factor))

        # Delay to reach desired angle before continuing
        time.sleep(2)

        print("fertig")

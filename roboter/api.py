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
    FQD_1 = 0
    ts = 0.01
    kp = 0.1
    tn = 0.1
    ticksPerRotation = 100
    gearRatio = 16/1
    motorVoltage = 5

    def __init__(self):
        self.sensorValues = []

        # Initialisierung der Motor-Instanzen als Klassenattribute
        self.m1 = driver.SignMagnitude(API.ts, API.PWM_CH0, API.PWM_CH1, API.FQD_1, API.ticksPerRotation, API.motorVoltage, API.gearRatio, API.kp, API.tn)
        self.m2 = driver.SignMagnitude(API.ts, API.PWM_CH0, API.PWM_CH1, API.FQD_1, API.ticksPerRotation, API.motorVoltage, API.gearRatio, API.kp, API.tn)

    def drive(self, speed):
        """
        Letting both of the robot's wheels move with the same speed and direction 

        Parameters:
            speed: Speed with which the wheels turn
                + -> Forward
                - -> Backward
        """
        pass

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
        # Calculate the time needed for the motors to rotate to the desired angle
        time_to_rotate = angle / speed

        # Set the desired speed for both motors
        self.drive_motors(speed, -speed)

        # Wait for the calculated time to rotate to the desired angle
        time.sleep(time_to_rotate)

        # Stop the motors after reaching the desired angle
        self.stop()

    def curve(self, leftSpeed, rightSpeed, angle):
        """
        Letting both of the robot's wheels move with different speeds and any direction of rotation
        resulting in driving a curve for a specified angle

        Parameters:
            leftSpeed: Rotation speed of the left wheel of the robot's perspective
            rightSpeed: Rotation speed of the right wheel of the robot's perspective
                + -> Forward
                - -> Backward
            angle: Angle by which the robot should have turned after the curve
        """
        pass

    def stop(self):
        """
        Stopping the robot's current movement by setting the wheels speed to 0
        """
        self.drive_motors(0, 0)

    def drive_motors(self, left_speed, right_speed):
        """
        Helper method to set the speed for both motors

        Parameters:
            left_speed: Speed for the left motor
            right_speed: Speed for the right motor
        """
        # Implement the code to set the speed for both motors using your driver
        # Beispiel: self.m1.setSpeed(left_speed)
        #          self.m2.setSpeed(right_speed)
        pass

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
        Rotating the gripper for a specified angle

        Parameters:
            angle: Angle by which the gripper should rotate
        """
        pass

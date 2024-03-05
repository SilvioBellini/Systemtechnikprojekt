import driver
import flink        
import math
import time

class API:
    """
    Class for basic functions of the robot (locomotion, sensors, etc.)
    """

    #Servo Parameter
    servoChannel = 8
    pwmFreq = 50

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
        # Calculate the time needed for the motors to rotate to the desired angle
        if (speed != 0):
            time_to_rotate = angle / speed

        # Set the desired speed for both motors
        self.driveMotors(speed, -speed)

        # Wait for the calculated time to rotate to the desired angle
        time.sleep(time_to_rotate)

        # Stop the motors after reaching the desired angle
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
            left_speed: Speed for the left motor
            right_speed: Speed for the right motor
        """
        # Implement the code to set the speed for both motors using your driver
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

        # Convert the desired angle to a range suitable for the servo
        min_angle = 0  # Minimum angle the servo can handle
        max_angle = 270  # Maximum angle the servo can handle

        # Ensure that the angle is within the valid range
        angle = max(min(angle, max_angle), min_angle)

        # Map the angle to the corresponding high time for the servo
        period = 1/self.pwmFreq
        min_high_time = (period / 20) * 1.2
        max_high_time = (period / 20) * 2.2
        high_time = min_high_time + (max_high_time - min_high_time) * (angle / max_angle)

        # Set the high time for the servo
        pwm.setHighTime(API.servoChannel, int(high_time))

        # Optionally, add a delay to allow the servo to reach the desired position
        time.sleep(1)  # Adjust the delay as needed

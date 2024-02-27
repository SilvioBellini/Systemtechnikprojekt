import flink        
import math
import time

class API:
    """
    Class for basic functions of the robot (locomotion, sensors etc.)
    """

    def __init__(self):
        self.sensorValues = []

        #Pins : motor 1
        self.PWM_CH0=0
        self.PWM_CH1 = 1
        self.FQD_1 = 0
        # Pins: Motor 2
        self.PWM_CH2 = 2
        self.PWM_CH3 = 3
        self.FQD_2 = 1
        # Variables
        self.fqd = flink.FlinkFQD()
        self.ts = 0.01
        self.kp = 0.1
        self.tn = 0.1
        self.ticksPerRotation = 100
        self.gearRatio = 16/1
        self.motorVoltage = 5
        self.Inkrement = 4*100*16
        self.scale = (2*math.pi)/self.Inkrement
        self.prevPosFQD1 = self.fqd.getCount(self.FQD_1)
        self.prevPosFQD2 = self.fqd.getCount(self.FQD_2)

        self.m = driver.SignMagnitude(self.ts, self.PWM_CH0, self.PWM_CH1, self.FQD_1,
                                      self.ticksPerRotation, self.motorVoltage, self.gearRatio, self.kp, self.tn)
        # Set desired speed, full turn once per second
        self.m.setSpeed(1 * math.pi)

        self.f = driver.SignMagnitude(self.ts, self.PWM_CH2, self.PWM_CH3, self.FQD_2,
                                      self.ticksPerRotation, self.motorVoltage, self.gearRatio, self.kp, self.tn)
        # Set desired speed, full turn once per second
        self.f.setSpeed(2 * math.pi)


    def drive(self, speed):
        """
        Letting both of the robots wheels move with the same speed and direction 

        Parameters:
            speed: Speed with which the wheels turn
                + -> Forward
                - -> Backward
        """

        if speed > 0:
            print ("Moving forward at {speed}.")
            self.m.setSpeed(speed * math.pi)
            self.f.setSpeed(speed * math.pi)
        elif speed < 0:
            print ("Moving forward at -{speed}.")
            self.m.setSpeed(-speed * math.pi)
            self.f.setSpeed(-speed * math.pi)
        else:
            print("Stopping.")
            self.m.setSpeed(0)
            self.f.setSpeed(0)
        pass

    robot = API()
    robot.drive(5)
    time.sleep(5)
    robot.drive(-5)
    time.sleep(5)
    robot.drive(0)
    

    def turn(self, speed, angle):
        """
        Letting both of the robots wheels move with the same speed but with opposite direction of rotation
        resulting in a rotation of the robot for a specified angle

        Parameters:
            speed: Speed with which the wheels turn
                + -> Forward
                - -> Backward
            angle: Angle by which the robot should rotate
        """

        pass

    def curve(self, leftSpeed, rightSpeed, angle):
        """
        Letting both of the robots wheels move with a different speed and any direction of rotation
        resulting in driving a curve for a specified angle

        Parameters:
            leftSpeed: Rotation speed of the left wheel of the robots perspective
            rightSpeed: Rotation speed of the right wheel of the robots perspective
                + -> Forward
                - -> Backward
            angle: Angle by which the robot should have turned after the curve
        """

        pass

    def stop(self):
        """
        Stopping the robots current movement by setting the wheels speed to 0
        """

        pass

    def getSensorValues(self):
        """
        Getting every sensors current value and saving it to a list
        Should be called before using readSensorValue()
        """

        pass

    def readSensorValue(self, index) -> int:
        """
        Getting the last saved value of a specific sensor
        Should only be called after using getSensorValues()

        Parameters:
            index: Specified index of the targetted sensor (Documentation)
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

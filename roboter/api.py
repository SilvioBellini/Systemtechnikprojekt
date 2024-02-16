class API:
    """
    Class for basic functions of the robot (locomotion, sensors etc.)
    """

    def __init__(self):
        self.sensorValues = []
    
    def drive(self, speed):
        """
        Letting both of the robots wheels move with the same speed and direction 

        Parameters:
            speed: Speed with which the wheels turn
                + -> Forward
                - -> Backward
        """

        pass

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

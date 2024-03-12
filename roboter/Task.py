class Task:
    def __init__(self):
        """
        Initializes the Task object with default values.
        """

    def findObject(self, mode):
        """
        Finds an object using the specified mode.

        Parameters:
            mode: The mode used for object detection.
        """

    def grabObject(self):
        """
        Grabs the currently detected object.
        """

    def moveToCounter(self, glassSlot):
        """
        drives to specific slot at the counter.

        Parameters:
            glassSlot: the slot where the glass is located.
        """

    def switchSlot(self):
        """
        switches slot if there is an obstacle.
        """

    def place(self):
        """
        Places either glass or bottle onto the counter.
        """

    def fill(self):
        """
        fills the glass with the bottle.
        """

    def moveToEndPos(self, mode):
        """
        Moves the robot to the end position based on the specified mode.

        Parameters:
            mode: The mode used for determining the end position.
        """

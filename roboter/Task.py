class Task:
    def __init__(self, mode, api, sharedData, communication, audio, statusLed):
        """
        Initializes the Task object with default values.
        """
        self.mode = mode
        self.api = api
        self.sharedData = sharedData
        self.com = communication
        self.audio = audio
        self.statusLed = statusLed

    def findObject(self, mode):
        """
        Finding either the glass or bottle specified with the mode

        Parameters:
            mode: Specifying what object should be found
        """
        pass

    def grabObject(self):
        """
        Grabbing the currently detected object.
        """
        pass

    def moveToCounter(self, glassSlot):
        """
        Driving to the specific slot at the counter

        Parameters:
            glassSlot: The slot where the glass is located
        """
        pass

    def switchSlot(self):
        """
        Switching the slot if an obstacle is detected
        """
        pass

    def place(self):
        """
        Placing either glass or bottle onto the counter
        """
        pass

    def fill(self):
        """
        Filling the glass with the bottle by tipping it over its head
        """
        pass

    def moveToEndPos(self, mode):
        """
        Moving the robot to the end position based on the specified mode

        Parameters:
            mode: Specifying the endposition based on what object got handled
        """
        pass
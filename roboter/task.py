#region Imports

from api import API
from sharedData import SharedData
from communication import Communication
from audioManager import AudioManager
from statusDisplay import StatusDisplay

#endregion

class Task:
    def __init__(self, mode : int, api : API, sharedData : SharedData, communication : Communication, audio : AudioManager, statusLed : StatusDisplay):
        """
        Initializes the Task object with default values.
        """
        self.mode = mode
        self.api = api
        self.sharedData = sharedData
        self.com = communication
        self.audio = audio
        self.statusLed = statusLed

    def findObject(self, mode : int) -> None:
        """
        Finding either the glass or bottle specified with the mode.

        Parameters
        ----------
        mode: Specifying what object should be found

        Returns
        ----------
        None
        """
        pass

    def grabObject(self) -> None:
        """
        Grabbing the currently detected object.

        Returns
        ----------
        None
        """
        pass

    def moveToCounter(self, glassSlot : int) -> None:
        """
        Driving to the specific slot at the counter.

        Parameters
        ----------
        glassSlot: The slot where the glass is located

        Returns
        ----------
        None
        """
        pass

    def switchSlot(self) -> None:
        """
        Switching the slot if an obstacle is detected

        Returns
        ----------
        None
        """
        pass

    def place(self) -> None:
        """
        Placing either glass or bottle onto the counter.

        Returns
        ----------
        None
        """
        pass

    def fill(self) -> None:
        """
        Filling the glass with the bottle by tipping it over its head.

        Returns
        ----------
        None
        """
        pass

    def moveToEndPos(self, mode : int) -> None:
        """
        Moving the robot to the end position based on the specified mode

        Parameters
        ----------
        mode: Specifying the endposition based on what object got handled

        Returns
        ----------
        None
        """
        pass

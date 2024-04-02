

class AudioManager:
    """
    Class for controlling audio output
    """

    def __init__(self):
        """
        Initialize the Audiomanager        
        """

    def playAudioClip (self, index : int) -> None:
        """
        Plays an audio clip with specified index.

        Parameter
        ----------
        index: Index of the audion clip to be played
        
        Retruns
        ----------
        None
        """
        
        message = "7E 04 41 00 {} EF".format(index)

    def pause(self) -> None:
        """
        Pause the currently playing Audio.
        If no audio is playing, doesn't do anything.

        Returns
        ----------
        None
        """
        pass

    def setVolume(self, volume : float):
        """
        Sets the volume of the audio.

        Parameters
        ----------
        volume: The desired volume level (0 to 100)
        
        Returns
        ----------
        None
        """
        pass
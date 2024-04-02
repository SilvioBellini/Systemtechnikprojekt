import flink

class AudioManager:
    """
    Class for controlling audio output
    """

    uartCh = 0

    def __init__(self):
        """
        Initialize the Audiomanager        
        """
        self.uart = flink.FlinkUART(self.uartCh)

    def sendByte(self, byteMessage : bytes) -> None:
        """
        Sends the message to the soundmodule, checking if the message could get transmitted correctly

        Parameter
        ----------
        byteMessage: Message that should get sent as a byte

        Returns
        ----------
        None
        """

        if(self.uart.write(byteMessage) == 0):
            raise Exception("Byte could not get sent")
        
    def playAudioClip (self, index : int) -> bytes:
        """
        Plays an audio clip with specified index.

        Parameter
        ----------
        index: Index of the audion clip to be played
        
        Returns
        ----------
        bytes
        """

        # Converting index to a hexadecimal number with capital letters and then to a byte
        message = "7E 04 41 00 {:0>2X} EF".format(index)
        byteMessage = bytes(message, "uft-8")

        return byteMessage

    def pause(self) -> bytes:
        """
        Pause the currently playing Audio.
        If no audio is playing, doesn't do anything.

        Returns
        ----------
        bytes
        """
        
        message = "7E 02 02 EF"
        byteMessage = bytes(message, "uft-8")

        return byteMessage
    
    def resume(self) -> bytes:
        """
        Continues the currently paused Audio.
        If no audio is currently paused, doens't do anything

        Returns
        ----------
        bytes
        """

        message = "7E 02 01 EF"
        bytesMessage = bytes(message, "uft-8")

        return bytesMessage


    def setVolume(self, volume : float) -> bytes:
        """
        Sets the volume of the audio.

        Parameters
        ----------
        volume: The desired volume level (0-100)
        
        Returns
        ----------
        bytes
        """

        # Clamping the volume from 0-100 and converting it to a hexadecimal number with capital letters and then to a byte
        volume = max(min(volume, 100), 0)
        message = "7E 03 31 {:0>X} EF".format(volume)
        byteMessage = bytes(message, "uft-8")
        
        return byteMessage
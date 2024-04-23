import flink
import time

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
        self.uart.start(9600)

    def sendByte(self, byteMessage : bytes) -> None:
        """
        Sends the message to the soundmodule, checking if the message could get transmitted correctly

        Parameter
        ----------
        byteMessage: Message that should get sent as bytes

        Returns
        ----------
        None
        """

        for byte in byteMessage:
            if(self.uart.write(byte) == 0):
                raise Exception("Byte could not get sent")

        time.sleep(0.1)

    def selectDevice(self) -> None:
        """
        Selects the storage device where the audio clips are saved (SD)

        Returns
        ----------
        None
        """
        
        command = "7E 03 35 01 EF"
        byteMessage = bytes.fromhex(command)

        self.sendByte(byteMessage)

    def playAudioClip(self, folder : int, number : int) -> None:
        """
        Plays an audio clip with specified index.

        Parameter
        ----------
        folder: Number of the folder the audio clip is in (Starting with 1)
        index: Number of the audio clip that should get played (Starting with 1)
        
        Returns
        ----------
        None
        """

        # Converting folder and number to a hexadecimal number with capital letters and then to a byte
        command = "7E 04 42 {:0>2X} {:0>2X} EF".format(folder, number)
        byteMessage = bytes.fromhex(command)

        self.sendByte(byteMessage)

    def pause(self) -> None:
        """
        Pause the currently playing Audio.
        If no audio is playing, doesn't do anything.

        Returns
        ----------
        None
        """
        
        command = "7E 02 02 EF"
        byteMessage = bytes.fromhex(command)

        self.sendByte(byteMessage)   
        
    def resume(self) -> None:
        """
        Continues the currently paused Audio.
        If no audio is currently paused, doens't do anything

        Returns
        ----------
        None
        """

        command = "7E 02 01 EF"
        byteMessage = bytes.fromhex(command)

        self.sendByte(byteMessage)

    def setVolume(self, volume : int) -> None:
        """
        Sets the volume of the audio.

        Parameters
        ----------
        volume: The desired volume level (0-30)
        
        Returns
        ----------
        None
        """

        # Clamping the volume from 0-30 and converting it to a hexadecimal number with capital letters and then to a byte
        volume = max(min(volume, 30), 0)
        command = "7E 03 31 {:0>2X} EF".format(volume)
        byteMessage = bytes.fromhex(command)
        
        self.sendByte(byteMessage)

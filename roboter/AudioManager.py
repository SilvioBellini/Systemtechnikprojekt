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
            else:
                print("Message sent: {}".format(byte))

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

    def playAudioClip (self, index : int) -> None:
        """
        Plays an audio clip with specified index.

        Parameter
        ----------
        index: Index of the audion clip to be played
        
        Returns
        ----------
        None
        """

        # Converting index to a hexadecimal number with capital letters and then to a byte
        # message = "7E 04 41 00 {:0>2X} EF".format(index)

        command = "7E 04 42 01 01 EF"
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
        byteMessage = bytes(command, "utf-8")

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
        byteMessage = bytes(command, "utf-8")

        self.sendByte(byteMessage)

    def setVolume(self, volume : float) -> None:
        """
        Sets the volume of the audio.

        Parameters
        ----------
        volume: The desired volume level (0-100)
        
        Returns
        ----------
        None
        """

        # Clamping the volume from 0-100 and converting it to a hexadecimal number with capital letters and then to a byte
        volume = max(min(volume, 100), 0)
        # message = "7E 03 31 {:0>X} EF".format(volume)
        command = "7E 03 31 32 EF"
        byteMessage = bytes.fromhex(command)
        
        self.sendByte(byteMessage)
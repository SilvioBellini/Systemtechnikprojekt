import flink
import time

from config import Config

class StatusDisplay:
    """
    Class for displaying different status with a RGB-LED

    Parameters
    ----------
    config: Object of the Config class
    """

    def __init__(self, config : Config):
        # Initializing instances
        self.config = config

    def setColor(self, red : int, green : int, blue : int) -> None:
        """
        Setting the color of the LED with 3 values, getting converted into a factor from 0-1

        Parameters
        ----------
        red: Red color value (0-255)
        green: Green color value (0-255)
        blue: Blue color value (0-255)

        Returns
        ----------
        None
        """

        # Creating a pwm for each color channel
        pwmRed = flink.FlinkPWM()
        pwmGreen = flink.FlinkPWM()
        pwmBlue = flink.FlinkPWM()

        period = pwmRed.getBaseClock() / self.config.pwmLedFreq

        # Calculating the highTimes as a factor of the color
        redHighTime = red / 255
        greenHighTime = green / 255
        blueHighTime = blue / 255

        # Setting period and highTime according to the calculated factor
        pwmRed.setPeriod(self.config.pwmChRed, int(period))
        pwmGreen.setPeriod(self.config.pwmChGreen, int(period))
        pwmBlue.setPeriod(self.config.pwmChBlue, int(period))
    
        pwmRed.setHighTime(self.config.pwmChRed, int(period * redHighTime))
        pwmGreen.setHighTime(self.config.pwmChGreen, int(period * greenHighTime))
        pwmBlue.setHighTime(self.config.pwmChBlue, int(period * blueHighTime))
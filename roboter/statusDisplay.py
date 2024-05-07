import flink
import time
#import neopixel

class StatusDisplay:
    """
    Class for displaying different status with a RGB-LED
    """
    #region Classattributes

    pwmChRed = 1
    pwmChGreen = 3
    pwmChBlue = 5
    pwmFreq = 10000

    #endregion

    def __init__(self):
        pass

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

        period = pwmRed.getBaseClock() / StatusDisplay.pwmFreq

        # Calculating the highTimes as a factor of the color
        redHighTime = red / 255
        greenHighTime = green / 255
        blueHighTime = blue / 255

        # Setting period and highTime according to the calculated factor
        pwmRed.setPeriod(StatusDisplay.pwmChRed, int(period))
        pwmGreen.setPeriod(StatusDisplay.pwmChGreen, int(period))
        pwmBlue.setPeriod(StatusDisplay.pwmChBlue, int(period))
    
        pwmRed.setHighTime(StatusDisplay.pwmChRed, int(period * redHighTime))
        pwmGreen.setHighTime(StatusDisplay.pwmChGreen, int(period * greenHighTime))
        pwmBlue.setHighTime(StatusDisplay.pwmChBlue, int(period * blueHighTime))
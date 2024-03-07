import flink
import time
#import neopixel

class StatusDisplay:
    #ledCount = 48
    #ledPin = 0
    #pixels = neopixel.NeoPixel(ledPin, ledCount)
    pwmChRed = 18
    pwmChGreen = 20
    pwmChBlue = 22
    pwmFreq = 10000

    def __init__(self):
        pass

    def setColor(self, red, green, blue):
        #StatusDisplay.pixels.fill(color)

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


        

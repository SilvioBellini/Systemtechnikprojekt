import flink
import time

S10  = 23
LED5 = 1
LED6 = 2
LED7 = 3
LED8 = 4

gpio = flink.FlinkGPIO()
gpio.setDir(LED5, True)
gpio.setDir(LED6, True)
gpio.setDir(LED7, True)
gpio.setDir(LED8, True)
gpio.setValue(LED5, False)
gpio.setValue(LED6, False)
gpio.setValue(LED7, False)
gpio.setValue(LED8, False)


LEDs =[LED5,LED6,LED7,LED8]
while True:
    if S10 == True:
        for i in LEDs:
            gpio.setValue(i,True)
            time.sleep(0.1)
            gpio.setValue(i,False)
    else:
        for i in reversed(LEDs):
            gpio.setValue(i,True)
            time.sleep(0.1)
            gpio.setValue(i,False)




import flink
import time

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

LEDs = [LED5, LED6, LED7, LED8]

for x in range(0, 4):
    gpio.setDir (LEDs[x], True)
    gpio.setValue (LEDs[x], False)

while True:
    for x in range(0, 4):
        gpio.setValue (LEDs[x], True)
        time.sleep(1)
        gpio.setValue (LEDs[x], False)

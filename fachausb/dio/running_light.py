import flink
import time

LED1 = 1
LED2 = 2
LED3 = 3
LED4 = 4

gpio = flink.FlinkGPIO()
gpio.setDir(LED1, True)
gpio.setDir(LED2, True)
gpio.setDir(LED3, True)
gpio.setDir(LED4, True)
gpio.setValue(LED1, False)
gpio.setValue(LED2, False)
gpio.setValue(LED3, False)
gpio.setValue(LED4, False)

while True:
    gpio.setValue(LED1, True)
    gpio.setValue(LED1, False)
    gpio.setValue(LED2, True)
    gpio.setValue(LED2, False)
    gpio.setValue(LED3, True)
    gpio.setValue(LED3, False)
    gpio.setValue(LED4, True)
    gpio.setValue(LED4, False)
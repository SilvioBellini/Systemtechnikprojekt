import flink
import time

LED3 = 7

gpio = flink.FlinkGPIO()
gpio.setDir(LED3, True)
gpio.setValue(LED3, False)

while True:
    gpio.setValue(LED3, True)
    time.sleep(0.4)
    gpio.setValue(LED3, False)
    time.sleep(0.8)

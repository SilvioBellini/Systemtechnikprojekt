import flink
import time

LED1 = 5
LED2 = 6

gpio = flink.FlinkGPIO()
gpio.setDir(LED1, True)
gpio.setDir(LED2, True)
gpio.setValue(LED1, False)
gpio.setValue(LED2, False)
while True:
    led1prev = gpio.getValue(LED1)
    gpio.setValue(LED1, not led1prev)
    gpio.setValue(LED2, led1prev)
    time.sleep(1)
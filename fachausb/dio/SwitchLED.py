import flink
import time

LED4 = 5
Schalter1 = 3

gpio = flink.FlinkGPIO()
gpio.setDir(LED4, True)
gpio.setDir(Schalter1, False)
gpio.setValue(LED4, False)

while True:
    state = gpio.getValue(Schalter1)
    gpio.setValue(LED4, state)
    time.sleep(2)
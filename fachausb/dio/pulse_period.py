import flink
import time

S10  = 23
LED5 = 1

gpio = flink.FlinkGPIO()
gpio.setDir(S10, False)
gpio.setValue(S10, False)

while True:
    state = gpio.setValue(S10)
    starttime = time.time()
    if state != gpio.setValue(S10):
        endtime = time.time()
    print(endtime)
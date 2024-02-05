import flink
import time

S10  = 23
LED5 = 1

gpio = flink.FlinkGPIO()
gpio.setDir(S10, False)
gpio.setValue(S10, False)

laststate = False

while True:
    state = gpio.getValue(S10)
    starttime = time.time()
    while state == laststate:
        state = gpio.getValue(S10)
        endtime = time.time()
        deltatime = (endtime - starttime)
    print(deltatime)
    laststate = state
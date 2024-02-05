import flink
import time

S10  = 23
LED5 = 1

gpio = flink.FlinkGPIO()
gpio.setDir(S10, False)
gpio.setValue(S10, False)

laststate = False
starttime = 0

while True:
    state = gpio.getValue(S10)
    endtime = time.time()
    if state != laststate:
        starttime = time.time()
        deltatime = int((endtime - starttime))
        print(deltatime)
    laststate = state
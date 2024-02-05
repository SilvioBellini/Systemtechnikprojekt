import flink
import time

S10  = 23
LED5 = 1

gpio = flink.FlinkGPIO()
gpio.setDir(S10, False)
gpio.setValue(S10, False)

laststate = False
switches = 0

while True:
    state = gpio.getValue(S10)
    if state != laststate:
        if switches == 0:
            startTime =
        endtime = time.time()
        deltatime = (endtime - starttime)
        print(deltatime)
    laststate = state
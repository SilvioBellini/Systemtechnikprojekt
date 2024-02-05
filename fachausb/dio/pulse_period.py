import flink
import time

S10  = 23
LED5 = 1

gpio = flink.FlinkGPIO()
gpio.setDir(S10, False)
gpio.setValue(S10, False)

state = True
laststate = False
starttime = time.time()

while True:
    state = gpio.getValue(S10)
    if state != laststate:
        endtime = time.time()
        deltatime = int((endtime - starttime))
        print(deltatime)
    laststate = state
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

    if state != laststate:
        if state:
            start_time = time.time()
        else:
            end_time = time.time()
            delta_time = end_time - start_time
            print(delta_time)
    laststate = state
    time.sleep(0.1)
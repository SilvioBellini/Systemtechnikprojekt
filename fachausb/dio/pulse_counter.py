import flink
import time

S10  = 23
LED5 = 1
x = 0

gpio = flink.FlinkGPIO()
gpio.setDir(LED5, True)
gpio.setValue(LED5, False)

currentState = False
lastState = False

while True:
    currentState = gpio.getValue(S10)
    if (currentState != lastState):
        x += 1
        print(x)

    else:
        time.sleep(0.01)
    
    lastState = currentState
        

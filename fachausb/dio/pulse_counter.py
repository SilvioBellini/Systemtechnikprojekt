import flink
import time

S10  = 23
LED5 = 1
x = 0

gpio = flink.FlinkGPIO()
gpio.setDir(LED5, True)
gpio.setValue(LED5, False)



while True:
    state = gpio.getValue(S10)
    if not state:
        x += 1
        print(x)

    else:
        time.sleep(0.01)
        

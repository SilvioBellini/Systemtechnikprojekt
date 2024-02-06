import time
import threading
import flink

stopEvent = threading.Event()

led1 = 5
led2 = 6

def flash(gpio: flink.FlinkGPIO):
    gpio.setDir(led1, True)
    gpio.setValue(led1, False)

    while True:
        gpio.setValue(led1, not gpio.getValue(led1))
        time.sleep(0.5)
        if (stopEvent.is_set()):
            break

gpio = flink.FlinkGPIO()
gpio.setDir(led2, True)
gpio.setValue(led1, False)

t1 = threading.Thread(target=flash, args=(gpio,))
t1.start()

try:
    while 1:
        gpio.setValue(led2, not gpio.getValue(led2))
        time.sleep(1/3)
except KeyboardInterrupt:
    stopEvent.set()
    t1.join()

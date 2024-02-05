import flink
import time

LEDs = [1, 2, 3, 4]

silvio = flink.FlinkGPIO ()
for x in LEDs:
    silvio.setDir (LEDs[x], True)
    silvio.setValue (LEDs[x], False)


while True:
    for x in reversed (LEDs):
        silvio.setValue (LEDs[x], True)
        time.sleep(1)
        silvio.setValue (LEDs[x], False)
import flink
import math
import time

ch = 0
scale = 2 * math.pi / (4 * 100 * 16)
period = 1
fqd = flink.FlinkFQD()
prevPos = fqd.getCount(ch)
absPos = 0

while True:
    actPos = fqd.getCount(ch)
    deltaPos = actPos - prevPos
    prevPos = actPos
    absPos += deltaPos
    print("speed =", deltaPos * scale / period, ", pos =", absPos * scale)
    time.sleep(period)

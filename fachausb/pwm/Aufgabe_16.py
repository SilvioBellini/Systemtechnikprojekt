import flink
import driver
import math
import time

PWM_CH0 = 0
PWM_CH1 = 1
FQD_1 = 0
fqd =flink.FlinkFQD()
ts = 0.01
kp = 0.1
tn = 0.1
ticksPerRotation = 100
gearRatio = 16/1
motorVoltage = 5
Inkrement =  4*100*16
scale = (2*math.pi)/Inkrement
prevPosCH0 = fqd.getCount(PWM_CH0)

m = driver.SignMagnitude(ts, PWM_CH0, PWM_CH1, FQD_1, ticksPerRotation, motorVoltage, gearRatio, kp, tn)
# Set desired speed, full turn once per second
m.setSpeed(2 * math.pi)


while True:
    actPosCH0 = fqd.getCount(PWM_CH0)
    deltaPosCH0 = actPosCH0 - prevPosCH0
    prevPosCH0 = actPosCH0
    print("speed=", deltaPosCH0 * scale)
    time.sleep(1)
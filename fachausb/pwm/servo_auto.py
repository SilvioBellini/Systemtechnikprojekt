import flink
import time

testChannel = 0
pwmFreq = 50

pwm = flink.FlinkPWM()
period = pwm.getBaseClock() / pwmFreq
pwm.setPeriod(testChannel, int(period))
pwm.setHighTime(testChannel, int(period * 0.2))
min_highTime = (period/20)*1.2
max_highTime = (period/20)*2.2


count = 0

while True:
    highTime=min_highTime

    while highTime <= max_highTime:
        pwm.setHighTime(testChannel,highTime)
        highTime += (max_highTime-min_highTime)/50
        time.sleep(5/50)

    highTime = max_highTime

    while highTime >= min_highTime:
        pwm.setHighTime(testChannel,highTime)
        highTime -= (max_highTime-min_highTime)/50
        time.sleep(5/50)



    #5 sek 50 schritten
    
    
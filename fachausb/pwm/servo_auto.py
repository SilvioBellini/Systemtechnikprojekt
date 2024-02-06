import flink
import time

testChannel = 0
pwmFreq = 50

pwm = flink.FlinkPWM()
period = pwm.getBaseClock() / pwmFreq
pwm.setPeriod(testChannel, int(period))
pwm.setHighTime(testChannel, int(period * 0.2))
min_highTime = (1.2/1000)*period
max_highTime = (2.2/1000)*period

highTime = min_highTime

while True:

    highTime = min_highTime
    time.sleep (1)
    highTime = max_highTime
    time.sleep(1)




    #highTime = min_highTime + (max_highTime-min_highTime)/50
    #time.sleep(5/50)

    #min_highTime = highTime

    #5 sek 50 schritten
    
    
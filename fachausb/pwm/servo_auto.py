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

while True:

    pwm.setHighTime(testChannel,int(min_highTime))
    time.sleep (1)
    pwm.setHighTime(testChannel,int(max_highTime))
    time.sleep(1)




    #highTime = min_highTime + (max_highTime-min_highTime)/50
    #time.sleep(5/50)

    #min_highTime = highTime

    #5 sek 50 schritten
    
    
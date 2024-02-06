import flink
import time

testChannel = 0
pwmFreq = 50

pwm = flink.FlinkPWM()
period = pwm.getBaseClock() / pwmFreq
pwm.setPeriod(testChannel, int(period))
pwm.setHighTime(testChannel, int(period * 0.2))
highTime = 2.2
while True:
    highTime = (highTime + period / 4) % period
    pwm.setHighTime(testChannel, int(highTime))
    time.sleep(2)

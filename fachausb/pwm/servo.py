import flink
import time

testChannel = 0
pwmFreq = 20000

pwm = flink.FlinkPWM()
period = pwm.getBaseClock() / pwmFreq
pwm.setPeriod(testChannel, int(period))
pwm.setHighTime(testChannel, int(period * 0.2))
highTime = 0
while True:
    highTime = (highTime + period / 4) % period
    pwm.setHighTime(testChannel, int(highTime))
    time.sleep(2)

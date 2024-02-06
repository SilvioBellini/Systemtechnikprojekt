import flink
import time

testChannel = 0
pwmFreq = 50

pwm = flink.FlinkPWM()
period = pwm.getBaseClock() / pwmFreq
pwm.setPeriod(testChannel, int(period))
pwm.setHighTime(testChannel, int(period * 0.2))

while True:
    # HighTime bestimmt Position. Sie wird berechnet als Prozentsatz der Periodenlänge. 1.2ms: Startposition, 2.2ms: Endposition
    pwm.setHighTime(testChannel, int(period * 0.06))
    time.sleep(2)
    pwm.setHighTime(testChannel, int(period * 0.085))
    time.sleep(2)
    pwm.setHighTime(testChannel, int(period * 0.11))
    time.sleep(2)

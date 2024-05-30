import flink
import driver

from api import API
from testClass import TestClass

pwmFreq = 50
channel1 = 13
channel2 = 14

api = API()
testclass = TestClass(api, None, None, None, None, None, None)
pwm = flink.FlinkPWM()

period = pwm.getBaseClock() / pwmFreq
pwm.setPeriod(channel1, int(period))
pwm.setHighTime(channel1, int(period * 0.2))

pwm.setPeriod(channel2, int(period))
pwm.setHighTime(channel2, int(period * 0.2))
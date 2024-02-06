import flink

chnL = 0
chnR = 1

pwmFreq = 20000
pwm = flink.FlinkPWM()

period = int(pwm.getBaseClock() / pwmFreq)
pwm.setPeriod(chnL, period)
pwm.setPeriod(chnR, period)

# left full
currHightimeL = period
currHightimeR = 0

# left half
# currHightimeL = int(period / 2)
# currHightimeR = 0

# right full
# currHightimeL = 0
# currHightimeR = period

# right half
# currHightimeL = 0
#currHightimeR=int(period/2)

#stop
#currHightimeL=0
#currHightimeR=0

pwm.setHighTime(chnL,currHightimeL)
pwm.setHighTime(chnR,currHightimeR)
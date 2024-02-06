import flink

chn=0
pwmFreq=20000

pwm=flink.FlinkPWM()
period=int(pwm.getBaseClock()/pwmFreq)
pwm.setPeriod(chn,period)

#leftfull
currHightime=period

#lefthalf
#currHightimeL=int(3 * period/4)

#rightfull
#currHightimeL=0

#righthalf
#currHightimeL=int(period/4)

#stop
#currHightimeL=int(period/2)

pwm.setHighTime(chn,currHightime)
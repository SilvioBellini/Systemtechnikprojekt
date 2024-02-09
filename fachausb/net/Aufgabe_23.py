import driver
import math
import time
from enum import Enum
import threading

stopEvent = threading.Event()

client = driver.MessagingClient(username="test", password="test", topic="test/team2")
client.connect()

if client.is_connected():
    print("connection established")

else:
    print("no connection")

State = Enum('State', ['WAITING', 'ACCELERATE', 'RUN', 'DECELERATE', 'PAUSE'])
state = State.WAITING
lastState = None
isFinished = False

PWM_CH0 = 0
PWM_CH1 = 1
FQD_1 = 0
ts = 0.01
kp = 0.1
tn = 0.1
ticksPerRotation = 100
gearRatio = 16/1
motorVoltage = 5
motor = driver.SignMagnitude(ts, PWM_CH0, PWM_CH1, FQD_1, ticksPerRotation, motorVoltage, gearRatio, kp, tn)
acc = 2 * math.pi / 10 # acceleration
speed = 0
maxSpeed = 2 * math.pi
minSpeed = 0.2 * math.pi
factor = 1
reversed = False

try:
    while True:
        message = client.read()

        if(state != lastState and not isFinished):
            client.send("State: " + str(state))
        lastState = state

        match state:
            case State.WAITING:
                if(message == "reversed"):
                    factor = -factor
                    reversed = not reversed
                    client.send("Switched rotation direction")
                if(message == "start"):
                    client.send("Starting")
                    time.sleep(5)
                    state = State.ACCELERATE
                    print("start driving")

            case State.ACCELERATE:
                speed += acc * ts
                if speed >= maxSpeed:
                    speed = maxSpeed
                    state = State.RUN
                motor.setSpeed(speed * factor)
                time.sleep(ts)

            case State.RUN:
                if motor.getPosition() >= 40 * math.pi:
                    state = State.DECELERATE

            case State.DECELERATE:
                speed -= acc * ts
                if speed <= minSpeed:
                    speed = minSpeed
                motor.setSpeed(speed * factor)
                time.sleep(ts)
                if motor.getPosition() >= 50 * math.pi:
                    motor.setSpeed(0)
                    print("stop driving")
                    lastState = state
                    state = State.PAUSE

            case PAUSE:
                time.sleep(0.5)
                motor.exit()
                if(not isFinished):
                    client.send("Stopped")
                isFinished = True
                pass    
    
except KeyboardInterrupt:
    motor.exit()
    stopEvent.set()

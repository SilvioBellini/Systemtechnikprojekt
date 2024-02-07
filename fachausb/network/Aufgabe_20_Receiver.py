import time
import driver
import flink

s1 = 10
s2 = 11
s3 = 12
s4 = 13

gpio = flink.FlinkGPIO()
gpio.setDir(s1, False)
gpio.setDir(s1, False)
gpio.setDir(s1, False)
gpio.setDir(s1, False)

switches = [s1, s2, s3, s4]

client = driver.MessagingClient(username="test", password="test", topic="test/team04")
#client.connect()

if client.is_connected():
    print("connection established")

else:
    print("no connection")

currentStates = []
lastStates = []

while KeyboardInterrupt:
    currentStates = []
    for i in range(0, 4):
        currentStates.append(gpio.getValue(switches[i]))

    if(currentStates != lastStates):
        print(currentStates)
        #client.send(currentStates)
        
    lastStates = currentStates
    time.sleep(0.1)
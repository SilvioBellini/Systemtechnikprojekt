import time
import driver
import flink

led1 = 0
led2 = 1
led3 = 2
led4 = 3

gpio = flink.FlinkGPIO()
gpio.setDir(led1, True)
gpio.setDir(led2, True)
gpio.setDir(led3, True)
gpio.setDir(led4, True)

gpio.setValue(led1, False)
gpio.setValue(led2, False)
gpio.setValue(led3, False)
gpio.setValue(led4, False)

leds = [led1, led2, led3, led4]

client = driver.MessagingClient(username="test", password="test", topic="test/team04")
client.connect()

if client.is_connected():
    print("connection established")

else:
    print("no connection")

while not KeyboardInterrupt:
    message = client.read()

    if message is not None:
        states = eval(message)
        print(states)

        for i in range(0,4):
            gpio.setValue(leds[i], states[i])

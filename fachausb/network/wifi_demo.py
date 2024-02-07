import time
import driver

client = driver.MessagingClient(username="test", password="test", topic="test/team1")
client.connect()

if client.is_connected():
    print("connection established")

else:
    print("no connection")

for i in range(1000):
    client.send(str(i))
    print("sent:", str(i))
    message = client.read()
    
    if message is not None:
        print("received:", message)
    time.sleep(1.1)
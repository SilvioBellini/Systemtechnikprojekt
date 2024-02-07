import flink
import driver
import time
import sysp24.roboter.SharedData as SharedData

class Network():
    def __init__(self):
        self.sharedData = SharedData()
        self.client = driver.MessagingClient(username="team2", password="1234", topic="roboter")
        self.client.connect()

        if(self.client.is_connected()):
            print("Connection established to: ", self.client.host)

        else:
            print("No connection can be established!")
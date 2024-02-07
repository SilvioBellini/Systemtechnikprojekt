import driver
import SharedData

class Network():
    """
    Base Class for establishing a wireless connection and exchaning information
    """
    def __init__(self):
        # Initializing a client and establishing a connection to a specific topic
        self.sharedData = SharedData()
        self.client = driver.MessagingClient(username="team2", password="1234", topic="roboter")
        self.client.connect()

        if(self.client.is_connected()):
            print("Connection established to: ", self.client.host)

        else:
            print("No connection can be established!")
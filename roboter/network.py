import driver
from sharedData import *

class Network():
    """
    Class for establishing a wireless connection and exchanging information
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

    def sendMessage(self, id, data):
        """
        Sending a string consisting of an identification number and a specific information to the specified topic.
        """

        message = [id, data]
        self.client.send(str(message))
        
        print("Sent Message: ", message)

    def receiveMessage(self):
        """
        Searching for an unread message on the specified topic. Saving received information in the SharedData Class.
        """

        message = self.client.read()

        if(message is not None):
            decodedMessage = eval(message)
            id = decodedMessage[0]
            data = decodedMessage[1]
            self.sharedData.setData(id, data)
            
            print("Received Message: ", message)

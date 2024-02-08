try:
    import driver
except ModuleNotFoundError:
    pass
from sharedData import *

class Network():
    """
    Class for establishing a wireless connection to a MQTTX-Server and exchanging information 

    Parameters:
        username: Name used for connection
        password: Password used for connection
        topic: Channel of connection
    """

    def __init__(self, username, password, topic):
        # Initializing a client and establishing a connection to a specific topic
        self.sharedData = SharedData()
        self.username = username
        self.password = password
        self.topic = topic

        try:
            self.client = driver.MessagingClient(username, password, topic)
            self.client.connect()
        except(NameError, AttributeError) as error:
            print("Connection failed - {}".format(error))

        if(self.client.is_connected()):
            print("Connection established to: ", self.client.host)
        else:
            print("No connection can be established!")

    def sendMessage(self, id, data):
        """
        Sending a string consisting of an identification number and a specific information to the specified topic.

        Parameters:
            ID: Unique identification number of the transmitted information 
                0 = Approval Kitchen
                1 = Approval Counter
                2 = Glass Slot
            Data: Information that should be transmitted
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

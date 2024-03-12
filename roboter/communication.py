try:
    import driver
except ModuleNotFoundError:
    pass

class Communication():
    """
    Class for establishing a wireless connection to a MQTTX-Server and exchanging information 

    Parameters:
        username: Name used for connection
        password: Password used for connection
        topic: Channel of connection
    """

    def __init__(self, username, password, topic, sharedData):
        # Initializing a client and establishing a connection to a specific topic
        self.sharedData = sharedData
        self.username = username
        self.password = password
        self.topic = topic

        try:
            self.client = driver.MessagingClient(username, password, topic)
            self.client.connect()
        except(NameError, AttributeError) as error:
            print("Connection failed - {}".format(error))

        if(self.client.is_connected()):
            print("Connection established to: ", self.client.host, " with the topic ", self.topic)
        else:
            print("No connection can be established!")

    def sendMessage(self, id, data):
        """
        Sending a string consisting of an identification number and a specific information to the specified topic.

        Parameters:
            id: Unique identification number of the transmitted information 
                0 = Approval Kitchen
                1 = Approval Counter
                2 = Glass Slot
            data: Information that should be transmitted
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
            print("ID: ", id)
            data = decodedMessage[1]
            print("Data: ", data)
            self.sharedData.setData(id, data)
            
            print("Received Message: ", message)

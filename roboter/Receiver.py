import Network

class Receiver(Network):
    def __init__(self):
        Network.__init__(self)

    def receiveMessage(self):
        """
        Searching for an unread message on the topic specified in its parent class.
        Saving received information in the SharedData Class.
        """
        message = self.client.read()

        if(message is not None):
            decodedMessage = eval(message)
            id = decodedMessage[0]
            data = decodedMessage[1]
            self.sharedData.setData(id, data)
            
            print("Received Message: ", message)